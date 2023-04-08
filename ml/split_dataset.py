import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

FILE_PATH = 'data/clear_full_dataset.csv'
RESULT_DIR = 'data/'

# split according to guide by datetime
def split_dataset(csv_file_path: str):
    df = pd.read_csv(csv_file_path, sep=';')
    
    disproportion = df[df['is_alarm']==0].is_alarm.count()/df[df['is_alarm']==1].is_alarm.count()
    ones  = df[df['is_alarm']==1]
    zeros = df[df['is_alarm']==0]
    zeros = zeros.iloc[::int(disproportion)]
    df = pd.concat([ones, zeros])

    df['day_datetimeEpoch'] = pd.to_datetime(df.day_datetimeEpoch, unit='s')
    df.set_index('day_datetimeEpoch', inplace=True)
    df.sort_index(inplace=True)

    tss = TimeSeriesSplit(n_splits = 4)
    for train_index, test_index in tss.split(df):
        train_df, test_df = df.iloc[train_index, :], df.iloc[test_index,:]

    train_df.to_csv(f'{RESULT_DIR}/train.csv',sep=';')
    test_df.to_csv(f'{RESULT_DIR}/test.csv',sep=';')

if __name__ == "__main__":
    split_dataset(FILE_PATH)