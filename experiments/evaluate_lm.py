from dictionary_corpus import Dictionary, tokenize_sentence
from numpy import array
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
                         "(as in Gulordava et al.'s \"generated.tab\") or not.")
parser.add_argument("--vocab", type=str, default="data/",
                    help="Path to the directory to the corpus "
                         "vocabulary (of the language model).")
parser.add_argument("--checkpoint", type=str,
                    help="Language model checkpoint to be used.")
parser.add_argument("--mask_target", type=bool, default=False,
                    help="Whether to mask or not the target word(s).")
parser.add_argument("--seed", type=int, default=532,
                    help="Random seed")
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
    The mandatory fields of the header are:
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
    for row in rows:
        sent = row["sent"].split()
        good_form = row["form"]
        bad_form = row["form_alt"]
        target_idx = row["len_prefix"]
        if args.mask_target:
            sent[int(target_idx)] = "***mask***"
        sent = " ".join(sent)
        data.append((sent, target_idx, good_form, bad_form))
    return data


def read_datafile_original():
    """
    Reads two rows at a time from a data file: the first row is always
    the grammatical one, the second one is the ungrammatical one.
    This implementation allows for an easier evaluation of the data
    files in the same format as originally proposed by Gulordava et al.
    The mandatory fields of the header are:
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
        row2 = next(rows)
        assert(row["sent"] == row2["sent"])
        assert(row["class"] == "correct")
        assert(row2["class"] == "wrong")
        sent = row["sent"].split()
        good_form = row["form"]
        bad_form = row2["form"]
        target_idx = row["len_prefix"]
        if args.mask_target:
            sent[int(target_idx)] = "***mask***"
        sent = " ".join(sent)
        data.append((sent, target_idx, good_form, bad_form))
    return data


def load_model():
    """
    Load a previously trained (on CUDA) language model.
    """
    with open(args.checkpoint, "rb") as f:
        print("Loading the model...")
        if args.cuda:
            model = torch.load(f)
        else:
            # Convert model trained on CUDA to CPU model.
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


def evaluate(data, model, dictionary):
    """
    Evaluate a language model on certain data examples.
    :param data: data to be evaluated by the language model
    :param model: a pre-trained language model
    :param dictionary: the vocabulary of the corpus on which
                       the language model has been trained
    """
    model.eval()
    hidden = model.init_hidden(bsz=1)
    for (sent, target_idx, good, bad) in tqdm(data):
        if args.mask_target:
            pre, target, post = sent.split("***")
            if "mask" in target.lower():
                target = "[MASK]"
            all_token_idx = tokenize_sentence(dictionary, pre + target + post)
        else:
            all_token_idx = tokenize_sentence(dictionary, sent)
        try:
            word_ids = [dictionary.word2idx[good], dictionary.word2idx[bad]]
        except KeyError:
            print("Skipping bad wins: %s and %s." % (good, bad))
            continue
        tokens_batch = all_token_idx.view(1, -1).t().contiguous()
        output, hidden = model(tokens_batch, hidden)
        output_flat = output.view(-1, len(dictionary))
        log_probs = F.log_softmax(output_flat).data
        log_probs_np = log_probs.cpu().numpy()

        # Create mask for the target word prediction
        mask = [False] * len(all_token_idx)
        mask[int(target_idx) - 1] = True
        mask = array(mask)

        # Get scores for the masked target word
        res = log_probs_np[mask][0]
        scores = [float(x) for x in res[word_ids]]

        hidden = repackage_hidden(hidden)
        good_score = scores[0]
        bad_score = scores[1]
        print(str(good_score > bad_score),
              good, good_score, bad, bad_score,
              sent.encode("utf8"), sep=u"\t")


def main():
    # Read and load the data to be evaluated
    if args.original:
        data = read_datafile_original()
    else:
        data = read_datafile()

    # Load the corpus dictionary
    dictionary = Dictionary(args.vocab)
    print("Vocabulary size = ", len(dictionary))

    # Load the model
    model = load_model()

    # Evaluate the sentences
    evaluate(data, model, dictionary)


if __name__ == "__main__":
    main()
