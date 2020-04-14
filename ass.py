import pandas as pd
import numpy as np
import sys
import ast
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
    data = np.array(data)

    data = data.tolist()
    return data


#get cast
def getCast(training):
    cast = []
    total = 0
    for i in training:
        for j in ast.literal_eval(i[1]):
            total+=j["cast_id"]
        cast.append(total)
        total = 0
    return cast

def getCrew(training):
    crew = []
    total = 0
    for i in training:
        for j in ast.literal_eval(i[2]):
            total+=j["id"]
        crew.append(total)
        total = 0
    return crew

def getbugdet(training):
    budget = []
    a= []
    for i in training:
        a.append(i[3])
    average = sum(a)/ len(a)
    for i in training:
        if i[3] < 100:
            i[3] = average
        budget.append(i[3])
    return budget

def getGenres(training):
    genres = []
    total = 0
    for i in training:
        for j in ast.literal_eval(i[4]):
            total+=j["id"]
        genres.append(total)
        total = 0
        

    return genres

def getKeywords(training):
    keywords = []
    total = 0
    for i in training:
        for j in ast.literal_eval(i[6]):
            total+=j["id"]
        keywords.append(total)
        total = 0
        

    return keywords

def getLanguage(training):
    language = []
    num = []
    for i in training:
        language.append(i[7])
    temp = []
    for item in language:
	    if not item in temp:
		    temp.append(item)
    language = temp
    for i in training:
        for j in language:
            if i[7] == j:
                num.append(language.index(j))
    return num

def getCompany(training):
    company = []
    total = 0
    for i in training:
        for j in ast.literal_eval(i[10]):
            total+=j["id"]
        company.append(total)
        total = 0

    return company

def getCountries(training,col,key):
    countries = []
    num = []
    
    for i in training:
        for j in ast.literal_eval(i[col]):
            countries.append(j[key])
    temp = []
    for item in countries:
	    if not item in temp:
		    temp.append(item)
    countries = temp
    for i in training:
        total = 0
        for j in ast.literal_eval(i[col]):
            total += countries.index(j[key])
        num.append(total)
        
    return num

def getRevenue(training):
    revenue = []
    for i in training:
        revenue.append(i[13])
    return revenue

def getRuntime(training):
    runtime = []
    for i in training:
        runtime.append(int(i[14]))
    return runtime

#all are same not work
def getReleased(training):
    release = []
    for i in training:
        release.append(i[16])
    return release

def minMaxScalar(tempp):
    changed = []
    for i in tempp:
        num = (i-min(tempp))/(max(tempp)-min(tempp))
        changed.append(round(num,2)) 
    return changed

def getMovie(training):
    revenue = []
    for i in training:
        revenue.append(i[0])
    return revenue

def getTrainingOrTestingX(data):
    movie = getMovie(data)
    cast = getCast(data)
    crew = getCrew(data)
    bugdet = getbugdet(data)
    genres = getGenres(data)
    language =getLanguage(data)
    company = getCompany(data)

    countries = getCountries(data,11,"iso_3166_1")
    runtime =getRuntime(data)
    spoken = getCountries(data,15,"iso_639_1")
    
    total = []
    for i in range(len(data)):
        
        total.append([cast[i],crew[i],bugdet[i],genres[i],language[i],company[i],countries[i],runtime[i],spoken[i]]) 

    return total

def getTrainingOrTestingY(data,col):
    revenue = []
    for i in data:
        revenue.append(i[col])
    return revenue

def getQ1(training,testing):
    trainingX = getTrainingOrTestingX(training)
    trainingY = getTrainingOrTestingY(training,13)
    testingX = getTrainingOrTestingX(testing)
    testingY = getTrainingOrTestingY(testing,13)
#
#    from sklearn import svm
#
#    clf = svm.SVR()
#    reg  = clf.fit(trainingX , trainingY)
#    
#    predict = reg.predict(testingX)
#
    from sklearn import tree
    from sklearn.linear_model import SGDClassifier

#    clf = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
#    clf.fit(trainingX , trainingY)
#    predict = clf.predict(testingX)
    clf = tree.DecisionTreeRegressor()
    clf = clf.fit(trainingX , trainingY)
    predict = clf.predict(testingX)

#    reg = LinearRegression().fit(trainingX , trainingY)
#    predict = reg.predict(testingX)
    mse = mean_squared_error(testingY,predict)
    cor = np.corrcoef(predict,testingY)[0][1]
    movie = getMovie(testing)
    with open("z5177443.PART1.summary.csv","w",newline='') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["zid","MSR","correlation"])
        writer.writerows([["z5177443",mse,cor]])
        
    with open("z5177443.PART1.output.csv","w",newline='') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["movie_id,predicted_revenue"])

        for i in range(len(predict)):
            writer.writerows([[movie[i],predict[i]]])


def getQ2(training,testing):
    trainingX = getTrainingOrTestingX(training)
    trainingY = getTrainingOrTestingY(training,-1)
    testingX = getTrainingOrTestingX(testing)
    testingY = getTrainingOrTestingY(testing,-1)


    from sklearn import tree
    from sklearn.metrics import recall_score
    from sklearn.metrics import accuracy_score
    
    from sklearn import svm

#    clf = svm.SVC()
#    clf.fit(trainingX, trainingY)

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(trainingX, trainingY)
    predict = clf.predict(testingX)
    warnings.filterwarnings('ignore')
    average = average_precision_score(testingY, clf.predict(testingX),pos_label=3)
    recall = recall_score(testingY, clf.predict(testingX),average = None)
    accuracy =accuracy_score(testingY, clf.predict(testingX))
    
    a = np.mean(recall)
    movie = getMovie(testing)
    with open("z5177443.PART2.summary.csv","w",newline='') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["zid","average_precision","average_recall","accuracy"])
        writer.writerows([["z5177443",average,a,accuracy]])
        
    with open("z5177443.PART2.output.csv","w",newline='') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["movie_id,predicted_rating"])

        for i in range(len(predict)):
            writer.writerows([[movie[i],predict[i]]])



if __name__ == "__main__":
#    if len(sys.argv) != 3:
#        sys.exit()
        
#    read from comandline
    training = getData(sys.argv[1])
    testing = getData(sys.argv[2])
    getQ1(training,testing)
    getQ2(training,testing)
    

    