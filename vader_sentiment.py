from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1, dataframe2 = None):
    analyzer = SentimentIntensityAnalyzer()
    #two arrays containing sentiment score(from -1 to 1) and sentiment result (Negative, Postive, Neutral)
    #that is to be bound to the output dataframe
    sentiment_score = []
    sentiment_result = []
    
    for comment in dataframe1['Context']:
        vs = analyzer.polarity_scores(str(comment))
        sentiment_score.append(vs["compound"])
        if eval(str(vs["compound"])) < 0:
            sentiment = 'Negative'
        elif eval(str(vs["compound"])) == 0:
            sentiment = 'Neutral'
        elif eval(str(vs["compound"])) > 0:
            sentiment = 'Positive'
        sentiment_result.append(sentiment)
    
    dataframe1['SentimentScore'] = sentiment_score
    dataframe1['SentimentResult'] = sentiment_result
    return dataframe1
