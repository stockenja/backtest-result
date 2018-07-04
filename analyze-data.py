import numpy as np
import json
import matplotlib.pyplot as plot

# PROBABILITY_THRESHOLD: Probability at which you will buy a stock
PROBABILITY_THRESHOLD = 0.80

EXPERIMENT_CONFIG = {   "lastDate": '2018-01-01', \
                        "experimentDayLength": 504, \
                        "recommendThreshold": PROBABILITY_THRESHOLD, \
                        "daysAhead": 20, \
                    }

def main():
    tickerList = ["GLD", "SPY", "XBI", "AMZN"]
    successRateList = []

    for ticker in tickerList:
        print("=================")
        print("Ticker: " + ticker)
        result = analysisOneTickerAccuracy(ticker)
        successRateList.append(result["accuracy"])
        print("=================\n\n")
    
    print("===== Overall Success Rate =====")
    averageSuccessRate = np.nanmean(successRateList)
    print("Average Prediction Success Rate: " + str(averageSuccessRate) + "%")
    print("================================\n")
    print("Please close graph to exit...\n\n")

    fig = plot.figure()
    ax = fig.add_subplot(111)
    ax.axhline(y=averageSuccessRate, label='Average', color="green", linestyle="-.")
    ax.text(0, averageSuccessRate+2, 'Average Success Rate')

    plot.bar(tickerList, successRateList)
    plot.title('Prediction Success Rate based on Probability of ' + str(PROBABILITY_THRESHOLD*100) + '%')
    plot.ylabel("Prediction Success Rate (%)")
    plot.show()

def analysisOneTickerAccuracy(ticker):
    
    SIGNAL_THRESHOLD = EXPERIMENT_CONFIG['recommendThreshold']


    filename = ticker + "_" + EXPERIMENT_CONFIG["lastDate"] + "_with_" \
                + str(EXPERIMENT_CONFIG["experimentDayLength"]) + "_" + str(EXPERIMENT_CONFIG["daysAhead"]) + "days"

    filepath = "data/2018-07-03_algorithm/" + str(EXPERIMENT_CONFIG["daysAhead"]) + "_trading_days_ahead/" + \
                str(EXPERIMENT_CONFIG["experimentDayLength"]) + "_total_trading_days/" + \
                str(EXPERIMENT_CONFIG["lastDate"]) + "_last_date/" + \
                filename + ".json"

    with open(filepath) as f:
        data = json.load(f)

    dateList = data["date"]
    probabilityList = data["probabilities"]
    returnList = data["actualReturn"]

    result = {}
    result["predictionAccuracyList"] = []
    result["date"] = []
    result["probabilityUsed"] = []
    result["predictedMove"] = []
    result["actualReturn"] = []

    for i in range(0, len(dateList)):
        result["date"].insert(0, dateList[i])
        bestProbability = probabilityList[i]
        try:
            returnChange = returnList[i]
            if(bestProbability >= SIGNAL_THRESHOLD):
                result["predictedMove"].insert(0, 'Up')
                result["actualReturn"].insert(0, returnChange)
                result["probabilityUsed"].insert(0, bestProbability)
                if(returnChange >= 0):
                    result["predictionAccuracyList"].insert(0, 1)
                else:
                    result["predictionAccuracyList"].insert(0, -1)
            elif(1-bestProbability >= SIGNAL_THRESHOLD):
                result["predictedMove"].insert(0, 'Down')
                result["actualReturn"].insert(0, returnChange)
                result["probabilityUsed"].insert(0, bestProbability)
                if(returnChange < 0):
                    result["predictionAccuracyList"].insert(0, 1)
                else:
                    result["predictionAccuracyList"].insert(0, -1)
            else:
                result["actualReturn"].insert(0, np.nan)
                result["probabilityUsed"].insert(0, np.nan)
                result["predictedMove"].insert(0, 'None')
                result["predictionAccuracyList"].insert(0,0)
        except Exception as ex:
            print(ex)
            print(endDate)
            result["actualReturn"].insert(0, np.nan)
            result["probabilityUsed"].insert(0, np.nan)
            result["predictedMove"].insert(0, 'None')
            result["predictionAccuracyList"].insert(0,0)
    
    predictionAccuracyList = np.asarray(result["predictionAccuracyList"])
    accuracy, totalPredictionsMade = calculateAccuracy(predictionAccuracyList)
    accuracy = accuracy*100

    result["accuracy"] = accuracy
    print("Number of predictions: " + str(totalPredictionsMade))
    print("Prediction Success Rate: " + str(accuracy) + "%")

    return result


def calculateAccuracy(predictionAccuracyList):
    totalPredictionsMade = len(predictionAccuracyList[predictionAccuracyList!=0])
    
    correctPredictionsMade = len(predictionAccuracyList[predictionAccuracyList>0])
    
    if(totalPredictionsMade > 0):
        accuracy = float(correctPredictionsMade)/float(totalPredictionsMade)
    else:
        accuracy = np.nan
    
    return accuracy, totalPredictionsMade

if __name__ == "__main__":
    main()

