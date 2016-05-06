# hmm-postagging-py

> A HMM algorithm for POS tagging. Using MLE to get the parameters.

Cause we assume the hidden states are the tag of POS, and the train corpus are tagged. So we only need to do some statistics, and calculate the parameters (*Pi & emission & transition*).

- Pi is the vector of start probability of tag.
- emission is the matrix of observation associated with hidden state.
- transition is the matrix of probability of transition from state *i* to state *j*


The tags of pos by CTB

- Verb, adjective (4): VA, VC, VE, VV
- Noun (3): NR, NT, NN
- Localizer (1): LC
- Pronoun (1): PN
- Determiner and number (3): DT, CD, OD
- Measure word (1): M
- Adverb (1): AD
- Preposition (1): P
- Conjunction (2): CC, CS
- Particle (8): DEC, DEG, DER, DEV, SP, AS, ETC, SP, MSP
- Others (8): IJ, ON, PU, JJ, FW, LB, SB, BA

33 tags in total.