import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import os
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pickle
import datetime as dt


def createFutureDates(days):
    dates_past = []
    today = dt.date.today()
    days = 31
    for day in range(1, days):
        date_pa = today - dt.timedelta(days=day)
        dates_past.append(date_pa.strftime("%Y-%m-%d"))
    return dates_past


def PlotNaiveBase(screen_name):
    APP_ROOT=os.path.dirname(os.path.abspath(__file__))
    target=os.path.join(APP_ROOT,'static')
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        past31days=createFutureDates(31)
        filename='{0}_tweets.csv'.format(screen_name)
        df3=pd.read_csv(filename)
        df2=df3.copy()
        df3=df3.loc[df3["created_date"].isin(past31days)]
        print(df3["created_date"])
        df3_x=df3["tweets"]

        df3_y1=df3["sentiment"]
        #df3_y=df3_y1[2:]
        #datetime.datetime.now() - tweet.created_at).days

        filename = 'finalized_naivebasemodel.sav'
        loaded_model = pickle.load(open(filename, 'rb'))

        labels1=loaded_model.predict(df3["tweets"].apply(lambda x: np.str_(x)))
        print(accuracy_score(df3_y1,labels1))
        print(classification_report(df3_y1,labels1))
        '''df3["predicted"]=labels1
        df3.to_csv("Bobpisanipredicted.csv")'''

        mat=confusion_matrix(df3["sentiment"],labels1)
        print(mat)
        report_data = []
        # print(mat)
        for label, metrics in classification_report(df3["sentiment"],labels1, output_dict=True).items():
            metrics['label'] = label
            report_data.append(metrics)

        report_df = pd.DataFrame(
            report_data,
            columns=['label', 'precision', 'recall', 'f1-score', 'support']
        )

        # Plot as a bar chart.

        confusionfull="confusionfull.png"
        confusionsupport="confusionsupport.png"
        heat="heatmap.png"
        confusionfulldir="\\".join([target,confusionfull])
        confusionsupportdir = "\\".join([target, confusionsupport])
        heatdir = "\\".join([target, heat])
        os.remove(heatdir)
        filelist=[]

        filelist.append(confusionfull)
        filelist.append(confusionsupport)
        filelist.append(heat)
        sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False, xticklabels=set(labels1),
                    yticklabels=set(labels1))
        plt.xlabel("train data")
        plt.ylabel("predicted data")

        plt.savefig(heatdir, bbox_inches="tight")
        report_df.plot(y=['precision', 'recall', 'f1-score'], x='label', kind='bar')
        plt.savefig(confusionfulldir,bbox_inches = "tight")
        report_df.plot(y=['support'], x='label', kind='bar')
        plt.savefig(confusionsupportdir,bbox_inches = "tight")




        return filelist
    #plt.show()