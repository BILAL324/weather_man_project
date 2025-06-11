import sys
import glob
import os
import datetime

folder_path = sys.argv[1]
args = sys.argv[2:]

# here we are saving tupples of each pair with tag and year_month argument as list
tag_month_pairs = []
i = 0
while i < len(args):
    if args[i].startswith('-'):
        if i + 1 < len(args) and not args[i+1].startswith('-'):
            tag_month_pairs.append((args[i], args[i+1]))
            i += 2
        else:
            print(f"Missing date for tag {args[i]}")

            sys.exit(1)
    else:
        i += 1

if not tag_month_pairs:
    print("Please provide at least one report tag (-e, -a, -c) with its date.")
    sys.exit(1)


# 3 functions for 3 operations in Module 1 of the Task
# Max temprature and its date from all months of seperate reports in the year
def max_temp (weather_files , highest_temp, high_date_time_string):

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
                    var = float(data[i]['Max TemperatureC'])
                    if var >= highest_temp:
                        highest_temp = var
                        high_date_time_string = data[i]['PKT']
                    else:
                        continue
                except ValueError:
                    continue

    return highest_temp, high_date_time_string


# Min temprature and its date from all months of seperate reports in the year
def min_temp (weather_files ,lowest_temp, low_date_time_string  ):

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
                    var = float(data[i]['Max TemperatureC'])
                    if var <= lowest_temp:
                        lowest_temp = var
                        low_date_time_string = data[i]['PKT']
                    else:
                        continue
                except ValueError:
                    continue

    return lowest_temp, low_date_time_string


# Max humidity and its date from all months of seperate reports in the year
def max_hunidity (weather_files, humidity, humidity_date_time_string ):

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


#converting date into datetime object using strptime and then formate it using strftime as we want
def parsing_date (strings):
    parse_obj = datetime.datetime.strptime(strings,'%Y-%m-%d')
    parse_date = parse_obj.strftime('%B %d')
    
    return parse_date


# Only one funtion for 2nd Module
#Here we calculate average min, max temp and average humidity using 1 funtion
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


# 3rd Module (Min Max Temp)
# min and max temp in a specific month
def min_max_temp(complete_file_name, highest_temp, lowest_temp):

    with open(complete_file_name, 'r') as file:
        header = file.readline().strip().split(',')

        data = []

        for line in file:
            values = line.strip().split(',')
            # we created the list of values of only 1 line now convert into dict with headers keys
            row = {}

            for i, column in enumerate(header):
                if i < len(values):
                    row[column] = values[i]

            data.append(row)

        # Maximum Temperature
        temp = -1000
        for row in data:
            temp_str = row.get('Max TemperatureC', '')
            if temp_str == "":
                continue
            try:
                temp_val = int(temp_str)
                if temp_val > temp:
                    temp = temp_val
            except ValueError:
                continue

        highest_temp = temp

        # Minimum Temperature
        temp = 1000
        for row in data:
            temp_str = row.get('Min TemperatureC', '')
            if temp_str == "":
                continue
            try:
                temp_val = int(temp_str)
                if temp_val < temp:
                    temp = temp_val
            except ValueError:
                continue

        lowest_temp = temp

    return highest_temp, lowest_temp

# loop over all tags so generate reports
for choice_tag, report_year in tag_month_pairs:
    if choice_tag == '-e':

        # Yearly Summary Report
        weather_files_pattern = os.path.join(folder_path, f"Murree_weather_{report_year}_*.txt")
        weather_files = glob.glob(weather_files_pattern)

        #default global variables to use or detected whether the values are updated or valid as well or not
        highest_temp = -1000
        lowest_temp = 1000
        humidity = -1000

        #default global strings
        low_date_time_string= ''
        high_date_time_string= ''
        humidity_date_time_string= ''

        highest , high_date_time_string= max_temp(weather_files, highest_temp, high_date_time_string)
        lowest, low_date_time_string = min_temp(weather_files, lowest_temp , low_date_time_string)
        max_humidity, humidity_date_time_string = max_hunidity(weather_files, humidity , humidity_date_time_string)

        high_date_time_string = parsing_date(high_date_time_string)
        low_date_time_string = parsing_date(low_date_time_string)
        humidity_date_time_string = parsing_date(humidity_date_time_string)

        print(f'\nHighest: {highest}°C on {high_date_time_string} \nLowest: {lowest}°C on {low_date_time_string} \nHumidity: {max_humidity} on {humidity_date_time_string}' )
        print("\n")


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
        print(f'\nHighest Average: {avg_high_temp:.2f}°C \nLowest Average: {avg_low_temp:.2f}°C \nAverage Mean Humidity: {avg_humidity:.2f}% ' )


    elif choice_tag == '-c':

        #Daily Temperature Chart (Bars)
        year_month_list = report_year.strip().split('/')
        year_month_parse = datetime.datetime(int(year_month_list[0]), int (year_month_list[1]), 1 )
        partial_file_name = year_month_parse.strftime("%Y_%b")
        complete_file_name = os.path.join(folder_path, f"Murree_weather_{partial_file_name}.txt")

        highest_temp = -1000
        lowest_temp = 1000

        highest_temp, lowest_temp = min_max_temp(complete_file_name, highest_temp, lowest_temp)

        # colors to change color in terminal (ANSI Escape (\033))
        RED = '\033[31m'
        BLUE = '\033[34m'
        RESET = '\033[0m' 
        print(f'\n{partial_file_name}')
        print(f"{RED}{'+' * highest_temp} {highest_temp}°C{RESET}")
        print(f"{BLUE}{'+' * lowest_temp} {lowest_temp}°C {RESET}")

    elif choice_tag == '-b':

        #Combined Daily Bar Chart
        year_month_list = report_year.strip().split('/')
        year_month_parse = datetime.datetime(int(year_month_list[0]), int (year_month_list[1]), 1 )
        partial_file_name = year_month_parse.strftime("%Y_%b")
        complete_file_name = os.path.join(folder_path, f"Murree_weather_{partial_file_name}.txt")

        highest_temp = -1000
        lowest_temp = 1000

        highest_temp, lowest_temp = min_max_temp(complete_file_name, highest_temp, lowest_temp)

        print(f'\n{partial_file_name}')
        print(f"{'+' * highest_temp}{'+' * lowest_temp} {lowest_temp}°C -- {highest_temp}°C")

if __name__ == "__main__":
    print("Weather report generation completed successfully.")

