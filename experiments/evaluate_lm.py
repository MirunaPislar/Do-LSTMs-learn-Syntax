from dictionary_corpus import Dictionary, tokenize_sentence
from torch.autograd import Variable
from numpy import array, argmax
from pytorch_pretrained_bert import BertForMaskedLM, tokenization
from tqdm import tqdm

import argparse
import csv
import sys
import torch
import torch.nn.functional as F
import warnings

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(
    description="Language Model Evaluation.")

parser.add_argument("--data", type=str, default="data/generated.tab",
                    help="Path to the data file to be evaluated.")
parser.add_argument("--original", default=False, action="store_true",
                    help="Whether the data file is in the original format"
                         "(as in Gulordava et al. \"generated.tab\") or not.")
parser.add_argument("--eval_target_word", default=False, action="store_true",
                    help="Whether to evaluate the language model only on "
                         "the target word or on the whole sentence.")
parser.add_argument("--print_word_probs", default=False, action="store_true",
                    help="Whether or not to print word probabilities too"
                         "(this only is effective if the evaluation "
                         "is performed on the whole sentence, "
                         "i.e. when \"eval_target_word\" is set to False)")
parser.add_argument("--vocab", type=str, default="data/vocab.txt",
                    help="Path to the vocabulary corresponding to the corpus "
                         "on which the language model has been trained.")
parser.add_argument("--mask_target", default=False, action="store_true",
                    help="Whether to mask or not the target word(s).")
parser.add_argument("--seed", type=int, default=532,
                    help="Random seed")
parser.add_argument("--model_name", type=str, default="lm",
                    help="Name of the model to perform the evaluation.")
parser.add_argument("--cuda", action="store_true",
                    help="use CUDA")
args = parser.parse_args()

torch.manual_seed(args.seed)
if torch.cuda.is_available():
    if not args.cuda:
        print("WARNING: CUDA device available. Consider running with --cuda.",
              file=sys.stderr)
    else:
        torch.cuda.manual_seed(args.seed)


def read_datafile():
    """
    Reads one row at a time from a data file.
    If your intention is to evaluate only a target (masked) word,
    (as proposed and done in Linzen et al. (2016) and Gulordava et al. (2018))
    then the data file needs to have the following *mandatory* header fields:
        * pattern - type of targeted syntactic test
        * sent - the sentence to be evaluated by the language model
               - it needs to be the same for pairs of grammatical
                and ungrammatical sentences
        * form - the correct form of the word to be evaluated (target)
        * form_alt - the incorrect form of the word to be evaluated (target)
        * len_prefix - length of the sentence up to the form/form_alt word
                       i.e. index (position) of the target

    Instead, if your intention is to evaluate the whole sentence
    (as proposed and done by Marvin and Linzen (2018))
    then the following fields either need to be in the header of the data file
    or they are extracted from a "target-only" data file:
        * pattern - type of targeted syntactic test
        * sent - the grammatical sentence to be evaluated by the language model
        * sent_alt - the ungrammatical variant of the sentence to be evaluated
    """
    rows = csv.DictReader(open(args.data, encoding="utf8"), delimiter="\t")
    headers = rows.fieldnames
    data = []

    # If scoring whole sentences, try first reading from an "own" data file.
    # Otherwise, try to obtain it from a "target-word"-only data file.
    if not args.eval_target_word \
            and ("sent" in headers and "sent_alt" in headers
                 and "pattern" in headers):
        for row in rows:
            data.append((row["pattern"], row["sent"], row["sent_alt"]))
        return data

    # If scoring individual tokens, but the data file is in "whole-sentence"
    # format, try converting it to obtain it (assumes only one word differs).
    if args.eval_target_word and not \
            ("sent" in headers and "form" in headers and "form_alt" in headers
             and "len_prefix" in headers and "pattern" in headers):
        converted_file = args.data.split(".")[0] + "_words_only." + args.data.split(".")[1]
        from_sent_to_tokens(rows, converted_file)
        rows = csv.DictReader(open(converted_file, encoding="utf8"), delimiter="\t")

    for row in rows:
        pattern = row["pattern"]
        sent = row["sent"].split(" ")
        good_form = row["form"]
        bad_form = row["form_alt"]
        target_idx = int(row["len_prefix"])
        if args.eval_target_word:
            if args.mask_target:
                sent[target_idx] = "***mask***"
            sent = " ".join(sent)
            data.append((pattern, sent, target_idx, good_form, bad_form))
        else:
            sent[target_idx] = good_form
            sent_good = " ".join(sent)
            sent[target_idx] = bad_form
            sent_bad = " ".join(sent)
            data.append((pattern, sent_good, sent_bad))
    return data


