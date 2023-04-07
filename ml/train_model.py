import pandas as pd
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_decomposition import PLSRegression
import pickle
import time


def prepare_data(filename):
    data = pd.read_csv('../data/' + filename, sep=';')
    data["day_datetimeEpoch"] = data["day_datetimeEpoch"].apply(lambda x: int(pd.Timestamp(x).timestamp()))
    x = data.drop(columns=[
        "all_region", 
        "alarms_in_other_regions", 
        "regions_in_fire", 
        "quantity_regions_in_fire",
        "alarms_in_region_for_last_24H",
        "duration", 
        "Short/Long",
    ])

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


def pls_regression_model(train_data, test_data):
    print('Run PLS regressions')

    start = time.time()
    model = PLSRegression()
    model.fit(train_data['x'], train_data['y'])
    score = model.score(test_data['x'], test_data['y'])

    print(f"PLS regressions score: {score}. Processing time {time.time() - start} seconds")
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
    pls_model = pls_regression_model(train_data, test_data)

    print(f"predict logistic regression {lg_model.predict(test_data['x'])}")
    print(f"predict SGD {sgd_model.predict(test_data['x'])}")
    print(f"predict RF {rf_model.predict(test_data['x'])}")
    print(f"predict SVC {svc_mod.predict(test_data['x'])}")
    print(f"predict Naive bayes {naive_model.predict(test_data['x'])}")
    print(f"predict PLS regression {pls_model.predict(test_data['x'])}")

    dump_model(lg_model, 'lg_model')
    dump_model(sgd_model, 'sgd_model')
    dump_model(rf_model, 'rf_model')
    dump_model(svc_mod, 'svc_mod')
    dump_model(naive_model, 'naive_model')
    dump_model(pls_model, 'pls_model')


if __name__ == "__main__":
    train_model()
