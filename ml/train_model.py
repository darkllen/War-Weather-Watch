import json
import pandas as pd
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import pickle
import time


def evaluate_model(model, validation_data, save_as_file):
    y_pred = model.predict(validation_data['x'])
    cm = confusion_matrix(validation_data['y'], y_pred)

    ConfusionMatrixDisplay(cm).plot()
    plt.savefig(f'../data/{save_as_file}.png')


def prepare_data(filename):
    data = pd.read_csv('../data/' + filename, sep=';')
    data["day_datetimeEpoch_int"] = data["day_datetimeEpoch"].apply(lambda x: int(pd.Timestamp(x).timestamp()))
    data["news_obj"] = [json.loads(news.replace("'", '"')) for news in data["news"]]
    x = data[[
        'region_title',
        'day_datetimeEpoch_int',
        'hour_temp',
        'hour_humidity',
        'hour_snow',
        'hour_windspeed',
        'hour_visibility',
        'hour_cloudcover',
        'news_obj'
    ]]
    y = data['is_alarm']

    x = x.apply(pd.to_numeric, errors='coerce')
    y = y.apply(pd.to_numeric, errors='coerce')

    x.fillna(0, inplace=True)
    y.fillna(0, inplace=True)

    return {"x": x, "y": y}


def logistic_regression(train_data, test_data):
    print('Run Logistic Regression')

    start = time.time()
    model = LogisticRegression()
    model.fit(train_data['x'], train_data['y'])
    score = model.score(test_data['x'], test_data['y'])

    print(f"Logistic regression score: {score}. Processing time {time.time() - start} seconds")
    return model


def svc_model(train_data, test_data):
    print('Run SVC')

    start = time.time()
    model = SVC()
    model.fit(train_data['x'], train_data['y'])
    print(f"Fit time {time.time() - start} seconds")
    score = model.score(test_data['x'], test_data['y'])

    print(f"SVC score: {score}. Processing time {time.time() - start} seconds")
    return model


def stochastic_gradient_descent_model(train_data, test_data):
    print('Run Stochastic gradient descent')

    start = time.time()
    model = SGDClassifier(max_iter = 1000, tol=1e-3,penalty = "elasticnet")
    model.fit(train_data['x'], train_data['y'])
    score = model.score(test_data['x'], test_data['y'])

    print(f"SGD score: {score}. Processing time {time.time() - start} seconds")
    return model


def random_forest_model(train_data, test_data):
    print('Run random forest')

    start = time.time()
    model = RandomForestClassifier()
    model.fit(train_data['x'], train_data['y'])
    score = model.score(test_data['x'], test_data['y'])

    print(f"Random forest score: {score}. Processing time {time.time() - start} seconds")
    return model


def naive_bayes_model(train_data, test_data):
    print('Run naive bayes')

    start = time.time()
    model = GaussianNB()
    model.fit(train_data['x'], train_data['y'])
    score = model.score(test_data['x'], test_data['y'])

    print(f"Naive bayes score: {score}. Processing time {time.time() - start} seconds")
    return model


def decision_tree_classifier_model(train_data, test_data):
    print('Run Decision tree classifier')

    start = time.time()
    model = tree.DecisionTreeClassifier()
    model.fit(train_data['x'], train_data['y'])
    score = model.score(test_data['x'], test_data['y'])

    print(f"Decision tree classifier score: {score}. Processing time {time.time() - start} seconds")
    return model


def dump_model(model, filename):
    file = open(f'../data/{filename}.dmp', 'wb')
    pickle.dump(model, file)


def train_model():
    train_data = prepare_data('train.csv')
    test_data = prepare_data('test.csv')

    lg_model = logistic_regression(train_data, test_data)
    sgd_model = stochastic_gradient_descent_model(train_data, test_data)
    rf_model = random_forest_model(train_data, test_data)
    svc_mod = svc_model(train_data, test_data)
    naive_model = naive_bayes_model(train_data, test_data)
    decision_tree_model = decision_tree_classifier_model(train_data, test_data)

    validation_data = prepare_data('validation.csv')

    print(f"predict logistic regression {lg_model.predict(validation_data['x'])}")
    print(f"predict SGD {sgd_model.predict(validation_data['x'])}")
    print(f"predict RF {rf_model.predict(validation_data['x'])}")
    print(f"predict SVC {svc_mod.predict(validation_data['x'])}")
    print(f"predict Naive bayes {naive_model.predict(validation_data['x'])}")
    print(f"predict Decision tree classifier {decision_tree_model.predict(validation_data['x'])}")

    dump_model(lg_model, 'lg_model')
    dump_model(sgd_model, 'sgd_model')
    dump_model(rf_model, 'rf_model')
    dump_model(svc_mod, 'svc_mod')
    dump_model(naive_model, 'naive_model')
    dump_model(decision_tree_model, 'decision_tree_model')

    print('Prepare confusion matrix')
    evaluate_model(lg_model, validation_data, 'lg_model_cm')
    evaluate_model(sgd_model, validation_data, 'sgd_model_cm')
    evaluate_model(rf_model, validation_data, 'rf_model_cm')
    evaluate_model(svc_mod, validation_data, 'svc_mod_cm')
    evaluate_model(naive_model, validation_data, 'naive_model_cm')
    evaluate_model(decision_tree_model, validation_data, 'decision_tree_model_cm')


if __name__ == "__main__":
    train_model()