def read_datafile_original():
    """
    Reads two rows at a time from a data file: the first row is always
    the grammatical one, the second one is the ungrammatical one.
    This implementation allows for an easier evaluation of the data
    files in the same format as originally proposed by Gulordava et al.
    The mandatory fields of the header are:
        * pattern - type of targeted syntactic structure that is evaluated
        * sent - the sentence to be evaluated by the language model
               - it needs to be the same for pairs of grammatical
                and ungrammatical sentences
        * class - can be either "correct" or "wrong" (always in this order)
        * form - the form of the word to be evaluated (e.g. "is" for the
                grammatical example and "are" for the ungrammatical one)
        * len_prefix - length of the sentence up to the form word;
                       this is the index of the target (e.g. "is" or "are")
    """
    rows = csv.DictReader(open(args.data, encoding="utf8"), delimiter="\t")
    data = []
    for row in rows:
        next_row = next(rows)
        assert(row["sent"] == next_row["sent"])
        assert(row["class"] == "correct")
        assert(next_row["class"] == "wrong")
        assert(next_row["pattern"] == row["pattern"])
        if "uncased" in args.model_name:
            sent = row["sent"].lower().split()
        else:
            sent = row["sent"].split()
        if "bert" in args.model_name:
            sent = sent[:-1]  # get rid of the <eos>
        good_form = row["form"]
        bad_form = next_row["form"]
        target_idx = int(row["len_prefix"])
        if args.mask_target:
            sent[target_idx] = "***mask***"
        sent = " ".join(sent)
        data.append((row["pattern"], sent, target_idx, good_form, bad_form))
    return data


