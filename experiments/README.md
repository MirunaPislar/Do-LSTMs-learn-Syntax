# Experiments: Do LSTMs learn Syntax?

## Introduction



## Instructions

1. Download the vocabulary corpus from [here](https://dl.fbaipublicfiles.com/colorless-green-rnns/training-data/English/vocab.txt) and place it under the [data/](data) directory.

2. Download Gulordava et al.'s pretrained language model from [here](https://dl.fbaipublicfiles.com/colorless-green-rnns/best-models/English/hidden650_batch128_dropout0.2_lr20.0.pt) and place it under the [trained_models](trained_models) directory. For more details check their [paper](https://arxiv.org/abs/1803.11138) and [code](https://github.com/facebookresearch/colorlessgreenRNNs).

3. To evaluate a certain language model, run:

```bash
python3 evaluate_lm.py --data data/generated.tab --vocab data/ --checkpoint trained_models/$language_model.pt$ > results/res_paper_generated.txt
```

## Requirements
* [Python](https://www.python.org/downloads/) tested with 3.5.2
* [PyTorch](https://pytorch.org/get-started/locally/) tested with 1.0.0 
* [numpy](https://github.com/numpy/numpy)
* [tqdm](https://github.com/tqdm/tqdm)

## License

Everything is licensed under the MIT license.
