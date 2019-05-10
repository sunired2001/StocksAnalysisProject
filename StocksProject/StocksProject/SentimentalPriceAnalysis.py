import os
from flask import Flask, render_template, jsonify, request, redirect
import TwitterSpecificTweet as tst
import TestNaiveBase as nb
import trainModel
import futureProjection
import csv

app = Flask(__name__,static_url_path='/static')


@app.route("/")
def home():
    return render_template("index.html")

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route("/sentimentsend")
def sentimentsend():
    return render_template("sentiment.html")


@app.route("/sentimentopt")

def sentimentopt():

    return render_template("sentiment.html")
@app.route("/sentimentresultsend", methods=["GET", "POST"])
def sentimentresultsend():
    if request.method == "POST":
        name = request.form["invselect"]
        print("sceen",name)
        tst.tweetsOfGivenInvestor(name)
        filelist=nb.PlotNaiveBase(name)
        print(filelist)

    return render_template("sentimentresult.html",selectedname=filelist)


@app.route("/priceprediction")
def priceprediction():
    list_funds_all = []
    path_master_file = os.getcwd() + '/data/ETFSymbols.csv'

    with open(path_master_file) as fp_master_reader:
        read_fund_list = csv.reader(fp_master_reader, delimiter=',')
        for fund in list(read_fund_list):
            for ticker in fund:
                list_funds_all.append(ticker)
    return render_template("prediction.html", option_list=list_funds_all)


@app.route("/priceopt", methods=['GET', 'POST'])
def priceopt():
    path_img = 'static/images'
    if not os.path.exists(path_img):
        os.mkdir(path_img)
    # list_funds_selected = []
    list_etf = []
    list_funds_all = []
    path_master_file = os.getcwd() + '/data/ETFSymbols.csv'

    with open(path_master_file) as fp_master_reader:
        read_fund_list = csv.reader(fp_master_reader, delimiter=',')
        for fund in list(read_fund_list):
            for ticker in fund:
                list_funds_all.append(ticker)

    if request.method == 'POST':
        list_etf = request.form.getlist("option")
        print("In Flask \n")
        print(list_etf)
        daysForProjection = request.form["daysForProjection"]
        dict_fund_model = {}
        dict_r2 = {}
        for etf in list_etf:
            model_etf = trainModel.TrainTestModel(etf)
            dict_r2[etf] = model_etf['r2']
            dict_fund_model[etf] = model_etf
        list_fund_progress_graphs = futureProjection.fundFutureProjection(dict_fund_model,
                                                                          list_etf,
                                                                          int(daysForProjection))
        length = len(list_fund_progress_graphs)
        print(list_fund_progress_graphs)
    return render_template("predictionresult.html",
                           list_fund_progress_graphs=list_fund_progress_graphs,
                           length=length)


if __name__== "__main__":
    app.run(debug=True)