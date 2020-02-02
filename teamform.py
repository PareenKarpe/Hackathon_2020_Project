from flask import Flask, request, Response, render_template
import base64
import mysql.connector
from mysql.connector import Error
from flask import abort
#from flask_basicauth import BasicAuth
from flask_bootstrap import Bootstrap

from functools import wraps
import uuid
import time
from flask import jsonify
import bcrypt
import re

#####imports for team
from pandas import Series, DataFrame

import pandas as pd

import numpy as np

import os

import matplotlib.pylab as plt

from sklearn.model_selection  import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.cluster import KMeans

import sklearn.metrics

from sklearn.preprocessing import StandardScaler

import pandasql as ps



app = Flask(__name__)
Bootstrap(app)

@app.route("/addAccount",methods=["POST"])
def addAccount():
  developer = request.form['developer']
  analyst = request.form['analyst']
  architect = request.form['architect']
  tester = request.form['qa']


  #take user input
  df = pd.read_csv(os.getcwd() + "/data/final.csv")

  df[df.isnull().any(axis=1)]
  # **********************Labeling regions*******************state = df['State'].valuesdf_state = pd.DataFrame({'state':state})le = LabelEncoder()le.fit(state)

  state = df['State'].values

  df_state = pd.DataFrame({'state': state})

  le = LabelEncoder()

  le.fit(state)
  state = le.transform(state)
  df['State'] = state

  # getting a copy
  df_state['encoded'] = state
  df_new = pd.DataFrame()
  df_new = df[['GenderID', 'PerfScoreID', 'PayRate', 'PositionID', 'State', 'EngagementSurvey', 'SpecialProjectsCount']]
  # df_new = df[['PerfScoreID','PositionID']]
  df_new.head()

  # Initialise the Scaler
  scaler = StandardScaler()

  # To scale data
  x = scaler.fit_transform(df_new)

  scaled_df = pd.DataFrame(x)

  scaled_df.head()

  scaled_df.columns = ['GenderID', 'PerfScoreID', 'PayRate', 'PositionID', 'State', 'EngagementSurvey',
                       'SpecialProjectsCount']

  # In[241]:

  # correlation = abs(scaled_df.corr())  # taking only the absolute values
  #
  # plt.figure(figsize=(25, 20))
  #
  # plt.title('Correlation of all the columns')
  #
  # sb.heatmap(round(correlation, 2), linewidths=.7, annot=True, vmin=-1, vmax=1)  # cmap="YlGnBu"

  df_final = scaled_df[['PerfScoreID', 'PayRate', 'PositionID', 'State']]

  # In[242]:

  from scipy.spatial.distance import cdist
  clusters = range(1, 10)
  meanDistortions = []

  for k in clusters:
    model = KMeans(n_clusters=k)
    model.fit(df_final)
    prediction = model.predict(df_final)
    meanDistortions.append(
      sum(np.min(cdist(df_final, model.cluster_centers_, 'euclidean'), axis=1)) / df_final.shape[0])

  # plt.cla()
  plt.plot(clusters, meanDistortions, 'bx-')
  plt.xlabel('k')
  plt.ylabel('Average distortion')
  plt.title('Selecting k with the Elbow Method')

  # In[244]:

  # Optimal clusters is 2
  final_model = KMeans(4)
  final_model.fit(scaled_df)
  prediction = final_model.predict(scaled_df)

  # In[245]:

  prediction

  # In[246]:

  df['clusters'] = prediction
  df['State'] = df_state['state']
  df.to_csv(os.getcwd() + '/data/final_ouput.csv', index=False)
  df_teams = df;
  # state = df['State'].values
  # state = df['State'].valuesdf_state = pd.DataFrame({'state': state})
  # le = LabelEncoder()
  # le.fit(state)
  # state = le.transform(state)
  # df['State'] = state  # getting a copy
  # #df_state['encoded'] = state
  # df_new = pd.DataFrame()
  # df_new = df[['GenderID', 'EmpStatusID', 'PerfScoreID', 'PayRate', 'PositionID', 'State', 'EngagementSurvey',
  #              'SpecialProjectsCount']]
  # # Optimal clusters is 2
  # final_model = KMeans(6)
  # final_model.fit(df_new)
  # prediction = final_model.predict(df_new)
  # df['clusters'] = prediction
  #
  #
  # df.to_csv(os.getcwd() + '/data/final_ouput1.csv', index=False)

  #print(df)
  s = """select count(distinct clusters) from df""";
  q = ps.sqldf(s, locals())
  #print(q)
  cluster_num = q.iloc[0]['count(distinct clusters)']
  print(cluster_num)

  # if cluster_num == 1:

  q_team1 = """select * from df where clusters == 0""";
  df_team1 = ps.sqldf(q_team1, locals())
  df_team1["EmpSatisfaction"] = pd.to_numeric(df["EmpSatisfaction"])
  print(len(df_team1))

  q_team2 = """select * from df where clusters == 1""";
  df_team2 = ps.sqldf(q_team2, locals())


  q_team3 = """select * from df where clusters == 2""";
  df_team3 = ps.sqldf(q_team3, locals())


  q_team4 = """select * from df where clusters == 3""";
  df_team4 = ps.sqldf(q_team4, locals())


  pd1 = pd.DataFrame()
  f = pd.DataFrame()
  for i in range(0,cluster_num):
    var = """/i/"""
    #q_team1 = (s"""select * from df where clusters == $param""")
    if i == 0:
      q_team1 = """select * from df where clusters == 0""";
      df_team1 = ps.sqldf(q_team1, locals())
      df_team1["EmpSatisfaction"] = pd.to_numeric(df["EmpSatisfaction"])
    elif i == 1:

      # print(df_team1)
      print("11111")

      q_team2 = """select * from df where clusters == 1""";
      df_team1 = ps.sqldf(q_team2, locals())
      df_team1["EmpSatisfaction"] = pd.to_numeric(df["EmpSatisfaction"])
    elif i == 2:

      q_team3 = """select * from df where clusters == 2""";
      print("22222")

      df_team1 = ps.sqldf(q_team3, locals())
      df_team1["EmpSatisfaction"] = pd.to_numeric(df["EmpSatisfaction"])
    elif i == 3:

      q_team4 = """select * from df where clusters == 3""";
      print("333333")

      df_team1 = ps.sqldf(q_team4, locals())
      df_team1["EmpSatisfaction"] = pd.to_numeric(df["EmpSatisfaction"])
    f = team_form(df_team1,developer,analyst,architect,tester)
    pd1 = pd.concat([pd1,f])
  print(pd1)
  pd1.to_csv(os.getcwd() + '/data/test7.csv', index=False)
  return render_template('displayTeams.html')












  #divide the resources based on input for each team






























  return ""
  #return render_template('sucess.html')

