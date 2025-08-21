import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

output_figures = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/imports//"
output_data    = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/imports//"


def plotImport():

    data1 = pd.read_csv(r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/data/02_processed_data/a0_alldata_combinedQuarterly.csv", index_col=0)

    wantThese = ['ImportsOfGoods_4_seasonCorrected_expenditure', 'ImportsOfServices_5_seasonCorrected_expenditure', 'ImportsOfGoods_4_expenditure', 'ImportsOfServices_5_expenditure', 'TotalImportsOfGoodsAndServices_179_additional', 'TotalImportsOfGoodsAndServices_179_seasonCorrected_additional']

    imports1 = data1[wantThese]

    subset = ["_seasonCorrected"]

    imports_season_corrected = [col for col in imports1.columns if any(sub in col for sub in subset)]
    imports_not_season_corrected = [col for col in imports1.columns if col not in imports_season_corrected]

    importsSeason = imports1[imports_season_corrected]
    importsNotSeason = imports1[imports_not_season_corrected]   


    return importsSeason, importsNotSeason

importsSeason, importsNotSeason  = plotImport()

############################
############################

fig, ax = plt.subplots(2, 1, layout='constrained', figsize=(12, 8.75))

# start 1996 for comparison
importsNotSeason = importsNotSeason.loc['1996-01-01':,:]
importsSeason = importsSeason.loc['1996-01-01':,:]
x = np.asarray(importsNotSeason.index, dtype='datetime64[s]')

ax[0].plot(x, importsNotSeason, linewidth=2)
ax[0].grid()
ax[0].set_title("Imports Not Seasonally Adjusted", loc='left', fontsize=12, fontweight=0, color='black')
ax[0].legend(importsNotSeason.columns, loc='lower right', fontsize=8, ncol=1)


ax[1].plot(x, importsSeason, linewidth=2)
ax[1].grid()
ax[1].set_title("Imports Seasonally Adjusted", loc='left', fontsize=12, fontweight=0, color='black')

plt.savefig(output_figures + "Imports.png", dpi=300, bbox_inches='tight')
plt.show()