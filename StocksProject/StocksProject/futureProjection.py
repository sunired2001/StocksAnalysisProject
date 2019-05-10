import numpy as np
import pandas as pd
from sklearn.svm import SVR
import pandas_datareader.data as web
import datetime as dt
from datetime import timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import unicodedata
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from pymongo import MongoClient
import csv
import os
import futureDates
import trainModel
pd.plotting.register_matplotlib_converters(explicit=True)



dict_future_projection = {}
list_fund_progress_image = []
def fundFutureProjection(dict_trained_stock_model, list_etf_fund, future_proj_days):
    APP_ROOT=os.path.dirname(os.path.abspath(__file__))
    target=os.path.join(APP_ROOT,'static')
    if not os.path.isdir(target):
        os.mkdir(target)
    length = len(list_etf_fund)
    print(length)
    print(list_etf_fund)
    for etf_iterator in range(0,length):
        fund = list_etf_fund[etf_iterator]
        #print(fund)
        fund_lr_model = dict_trained_stock_model[fund]
        r2_value = round(fund_lr_model['r2'],6)*100
        coefficient = fund_lr_model['Coefficient'][0]
        intercept = fund_lr_model['Intercept'][0]
        df_fund_model_dataset = pd.DataFrame(fund_lr_model['Test_Pred_data'])
        plt.plot(df_fund_model_dataset['Date'],df_fund_model_dataset['ActualPrice'])
        plt.plot(df_fund_model_dataset['Date'],df_fund_model_dataset['PredictedPrice'])
        plt.title(f'Performance Trend for {fund} with confidence level of {r2_value}% \n')
        name = '\\Projection_' + fund + '.png'
        name1 = 'Projection_' + fund + '.png'
        image = target + name
        #image_name = os.join(target,image)
        print(image)
        plt.savefig(image)
        list_fund_progress_image.append(name1)
        df_future_projection = futureDates.createFutureDates(future_proj_days)
        df_future_projection['FutureValue'] = ((df_future_projection['DateFloat']).values.reshape(-1,1) * coefficient) + intercept
        dict_future_projection[fund] = df_future_projection
        #df_future_projection['FutureValue'] = ((df_future_projection['DateFloat']) * coefficient) + intercept
        file_name = 'FutureProjections_' + fund + '.csv'
        #image_future_projection = 'FutureProjections_' + list_etf[etf_iterator] + '.csv'
        #file_
        df_future_projection.to_csv(file_name)
    return list_fund_progress_image