def team_form(df_team1,developer,analyst,architect,tester):
  try:
    df_team_1 = pd.DataFrame()
    q_soft = """select * from df_team1 where position == 'Software Engineer' order by PayRate ASC, EmpSatisfaction DESC """;
    df_soft = (ps.sqldf(q_soft, locals())).head(int(developer))
    if len(df_soft) < 1:
      f1 = pd.DataFrame()
      return f1

    df_team_1 = df_soft
  except:
    f1 = pd.DataFrame()
    return f1




  #print(df_team_1)
  print("*****************************************")




  try:
    q_alyst = """select * from df_team1 where position == 'Data Analyst' order by PayRate ASC, EmpSatisfaction DESC """;
    df_alyst = (ps.sqldf(q_alyst, locals())).head(int(analyst))

    df1_team1 = pd.concat([df_team_1,df_alyst])
    if len(df_alyst) < 1:
      f1 = pd.DataFrame()
      return f1
  except:
    f1 = pd.DataFrame()
    return f1
  #print(df1_team1)


  try:

    q_architect = """select * from df_team1 where position == 'Technical Architect' order by PayRate ASC, EmpSatisfaction DESC""";
    df_architect = (ps.sqldf(q_architect, locals())).head(int(architect))
    if len(df_architect) < 1:
      f1 = pd.DataFrame()
      return f1
    df2_team1 = pd.concat([df1_team1,df_architect])
  except:
    f1 = pd.DataFrame()
    return f1




  try:

    q_tester = """select * from df_team1 where position == 'Tester' order by PayRate ASC, EmpSatisfaction DESC""";
    df_tester = (ps.sqldf(q_tester, locals())).head(int(tester))
    if len(df_tester) < 1:
      f1 = pd.DataFrame()
      return f1
    df3_team1 = pd.concat([df2_team1,df_tester])
  except:
    f1 = pd.DataFrame()
    return f1


  try:
    q_lead = """select * from df_team1 where position == 'Technical Lead' order by PayRate ASC, EmpSatisfaction DESC""";
    df_lead = (ps.sqldf(q_lead, locals())).head(1)
    if len(df_lead) < 1:
      f1 = pd.DataFrame()
      return f1

    final_team1 = pd.concat([df3_team1,df_lead])
  except:
    f1 = pd.DataFrame()
    return f1
  return  final_team1


  #"""select position, * from """

  #print(final_team1)


  #team2





















  final_team1.to_csv(os.getcwd() + '/data/test.csv', index=False)



@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':

    app.run(port=8080)
