from transfer import VocTransfer
from myprocessor import MyProcessor

if __name__ == '__main__':
    train_csv = 'lib/train.csv'

    dp = MyProcessor(VocTransfer, output='output')
    dp.set_data_root_path('lib/images')
    dp.load_from_csv(train_csv, stop_at=0)
