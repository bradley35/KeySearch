import extract as e
import xgboost as xgb
import numpy as np
import matplotlib.pyplot as plt
import json
data_all = e.intake()
outcomes = []
for i in range(0, len(data_all)):
    data_1 = e.convert(e.preprocess(i,e.intake()))
    dtrain = xgb.DMatrix(data_1[0][0], label = data_1[0][1])
    dtest = xgb.DMatrix(data_1[1][0], label = data_1[1][1])

    y_test = data_1[1][1]

    param = {'booster':'gbtree', 'subsample':0.1,'max_depth': 15, 'scale_pos_weight':1, 'learning_rate': 0.01, 'min_child_weight':1, 'gamma':1, 'verbosity': 0, 'objective': 'binary:logistic'}#https://xgboost.readthedocs.io/en/latest/parameter.html
    num_round = 100
    evallist = [(dtest, 'Test'), (dtrain, 'Train')]
    bst = xgb.train(param, dtrain, num_round, evallist)
    #xgb.plot_importance(bst)
    #plt.show()
    prdt = 1-bst.predict(dtest)
    results = np.round(np.absolute(prdt-y_test))

    outcomes.append(np.sum(results)/results.shape[0])
    with open('xgb.json', 'w') as outfile:
        json.dump(outcomes, outfile)
print(outcomes)
