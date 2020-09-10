import csv
import os
import numpy as np
np.random.seed(1337)
map = {0:65, 1:78, 2:68}
def intake():
    files = sorted(os.listdir(os.path.dirname(os.path.realpath(__file__))+"/../Downloads"))
    print(files)
    people = []
    for file in files:
        csv_file = open(os.path.dirname(os.path.realpath(__file__))+"/../Downloads/"+file)
        csv_reader = csv.reader(csv_file, delimiter=',')
        ands = []
        anand = []
        for row in csv_reader:
            if row[0]==str(map[len(anand)]):
                anand.append(np.array([round(float(string)) for string in row]))
            else:
                anand = []
            if len(anand) == 3:
                ands.append(np.array(anand))
                anand = []
        people.append(np.array(ands))
    return people
def preprocess(usernum, intake): #75,25 split
    user_train = np.zeros((0,3,2))
    user_test = np.zeros((0,3,2))
    other_train = np.zeros((0,3,2))
    other_test = np.zeros((0,3,2))
    for i, data in enumerate(intake):
        data = np.delete(data, 0, 2)
        #data
        #print(data)
        temp = np.pad(data[:,:,0],((0,0),(1,0)), mode='constant')[:, :-1]
        temp[:,0] = data[:,:,0][:,0]
        delta = np.insert(data,0,temp,2).dot(np.array([[-1,0],[1,0],[0,1]]))
        if i==usernum:
            user_train = np.append(user_train,delta[:int(delta.shape[0]*3/4)], axis=0)
            user_test = np.append(user_test,delta[int(delta.shape[0]*3/4):], axis=0)
        else:
            other_train = np.append(other_train,delta[:int(delta.shape[0]*3/4)], axis=0)
            other_test = np.append(other_test,delta[int(delta.shape[0]*3/4):], axis=0)
    user_train = np.tile(user_train, (int(other_train.shape[0]/user_train.shape[0]),1,1))
    user_test = np.tile(user_test, (int(other_test.shape[0]/user_test.shape[0]),1,1))
    return ((user_train, other_train),(user_test,other_test))

def convert(data):
    train_data = np.concatenate((data[0][0], data[0][1]))
    train_data = train_data.reshape(train_data.shape[0], 6)
    train_label = np.concatenate((np.ones((data[0][0].shape[0])), np.zeros((data[0][1].shape[0]))))
    s = np.arange(train_label.shape[0])
    np.random.shuffle(s)
    train_data = train_data[s]
    train_label = train_label[s]

    test_data = np.concatenate((data[1][0], data[1][1]))
    test_data = test_data.reshape(test_data.shape[0], 6)
    test_label = np.concatenate((np.ones((data[1][0].shape[0])), np.zeros((data[1][1].shape[0]))))
    s = np.arange(test_label.shape[0])
    np.random.shuffle(s)
    test_data = test_data[s]
    test_label = test_label[s]
    return ((train_data, train_label), (test_data, test_label))
