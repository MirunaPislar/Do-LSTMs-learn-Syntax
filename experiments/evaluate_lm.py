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
parser.add_argument("--vocab", type=str, default="data/",
                    help="Path to the directory to the corpus "
                         "vocabulary (of the language model).")
parser.add_argument("--checkpoint", type=str,
                    help="Language model checkpoint to be used.")
parser.add_argument("--seed", type=int, default=532,
                    help="Random seed")
parser.add_argument("--cuda", action="store_true",
                    help="use CUDA")
args = parser.parse_args()
eval_batch_size = 1


def read_datafile(mask_target=False):
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
        if mask_target:
            sent[int(target_idx)] = "***mask***"
        sent = " ".join(sent)
        data.append((sent, target_idx, good_form, bad_form))
    return data


def load_model():
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        if not args.cuda:
            print("WARNING: you have a CUDA device available. "
                  "Consider running with --cuda.")
        else:
            torch.cuda.manual_seed(args.seed)

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
    # Detach hidden states from their history.
    if isinstance(hidden, torch.Tensor):
        return hidden.detach()
    else:
        return tuple(repackage_hidden(v) for v in hidden)


def batchify(data, cuda):
    # Work out how cleanly we can divide the dataset into bsz parts.
    nbatch = data.size(0) // eval_batch_size
    # Trim off any extra elements that wouldn't cleanly fit (remainders).
    data = data.narrow(0, 0, nbatch * eval_batch_size)
    # Evenly divide the data across the bsz batches.
    data = data.view(eval_batch_size, -1).t().contiguous()
    if cuda:
        data = data.cuda()
    return data


def get_scores_for_words(
        model, hidden, dictionary, sent, target_idx,
        good, bad, mask_target=False):
    if mask_target:
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
        return None
    tokens_batch = batchify(all_token_idx, args.cuda)
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
    scores = res[word_ids]
    return [float(x) for x in scores], hidden


def evaluate(data, model, dictionary):
    model.eval()
    hidden = model.init_hidden(eval_batch_size)
    for (masked_sent, target_idx, good, bad) in tqdm(data):
        scores, hidden = get_scores_for_words(
            model, hidden, dictionary, masked_sent,
            target_idx, good, bad)
        hidden = repackage_hidden(hidden)
        if scores is None:
            continue
        good_score = scores[0]
        bad_score = scores[1]
        print(str(good_score > bad_score),
              good, good_score, bad, bad_score,
              masked_sent.encode("utf8"), sep=u"\t")


def main():
    # Read and load the data to be evaluated
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
