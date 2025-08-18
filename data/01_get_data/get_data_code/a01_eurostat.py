import eurostat
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
from itertools import chain
import os

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
output = os.path.abspath("C:/Users/jpark/vscode/NowCast_Data_Analysis_scripts/output_mo_qt")

start_date = "1983-01-01"

data = eurostat.get_data_df('une_rt_m')   ###############
data.to_csv("tmp.csv")

data = data[data['freq'] == 'M']
data = data[data['s_adj'] == 'SA']
data = data[data['age'] == 'TOTAL']
data = data[data['unit'] == 'PC_ACT']
data = data[data['sex'].isin(['M', 'F'])]
data.head()

############################
############################

print("eurostat data")

dt2 = data.iloc[:, 5:]
dt2 = dt2.T
# after transpose, first row is the column names
dt2.columns = dt2.iloc[0,:]
# remove first row
data1 = dt2.iloc[1:]

data1.index = pd.date_range(start = start_date,  periods = data1.shape[0], freq = "MS")
data1 = data1.loc[:, ['NL','DE','FR','IT','ES','BE','JP','US']]
data1.columns = ['Netherlands_unemply_F', 'Netherlands_unemply_M', 'Germany_unemply_F', 'Germany_unemply_M', 'France_unemply_F', 'France_unemply_M','Italy_unemply_F','Italy_unemply_M','Spain_unemply_F', 'Spain_unemply_M','Belgium_unemply_F','Belgium_unemply_M','Japan_unemply_F','Japan_unemply_M', 'United States_unemply_F','United States_unemply_M']

data1.to_csv(output + "/unemployment_mo.csv")

dt2 = data.iloc[:, 5:]
dt2 = dt2.T
# after transpose, first row is the column names
dt2.columns = dt2.iloc[0,:]
# remove first row
data1 = dt2.iloc[1:]

data1.index = pd.date_range(start = start_date,  periods = data1.shape[0], freq = "MS")
data1 = data1.loc[:, ['NL','DE','FR','IT','ES','BE','JP','US']]
data1.columns = ['Netherlands_unemply_F', 'Netherlands_unemply_M', 'Germany_unemply_F', 'Germany_unemply_M', 'France_unemply_F', 'France_unemply_M','Italy_unemply_F','Italy_unemply_M','Spain_unemply_F', 'Spain_unemply_M','Belgium_unemply_F','Belgium_unemply_M','Japan_unemply_F','Japan_unemply_M', 'United States_unemply_F','United States_unemply_M']

data1.to_csv(output + "/unemployment_mo.csv")

##################
### European GDP
##################

start_date = '01/01/1975'

data = eurostat.get_data_df('namq_10_gdp')
data = data[data["unit"] == "CLV10_MEUR"]
data = data[data["s_adj"] == "SCA"] #NSA
data = data[data['na_item'] == 'B1G']

##################
# select needed items for analysis
##################

dt2 = data.iloc[:, 4:]
dt2 = dt2.T
# after transpose, first row is the column names
dt2.columns = dt2.iloc[0,:]
# remove first row
data1 = dt2.iloc[1:]
data1.index = pd.date_range(start = start_date,  periods = data1.shape[0], freq = "QS")
data1 = data1.loc[:, ['NL','DE','FR','IT','ES','BE','EE']]
data1.columns = ['Netherlands_GDP', 'Germany_GDP', 'France_GDP', 'Italy_GDP', 'Spain_GDP', 'Belgium_GDP','Europe_GDP']

data1.to_csv(output + "/europe_gdp_qt.csv")

##################
# inflation
##################

start_date = '1997-01-01'

data = eurostat.get_data_df('prc_hicp_manr')
data = data[data['freq'] == 'M']
data = data[data['unit'] == 'RCH_A']
data = data[data['coicop'] == 'CP00']

data = data[data['geo\\TIME_PERIOD'].isin(['BE','DE','EE','ES','FR','IT','NL'])]

dt2 = data.iloc[:, 3:]
dt2 = dt2.T
dt2.columns = dt2.iloc[0,:]
dt2.columns = [x + "_Inflation" for x in dt2.columns]
dt2 = dt2.iloc[1:]
dt2.index = pd.date_range(start = start_date,  periods = dt2.shape[0], freq = "MS")

dt2 = dt2.rename_axis(None, axis=1)

dt2.to_csv(output + "/europe_inflation_mo.csv")

##################
# Sentiment
##################

start_date = '01/01/1980'

data = eurostat.get_data_df('ei_bssi_m_r2')

data = data[data["freq"] == "M"]
data = data[data["s_adj"] == "SA"] #NSA
data = data[data['geo\\TIME_PERIOD'].isin(['BE','DE','EE','ES','FR','IT','NL'])]
data = data[data['indic'].isin(['BS-CCI-BAL','BS-CSMCI-BAL','BS-ESI-I','BS-ICI-BAL','BS-RCI-BAL','BS-SCI-BAL'])]

dt2 = data.iloc[:, 3:]
dt2 = dt2.T
dt2.columns = dt2.iloc[0,:]

dt2 = dt2.iloc[1:]
dt2.index = pd.date_range(start = start_date,  periods = dt2.shape[0], freq = "MS")

dt2 = dt2.rename_axis(None, axis=1)

colnames = ["_Construction_confidence", "_Consumer_confidence", "_Economic_sentiment_confidence",  "_Industrial_confidence", "_Retail_confidence", "_Service_confidence"]

numberCountries = 7
namelist = []
for i, _ in enumerate(colnames):
    a1 = numberCountries * i
    x = dt2.columns[a1:(a1 + numberCountries)] + colnames[i]
    namelist.append(x.tolist())

dt2.columns = list(chain(*namelist))

dt2 = dt2.iloc[1:]
dt2.index = pd.date_range(start = start_date,  periods = dt2.shape[0], freq = "MS")

dt2 = dt2.rename_axis(None, axis=1)

dt2.to_csv(output + "/europe_Confidence_mo.csv")