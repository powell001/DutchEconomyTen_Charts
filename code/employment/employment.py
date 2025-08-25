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
output_data_mo = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/employment//"
output_figures = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/employment//"

print("employment data english")

def macro_data_cbs(identifier, verbose = False):
    start_date = '01/01/2003'

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
    data = data[~data['Periods'].str.contains('quater')] ########################### CBS

    # drop unnecessary columns
    data.drop(columns = ['ID','Periods'], inplace = True)

    # per gender
    data_allGenders = data[data['Sex'] == 'Total sex']
    data_male = data[data['Sex'] == 'Men']
    data_female = data[data['Sex'] == 'Women']

    categories = ['Labor_Force', 'Employed_Labor_Force', 'Unemployed_Labor_Force', "UnemplyRate", "Not_in_Labor_Force", "Gross_Labor_Particp", "Net_Labor_Particp"]
    allBranches = []
    for age in data_allGenders['Age'].unique():
        data_age = data_allGenders[data_allGenders['Age'] == age]
        data_age = data_age.set_index(pd.date_range(start = start_date, periods = data_age.shape[0], freq = "M").to_period('M'))
        data_age.index = pd.PeriodIndex(data_age.index, freq='M').to_timestamp()
        wantThese = [col for col in data_age.columns if "Not" not in col]
        data_age = data_age[wantThese]
        data_age.drop(columns = ['Sex', 'Age'], inplace = True)
        data_age.columns = ["Employment_" + "allGenders_" + age + "_" + col for col in data_age.columns]
        data_age.columns = [x + "_" + y for x, y in zip(data_age.columns, categories)]
       
        allBranches.append(data_age)

    data_all = pd.concat(allBranches, axis=1)

    data_allGenders = data_all.copy()
    
    # save locally
    data_all.to_csv(output_data_mo + "employment_all_genders_mo.csv")

    #############################################
    #############################################

    categories = ['Labor_Force', 'Employed_Labor_Force', 'Unemployed_Labor_Force', "UnemplyRate", "Not_in_Labor_Force", "Gross_Labor_Particp", "Net_Labor_Particp"]
    allBranches = []
    for age in data_male['Age'].unique():
        data_age = data_male[data_male['Age'] == age]
        data_age = data_age.set_index(pd.date_range(start = start_date, periods = data_age.shape[0], freq = "M").to_period('M'))
        data_age.index = pd.PeriodIndex(data_age.index, freq='M').to_timestamp()
        wantThese = [col for col in data_age.columns if "Not" not in col]
        data_age = data_age[wantThese]
        data_age.drop(columns = ['Sex', 'Age'], inplace = True)
        data_age.columns = ["Employment_" + "male_" + age + "_" + col for col in data_age.columns]
        data_age.columns = [x + "_" + y for x, y in zip(data_age.columns, categories)]
       
        allBranches.append(data_age)

    data_all = pd.concat(allBranches, axis=1)

    data_male = data_all.copy()

    # save locally
    data_all.to_csv(output_data_mo + "employment_males_mo.csv")

    #############################################
    #############################################

    categories = ['Labor_Force', 'Employed_Labor_Force', 'Unemployed_Labor_Force', "UnemplyRate", "Not_in_Labor_Force", "Gross_Labor_Particp", "Net_Labor_Particp"]
    allBranches = []
    for age in data_female['Age'].unique():
        data_age = data_female[data_female['Age'] == age]
        data_age = data_age.set_index(pd.date_range(start = start_date, periods = data_age.shape[0], freq = "M").to_period('M'))
        data_age.index = pd.PeriodIndex(data_age.index, freq='M').to_timestamp()
        wantThese = [col for col in data_age.columns if "Not" not in col]
        data_age = data_age[wantThese]
        data_age.drop(columns = ['Sex', 'Age'], inplace = True)
        data_age.columns = ["Employment_" + "female_" + age + "_" + col for col in data_age.columns]
        data_age.columns = [x + "_" + y for x, y in zip(data_age.columns, categories)]
       
        allBranches.append(data_age)

    data_all = pd.concat(allBranches, axis=1)

    data_female = data_all.copy()

    # save locally
    data_all.to_csv(output_data_mo + "employment_females_mo.csv")

    return data_allGenders, data_male, data_female

data_allGenders, data_male, data_female = NLD_basic_macro_data = macro_data_cbs(identifier = '80590eng', verbose = False)

fig, ax = plt.subplots(2, 1, layout='constrained', figsize=(12, 8.75))

# start 2005 for comparison
employment_index = data_allGenders.loc['2003-01-01':,:]
employment_percent = data_female.loc['2003-01-01':,:]

x = np.asarray(employment_index.index, dtype='datetime64[s]')

wantThese = [col for col in employment_index.columns if "UnemplyRate" in col]
# wantThese = ['Employment_F Employment_TurnoverIndices_1', 'Employment_41 Employment buildings, development_TurnoverIndices_1', 'Employment_42 Civil engineering_TurnoverIndices_1', 'Employment_43 Specialised construction activities_TurnoverIndices_1']

employment_index = employment_index.loc[:, wantThese]
ax[0].plot(x, employment_index, linewidth=2)
#ax[0].grid()
ax[0].set_title("Unemployment Rate, Total", loc='left', fontsize=12, fontweight=0, color='black')
ax[0].legend(employment_index.columns, loc='upper left', fontsize=8, ncol=1)

wantThese = [col for col in employment_percent.columns if "UnemplyRate" in col]

employment_percent = employment_percent.loc[:, wantThese]
ax[1].plot(x, employment_percent, linewidth=2)
#ax[1].grid()
ax[1].set_title("Unemployment Rate, Female", loc='left', fontsize=12, fontweight=0, color='black')
ax[1].legend(employment_percent.columns, loc='upper left', fontsize=8, ncol=1)

plt.savefig(output_figures + "Employment.png", dpi=300, bbox_inches='tight')
plt.show()