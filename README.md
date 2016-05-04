# hmm-postagging-py

> A HMM algorithm for POS tagging. Using MLE to get the parameters.

Cause we assume the hidden states are the tag of POS, and the train corpus are tagged. So we only need to do some statistics, and calculate the parameters (*Pi & emission & transition*).

- Pi is the vector of start probability of tag.
- emission is the matrix of observation associated with hidden state.
- transition is the matrix of probability of transition from state *i* to state *j*

