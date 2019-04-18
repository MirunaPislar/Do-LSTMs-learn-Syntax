from dictionary_corpus import Dictionary, tokenize_sentence
from numpy import array
from pytorch_pretrained_bert import BertForMaskedLM, tokenization
from tqdm import tqdm

import argparse
import csv
import torch
import torch.nn.functional as F

parser = argparse.ArgumentParser(
    description="Language Model Evaluation: "
    "extracts softmax vectors for the specified words.")

parser.add_argument("--data", type=str, default="data/generated.tab",
                    help="Path to the data file to be evaluated.")
parser.add_argument("--original", type=bool, default=False,
                    help="Whether the data file is in the original format"
                         "(as in Gulordava et al. \"generated.tab\") or not.")
parser.add_argument("--eval_only_target_word", type=bool, default=False,
                    help="Whether to evaluate the langauge model only on "
                         "the target words or on the whole sentence.")
parser.add_argument("--vocab", type=str, default="data/",
                    help="Path to the directory to the corpus "
                         "vocabulary (of the language model).")
parser.add_argument("--mask_target", type=bool, default=False,
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
        print("WARNING: CUDA device available. Consider running with --cuda.")
    else:
        torch.cuda.manual_seed(args.seed)


def read_datafile():
    """
    Reads one row at a time from a data file.
    If the intention is to evaluate only a target (masked) word, then
    the data file needs to have the following mandatory header fields:
        * pattern - type of targeted syntactic structure that is evaluated
        * sent - the sentence to be evaluated by the language model
               - it needs to be the same for pairs of grammatical
                and ungrammatical sentences
        * form - the correct form of the word to be evaluated (target)
        * form_alt - the incorrect form of the word to be evaluated (target)
        * len_prefix - length of the sentence up to the form/form_alt word
                       i.e. index (position) of the target
    """
    rows = csv.DictReader(open(args.data, encoding="utf8"), delimiter="\t")
    data = []
    if args.eval_only_target_word:
        for row in rows:
            pattern = row["pattern"]
            sent = row["sent"].split()
            good_form = row["form"]
            bad_form = row["form_alt"]
            target_idx = row["len_prefix"]
            if args.mask_target:
                sent[int(target_idx)] = "***mask***"
            sent = " ".join(sent)
            data.append((pattern, sent, target_idx, good_form, bad_form))
    else:
        for row in rows:
            data.append((row["pattern"], row["sent"], row["sent_alt"]))
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
        good_form = row["form"]
        bad_form = next_row["form"]
        target_idx = row["len_prefix"]
        if args.mask_target:
            sent[int(target_idx)] = "***mask***"
        sent = " ".join(sent)
        data.append((row["pattern"], sent, target_idx, good_form, bad_form))
    return data


def load_model():
    """
    Load a previously trained language model.
    """
    if args.model_name == "lm":
        model_path = "trained_models/hidden650_batch128_dropout0.2_lr20.0.pt"
    else:
        raise ValueError("Invalid model name: %s." % args.model_name)
    with open(model_path, "rb") as f:
        print("Loading the model...")
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


def evaluate_lm_target_words(data, model, dictionary):
    """
    Evaluate a language model on certain data examples.
    :param data: data to be evaluated by the language model
    :param model: a pre-trained language model
    :param dictionary: the vocabulary of the corpus on which
                       the language model has been trained
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
            print("Skipping bad wins: %s and %s." % (good, bad))
            continue
        token_tensor = token_ids.view(1, -1).t().contiguous()
        output, hidden = model(token_tensor, hidden)
        output_flat = output.view(-1, len(dictionary))  # [sent_len, vocab_size]
        log_probs = F.log_softmax(output_flat).data
        log_probs_np = log_probs.cpu().numpy()

        # Create mask for the target word prediction
        mask = [False] * len(token_ids)
        mask[int(target_idx) - 1] = True
        mask = array(mask)

        # Get scores for the target word
        log_probs_target = log_probs_np[mask][0]
        scores = [float(x) for x in log_probs_target[word_ids]]

        hidden = repackage_hidden(hidden)
        good_score = scores[0]
        bad_score = scores[1]
        print(str(good_score > bad_score), pattern,
              good, good_score, bad, bad_score,
              sent.encode("utf8"), sep=u"\t")


def eval_whole_sent(token_ids, model, dictionary):
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
        mask = [False] * seq_len
        mask[i] = True
        log_probs_target = float(log_probs_np[mask][0][word_idx])
        word_scores.append(log_probs_target)
        print(str(dictionary.idx2word[word_idx]),
              str(i),
              str(log_probs_target),
              sep="\t")
    print()
    return word_scores


def evaluate_lm_sentences(data, model, dictionary):
    """
    Evaluate a language model on certain data examples.
    :param data: data to be evaluated by the language model
    :param model: a pre-trained language model
    :param dictionary: the vocabulary of the corpus on which
                       the language model has been trained
    """
    for (pattern, sent, sent_alt) in tqdm(data):
        print()
        token_ids = tokenize_sentence(dictionary, sent)
        token_ids_alt = tokenize_sentence(dictionary, sent_alt)

        word_scores = eval_whole_sent(
            token_ids, model, dictionary)
        word_scores_alt = eval_whole_sent(
            token_ids_alt, model, dictionary)

        assert(len(word_scores) == len(word_scores_alt)), \
            "Word scores don't match!\n%s\n%s" \
            % (" ".join([str(w) for w in word_scores]),
               " ".join([str(w) for w in word_scores_alt]))

        good_score = sum(word_scores)
        bad_score = sum(word_scores_alt)

        print(str(good_score > bad_score), pattern,
              good_score, bad_score,
              sent.encode("utf8"),
              sent_alt.encode("utf8"), sep=u"\t")


def evaluate_bert(data, bert, tokenizer):
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
            print("Skipping bad wins: %s and %s." % (good, bad))
            continue
        token_tensor = torch.LongTensor(token_ids).unsqueeze(0)

        # Get the masked language modeling logits.
        logits = bert(token_tensor)  # [batch_size=1, sent_len, vocab_size]

        # Get the word probabilities for the target (masked) word.
        probs = F.softmax(logits[0, tok_target_idx], dim=-1)

        # Maximum prediction token
        predicted_index = torch.argmax(probs).item()
        predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])[0]

        scores = [float(x) for x in probs[word_ids]]

        good_score = scores[0]
        bad_score = scores[1]
        print(str(good_score > bad_score), pattern,
              "MAX_TOKEN=%s" % predicted_token,
              good, good_score, bad, bad_score,
              sent.encode("utf8"), sep=u"\t")


def main():
    # Load the data to be evaluated
    if args.original:
        data = read_datafile_original()
    else:
        data = read_datafile()

    # Load the corpus dictionary
    dictionary = Dictionary(args.vocab)
    print("Vocabulary size = ", len(dictionary))

    # Load and evaluate a model
    if args.model_name == "lm":
        model = load_model()
        if args.eval_only_target_word:
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
        tokenizer = tokenization.BertTokenizer.from_pretrained(model_name)
        evaluate_bert(data, bert, tokenizer)
    else:
        raise ValueError("Invalid model name %s" % args.model_name)


if __name__ == "__main__":
    main()
