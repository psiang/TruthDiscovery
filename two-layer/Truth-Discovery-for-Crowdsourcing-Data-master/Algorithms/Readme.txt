This folder contains different methodologies for aggregating crowdsourced data (ratings).

The average_voting.py file: aggregating crowd data by averaging the ratings.

The MajorityVoting.py file: aggregating the data collected from crowds through majority voting.

The DavidSkene_EM.py file: it is a python implementation of extension on David and Skene model. The David and Skene model is presented here: http://www.jstor.org/stable/2346806?origin=JSTOR-pdf. (A. P. Dawid and A. M. Skene. 1979.  Maximum Likelihood Estimation of Observer Error-Rates Using the EM Algorithm.  Journal of RoyalStatistical Society, Series C (Applied Statistics) 28(1):20--28.)
The extension of the model is shown in the paper as: http://www.transacl.org/wp-content/uploads/2014/10/taclpaper60.pdf (R. J. Passonneau and B. Carpenter. 2014.  The Benefits of a Model of Annotation.  Transactions of the Association for Computational Linguistics 2(Oct):311-326.)

The ExpectationMaximization.py file: the file contains the python implementation of GLAD algorithm proposed by Whitehill et al. The model includes both the worker expertise and task difficulty while inferencing the truths. The detailed algorithm is
described here: http://papers.nips.cc/paper/3644-whose-vote-should-count-more-optimal-integration-of-labels-from-labelers-of-unknown-expertise.pdf

The WeightedVoting.py file: it is a python implementation of the optimization based truth discovery model. Two different methods are developed here: 1. For categorical data. 2. For numerical data. The details of the description of the algorithms are presented here:
https://pdfs.semanticscholar.org/7dd6/74c3bf55409411d3f08868fff1def9438c01.pdf (Q. Li et al. "Resolving conflicts in heterogeneous data by truth discovery and source reliability estimation." Proceedings of the 2014 ACM SIGMOD international conference on Management of data. ACM, 2014.)