def from_sent_to_tokens(rows, filename):
    with open(filename, "w") as f:
        fieldnames = ["pattern", "form", "form_alt", "len_prefix", "sent"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            pattern = row["pattern"]
            sent = row["sent"]
            sent_alt = row["sent_alt"]
            len_prefix, form, form_alt = find_target_word(sent, sent_alt)
            writer.writerow(
                {"pattern": pattern, "form": form, "form_alt": form_alt,
                 "len_prefix": len_prefix, "sent": sent})


def find_target_word(sent, sent_alt):
    tokens_sent = sent.split()
    tokens_sent_alt = sent_alt.split()
    for i, (tok, tok_alt) in enumerate(zip(tokens_sent, tokens_sent_alt)):
        if tok != tok_alt:
            return i, tok, tok_alt
    raise ValueError("Reached end of sentences and no target word found! "
                     "Sentences are identical:\n1. %s\n2. %s" % sent, sent_alt)


def load_model():
    """
    Load a previously trained language model.
    """
    if args.model_name == "lm":
        model_path = "trained_models/hidden650_batch128_dropout0.2_lr20.0.pt"
    elif "ccg" in args.model_name.lower():
        model_path = "trained_models/lm_multitask_ccg.pt"
    elif "pos" in args.model_name.lower():
        model_path = "trained_models/lm_multitask_pos.pt"
        # model_path = "trained_models/lm_multitask_pos_failed_ep7.pt"
    else:
        raise ValueError("Invalid model name: %s." % args.model_name)
    with open(model_path, "rb") as f:
        print("Loading the model...", file=sys.stderr)
        print("model_name = \"%s\"." % model_path, file=sys.stderr)
        if args.cuda:
            model = torch.load(f)
        else:
            model = torch.load(f, map_location=lambda storage, loc: storage)
    model.eval()
    if args.cuda:
        model.cuda()
    else:
        model.cpu()
    return model


def repackage_hidden(hidden):
    """
    Detach hidden states from their history.
    """
    if isinstance(hidden, torch.Tensor):
        return hidden.detach()
    else:
        return tuple(repackage_hidden(v) for v in hidden)


def test_get_batch(source, evaluation=False):
    if isinstance(source, tuple):
        seq_len = len(source[0]) - 1
        data = Variable(source[0][:seq_len], volatile=evaluation)
        target = Variable(source[1][:seq_len], volatile=evaluation)

    else:
        seq_len = len(source) - 1
        data = Variable(source[:seq_len], volatile=evaluation)
        target = Variable(source[1:1 + seq_len].view(-1))
    # This is where data should be CUDA-fied to lessen OOM errors
    if args.cuda:
        return data.cuda(), target.cuda()
    else:
        return data, target


def evaluate_lm_target_words(data, model, dictionary):
    """
    Evaluate a language model on certain data examples.
    This method only computes and prints the probability
    of a target word in a pair of sentences. A language model
    that captures syntax is expected to assign a higher
    probabilities to the correct form of the target word.
    :param data: data to be evaluated by the language model
    :param model: a pre-trained language model
    :param dictionary: based on the vocabulary of the corpus
                       on which the LM has been trained
    """
    model.eval()
    hidden = model.init_hidden(bsz=1)  # no. of parallel sentences processed
    for (pattern, sent, target_idx, good, bad) in tqdm(data):
        if args.mask_target:
            pre, target, post = sent.split("***")
            token_ids = tokenize_sentence(dictionary, pre + target + post)
        else:
            token_ids = tokenize_sentence(dictionary, sent)
        try:
            word_ids = [dictionary.word2idx[good], dictionary.word2idx[bad]]
        except KeyError:
            print("Skipping bad wins: %s and %s." % (good, bad), file=sys.stderr)
            continue
        token_tensor = token_ids.view(1, -1).t().contiguous()

        output, hidden = model(token_tensor, hidden)
        output_flat = output.view(-1, len(dictionary))  # [sent_len, vocab_size]
        log_probs = F.log_softmax(output_flat).data
        log_probs_np = log_probs.cpu().numpy()

        # Create mask for the target word.
        mask = [False] * len(token_ids)
        mask[target_idx - 1] = True
        mask = array(mask)

        # Get scores for the target word.
        log_probs_target = log_probs_np[mask][0]
        scores = [float(x) for x in log_probs_target[word_ids]]
        good_score = scores[0]
        bad_score = scores[1]

        # Identify the maximum prediction token.
        max_pred_index = argmax(log_probs_target).item()
        max_pred_token = dictionary.idx2word[max_pred_index]

        hidden = repackage_hidden(hidden)

        print(str(good_score > bad_score), pattern,
              good, good_score, bad, bad_score,
              "max_pred=%s" % max_pred_token,
              sent.encode("utf8"), sep=u"\t")


def eval_each_word_in_sentence(token_ids, model, dictionary, grammatical):
    model.eval()
    hidden = model.init_hidden(bsz=1)

    token_tensor = token_ids[:-1].view(1, -1).t().contiguous()
    output, hidden = model(token_tensor, hidden)
    output_flat = output.view(-1, len(dictionary))  # [sent_len, vocab_size]
    log_probs = F.log_softmax(output_flat).data
    log_probs_np = log_probs.cpu().numpy()

    seq_len = len(token_ids) - 1
    word_scores = []
    for i in range(seq_len):
        word_idx = token_ids[i + 1]
        if dictionary.idx2word[word_idx].lower() == "<eos>":
            continue
        mask_this_word = [False] * seq_len
        mask_this_word[i] = True
        log_prob_this_word = float(log_probs_np[mask_this_word][0][word_idx])
        word_scores.append(log_prob_this_word)
        if args.print_word_probs:
            print(str(dictionary.idx2word[token_ids[i]]), grammatical,
                  str(i), str(log_prob_this_word), sep="\t")
    return word_scores


def evaluate_lm_sentences(data, model, dictionary):
    """
    Evaluate a language model on certain data examples.
    This method computes and prints the probabilities
    of all the words in a pair of sentences. A language model
    that captures syntax is expected to assign a higher
    probabilities to the grammatical sentence (as a whole).
    :param data: data to be evaluated by the language model
    :param model: a pre-trained language model
    :param dictionary: based on the vocabulary of the corpus
                       on which the LM has been trained
    """
    print_at_the_end = ""
    for (pattern, sent_good, sent_bad) in tqdm(data):
        if args.print_word_probs:
            print("\n", "=" * 55)
        token_ids = tokenize_sentence(dictionary, sent_good)
        token_ids_alt = tokenize_sentence(dictionary, sent_bad)

        word_scores = eval_each_word_in_sentence(
            token_ids, model, dictionary, grammatical="grammatical")
        if args.print_word_probs:
            print("\n")
        word_scores_alt = eval_each_word_in_sentence(
            token_ids_alt, model, dictionary, grammatical="ungrammatical")

        assert(len(word_scores) == len(word_scores_alt)), \
            "Word scores don't match!\n%s\n%s" \
            % (" ".join([str(w) for w in word_scores]),
               " ".join([str(w) for w in word_scores_alt]))

        good_score = sum(word_scores)
        bad_score = sum(word_scores_alt)

        print_at_the_end += "\t".join([
            str(good_score > bad_score), pattern,
            str(good_score), str(bad_score), sent_good, sent_bad]) + "\n"

    print(print_at_the_end)


def evaluate_bert(data, bert, tokenizer):
    """
    Evaluate BERT on certain data examples.
    This method only computes and prints the probability
    of a masked target word in a pair of sentences.
    This implementation is based on Goldberg's. Check:
    https://github.com/yoavg/bert-syntax for more details.
    :param data: data to be evaluated by the language model
    :param bert: a pre-trained BERT language model
    :param tokenizer: BERT's tokenizer
    """
    bert.eval()
    for (pattern, sent, target_idx, good, bad) in tqdm(data):
        if args.mask_target:
            pre, target, post = sent.split("***")
            target = ["[MASK]"]
        else:
            splits = sent.split()
            pre, target, post = " ".join(splits[:target_idx]), \
                                splits[target_idx], \
                                " ".join(splits[(target_idx + 1):])
            target = tokenizer.tokenize(target)

        tokens = ["[CLS]"] + tokenizer.tokenize(pre)
        tok_target_idx = len(tokens)
        tokens += target + tokenizer.tokenize(post) + ["[SEP]"]
        token_ids = tokenizer.convert_tokens_to_ids(tokens)
        try:
            word_ids = tokenizer.convert_tokens_to_ids([good, bad])
        except KeyError:
            print("Skipping bad wins: %s and %s." % (good, bad), file=sys.stderr)
            continue
        token_tensor = torch.LongTensor(token_ids).unsqueeze(0)

        # Get the masked language modeling logits.
        logits = bert(token_tensor)  # [batch_size=1, sent_len, vocab_size]

        # Get the word probabilities for the target (masked) word.
        probs = F.softmax(logits[0, tok_target_idx], dim=-1)
        scores = [float(x) for x in probs[word_ids]]
        good_score = scores[0]
        bad_score = scores[1]

        # Identify the maximum prediction token.
        max_pred_index = torch.argmax(probs).item()
        max_pred_token = tokenizer.convert_ids_to_tokens([max_pred_index])[0]

        print(str(good_score > bad_score), pattern,
              "max_pred=%s" % max_pred_token,
              good, good_score, bad, bad_score,
              sent.encode("utf8"), sep=u"\t")


def main():
    # Load the data/templates to be evaluated.
    if args.original:
        data = read_datafile_original()
    else:
        data = read_datafile()

    # Load the corpus vocabulary into a dictionary.
    dictionary = Dictionary(args.vocab)
    print("Vocabulary size = ", len(dictionary), file=sys.stderr)

    # Load and evaluate a pre-trained language model.
    if "lm" in args.model_name:
        model = load_model()
        if args.eval_target_word:
            evaluate_lm_target_words(data, model, dictionary)
        else:
            evaluate_lm_sentences(data, model, dictionary)
    elif "bert" in args.model_name:
        if "uncased" in args.model_name:
            case = "uncased"
        else:
            case = "cased"
        model_name = "bert-large-" + case
        if "base" in args.model_name:
            model_name = "bert-base-" + case
        bert = BertForMaskedLM.from_pretrained(model_name)
        do_lower_case = "uncased" in args.model_name
        tokenizer = tokenization.BertTokenizer.from_pretrained(
            model_name, do_lower_case=do_lower_case)
        evaluate_bert(data, bert, tokenizer)
    else:
        raise ValueError("Invalid model name %s!" % args.model_name)


if __name__ == "__main__":
    main()
