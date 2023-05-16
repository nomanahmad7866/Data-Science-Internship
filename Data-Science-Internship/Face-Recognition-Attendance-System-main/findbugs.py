import datetime
import csv
import shutil

import time
ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

id = 22



import pandas as pd
import numpy as np

df = pd.read_csv("Attendance_Report/Attendance_Report_" + date + ".csv")

df["Id"]=df["Id"].apply(str)
# print(df)
# df.info(
#print(df.head())

for i in df.iterrows():
    if id in i.items():
        print(i)

  # # if i[3]["Id"]=="54":
  #   #print(i)
  #   i[1]["Time_Out"]="djangoo baba"
  #   print(i)


# with open("Attendance_Report/Attendance_Report_" + date + ".csv", 'a+') as csvFile1:
#     writer = csv.writer(csvFile1)
#     #print("writing columns if not exist..")
#     #col_names = ['Id', 'Name', 'Time_In', 'Time_Out']
#     #writer.writerow(col_names)
#     # Marking attendance
# col_list = ["Id", "Name", "Time_In", "Time_Out"]
# df = pd.read_csv("Attendance_Report/Attendance_Report_" + date + ".csv", usecols=col_list)
# bool_2 = False
# for i_d in df['Id']:
#     if i_d == id:
#         print(i_d)
#
#     else:
#          ""





