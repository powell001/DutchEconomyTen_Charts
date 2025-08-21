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
# Want consumer disposable income data
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

    # want quarters
    data = data[data['Periods'].str.contains('quarter')]

    # drop unnecessary columns
    data.drop(columns = ['ID','Periods'], inplace = True)
    
    data.index = pd.date_range(start = start_date, periods = data.shape[0], freq = "Q").to_period('Q')
    data.index = pd.PeriodIndex(data.index, freq='Q').to_timestamp()
    
    # save locally
    data.to_csv(output_data_qt + "consumerConsumption.csv")

    return data

nationalAccounts = NLD_basic_macro_data = macro_data_cbs(identifier = '85881ENG', verbose = False)


#######################
# Real Disposable Income
#######################

realDisposableIncome = nationalAccounts[['RealDisposableIncome_37']]

consumptionIncome = nationalAccounts[['MixedIncome_35', 'GrossDisposableIncome_36','AdjustedDisposableIncome_38', 'FinalConsumptionExpenditure_39']]
consumptionIncome_percent =  consumptionIncome.pct_change(4) * 100
consumptionIncome_percent.columns = [col + "_pct_change" for col in consumptionIncome_percent.columns]


fig, ax = plt.subplots(2, 1, layout='constrained', figsize=(12, 8.75))

# string to dates, helps with plotting
realDisposableIncome = realDisposableIncome.loc['2000-10-01':,:]
consumptionIncome_percent = consumptionIncome_percent.loc['2000-10-01':,:]
x = np.asarray(consumptionIncome_percent.index, dtype='datetime64[s]')


ax[0].plot(x, realDisposableIncome, linewidth=1)
ax[0].set_title("Real Disposable Income Percent", loc='left', fontsize=12, fontweight=0, color='black')
ax[0].legend(realDisposableIncome.columns, loc='upper right', fontsize=8, ncol=1)

ax[1].plot(x, consumptionIncome_percent, linewidth=1)
ax[1].set_title("Disposable Income Percent", loc='left', fontsize=12, fontweight=0, color='black')
ax[1].legend(consumptionIncome_percent.columns, loc='upper right', fontsize=8, ncol=1)


plt.savefig(output_figures + "realDisposableIncome.png", dpi=300, bbox_inches='tight')
plt.show()