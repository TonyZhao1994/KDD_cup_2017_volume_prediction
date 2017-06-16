# KDD_cup_2017_volume_prediction

## Task period
2017.04 to 2017.06

## Task background and requirement

[Refer to this link](https://tianchi.aliyun.com/competition/introduction.htm?spm=5176.100150.711.7.o4v0wU&raceId=231597)

## Task Code instruction

### Raw data disposal

Divide one day into 72 parts with 20 minutes as a time window while caculate the total numbers, the numbers of using etc and the numbers of different type of vehicles passing one tollgate 
(totally 6 considering direction) at each time window.

### Fill up the missing data

Import the statistical data from step 1, classify the dataset into 5 classed according to tollgate and direction. We need to fill up the missing data because we will use last 2 hour volumes data 
as features.

### Feature engineering

1.Take last 2 hour volumes as input features, i.e. 6 dimensions

2.Delete all filled data because of effects of inaccuracy

3.Add specific time dimension: such as month, week, weekday, hour and which part of 72 time windows

4.Add weather information, though I don't use it finally

5.Add another dimension of judging whether today is holiday

6.Encode and Disperse irrelevant features with onehot coding

### Compress the training ground truth with log function

As the objective function is MAPE (Mean Average Percentage Error), the final score will be more sensitive to low volume time periods. Comparing with high volume time periods, the same error with low
volume will lead to larger MAPE. So we use log funciton to  realize nonlinear transformation since our actual objective function is MSE.

### Selection of validation sets with KNN

The final score online is highly related to the selection of validation sets. According to the given last 2 hour volume data of predicting period, we use KNN to select the nearest periods from the 
training set after dividing the data into 10 parts (10morning, 11m, 20m, 30m, 31m, 10aftrenoon, 11a, 20a, 30a, 31a).

### Train models with xgboost

Finally, we train 10 xgboost models to accomplish prediction task.

