import eurostat
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
from itertools import chain
import os
import numpy as np

import warnings
warnings.filterwarnings("ignore")

settings = {'figure.figsize':(14,4),
            'figure.dpi':144,
            'figure.facecolor':'w',
            'axes.spines.top':False,
            'axes.spines.bottom':False,
            'axes.spines.left':False,
            'axes.spines.right':False,
            'axes.grid':True,
            'grid.linestyle':'--',
            'grid.linewidth':0.5, 
            'figure.constrained_layout.use':True}
plt.rcParams.update(settings)

#### WHERE TO SAVE DATA
output_data_local = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/interestRates//"
output_figures = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/interestRates//"

####################
# Short term interest rates
####################

def shortterm_interest_rates():

    start_date = '01/01/1970'

    data = eurostat.get_data_df('irt_st_m')

    data.to_csv("tmp_all.csv")
    print(data.head())

    data = data[data["freq"] == "M"]

    data = data[data['geo\\TIME_PERIOD'].isin(['EA'])]
    interest_rates = data.iloc[:, 3:]

    interest_rates = interest_rates.T
    interest_rates.columns = interest_rates.iloc[0,:]

    interest_rates = interest_rates.set_index(pd.date_range(start = start_date, periods = interest_rates.shape[0], freq = "M").to_period('M'))
    interest_rates.index = pd.PeriodIndex(interest_rates.index, freq='M').to_timestamp()

    interest_rates = interest_rates.rename_axis(None, axis=1)

    mycolumns = ["EuropeanArea_MoneyMarketIntRates"] *5
    int_rates = ["Intr_DayTDay", "Intr_M1", "Intr_M12", "Intr_M3", "Intr_M6"] 

    interest_rates.columns = [x + "_" + y for x, y in zip(mycolumns, int_rates)]

    interest_rates.to_csv(output_data_local + "eurostat_MoneyMarketIntRates_mo.csv")

    return interest_rates

intRate = shortterm_interest_rates()

############################
############################

fig, ax = plt.subplots(2, 1, layout='constrained', figsize=(12, 8.75))

# start 1996 for comparison
allmonths = intRate
fewmonths = intRate.loc["01/01/2014":,]

x = np.asarray(allmonths.index, dtype='datetime64[s]')
ax[0].plot(x, allmonths, linewidth=2)
ax[0].grid(visible=True)
ax[0].set_title("Short-term European Interest Rates", loc='left', fontsize=12, fontweight=0, color='black')
ax[0].legend(allmonths.columns, loc='upper right', fontsize=8, ncol=1)

x = np.asarray(fewmonths.index, dtype='datetime64[s]')
ax[1].plot(x, fewmonths, linewidth=2)
ax[1].grid(visible=True)
ax[1].set_title("Short-term European Interest Rates (2014 Onwards)", loc='left', fontsize=12, fontweight=0, color='black')
ax[1].legend(fewmonths.columns, loc='upper center', fontsize=8, ncol=1)

plt.savefig(output_figures + "Short-term_European_Interest_Rates.png", dpi=300, bbox_inches='tight')
plt.show()