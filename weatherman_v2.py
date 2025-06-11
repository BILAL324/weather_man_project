# PKT,Max TemperatureC,Mean TemperatureC,Min TemperatureC,Dew PointC,MeanDew PointC,Min DewpointC,Max Humidity, Mean Humidity, Min Humidity, Max Sea Level PressurehPa, Mean Sea Level PressurehPa, Min Sea Level PressurehPa, Max VisibilityKm, Mean VisibilityKm, Min VisibilitykM, Max Wind SpeedKm/h, Mean Wind SpeedKm/h, Max Gust SpeedKm/h,Precipitationmm, CloudCover, Events,WindDirDegrees
# 2014-4-1,18,12,5,2,0,-3,54,33,16,,,,10.0,7.0,4.0,7,1,,0.0,,,-1

# {'PKT': '2004-8-1', 'Max TemperatureC': '23', 'Mean TemperatureC': '', 'Min TemperatureC': '22', 'Dew PointC': '18', 'MeanDew PointC': '18', 'Min DewpointC': '18', 'Max Humidity': '68', ' Mean Humidity': '68', ' Min Humidity': '68', ' Max Sea Level PressurehPa': '', ' Mean Sea Level PressurehPa': '', ' Min Sea Level PressurehPa': '', ' Max VisibilityKm': '10.0', ' Mean VisibilityKm': '10.0', ' Min VisibilitykM': '10.0', ' Max Wind SpeedKm/h': '6', ' Mean Wind SpeedKm/h': '6', ' Max Gust SpeedKm/h': '', 'Precipitationmm': '0.0', ' CloudCover': '', ' Events': '', 'WindDirDegrees': '-1'},

import sys
import glob
import os
import datetime


folder_path = sys.argv[1]
choice_tag =sys.argv[2]
report_year = sys.argv[3]


# 3 functions for 3 operations in Module 1 of the Task
def max_temp (weather_files , highest_temp, high_date_time_string):

    for i in weather_files:
        with open(i, 'r') as file:
            header = file.readline().strip().split(',')
            max = header[1]

            data = []

            for lines in file:
                values = lines.strip().split(',')

                row = {}
                for i , column in enumerate(header):
                    if i < len(values):
                        row[column] = values[i]
                        
                data.append(row)

            for i in range(len(data)):
                try:       
                    var = float(data[i]['Max TemperatureC'])
                    if var >= highest_temp:
                        highest_temp = var
                        high_date_time_string = data[i]['PKT']
                    else:
                        continue
                except ValueError:
                    continue

    return highest_temp, high_date_time_string


def min_temp (weather_files ,lowest_temp, low_date_time_string  ):

    for i in weather_files:
        with open(i, 'r') as file:
            header = file.readline().strip().split(',')
            max = header[1]

            data = []

            for lines in file:
                values = lines.strip().split(',')

                row = {}
                for i , column in enumerate(header):
                    if i < len(values):
                        row[column] = values[i]
                        
                data.append(row)

            for i in range(len(data)):
                try:       
                    var = float(data[i]['Max TemperatureC'])
                    if var <= lowest_temp:
                        lowest_temp = var
                        low_date_time_string = data[i]['PKT']
                    else:
                        continue
                except ValueError:
                    continue

    return lowest_temp, low_date_time_string


def max_hunidity (weather_files, humidity ,humidity_date_time_string ):

    for i in weather_files:
        with open(i, 'r') as file:
            header = file.readline().strip().split(',')

            data = []

            for lines in file:
                values = lines.strip().split(',')

                row = {}
                for i , column in enumerate(header):
                    if i < len(values):
                        row[column] = values[i]
                        
                data.append(row)

            for i in range(len(data)):
                try:       
                    var = float(data[i]['Max Humidity'])
                    if var >= humidity:
                        humidity = var
                        humidity_date_time_string = data[i]['PKT']
                    else:
                        continue
                except ValueError:
                    continue
            
    max_humidity = f"{humidity}%"

    return max_humidity, humidity_date_time_string


def parsing_date (strings):
    if not strings:
        return "N/A"
    parse_obj = datetime.datetime.strptime(strings,'%Y-%m-%d')
    parse_date = parse_obj.strftime('%B %d')
    
    return parse_date


# Only one funtion for 2nd Module
def avg_temp (complete_file_name, avg_high_temp, avg_low_temp, avg_humidity):

    with open(complete_file_name, 'r') as file:
        header = file.readline().strip().split(',')

        data = []

        for line in file:
            values = line.strip().split(',')
            #we creatd the list of values of only 1 line now convert into dict with headers keys
            row = {}

            for i, column in enumerate(header):
                if i < len(values):
                    row[column]= values[i]
                    
            data.append(row)

        #Average Maximum Temperature
        count = 0
        total = 0

        for i in data:
            temp = i['Max TemperatureC']
            if temp == "":
                continue
            else:
                temp = int(temp)
                count+=1
                total += temp 
            
        avg_high_temp = total/count

        #Average Minimum Temperature        
        count = 0
        total = 0

        for i in data:
            temp = i['Min TemperatureC']
            if temp == "":
                continue
            else:
                temp = int(temp)
                count+=1
                total += temp 
            
        avg_low_temp = total/count

        #Average Mean Humidity        
        count = 0
        total = 0

        for i in data:
            temp = i[' Mean Humidity']
            if temp == "":
                continue
            else:
                temp = int(temp)
                count+=1
                total += temp 
            
        avg_humidity = total/count

    return avg_high_temp, avg_low_temp, avg_humidity


if choice_tag =='-e':

    # Yearly Summary Report
    weather_files_pattern = os.path.join(folder_path, f"Murree_weather_{report_year}_*.txt")
    weather_files = glob.glob(weather_files_pattern)

    highest_temp = -1000
    lowest_temp = 1000
    humidity = -1000

    low_date_time_string= ''
    high_date_time_string= ''
    humidity_date_time_string= ''

    highest , high_date_time_string= max_temp(weather_files, highest_temp, high_date_time_string)
    lowest, low_date_time_string = min_temp(weather_files, lowest_temp , low_date_time_string)
    max_humidity, humidity_date_time_string = max_hunidity(weather_files, humidity , humidity_date_time_string)

    high_date_time_string = parsing_date(high_date_time_string)
    low_date_time_string = parsing_date(low_date_time_string)
    humidity_date_time_string = parsing_date(humidity_date_time_string)


    print(f'Highest: {highest}°C on {high_date_time_string} \nLowest: {lowest}°C on {low_date_time_string} \nHumidity: \
{max_humidity} on {humidity_date_time_string}' )


elif choice_tag == '-a':

    # Monthly Averages Report
    year_month_list = report_year.strip().split('/')
    year_month_parse = datetime.datetime(int(year_month_list[0]), int (year_month_list[1]), 1 )
    partial_file_name = year_month_parse.strftime("%Y_%b")
    complete_file_name = os.path.join(folder_path, f"Murree_weather_{partial_file_name}.txt")

    avg_high_temp = -1000
    avg_low_temp = 1000
    avg_humidity = -1000


    avg_high_temp, avg_low_temp, avg_humidity = avg_temp(complete_file_name, avg_high_temp, avg_low_temp, avg_humidity)
    print(f'Highest Average: {avg_high_temp:.2f}°C \nLowest Average: {avg_low_temp:.2f}°C \nAverage Mean Humidity: {avg_humidity:.2f}% ' )


elif choice_tag == '-c':
    print("Choice tag -c is in Progress")


else:
    print("Please check your tag or Command")
