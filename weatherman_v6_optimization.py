import os
import argparse
import datetime
import csv

#Get all files of specfic year
def get_weather_files(folder, year):
    all_files = []
    for filename in os.listdir(folder):
        if f"Murree_weather_{year}_" in filename and filename.endswith('.txt'):
            full_file_path = os.path.join(folder, filename)
            all_files.append(full_file_path)
    
    return all_files

#parsing date to specific format
def parse_date(date_str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')

    return date.strftime('%B %d')

#read CSV files
def read_csv(filepath):
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)

        return [row for row in reader]
    
#get max , min values for temp in all files, and Humidity values
def get_extreme_value(all_files, column, compare, default):
    value = default
    date_string = ''
    for file in all_files:
        for row in read_csv(file):
            try:
                current = float(row[column])
                if compare(current, value):
                    value = current
                    date_string = row.get('PKT')
                    if date_string == "":
                        continue
                    else:
                        date_string = date_string
            except (ValueError, KeyError):
                continue

    return value, parse_date(date_string)

# compute the average temperatures and humidity
def compute_averages(file):
    rows = read_csv(file)
    def avg(column):
        vals = [int(row[column]) for row in rows if row.get(column, '').isdigit()]
        return sum(vals) / len(vals)
    
    return avg('Max TemperatureC'), avg('Min TemperatureC'), avg(' Mean Humidity')

# min and max temp in a specific file
def get_month_min_max(file):
    rows = read_csv(file)
    max_temp = max((int(row['Max TemperatureC']) for row in rows if row.get('Max TemperatureC', '').isdigit()), default=-1000)
    min_temp = min((int(row['Min TemperatureC']) for row in rows if row.get('Min TemperatureC', '').isdigit()), default=1000)

    return max_temp, min_temp

#bar chart funtion for representing temp with colors and + sign
def print_bar_chart(high, low, label='', combine=False):
    RED =  '\033[31m'
    BLUE = '\033[34m'
    RESET = '\033[0m'
    print(f'\n{label}')
    if combine:
        print(f"{'+' * low}{'+' * high} {low}°C -- {high}°C")
    else:
        print(f"{RED}{'+' * high} {high}°C{RESET}")
        print(f"{BLUE}{'+' * low} {low}°C{RESET}")

#function to parse arguments from the CLI
def parse_args():
    parser = argparse.ArgumentParser(description='Weather Report Input Arguments')
    parser.add_argument('folder', help='folder containing weather files')
    parser.add_argument('-e', '--extreme', help='Extreme weather report for year ')
    parser.add_argument('-a', '--average', help='Monthly average report ')
    parser.add_argument('-c', '--chart', help='Bar chart for a month ')
    parser.add_argument('-b', '--barchart', help='Combined high/low bar chart ')

    return parser.parse_args()


def main():
    args = parse_args()

# for yearly reports from multiple files
    if args.extreme:
        files = get_weather_files(args.folder, args.extreme)

        high, high_date = get_extreme_value(files, 'Max TemperatureC', lambda x, y: x > y, -1000)
        low, low_date = get_extreme_value(files, 'Max TemperatureC', lambda x, y: x < y, 1000)
        hum, hum_date = get_extreme_value(files, 'Max Humidity', lambda x, y: x > y, -1000)

        print(f"\nHighest: {high}°C on {high_date}")
        print(f"Lowest: {low}°C on {low_date}")
        print(f"Humidity: {hum}% on {hum_date}")

# for monthly reports form single files 
    for choice_tag, value in {
        'average': args.average,
        'chart': args.chart,
        'barchart': args.barchart
    }.items():
        if not value:
            continue

        try:
            year, month = map(int, value.split('/'))
            file_name = datetime.datetime(year, month, 1).strftime('Murree_weather_%Y_%b.txt')
            file_path = os.path.join(args.folder, file_name)

            if choice_tag == 'average':
                high_avg, low_avg, hum_avg = compute_averages(file_path)
                print(f"\nHighest Avg: {high_avg:.2f}°C\nLowest Avg: {low_avg:.2f}°C\nAvg Humidity: {hum_avg:.2f}%")

            elif choice_tag == 'chart':
                high, low = get_month_min_max(file_path)
                print_bar_chart(high, low, label=file_name)

            elif choice_tag == 'barchart':
                high, low = get_month_min_max(file_path)
                print_bar_chart(high, low, label=file_name, combine=True)

        except Exception as e:
            print(f"Error parsing input {value}: {e}")

if __name__ == '__main__':
    main()
