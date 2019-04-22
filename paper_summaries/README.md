# Do LSTMs learn Syntax?

## Why LSTMs?



## Common practices when evaluating the syntactic benefits of LSTMs

- in most of the papers, rare words are replaced by their part-of-speech tags, using the Penn Treebank tagset.
- when wanting to evaluate certain syntactic structures, it is common practice to isolate it in some controlled way by constructing your own (artificial) corpus. For instance, Marvin and Linzen (2018) construct minimal pairs of grammatical and ungrammatical sentences based on templates described by non-recursive context-free grammars. The model is correct if it assigns the grammatical sentence a higher probability than to the ungrammatical one.
- when evaluating subject-verb agreement, there are two common baselines: 
	* predict the number of the verb based on the number of the most recent noun
	* always predict the number of the verb to be singular as these are the most common in the corpus (majority baseline)
- two ways of evaluating syntax captured by a language model on natural language:
	* simplified setting: evaluate prediction only for the target word in the dependency i.e. compare the probability that the LM assigns to a single word that is the locus of ungrammaticality (Gulordava et al., 2018)
	* general setting: evaluate prediction for the complete sentence; if two closely matched sentences differ only in their grammaticality, the probability of the grammatical sentence should be higher than the probability of the ungrammatical one (Marvin and Linzen, 2018)

## Various findings: what can or cannot LSTMs do?

- can learn grammatical structures and dependencies of context-free grammars (Elman, 1990)
- can learn the fine distinction between sequences of spikes separated by either 50 or 49 discrete time steps (Gers and Schmidhuber, 2000)
- they can learn to process a simple deterministic context free language (DCFL), a^n b^n, in a way that generalizes to longer strings by developing up/down counters in separate regions of phase space (Chalup and Blair, 2003)
- their generalisation ability is very unstable during training and highly dependeds on weight initialisations of the hidden states (Boden and Wiles, 2003)
- many other aspects (such as window length, number of hidden units and the generative distribution) can impact the stability of a vanilla LSTM when learning to model formal languages (Suzgun, 2019)
- Greff et al. (2015) examined the capabilities of different variants of LSTM architectures and concluded that the forget gate and the output activation function are its most critical components
- adding a bias of 1 to the LSTM’s forget gate closes the gap between the LSTM and the GRU (Jozefowicz, 2015)
- they can learn artificial context-free languages, as well as nesting and indentation (Karpathy, 2015)
- LSTMs can learn to approximate structure-sensitive dependencies fairly well given explicit supervision (Linzen et al., 2016)
- RNNs might be relying on semantic or collocational/frequency-based information, rather than purely on syntactic structure
- RNNs are better at long-distance agreement when they construct rich lexical representations of words (Bernardy and Lappin, 2017)
- in the subject-verb agreement task, Linzen et al. (2016) show that LSTMs can capture a non-trivial amount of grammatical structure given targeted supervision, but they make a lot of mistakes when no direct supervision is provided (i.e. when solely using the language modeling signal); function words, verbs and other syntactically informative elements play an important role in the model's ability to correctly predict the verb's number
- Gulordava et al. (2018) claim that a careful hyperparameter search is crucial to obtain RNNs that are not only good at language modeling, but able to extract syntactic generalizations

*Note* that LSTMs and RNNs are used interchangeably (at least in the vast majority of the papers I have read). 
