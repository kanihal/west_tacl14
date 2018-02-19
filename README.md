Build & Run Instructions
-------------
This code depends on Java 7 and Java 8 and Maven 3 (http://maven.apache.org). 
Python3 is also required to for positive/negative sentiment analysis using logistic regression available in `sklearn` library.

##### Install PSL
The algorithms for these experiments are implemented in the PSL library, version 1.1 (https://github.com/linqs/psl). Clone this particular project and Run 

```
git clone https://github.com/linqs/psl
cd psl
git checkout 1.1
export JAVA_HOME = /path/to/jave8(oracle 1.8)
mvn install
```

##### Build west_tacl14
```
cd this/project/dir
export JAVA_HOME = /path/to/jave7(oracle 1.7)
mvn install
```

##### Dataset
we are using [wiki-Rfa](https://snap.stanford.edu/data/wiki-RfA.html) dataset as mentioned west et al. paper.

Wikipedia Requests for Adminship (with text)
For a Wikipedia editor to become an administrator, a request for adminship (RfA) must be submitted, either by the candidate or by another community member. Subsequently, any Wikipedia member may cast a supporting, neutral, or opposing vote. Besides, there is also a rich textual component in RfAs: each vote is typically accompanied by a short comment.


preprocessing scripts are available in `data` folder.

## Experiment Results 
This section will be updated with more info - see the note above

#### Sentiment Analysis based only comment text (lexicon based SA)
We used logistic classifier to classify comment text as Negative/positive  sentiment. Use `sentiment_analysis.py` in `senti` folder for this.

We train this sentiment analyser for comments between 1000 users.(about 8000 comments out of 160k comments i.e. 5%, so as to make sure during combined(network+lexicon) evaluations, it would not have seen most of the comments that are going to be there during testing period, hence we simulating real world scenario where you see text which you might not have trained upon (no overfitting)
```
             precision    recall  f1-score   support

         -1       0.77      0.33      0.46      2989
          1       0.73      0.95      0.83      5750

avg / total       0.75      0.74      0.70      8739

---------------------------------------------------------

The accuracy score is 73.81%

The postive AUC/PrecisionRecall is 86.21%
The negative AUC/PrecisionRrecall is 67.09%
The AUC/ROC is 79.05%
```

#### Sentiment Analysis as positive/negative edge detection in the network
use `runWikiNet.sh` to run the edge sign prediction task using psl.


For 70% edge evidence ratio, the results for inferring the polarity of other 30% are

```
Area under positive-class PR curve: 0.9510398800525737
Area under negative-class PR curve: 0.6243350940902824
Area under ROC curve: 0.8417226559882047

Method quad-mle-100-5.0, fold 0, auprc positive: 0.9510398800525737, negative: 0.6243350940902824, auROC: 0.8417226559882047
Method quad-mle-100-5.0, auprc positive: (mean/variance) 0.9510398800525737  /  0.0
Method quad-mle-100-5.0, auprc negative: (mean/variance) 0.6243350940902824  /  0.0
Method quad-mle-100-5.0, auROC: (mean/variance) 0.8417226559882047  /  0.0

```

For 40% edge evidence ratio
```
Area under positive-class PR curve: 0.9345657380143807
Area under negative-class PR curve: 0.42931297340431146
Area under ROC curve: 0.7670102734573235

Method quad-mle-100-5.0, fold 0, auprc positive: 0.9345657380143807, negative: 0.42931297340431146, auROC: 0.7670102734573235
Method quad-mle-100-5.0, auprc positive: (mean/variance) 0.9345657380143807  /  0.0
Method quad-mle-100-5.0, auprc negative: (mean/variance) 0.42931297340431146  /  0.0
Method quad-mle-100-5.0, auROC: (mean/variance) 0.7670102734573235  /  0.0

```

#### Sentiment Analysis using both comment text (lexicon features) and network structure
use `runWikiCombined.sh` to run the edge sign prediction task using psl.

Results for 70% of edges shown as evidence to infer polarity for the leftover 30% of edges

```
Area under positive-class PR curve: 0.9681823778320722
Area under negative-class PR curve: 0.7119410475513349
Area under ROC curve: 0.8919161751893306



Method quad-mle-100-5.0, fold 0, auprc positive: 0.9681823778320722, negative: 0.7119410475513349, auROC: 0.8919161751893306
Method quad-mle-100-5.0, auprc positive: (mean/variance) 0.9681823778320722  /  0.0
Method quad-mle-100-5.0, auprc negative: (mean/variance) 0.7119410475513349  /  0.0
Method quad-mle-100-5.0, auROC: (mean/variance) 0.8919161751893306  /  0.0

```

for 40% edge evidence ratio
```
Area under positive-class PR curve: 0.9757467522834871
Area under negative-class PR curve: 0.6951085647558664
Area under ROC curve: 0.9009646428325506

Method quad-mle-100-5.0, fold 0, auprc positive: 0.9757467522834871, negative: 0.6951085647558664, auROC: 0.9009646428325506
Method quad-mle-100-5.0, auprc positive: (mean/variance) 0.9757467522834871  /  0.0
Method quad-mle-100-5.0, auprc negative: (mean/variance) 0.6951085647558664  /  0.0
Method quad-mle-100-5.0, auROC: (mean/variance) 0.9009646428325506  /  0.0
```
#### Discussion
We are able to reproduce the results shown in the west et al. paper i.e. Combined model for predicting person-person sentiment polarity performs better than individual models mentioned above.
