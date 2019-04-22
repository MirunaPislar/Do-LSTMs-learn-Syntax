# Do LSTMs learn Syntax?

Time underlies many aspects of human behaviour. 

In 1990, Elman proposed representing time implicitly, by the effect it has on processing. In this framework, hidden units are fed back to themselves determining systems to gain dynamic properties and become responsive to temporal sequences. Therefore, Recurrent Neural Networks (RNNs) arose from the necessity to represent time. 

RNNs are both general and effective at capturing long-term temporal dependencies. Their gated variants, Long Short-term Memories (LSTMs), have proven even better at modelling long-distance regularities and have become the de facto building block in many neural processing tasks, such as machine translation and language modelling.

RNNs do not explicitly encode hierarchical structures encountered in many natural settings, amongst which language. However, due to their memory and processing capacity, they are able to develop powerful internal representations that reflect task demands in the context of prior internal states. The question arising is, then: **are RNNs able to implicitly discover syntactic features?**

This is a fascinating topic that requires further investigations as there is no definite answer yet.

In this repository, I give away:
 - [a selection of papers](#papers) that I found relevant/interesting on the topic with links to the code, if publicly available
 - some [experimental code](experiments) to build your own templates and run your own evaluation experiments on your favourite pre-trained language model (recurrent or non-recurrent)
 - some [paper summaries](paper-summaries) along with my thoughts and findings related to the topic

# <a name="papers">Some relevant papers</a>

[Finding Structure in Time](https://crl.ucsd.edu/~elman/Papers/fsit.pdf), Elman (1990)

[Distributed Representations, Simple Recurrent Networks, and Grammatical Structure](https://link.springer.com/content/pdf/10.1023/A:1022699029236.pdf), Elman (1991)

[Learning and development in neural networks: The importance of starting small](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.128.4487&rep=rep1&type=pdf), Elman (1993)

[A Recurrent Neural Network that Learns to Count](http://fuzzy.cs.ovgu.de/publications/other/RodWilElm99.pdf), Rodriguez et al. (1999)

[Toward a connectionist model of recursion in human linguistic performance](https://pdfs.semanticscholar.org/6111/e54dca481ee9176f718e2f33281d944d1fcd.pdf), Christiansen and Chater (1999)

[Recurrent Nets That Time and Count](ftp://ftp.idsia.ch/pub/juergen/TimeCount-IJCNN2000.pdf), Gers and Schmidhuber (2000)

[Context-free and context-sensitive dynamics in recurrent neural networks](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.1917&rep=rep1&type=pdf),  Boden and Wiles

[LSTM recurrent networks learn simple context-free and context-sensitive languages](https://www.researchgate.net/publication/3303030_LSTM_recurrent_networks_learn_simple_context-free_and_context-sensitive_languages), Gers and Schmidhuber (2001)

[Incremental training of first order recurrent neural networks to predict a context-sensitive language](https://www.cse.unsw.edu.au/~blair/pubs/2003ChalupBlairNN.pdf), Chalup and Blair (2003)

[Statistical Representation of Grammaticality Judgements: the Limits of N-Gram Models](https://pdfs.semanticscholar.org/e442/a3ca917b8b491375c9662843f7fd8c729598.pdf), Clark et al. (2013)

[LSTM: A Search Space Odyssey](https://arxiv.org/abs/1503.04069), Greff et al. (2015)

[Unsupervised Prediction of Acceptability Judgements](https://www.aclweb.org/anthology/P15-1156), Lau et al. (2015)

[Structures, Not Strings: Linguistics as Part of the Cognitive Sciences](https://www.sciencedirect.com/science/article/pii/S1364661315002326), Everaert et al. (2015) 

[An Empirical Exploration of Recurrent Network Architectures](http://proceedings.mlr.press/v37/jozefowicz15.pdf), Jozefowicz et al. (2015)

[The Now-or-Never bottleneck: A fundamental constraint on language](http://cnl.psych.cornell.edu/pubs/2016-cc-BBS.pdf), Christiansen and Chater (2016)

[Assessing the Ability of LSTMs to Learn Syntax-Sensitive Dependencies](http://aclweb.org/anthology/Q16-1037), Linzen et al. (2016) [[code]](https://github.com/TalLinzen/rnn_agreement)

[Recurrent Neural Network Grammars](https://www.aclweb.org/anthology/N16-1024), Dyer et al. (2016)

[Sequence Memory Constraints Give Rise to Language-Like Structure through Iterated Learning](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0168532), Cornish et al. (2017)

[Exploring the Syntactic Abilities of RNNs with Multi-task Learning](http://aclweb.org/anthology/K17-1003), Enguehard et al. (2017) [[code]](https://github.com/emengd/multitask-agreement)

[What Do Recurrent Neural Network Grammars Learn About Syntax?](http://aclweb.org/anthology/E17-1117), Kuncoro et al. (2017)

[On the State of the Art of Evaluation in Neural Language Models](https://arxiv.org/pdf/1707.05589.pdf), Melis et al. (2017) 

[How Grammatical is Character-level Neural Machine Translation? Assessing MT Quality with Contrastive Translation Pairs](https://aclweb.org/anthology/E17-2060), Rico Sennrich (2017)

[Using Deep Neural Networks to Learn Syntactic Agreement](http://csli-lilt.stanford.edu/ojs/index.php/LiLT/article/view/94/79), Bernardy and Lappin (2017)

[Colorless green recurrent networks dream hierarchically](http://aclweb.org/anthology/N18-1108), Gulordava et al. (2018) [[code]](https://github.com/facebookresearch/colorlessgreenRNNs)

[Targeted Syntactic Evaluation of Language Models](http://aclweb.org/anthology/D18-1151), Marvin and Linzen (2018) [[code]](https://github.com/BeckyMarvin/LM_syneval)

[Deep RNNs Encode Soft Hierarchical Syntax](https://aclweb.org/anthology/P18-2003), Blevins et al. (2018)

[Why Self-Attention? A Targeted Evaluation of Neural Machine Translation Architectures](https://aclweb.org/anthology/D18-1458), Tang et al. (2018)

[The Importance of Being Recurrent for Modeling Hierarchical Structure](http://aclweb.org/anthology/D18-1503), Tran et al. (2018) [[code]](https://github.com/ketranm/fan_vs_rnn)

[What can linguistics and deep learning contribute to each other?](https://arxiv.org/pdf/1809.04179.pdf), Linzen (2018)

[Do RNNs learn human-like abstract word order preferences?](https://arxiv.org/pdf/1811.01866.pdf), Futrell and Levy (2018) [[code]](https://github.com/langprocgroup/rnn_soft_constraints)

[What do RNN Language Models Learn about Filler–Gap Dependencies?](http://aclweb.org/anthology/W18-5423), Wilcox et al. (2018)

[LSTMs Can Learn Syntax-Sensitive Dependencies Well, But Modeling Structure Makes Them Better](http://aclweb.org/anthology/P18-1132), Kuncoro et al. (2018)

[On Evaluating the Generalization of LSTM Models in Formal Languages](https://arxiv.org/pdf/1811.01001.pdf), Suzgun et al. [[code]](https://github.com/suzgunmirac/lstm-eval)

[Evaluating the Ability of LSTMs to Learn Context-Free Grammars](http://aclweb.org/anthology/W18-5414), Sennhauser and Berwick (2018)

[Finding Syntax in Human Encephalography with Beam Search](http://aclweb.org/anthology/P18-1254), Hale et al. (2018)

[Ordered Neurons: Integrating Tree Structures into Recurrent Neural Networks](https://arxiv.org/pdf/1810.09536.pdf), Shen et al. (2018) [[code]](https://github.com/yikangshen/Ordered-Neurons)

[Sharp Nearby, Fuzzy Far Away: How Neural Language Models Use Context](http://aclweb.org/anthology/P18-1027), Khandelwal et al. (2018)

[On the State of the Art of Evaluation in Neural Language Models](https://openreview.net/pdf?id=ByJHuTgA-), Melis et al. (2018)

[Neural Network Acceptability Judgments](https://arxiv.org/pdf/1805.12471.pdf), Warstadt et al. (2018) [[code]](https://github.com/nyu-mll/CoLA-baselines)

[Assessing BERT’s Syntactic Abilities](https://arxiv.org/pdf/1901.05287.pdf), Goldberg (2019) [[code]](https://github.com/yoavg/bert-syntax)

[Human few-shot learning of compositional instructions](https://arxiv.org/pdf/1901.04587.pdf), Lake, Linzen, and Baroni (2019)

[Neural Language Models as Psycholinguistic Subjects: Representations of Syntactic State](https://arxiv.org/pdf/1903.03260.pdf), Futrell et al. (2019) [[code]](https://github.com/langprocgroup/nn_syntactic_state)

[Studying the Inductive Biases of RNNs with Synthetic Variations of Natural Languages](https://arxiv.org/pdf/1903.06400.pdf),  Ravfogel, Goldberg, and Linzen (2019)
