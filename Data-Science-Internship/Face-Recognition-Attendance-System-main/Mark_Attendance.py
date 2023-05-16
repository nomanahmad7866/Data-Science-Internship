
######## Importing Libraries######################
import pandas as pd
import datetime
import csv
import time
ts = time.time()
import os

date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%I:%M:%S:%p")

#==============================Function to Find Time Duration============================================#

def is_time_between(begin_time, end_time, check_time):
    """
     #print(help(time_in_range)) to print description of function on run time

    :param begin_time: starting office time of JMM
    :param end_time: starting office time of JMM
    :param check_time: leaving office time of JMM
    :return: Return true if x is in the range [start, end]
    """
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

#JMM Office in Time range
begin_time_1 ="09:00:00:AM"
end_time_1 = "05:59:00:PM"

#JMM Office Out time range
begin_time_2 ="06:00:00:PM"
end_time_2 = "08:00:00:PM"


range_in = is_time_between(begin_time_1, end_time_1 , current_time)
range_out = is_time_between(begin_time_2, end_time_2 , current_time)

print("range in time status now is :",range_in)
print("range out time right now is: ",range_out)



def Mark_attendance_here( id, name):
    """

    :param id: individual ID assigned to each employee
    :param name: name of employee
    """

    col_names = ['Id' , 'Name'  , 'Time_In',  'Time_Out']
    exists = os.path.isfile("Attendance_Report/Attendance_Report_" + date + ".csv")

    #if time in value is true
    if range_in:
        #checking csv attendance file of current date is exist or not
        if exists:
            bool_1 = False
            #print("range in ", range_in)
            #print("file exist if not go in else:" , exists)
            col_list = ["Id", "Name", "Time_In", "Time_Out"]
            df = pd.read_csv("Attendance_Report/Attendance_Report_" + date + ".csv", usecols=col_list)
            for i_d in df['Id']:
                if i_d == id:
                    print("id found ")
                    print(f"Attendance of Id: {id} marked in already ")
                    bool_1 = True
                    print("now bool update", bool_1)
                else:
                    ""

            #if attendance not marked already in
            if bool_1 == False:
                with open("Attendance_Report/Attendance_Report_" + date + ".csv", 'a+') as file:
                    print("saving attendance of in time....")
                    attendance_in = ["\n", str(id) + " ,", name + " ," ,  str(timeStamp) + " ,", " "]
                    file.writelines(attendance_in )
                    print("Attendance in saved successfully..")


        #if attendance file not exist
        else:
            print("i am in else because file not exist")
            with open("Attendance_Report/Attendance_Report_" + date + ".csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                print("writing columns if not exist..")
                col_names = ['Id', 'Name', 'Time_In', 'Time_Out']
                writer.writerow(col_names)
            #Marking attendance
            col_list = ["Id", "Name", "Time_In", "Time_Out"]
            df = pd.read_csv("Attendance_Report/Attendance_Report_" + date + ".csv", usecols=col_list)
            bool_2 = False
            for i_d in df['Id']:
                if i_d == id:
                    print("id found")
                    print(f"Attendance of Id: {id} marked already in ")
                    bool_2 = True
                else:
                    ""
            print("bool 2 values is", bool_2)
            if bool_2 == False:
                with open("Attendance_Report/Attendance_Report_" + date + ".csv", 'a+') as file:
                    print("writing attendance in if not exist..")
                    attendance_in = ["\n", str(id) + " ,", name + " ," ,  str(timeStamp) + " ,", " "]
                    file.writelines(attendance_in)

    # if time out is true than marking out time attendance here
    elif range_out:
        col_names = ['Id' , 'Name'  , 'Time_In',  'Time_Out']
        exists = os.path.isfile("Attendance_Report/Attendance_Report_" + date + ".csv")
        if exists:
            print("range out check..", range_out)
            col_list = ["Id", "Name", "Time_In", "Time_Out"]
            df = pd.read_csv("Attendance_Report/Attendance_Report_" + date + ".csv", usecols=col_list)
            bool_2 = False
            for i_d in df['Id']:
                if i_d == id:
                    bool_2 = True
                    print(f"Marking out attendance of id : {id}  ")
                    col_list = ["Id", "Name", "Time_In", "Time_Out"]
                    with open("Attendance_Report/Attendance_Report_" + date + ".csv", 'a+') as file:
                        print("writing attendance of out time..")
                        attendance_in = [ str(timeStamp)]
                        print("writing time out..")
                        file.writelines(attendance_in)
                        writer = csv.writer(file)
                        break
                else:
                    print("out time marked already")

    ############################################################################################

"""Testing Attendance here with Dummy id, and name"""

# id = 21
# name = "Nomi Smart"
#
# Mark_attendance_here( id, name)

