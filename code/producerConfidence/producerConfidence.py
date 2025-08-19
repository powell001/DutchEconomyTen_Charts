import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


output_figures = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/output/figures//"
output_data = r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/code/producerConfidence/data//"

def collectData(verbose):

    data1 = pd.read_csv(r"C:/Users/jpark/vscode/DutchEconomyTen_Charts/data/02_processed_data/a0_alldata_combinedMonthly.csv", index_col=0)

    wantThese = ['ProducerConfidence_1',
                    'ExpectedActivity_2',
                    'H-S Sevices_BusinessConfidence',
                    'H Transportation and storage_BusinessConfidence',
                    'I Accommodation and food serving_BusinessConfidence',
                    'J Information and communication_BusinessConfidence',
                    'L Renting, buying, selling real estate_BusinessConfidence',
                    'M-N Business services_BusinessConfidence',
                    'R Culture, sports and recreation_BusinessConfidence',
                    'S Other service activities_BusinessConfidence',
                    'H-S SevicesBusinessSituationNextThreeMonths',
                    'H Transportation and storageBusinessSituationNextThreeMonths',
                    'I Accommodation and food servingBusinessSituationNextThreeMonths',
                    'J Information and communicationBusinessSituationNextThreeMonths',
                    'L Renting, buying, selling real estateBusinessSituationNextThreeMonths',
                    'M-N Business servicesBusinessSituationNextThreeMonths',
                    'R Culture, sports and recreationBusinessSituationNextThreeMonths',
                    'S Other service activitiesBusinessSituationNextThreeMonths',
                    'H-S SevicesBusinessSituationPastThreeMonths',
                    'H Transportation and storageBusinessSituationPastThreeMonths',
                    'I Accommodation and food servingBusinessSituationPastThreeMonths',
                    'J Information and communicationBusinessSituationPastThreeMonths',
                    'L Renting, buying, selling real estateBusinessSituationPastThreeMonths',
                    'M-N Business servicesBusinessSituationPastThreeMonths',
                    'R Culture, sports and recreationBusinessSituationPastThreeMonths',
                    'S Other service activitiesBusinessSituationPastThreeMonths',
                    'C Industry, H-S services and 45+47_UncertaintyIndicatorBusinessClimate',
                    'C Manufacturing_UncertaintyIndicatorBusinessClimate',
                    '45 Sale and repair of motor vehicles_UncertaintyIndicatorBusinessClimate',
                    '47 Retail trade (not in motor vehicles)_UncertaintyIndicatorBusinessClimate',
                    'C Manufacturing_UncertaintyIndicatorBusinessClimate', 
                    '45 Sale and repair of motor vehicles_UncertaintyIndicatorBusinessClimate', 
                    '47 Retail trade (not in motor vehicles)_UncertaintyIndicatorBusinessClimate', 
                    'H-S Sevices_UncertaintyIndicatorBusinessClimate', 
                    'H Transportation and storage_UncertaintyIndicatorBusinessClimate', 
                    'I Accommodation and food serving_UncertaintyIndicatorBusinessClimate', 
                    'J Information and communication_UncertaintyIndicatorBusinessClimate', 
                    'L Renting, buying, selling real estate_UncertaintyIndicatorBusinessClimate', 
                    'M-N Business services_UncertaintyIndicatorBusinessClimate', 
                    'R Culture, sports and recreation_UncertaintyIndicatorBusinessClimate', 
                    'S Other service activities_UncertaintyIndicatorBusinessClimate']

    numberofProducerSeries = len(wantThese)
    print("Number of producer series: ", numberofProducerSeries)
    proCon1 = data1[wantThese]
    assert numberofProducerSeries == proCon1.shape[1]

    if verbose:
        print(proCon1.head())
        proCon1.to_csv("tmp_proCon1.csv")

    return proCon1

proCon1 = collectData(verbose=True)


subsets = ["ProducerConfidence", "ExpectedActivity", "BusinessConfidence", "BusinessSituationNextThreeMonths", "BusinessSituationPastThreeMonths", "UncertaintyIndicatorBusinessClimate"]

proConavgs = []
for i in subsets:
    # select groups of confidence indicators
    sub1 = [col for col in proCon1.columns if i in col]
    seriesDF = proCon1[sub1]
    proConavgs.append(seriesDF.mean(axis=1))


proConavgs = pd.concat(proConavgs, axis=1)
proConavgs.columns = subsets
proConavgs['Average'] = proConavgs.mean(axis=1)

proConavgs.to_csv(output_data + "processed_producer_confidence.csv")

print(proConavgs.head())

##################################
##################################
# Plot
##################################
##################################

fig, ax = plt.subplots(3, 1, layout='constrained', figsize=(12, 8.75))
x = np.asarray(proConavgs.index, dtype='datetime64[s]')

# plot multiple lines
for column in proConavgs.columns:
    ax[0].plot(x, proConavgs[column], marker='', color='grey', linewidth=1, alpha=0.4)

# Now re do the interesting curve, but biger with distinct color
ax[0].plot(x, proConavgs['Average'], marker='', color='orange', linewidth=2, alpha=0.7)
ax[0].grid()
ax[0].set_title("Producer Confidence Indicators", loc='left', fontsize=12, fontweight=0, color='black')

############################
############################

proConavgsSubset = proConavgs.loc['2015-01-01':,:]
x1 = np.asarray(proConavgsSubset.index, dtype='datetime64[s]')

# plot multiple lines
for column in proConavgsSubset.columns:
    ax[1].plot(x1, proConavgsSubset[column], marker='', color='grey', linewidth=1, alpha=0.4)

# Now re do the interesting curve, but biger with distinct color
ax[1].plot(x1, proConavgsSubset['Average'], marker='', color='orange', linewidth=2, alpha=0.7)
ax[1].grid()
ax[1].set_title("Producer Confidence Indicators (2015-2025)", loc='left', fontsize=12, fontweight=0, color='black')

############################
############################

proConavgs.index = pd.to_datetime(proConavgs.index)
proConavgs2 = proConavgs.loc['2022-01-01':,:]

ax[2].plot(proConavgs2)
ax[2].legend(proConavgs2.columns, loc='upper right', fontsize=8, ncol=2)
ax[2].grid()
ax[2].set_title("Producer Confidence Indicators (2022-2025)", loc='left', fontsize=12, fontweight=0, color='black')

plt.savefig(output_figures + "proConavgs.png")
plt.show()