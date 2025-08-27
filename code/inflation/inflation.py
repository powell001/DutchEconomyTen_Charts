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
    data_allItems.columns = ["CPI" + "_" + x for x in data_allItems]
    
    categories = ['DerivedCPI_2', 'MonthOnMonthChangeDerivedCPI_4', 'YearOnYearChangeDerivedCPI_6']
    data_energy = data_energy[['DerivedCPI_2', 'MonthOnMonthChangeDerivedCPI_4', 'YearOnYearChangeDerivedCPI_6']]
    data_energy = data_energy.set_index(pd.date_range(start = start_date, periods = data_energy.shape[0], freq = "M").to_period('M'))
    data_energy.index = pd.PeriodIndex(data_energy.index, freq='M').to_timestamp()
    data_energy.columns = ["CPI" + "_" + x for x in data_energy]

    categories = ['DerivedCPI_2', 'MonthOnMonthChangeDerivedCPI_4', 'YearOnYearChangeDerivedCPI_6']
    data_service = data_service[['DerivedCPI_2', 'MonthOnMonthChangeDerivedCPI_4', 'YearOnYearChangeDerivedCPI_6']]
    data_service = data_service.set_index(pd.date_range(start = start_date, periods = data_service.shape[0], freq = "M").to_period('M'))
    data_service.index = pd.PeriodIndex(data_service.index, freq='M').to_timestamp()
    data_service.columns = ["CPI" + "_" + x for x in data_service]

    inflationData = pd.concat([data_allItems, data_energy, data_service], axis = 1)

    return inflationData

inflation_data_cbs(identifier = '83131ENG', verbose = False)