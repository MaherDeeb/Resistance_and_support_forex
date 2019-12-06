import pandas as pd


# 2.read csv file (4h time frame will be used for this example)
def load_data(filename: str, header=None):
    """ Data Loader

    :param str filename: the name of the file e.g. EURUSD.csv
    :param header: Check the pandas library. (if there is no columns names, keep it None)
    :return:

        - dataframe: Pandas dataframe with 7 columns
    """

    dataframe = pd.read_csv(filename, header=header)
    # 2.1give names to the columns
    dataframe.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
    # 2.3the amount of the data
    print("The loaded data has a size of ", dataframe.shape)
    return dataframe
