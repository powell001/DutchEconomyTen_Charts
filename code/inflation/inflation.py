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

#  https://opendata.cbs.nl/#/CBS/en/dataset/83131ENG/table


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
output_data_mo = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/inflation//"
output_figures = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/inflation//"

print("inflation data english")

def inflation_data_cbs(identifier, verbose = False):
    start_date = '01/01/1996'

    # get data
    data = pd.DataFrame(cbsodata.get_data(identifier))

    if verbose:
        info = cbsodata.get_info(identifier)
        print(info)
        tables = pd.DataFrame(cbsodata.get_table_list())
        tables.to_csv(output_data_mo + "cbs_table_list.csv")
        data.to_csv(output_data_mo + "unprocessed_mo_data.csv")
        columns_unprocessed = data.columns
        print("Columns unprocessed: ", len(columns_unprocessed))
        print(data.Periods)

    # dont want quarters
    data = data[~data['Periods'].str.isnumeric()]
    
    # drop unnecessary columns
    data.drop(columns = ['ID','Periods'], inplace = True)

    # per category
    data_allItems = data[data['ExpenditureCategories'] == '000000 All items']
    data_energy = data[data['ExpenditureCategories'] == 'SA07 Energy, including other fuels']
    data_service = data[data['ExpenditureCategories'] == 'SA11 Services']

    categories = ['DerivedCPI_2', 'MonthOnMonthChangeDerivedCPI_4', 'YearOnYearChangeDerivedCPI_6']
    data_allItems = data_allItems[['DerivedCPI_2', 'MonthOnMonthChangeDerivedCPI_4', 'YearOnYearChangeDerivedCPI_6']]
    data_allItems = data_allItems.set_index(pd.date_range(start = start_date, periods = data_allItems.shape[0], freq = "M").to_period('M'))
    data_allItems.index = pd.PeriodIndex(data_allItems.index, freq='M').to_timestamp()
    data_allItems.columns = ["CPI_AllItems" + "_" + x for x in data_allItems]
    
    categories = ['DerivedCPI_2', 'MonthOnMonthChangeDerivedCPI_4', 'YearOnYearChangeDerivedCPI_6']
    data_energy = data_energy[['DerivedCPI_2', 'MonthOnMonthChangeDerivedCPI_4', 'YearOnYearChangeDerivedCPI_6']]
    data_energy = data_energy.set_index(pd.date_range(start = start_date, periods = data_energy.shape[0], freq = "M").to_period('M'))
    data_energy.index = pd.PeriodIndex(data_energy.index, freq='M').to_timestamp()
    data_energy.columns = ["CPI_Energy" + "_" + x for x in data_energy]

    categories = ['DerivedCPI_2', 'MonthOnMonthChangeDerivedCPI_4', 'YearOnYearChangeDerivedCPI_6']
    data_service = data_service[['DerivedCPI_2', 'MonthOnMonthChangeDerivedCPI_4', 'YearOnYearChangeDerivedCPI_6']]
    data_service = data_service.set_index(pd.date_range(start = start_date, periods = data_service.shape[0], freq = "M").to_period('M'))
    data_service.index = pd.PeriodIndex(data_service.index, freq='M').to_timestamp()
    data_service.columns = ["CPI_Service" + "_" + x for x in data_service]

    inflationData = pd.concat([data_allItems, data_energy, data_service], axis = 1)

    return inflationData

infl1 = inflation_data_cbs(identifier = '83131ENG', verbose = False)

print(infl1)

print(infl1.columns)

############################
############################

fig, ax = plt.subplots(3, 1, layout='constrained', figsize=(12, 8.75))

infl1 = infl1[infl1.index >= '2021-01-01']

# start 2005 for comparison
wantThese_all = [col for col in infl1.columns if "CPI_AllItems" in col]
wantThese_energy = [col for col in infl1.columns if "CPI_Energy" in col]
wantThese_service = [col for col in infl1.columns if "CPI_Service" in col]

x = infl1.index

dt_all = infl1[wantThese_all]
ax[0].plot(x, dt_all, linewidth=2)
#ax[0].grid()
ax[0].set_title("Inflation Rate, Total", loc='left', fontsize=12, fontweight=0, color='black')
ax[0].legend(dt_all.columns, loc='upper left', fontsize=8, ncol=1)

dt_energy = infl1[wantThese_energy]
ax[1].plot(x, dt_energy, linewidth=2)
#ax[1].grid()
ax[1].set_title("Inflation Rate, Energy", loc='left', fontsize=12, fontweight=0, color='black')
ax[1].legend(dt_energy.columns, loc='upper left', fontsize=8, ncol=1)

dt_service = infl1[wantThese_service]
ax[2].plot(x, dt_service, linewidth=2)
#ax[2].grid()
ax[2].set_title("Inflation Rate, Services", loc='left', fontsize=12, fontweight=0, color='black')
ax[2].legend(dt_service.columns, loc='upper left', fontsize=8, ncol=1)

plt.savefig(output_figures + "consumPriceInd.png", dpi=300, bbox_inches='tight')
plt.show()
