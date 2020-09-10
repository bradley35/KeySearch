import extract as e
import numpy as np
import matplotlib.pyplot as plt
import keras as k
import json
data_all = e.intake()
outcomes = []
for i in range(0, len(data_all)):
    data = e.convert(e.preprocess(i,e.intake()))
    model = k.models.Sequential()
    model.add(k.layers.Dense(8, input_dim=6, activation='sigmoid'))
    model.add(k.layers.Dense(6, activation='sigmoid'))
    model.add(k.layers.Dense(4, activation='sigmoid'))
    model.add(k.layers.Dense(4, activation='sigmoid'))
    model.add(k.layers.Dense(4, activation='sigmoid'))
    model.add(k.layers.Dense(2, activation='sigmoid'))

    model.add(k.layers.Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer=k.optimizers.Adam(lr=0.00005), metrics=['accuracy'])

    x_train = data[0][0]
    y_train = data[0][1]

    x_test = data[1][0]
    y_test = data[1][1]
    es = k.callbacks.EarlyStopping(monitor='val_loss', patience=100)
    print(len(x_train))
    history = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=15000, batch_size=500, callbacks=[es], verbose=0)

    #plt.plot(history.history['loss'], label='train')
    #plt.plot(history.history['val_loss'], label='test')
    #plt.legend()
    #plt.show()

    prdt = 1-model.predict(x_test)[:,0]
    results = np.round(np.absolute(prdt-y_test))
    outcomes.append(np.sum(results)/results.shape[0])
    with open('deep.json', 'w') as outfile:
        json.dump(outcomes, outfile)
print(outcomes)
