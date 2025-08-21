import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


output_figures = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/consumerConfidence//"
output_data = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/consumerConfidence//"

def collectData(verbose):

    data1 = pd.read_csv(r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/data/02_processed_data/a0_alldata_combinedMonthly.csv", index_col=0)

    wantThese = ['Consumentenvertrouwen_1',
                        'EconomischKlimaat_2', 
                        'Koopbereidheid_3', 
                        'EconomischeSituatieLaatste12Maanden_4', 
                        'EconomischeSituatieKomende12Maanden_5', 
                        'FinancieleSituatieLaatste12Maanden_6', 
                        'FinancieleSituatieKomende12Maanden_7',
                         'GunstigeTijdVoorGroteAankopen_8']
    

    numberofConsumerSeries = len(wantThese)
    print("Number of consumer series: ", numberofConsumerSeries)
    conCon1 = data1[wantThese]
    assert numberofConsumerSeries == conCon1.shape[1]

    if verbose:
        print(conCon1.head())
        conCon1.to_csv("tmp_conCon1.csv")

    return conCon1

conCon1 = collectData(verbose=True)

conCon1.to_csv(output_data + "processed_consumer_confidence.csv")

print(conCon1.head())

##################################
##################################
# Plot
##################################
##################################

conCon1['Average'] = conCon1.mean(axis=1)   

fig, ax = plt.subplots(3, 1, layout='constrained', figsize=(12, 8.75))
x = np.asarray(conCon1.index, dtype='datetime64[s]')

# plot multiple lines
for column in conCon1.columns:
    ax[0].plot(x, conCon1[column], marker='', color='grey', linewidth=1, alpha=0.4)

# Now re do the interesting curve, but biger with distinct color
ax[0].plot(x, conCon1['Average'], marker='', color='orange', linewidth=2, alpha=0.7)
ax[0].grid()
ax[0].set_title("Consumer Confidence Indicators", loc='left', fontsize=12, fontweight=0, color='black')

############################
############################

conCon1Subset = conCon1.loc['2015-01-01':,:]
x1 = np.asarray(conCon1Subset.index, dtype='datetime64[s]')

# plot multiple lines
for column in conCon1Subset.columns:
    ax[1].plot(x1, conCon1Subset[column], marker='', color='grey', linewidth=1, alpha=0.4)

# Now re do the interesting curve, but biger with distinct color
ax[1].plot(x1, conCon1Subset['Average'], marker='', color='orange', linewidth=2, alpha=0.7)
ax[1].grid()
ax[1].set_title("Consumer Confidence Indicators (2015-2025)", loc='left', fontsize=12, fontweight=0, color='black')

############################
############################

conCon1.index = pd.to_datetime(conCon1.index)
conConavgs2 = conCon1.loc['2022-01-01':,:]

ax[2].plot(conConavgs2)
ax[2].legend(conConavgs2.columns, loc='upper right', fontsize=8, ncol=2)
ax[2].grid()
ax[2].set_title("Consumer Confidence Indicators (2022-2025)", loc='left', fontsize=12, fontweight=0, color='black')

plt.savefig(output_figures + "conConavgs.png")
plt.show()