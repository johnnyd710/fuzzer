## Modules
learners/* is the learning algorithms 
mappers/* turn queries into system/device inputs, usually ON the system itself
classifiers/* are the algorithms that translate time series data to clusters


## Scripts
1. train.py: "warm up phase", train the State Detector on offline data collected (and saving centroids)
2. main.py: running the algorithm
3. test_harness.py: for evaluating clustering