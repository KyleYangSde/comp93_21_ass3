import pandas as pd
import numpy as np
import sys
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import precision_score
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import average_precision_score
import csv
import warnings

#python ass.py https://raw.githubusercontent.com/mysilver/COMP9321-Data-Services/master/20t1/assign3/training.csv http s://raw.githubusercontent.com/mysilver/COMP9321-Data-Services/master/20t1/assign3/validation.csv 
def getData(url):
#    change it ro url inlater
    data = pd.read_csv(url)
    return data

def processDataset(data):
    data = data[["cast","crew","budget","original_language","runtime"]]
    return data


def getY(data):
    data = data[["revenue"]]
    return data


def removeDup(data):
    temp = []
    for i in data:
        if i not in temp:
            temp.append(i)
    return temp


def get(data):
    total = []
    warnings.filterwarnings('ignore')
    for i in range(len(data["cast"])):
        a = ast.literal_eval(data["cast"][i])
        total.append(a[0]["name"])
        
    total = removeDup(total)
    for i in range(len(data["cast"])):
        data["cast"][i] = total.index(ast.literal_eval(data["cast"][i])[0]["name"])
    
    crew = []
    for i in range(len(data["crew"])):
        a = ast.literal_eval(data["crew"][i])
        for j in a:
            if j["job"] == "Director":
                crew.append(j["name"])
                
    crew = removeDup(crew)        
    for i in range(len(data["crew"])):
        a = ast.literal_eval(data["crew"][i])
        for j in a:
            if j["job"] == "Director":
                data["crew"][i] = crew.index(j["name"])
    
    language = []
    for i in data["original_language"]:
        language.append(i)
    language = removeDup(language)
    for i in range(len(data["original_language"])):
        data["original_language"][i] = language.index(data["original_language"][i]) 


    return data

def getMovie(training):
    revenue = []
    for i in training:
        revenue.append(i[0])
    return revenue

def getQ1(training,testing):
    trainingY = getY(training)

    trainingX = get(processDataset(training))
    testingX = get(processDataset(testing))
    testingY = getY(testing)


    reg = LinearRegression().fit(trainingX , trainingY)
    predict = reg.predict(testingX)
    mse = mean_squared_error(testingY,predict)
    cor = np.corrcoef(predict,testingY)[0][1]
    movie = getMovie(testing)
    with open("z51774433.PART1.summary.csv","w",newline='') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["zid","MSR","correlation"])
        writer.writerows([["z5177443",mse,cor]])
        
    with open("z51774433.PART1.output.csv","w",newline='') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["movie_id,predicted_revenue"])

        for i in range(len(predict)):
            writer.writerows([[movie[i],predict[i]]])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit()
        
#    read from comandline
    training = getData(sys.argv[1])
    testing = getData(sys.argv[2])
    getQ1(training,testing)
    