import pickle
from train_model import prepare_data


def get_top_features(model_filepath, colums):
    model = pickle.load(open(model_filepath, 'rb'))
    print(model_filepath)
    named_features = list(zip(colums, model.coef_[0]))
    sorted_features = sorted(named_features, key=lambda x: x[1], reverse=True)
    for column, coef in sorted_features[:20]:
        print(column, coef)


def get_top_features_tree(model_filepath, colums):
    model = pickle.load(open(model_filepath, 'rb'))
    print(model_filepath)
    named_features = list(zip(colums, model.feature_importances_))
    sorted_features = sorted(named_features, key=lambda x: x[1], reverse=True)
    for column, coef in sorted_features[:20]:
        print(column, coef)


if __name__ == '__main__':
    data = prepare_data('test.csv')
    get_top_features('../data/lg_model_tuned.dmp', data['x'].columns)
    get_top_features_tree('../data/decision_tree_model_tuned.dmp', data['x'].columns)