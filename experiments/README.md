# Evaluate LSTMs for syntax 

This repository does _not_ contain the code to _train_ a language model. Instead, it should get you started quickly on testing LSTMs' syntactic abilities. Here you can find the code to make templates for your desired syntactic constructions and evaluate a pre-trained language model on them.

## Data format

Three data formats are compatible with the evaluation script:

1. Original
    - This is the original _.tab_ file format proposed by Gulordava et al. (2018).
    - An example file is available [here](https://raw.githubusercontent.com/facebookresearch/colorlessgreenRNNs/master/data/agreement/English/generated.tab).
    
2. Word-focused format
    - Because Gulordava et al.'s format contains a lot of extra information that is not useful for our purposes, I created another file format that needs to have the following header fields: 
        - _pattern_ -- this is the name of the syntactic test case
        - _form_ -- grammatical form of the target word
        - _form_alt_ -- ungrammatical form of the target word
        - _sent_ -- sentence to be evaluated
        - _len_prefix_ -- number of words up to and excluding the target
    - This format is designed for tests on specific words, and not on the whole sentence. You can only introduce one error at the time and test for it. The locus of ungrammaticality specified by _len_prefix_.
    - An example file is provided in _preliminary_experiments_ under the [data/](data) directory.

3. Sentence-focused format
    - This format allows for evaluations between pairs of sentences that differ in more than one word (so you can introduce multiple errors).
    - The file format should have the following header fields:
        - _pattern_ -- name of the syntactic test case
        - _sent_ -- the grammatical form of the sentence 
        - _sent_alt_ -- the ungrammatical form of the sentence
    - An example is provided in the _my_coord_templates_ file under the [data/](data) directory.

## Requirements

* [Python](https://www.python.org/downloads/) (tested with 3.5.2)
* [PyTorch](https://pytorch.org/get-started/locally/) (tested with 1.0.0 )
* [pytorch_pretrained_bert](https://github.com/huggingface/pytorch-pretrained-BERT)
* [numpy](https://github.com/numpy/numpy)
* [tqdm](https://github.com/tqdm/tqdm)

## Instructions

**1. Get a language model**

To test a pre-trained language model (LM), you will need the *.pt* model file and the vocabulary corresponding to the LM's training corpus.

If you want to use Gulordava et al.'s (2018) language model (perplexity 52.10), download the vocabulary corpus from [here](https://dl.fbaipublicfiles.com/colorless-green-rnns/training-data/English/vocab.txt) and place it under the [data/](data) directory. Then, download Gulordava et al.'s pretrained language model from [here](https://dl.fbaipublicfiles.com/colorless-green-rnns/best-models/English/hidden650_batch128_dropout0.2_lr20.0.pt). For more details about this model, check their [paper](https://arxiv.org/abs/1803.11138) and [code](https://github.com/facebookresearch/colorlessgreenRNNs).

I have also trained my own language model in a multitask learning setting, using part-of-speech tagging as the secondary objective (perplexity 63.14). Get in touch if you want to try it.

**2. Get or create some syntactic test cases.**

You could use some of the templates provided by Linzen et al. (2016), Gulordava et al. (2018) or Marvin and Linzen (2018) to test the model's syntactic abilities (mainly agreement in number, but check their papers for details).

We also provide templates for verb agreement with a short/long NP-coordination and for tense agreement in anaphoric sentences (under the [data/](data) directory).

To create the templates for NP-coordination, run:

```bash
python make_templates.py --filename data/my_coord_templates.tab --type coord
```

To create the templates for verbal tense agreement, just replace *coord* with *tense*. The templates will be generated in the _sentence-focused_ format.

**3. Evaluate your language model**

To evaluate a language model, you just need to run ```bash evaluate_lm.py``` with your desired flags.

For instance, to replicate Gulordava et al.'s (2018) results, run:

```bash
python evaluate_lm.py --data data/generated.tab --original --eval_target_word --vocab data/vocab.txt --model $path/to/pretrained/lang_model_name.pt$ > results/results_generated.txt
```

To replicate the results on my coordination templates ([results/coord_whole_sentences.txt](results)) run:

```bash
python evaluate_lm.py --data data/my_coord_templates.tab --vocab data/vocab.txt --model $path/to/pretrained/lang_model_name.pt$ > results/lm_coord_templates_whole_sentences.txt
```

To evaluate one of BERT's language models, run:

```bash
python evaluate_lm.py --data data/my_coord_templates.tab --vocab data/vocab.txt --model $BERT_MODEL_NAME$ --mask_target --eval_target_word > results/bert_coord_templates_whole_sentences.txt
```

where ```$BERT_MODEL_NAME$``` can be one of these: _bert_base_uncased_, _bert_base_cased_, _bert_large_uncased_, or _bert_large_cased_. Note that evaluating a BERT LM only works for individual word prediction, which should be masked.

## Flags
-------------------------

* **data** - Path to the file containing certain test cases (templates or not). It needs to be in one of the formats specified above.
* **model** - Path to the pre-trained language model (.pt file)
* **vocab** - Path to the vocabulary (as used by the LM during its training)
* **original** - Whether the data is in the _original_ format (i.e. as used by Gulordava et al.)
* **eval_target_word** - Whether to evaluate each word individually (if set) or rather the sentence as a whole (if not set; this is the default as it captures word interactions and is not limited to evaluating pairs of sentences that differ in only one word)
* **print_word_probs** - Whether to print the log probability of each word in the sentence (works only if you evaluate the whole sentence i.e. you haven't set the eval_target_word flag).
* **mask_target** - Whether to mask or not the target word.
* **seed** - The random seed.
* **cuda** - Whether to use CUDA or not.

## License
-------------------------

Everything is licensed under the MIT license.
