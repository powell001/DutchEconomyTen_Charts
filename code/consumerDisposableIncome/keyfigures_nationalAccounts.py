import pandas as pd
import cbsodata
import matplotlib.pyplot as plt
import numpy as np
import functools as ft
from datetime import datetime
import os
import warnings
warnings.filterwarnings("ignore")

todayDate = datetime.today().strftime('%Y_%m_%d')
pd.set_option('display.max_columns', 40)


#  https://opendata.cbs.nl/#/CBS/en/dataset/85881ENG/table


todayDate = datetime.today().strftime('%Y_%m_%d')
pd.set_option('display.max_columns', 40)

settings = {'figure.figsize':(14,4),
            'figure.dpi':144,
            'figure.facecolor':'w',
            'axes.spines.top':False,
            'axes.spines.bottom':False,
            'axes.spines.left':False,
            'axes.spines.right':False,
            'axes.grid':True,
            'grid.linestyle':'--',
            'grid.linewidth':0.5}
plt.rcParams.update(settings)

###################################
#
###################################

#### Where to save data and figures
output_data_qt = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/consumerDisposableIncome//"
output_figures = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/consumerDisposableIncome//"


print("household consumption data english")


def macro_data_cbs(identifier, verbose = False):
    start_date = '01/01/1999'

    # get data
    data = pd.DataFrame(cbsodata.get_data(identifier))

    if verbose:
        info = cbsodata.get_info(identifier)
        print(info)
        tables = pd.DataFrame(cbsodata.get_table_list())
        tables.to_csv(output_data_qt + "cbs_table_list.csv")
        data.to_csv(output_data_qt + "unprocessed_qt_data.csv")
        columns_unprocessed = data.columns
        print("Columns unprocessed: ", len(columns_unprocessed))
        print(data.Periods)

    # subsetting data rows data = data[data["TypeOfData"] == 'Prices of 2021 seasonally adjusted']

    # dont want quarters
    data = data[data['Periods'].str.contains('quarter')]
    data.to_csv(output_data_qt + "unprocessed_qt_data.csv")
    

    data.drop(columns = ['ID','Periods'], inplace = True)
    
    data.index = pd.date_range(start = start_date, periods = data.shape[0], freq = "Q").to_period('Q')
    data.index = pd.PeriodIndex(data.index, freq='Q').to_timestamp()
    
    # save locally
    data.to_csv(output_data_qt + "consumerConsumption.csv")

    return data

nationalAccounts = NLD_basic_macro_data = macro_data_cbs(identifier = '85881ENG', verbose = False)