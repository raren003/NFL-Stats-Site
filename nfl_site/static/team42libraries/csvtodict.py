import re
import pandas as pd


def csv_to_dict(file_name, ret_df = 0):
    # regex to get data from each line of the csv file
    row_regex = re.compile(r'(?:,|\n|^)("(?:(?:"")*[^"]*)*"|[^",\n]*|(?:\n|$))')

    csv_dict = {}  # dictionary to contain all the columns of a csv file
    misses = 0  # count how many records in a file where not extractable

    with open(file_name) as f:

        line = f.readline()  # read in fist line that should contain csv headers

        # get the headers of the csv file from first line using regex
        csv_headers = row_regex.findall(line.strip())

        lines = f.readlines()  # get all lines after the header line in the csv

    # create dictionary of arrays with csv headers (column names) as keys
    for header in csv_headers:
        csv_dict[header] = []

    # loop through each line extracted from the csv and get data
    for line in lines:
        counter = 0  # counter to cycle through values extracted from a line
        temp_list = row_regex.findall(line.strip())  # grab all values for a line

        # in the number of values extracted from the line is equal to the number of csv headers (columns)
        # data is valid and can be added to csv dictionary
        if len(csv_headers) == len(temp_list):
            for header in csv_headers:
                # if the value in a field was not empty add it to proper column else insert None
                if temp_list[counter]:
                    csv_dict[header].append(temp_list[counter])
                else:
                    csv_dict[header].append(None)
                counter += 1
        else:
            # increment counter to indicate that a line could not be added to csv dictionary
            misses += 1

    print('missed rows (' + file_name + '): ', misses)

    if ret_df:
        return pd.DataFrame(csv_dict)
    return csv_dict
