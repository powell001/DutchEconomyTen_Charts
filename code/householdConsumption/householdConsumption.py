import pandas as pd
import cbsodata
import matplotlib.pyplot as plt
import numpy as np
import functools as ft
from datetime import datetime
import os

import warnings
warnings.filterwarnings("ignore")

# https://opendata.cbs.nl/#/CBS/en/dataset/85937ENG/table


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
output_data_mo = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/householdConsumption//"
output_figures = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/householdConsumption//"


print("household consumption data english")


def macro_data_cbs(identifier, verbose = False):
    start_date = '01/01/2000'

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

    # subsetting data rows data = data[data["TypeOfData"] == 'Prices of 2021 seasonally adjusted']

    # dont want quarters
    data = data[~data['Periods'].str.contains('quarter')]
    # dont want years
    data = data[~data['Periods'].str.isnumeric()]

    data.to_csv(output_data_mo + "unprocessed_mo_data.csv")


    # rename columns
    data.rename(columns = {"Indices_1": "Volume_Index",
                           "VolumeChanges_2": "Volume_Changes_Index",
                           "VolumeChangesShoppingdayAdjusted_3": "Volume_Changes_Shoppingday_Adjusted_Index",
                           "Indices_4": "Value_Index",
                           "ValueChanges_5": "Value_Changes_Index",
                           "PriceChanges_6": "Price_Changes_Index"
    })

    data.drop(columns = ['ID','Periods'], inplace = True)
    
    all_categories = []
    for i in data['ConsumptionByHouseholds'].unique():
        category1 = data[data['ConsumptionByHouseholds'] == i]
        category1.index = pd.date_range(start = start_date, periods = category1.shape[0], freq = "M").to_period('M')
        category1.index = pd.PeriodIndex(category1.index, freq='M').to_timestamp()
        
        category1.drop(columns = ['ConsumptionByHouseholds'], inplace = True)

        category1.columns = [i + "_" + col for col in category1.columns]
        category1.columns = [col.replace(" ", "_") for col in category1.columns]

        all_categories.append(category1)

    all_data = pd.concat(all_categories, axis=1)

    # save locally
    all_data.to_csv(output_data_mo + "consumerConsumption.csv")

    return all_data

consumerConsumption = NLD_basic_macro_data = macro_data_cbs(identifier = '85937ENG', verbose = False)



def consumerConsumption_volumes():

    ########################
    ########################
    # Volume Changes
    ########################
    ########################

    subset = ["_VolumeChanges"]
    # select if column name contains subset
    sub1 = [col for col in consumerConsumption.columns if any(sub in col for sub in subset)]
    sub1 = [col for col in sub1 if not "VolumeChangesShoppingdayAdjusted" in col]  # remove shopping day adjusted index

    # select data
    volumeChanges = consumerConsumption[sub1]

    # remove subset from column names
    volumeChanges.columns = [col[:-16] for col in volumeChanges.columns]
    volumeChanges.to_csv("tmp_volumeChanges.csv")

    print(volumeChanges.columns)

    # further selection
    further_selection = ['Domestic_consumption_by_households', 'Consumption_of_goods_by_households', 'Durable_consumer_goods', 'Consumption_of_services_by_households']
    volumeChanges = volumeChanges[further_selection]


    fig, ax = plt.subplots(2, 1, layout='constrained', figsize=(12, 8.75))

    # string to dates, helps with plotting
    x = np.asarray(volumeChanges.index)

    ax[0].plot(x, volumeChanges, linewidth=1)
    ax[0].set_title("Volume Changes (selected series)", loc='left', fontsize=12, fontweight=0, color='black')
    ax[0].legend(volumeChanges.columns, loc='upper left', fontsize=8, ncol=1)

    #############################
    volumeChanges_subset = volumeChanges.loc['2022-01-01':,:]
    volumeChanges_subset.to_csv("tmp_volumeChanges_subset.csv")

    x = np.asarray(volumeChanges_subset.index)

    ax[1].plot(x, volumeChanges_subset, linewidth=1)
    ax[1].set_title("Volume Changes since 2022-01-01(selected series)", loc='left', fontsize=12, fontweight=0, color='black')
    ax[1].legend(volumeChanges_subset.columns, loc='upper left', fontsize=8, ncol=1)

    plt.savefig(output_figures + "consumerConsumption_volumes.png", dpi=300, bbox_inches='tight')
    plt.show()

consumerConsumption_volumes()


def consumerConsumption_value():

    ########################
    ########################
    # Value Changes
    ########################
    ########################

    subset = ["_ValueChanges"]
    # select if column name contains subset
    sub1 = [col for col in consumerConsumption.columns if any(sub in col for sub in subset)]

    # select data
    valueChanges = consumerConsumption[sub1]

    # remove subset from column names
    valueChanges.columns = [col[:-15] for col in valueChanges.columns]
    valueChanges.to_csv("tmp_valueChanges.csv")

    print(valueChanges.columns)

    # further selection
    further_selection = ['Domestic_consumption_by_households', 'Consumption_of_goods_by_households', 'Durable_consumer_goods', 'Consumption_of_services_by_households']
    valueChanges = valueChanges[further_selection]


    fig, ax = plt.subplots(2, 1, layout='constrained', figsize=(12, 8.75))

    # string to dates, helps with plotting
    x = np.asarray(valueChanges.index)

    ax[0].plot(x, valueChanges, linewidth=1)
    ax[0].set_title("Value Changes (selected series)", loc='left', fontsize=12, fontweight=0, color='black')
    ax[0].legend(valueChanges.columns, loc='upper left', fontsize=8, ncol=1)

    #############################
    valueChanges_subset = valueChanges.loc['2022-01-01':,:]
    valueChanges_subset.to_csv("tmp_valueChanges_subset.csv")

    x = np.asarray(valueChanges_subset.index)

    ax[1].plot(x, valueChanges_subset, linewidth=1)
    ax[1].set_title("Value Changes since 2022-01-01(selected series)", loc='left', fontsize=12, fontweight=0, color='black')
    ax[1].legend(valueChanges_subset.columns, loc='upper left', fontsize=8, ncol=1)

    plt.savefig(output_figures + "consumerConsumption_volumes.png", dpi=300, bbox_inches='tight')
    plt.show()

consumerConsumption_value()