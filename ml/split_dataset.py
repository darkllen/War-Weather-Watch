import pandas as pd

FILE_PATH = 'data/clear_full_dataset.csv'
RESULT_DIR = 'data/'

# split according to guide by datetime
def split_dataset(csv_file_path: str):
    df = pd.read_csv(csv_file_path, sep=';')

    df['start_hour_epoch'] = pd.to_datetime(df.start_hour_epoch)
    min_date = df.start_hour_epoch.min()
    max_date = df.start_hour_epoch.max()

    train_percent = .70
    test_percent = .20
    time_between = max_date - min_date
    train_cutoff = min_date + train_percent*time_between
    test_cutoff = min_date + (train_percent+test_percent)*time_between

    train_df = df[df.start_hour_epoch <= train_cutoff]
    test_df = df[(df.start_hour_epoch > train_cutoff) & (df.start_hour_epoch <= test_cutoff)]
    validation_df = df[df.start_hour_epoch > test_cutoff]

    train_df.to_csv(f'{RESULT_DIR}/train.csv',sep=';')
    test_df.to_csv(f'{RESULT_DIR}/test.csv',sep=';')
    validation_df.to_csv(f'{RESULT_DIR}/validation.csv',sep=';')

if __name__ == "__main__":
    split_dataset(FILE_PATH)