import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

output_figures = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/output/figures//"
output_data = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/exports/data//"


def plotExport():

    data1 = pd.read_csv(r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/data/02_processed_data/a0_alldata_combinedQuarterly.csv", index_col=0)

    wantThese = ['ExportsOfGoods_16_expenditure', 'ExportsOfServices_17_expenditure', 'TotalExportsOfGoodsAndServices_155_additional', 
                 'ExportsOfGoodsFromProduction_173_additional', 'ReExports_174_additional', 'OtherExportsOfServices_177_additional',

                 'ExportsOfGoods_16_seasonCorrected_expenditure', 'ExportsOfServices_17_seasonCorrected_expenditure',
                 'TotalExportsOfGoodsAndServices_155_seasonCorrected_additional', 'ExportsOfGoodsFromProduction_173_seasonCorrected_additional',
                 'ReExports_174_seasonCorrected_additional'
                 
                 ]
    

    Exports1 = data1[wantThese]

    subset = ["_seasonCorrected"]

    Exports_season_corrected = [col for col in Exports1.columns if any(sub in col for sub in subset)]
    Exports_not_season_corrected = [col for col in Exports1.columns if not any(sub in col for sub in subset)]

    ExportsSeason = Exports1[Exports_season_corrected]
    ExportsNotSeason = Exports1[Exports_not_season_corrected]   

    return ExportsSeason, ExportsNotSeason

ExportsSeason, ExportsNotSeason  = plotExport()


ExportsSeason.to_csv(output_data + "ExportsSeason.csv")
ExportsNotSeason.to_csv(output_data + "ExportsNotSeason.csv")

############################
############################

fig, ax = plt.subplots(2, 1, layout='constrained', figsize=(12, 8.75))

# start 1996 for comparison
ExportsNotSeason = ExportsNotSeason.loc['1996-01-01':,:]
ExportsSeason = ExportsSeason.loc['1996-01-01':,:]
x = np.asarray(ExportsNotSeason.index, dtype='datetime64[s]')

ax[0].plot(x, ExportsNotSeason, linewidth=2)
ax[0].grid()
ax[0].set_title("Exports Not Seasonally Adjusted", loc='left', fontsize=12, fontweight=0, color='black')
ax[0].legend(ExportsNotSeason.columns, loc='upper left', fontsize=8, ncol=1)


ax[1].plot(x, ExportsSeason, linewidth=2)
ax[1].grid()
ax[1].set_title("Exports Seasonally Adjusted", loc='left', fontsize=12, fontweight=0, color='black')
ax[1].legend(ExportsSeason.columns, loc='upper left', fontsize=8, ncol=1)

plt.show()