import pickle
from train_model import prepare_data
from tabulate import tabulate

def get_top_features(model_filepath, colums):
    model = pickle.load(open(model_filepath, 'rb'))
    print("Logistic regression")
    named_features = list(zip(colums, model.coef_[0]))
    sorted_features = sorted(named_features, key=lambda x: x[1], reverse=True)
    table = []
    for ind, (column, coef) in enumerate(sorted_features[:20]):
        table.append([ind+1, column, coef])
    print(tabulate(table))


def get_top_features_tree(model_filepath, colums):
    model = pickle.load(open(model_filepath, 'rb'))
    print("Decision tree")
    named_features = list(zip(colums, model.feature_importances_))
    sorted_features = sorted(named_features, key=lambda x: x[1], reverse=True)
    table = []
    for ind, (column, coef) in enumerate(sorted_features[:20]):
        table.append([ind+1, column, coef])
    print(tabulate(table))


if __name__ == '__main__':
    data = prepare_data('test.csv')
    get_top_features('../data/lg_model_tuned.dmp', data['x'].columns)
    get_top_features_tree('../data/decision_tree_model_tuned.dmp', data['x'].columns)