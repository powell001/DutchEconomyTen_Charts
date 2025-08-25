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
output_data_mo = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/construction//"
output_figures = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/construction//"

print("construction data english")

def macro_data_cbs(identifier, verbose = False):
    start_date = '01/01/2005'

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
    data = data[~data['Periods'].str.contains('quarter')]
    data = data[data['EnterpriseSize'] == 'Total 1 or more employed persons']

    # drop unnecessary columns
    data.drop(columns = ['ID','Periods', 'EnterpriseSize'], inplace = True)

    allBranches = []
    for brnch in data['SectorBranchesSIC2008'].unique():
        data_brnch = data[data['SectorBranchesSIC2008'] == brnch]
        data_brnch = data_brnch.drop(columns = ['SectorBranchesSIC2008'])
        data_brnch = data_brnch.set_index(pd.date_range(start = start_date, periods = data_brnch.shape[0], freq = "M").to_period('M'))
        data_brnch.index = pd.PeriodIndex(data_brnch.index, freq='M').to_timestamp()
        data_brnch.columns = ["Construction_" + brnch + "_" + col for col in data_brnch.columns]
        allBranches.append(data_brnch)
        
    data = pd.concat(allBranches, axis=1)

    
    # save locally
    data.to_csv(output_data_mo + "construction.csv")

    return data

construction = NLD_basic_macro_data = macro_data_cbs(identifier = '85809ENG', verbose = False)

fig, ax = plt.subplots(2, 1, layout='constrained', figsize=(12, 8.75))

# start 2005 for comparison
construction_index = construction.loc['2015-01-01':,:]
construction_percent = construction.loc['2015-01-01':,:]

x = np.asarray(construction_index.index, dtype='datetime64[s]')

wantThese = [col for col in construction_index.columns if "TurnoverIndices" in col]
wantThese = ['Construction_F Construction_TurnoverIndices_1', 'Construction_41 Construction buildings, development_TurnoverIndices_1', 'Construction_42 Civil engineering_TurnoverIndices_1', 'Construction_43 Specialised construction activities_TurnoverIndices_1']

construction_index = construction_index.loc[:, wantThese]
ax[0].plot(x, construction_index, linewidth=2)
#ax[0].grid()
ax[0].set_title("Construction Index", loc='left', fontsize=12, fontweight=0, color='black')
ax[0].legend(construction_index.columns, loc='upper left', fontsize=8, ncol=1)

wantThese = [col for col in construction_percent.columns if "TurnoverYearOnYearChange" in col]
print(wantThese)
wantThese = ['Construction_F Construction_TurnoverYearOnYearChange_2', 'Construction_41 Construction buildings, development_TurnoverYearOnYearChange_2', 'Construction_42 Civil engineering_TurnoverYearOnYearChange_2', 'Construction_43 Specialised construction activities_TurnoverYearOnYearChange_2']  
construction_percent = construction_percent.loc[:, wantThese]
ax[1].plot(x, construction_percent, linewidth=2)
#ax[1].grid()
ax[1].set_title("Construction Percent Change", loc='left', fontsize=12, fontweight=0, color='black')
ax[1].legend(construction_percent.columns, loc='upper left', fontsize=8, ncol=1)

plt.savefig(output_figures + "Construction.png", dpi=300, bbox_inches='tight')
plt.show()