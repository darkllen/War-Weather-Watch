from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
import time

from train_model import prepare_data, dump_model, evaluate_model



def random_forest_model(train_data, test_data):
    print('Run random forest grid searching over the hyperparameters')
    start = time.time()

    n_estimators = [50, 100, 200]
    criterion = ['gini', 'entropy', 'log_loss']
    max_features = ['auto', 'sqrt', 'log2'] 
    grid = dict(n_estimators=n_estimators, criterion=criterion, max_features=max_features)

    model = RandomForestClassifier()
    cvFold = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    gridSearch = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1,
        cv=cvFold, scoring="neg_mean_squared_error")
    searchResults = gridSearch.fit(train_data['x'], train_data['y'])
    # extract the best model and evaluate it
    print("evaluating...")
    bestModel = searchResults.best_estimator_
    score = bestModel.score(test_data['x'], test_data['y'])
    print(f"Random forest score: {score}. Processing time {time.time() - start} seconds")
        
    return bestModel



def naive_bayes_model(train_data, test_data):
    print('Run naive bayes')

    start = time.time()

    var_smoothing = [1e-10, 1e-9, 1e-8]
    grid = dict(var_smoothing=var_smoothing)

    model = GaussianNB()
    cvFold = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    gridSearch = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1,
        cv=cvFold, scoring="neg_mean_squared_error")
    searchResults = gridSearch.fit(train_data['x'], train_data['y'])
    # extract the best model and evaluate it
    print("evaluating...")
    bestModel = searchResults.best_estimator_
    score = bestModel.score(test_data['x'], test_data['y'])

    print(f"Naive bayes score: {score}. Processing time {time.time() - start} seconds")
    return bestModel


def decision_tree_classifier_model(train_data, test_data):
    print('Run Decision tree classifier')

    start = time.time()

    criterion = ['gini', 'entropy', 'log_loss']
    splitter= ['best', 'random']
    max_features = ['auto', 'sqrt', 'log2'] 
    grid = dict(criterion=criterion, splitter=splitter, max_features=max_features)

    model = tree.DecisionTreeClassifier()
    cvFold = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    gridSearch = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1,
        cv=cvFold, scoring="neg_mean_squared_error")
    searchResults = gridSearch.fit(train_data['x'], train_data['y'])
    # extract the best model and evaluate it
    print("evaluating...")
    bestModel = searchResults.best_estimator_
    score = bestModel.score(test_data['x'], test_data['y'])

    print(f"Decision tree classifier score: {score}. Processing time {time.time() - start} seconds")
    return bestModel

def tune_model():
    train_data = prepare_data('train.csv')
    test_data = prepare_data('test.csv')

    forest_model = random_forest_model(train_data, test_data)
    naive_model = naive_bayes_model(train_data, test_data)
    decision_tree_model = decision_tree_classifier_model(train_data, test_data)

    print(f"predict random forest {forest_model.predict(test_data['x'])}")
    print(f"predict Naive bayes {naive_model.predict(test_data['x'])}")
    print(f"predict Decision tree {decision_tree_model.predict(test_data['x'])}")

    dump_model(forest_model, 'rf_model_tuned')
    dump_model(naive_model, 'naive_model_tuned')
    dump_model(decision_tree_model, 'decision_tree_model_tuned')

    print('Prepare confusion matrix')
    evaluate_model(forest_model, test_data, 'rf_model_cm_tuned', 'RandomForestTuned')
    evaluate_model(naive_model, test_data, 'naive_model_cm_tuned', 'GaussianNBTuned')
    evaluate_model(decision_tree_model, test_data, 'decision_tree_model_cm_tuned', 'DecisionTreeClassifierTuned')


if __name__ == "__main__":
    tune_model()