import csv
import re
from pathlib import Path
import time

# A data collection tool to analyze error history csv files to combine them into one document and update it continuously
# see constructor for details of params needed.
# use the function run() to start the program.

class Err_parse:
    month_dict={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    
    #interval is in seconds
    #@params directory filename to store the files in. 
    #The directory filename to open to find the data. 
    #The interval in seconds to poll the data.
    def __init__(self, store_dir, open_dir, interval, u, p):
        self.sto_dir = store_dir
        self.inter = interval
        self.op_dir = open_dir
        self.user = u
        self.pswd = p
        self.p_month = 0
        self.p_day = 0
        self.p_time = 0

    #ok
    #load the data
    def load(self, file_name):
        data = []
        with open(file_name) as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            data = list(data)
        data = data[2:]
        return data
    
    #ok
    #destructivly merges the content row of the log so that the contents are all in one line.
    def merge_content(self, data):
        for row in data:
            row[5] = row[5].strip()
            if row[0] != '':
                master = row
            else:
                master[5] += ' ' + row[5]
        #get rid of excess
        rv = []
        for row in data:
            if row[0] != '':
                rv.append(row)
        return rv
    
    #ok
    #returns index to start getting new data
    def start(self, data):
        for i in range(len(data)):
            row = data[i]
            first = row[0].split('.')
            month = err_parser.month_dict[first[0]]
            day = int(first[1])
            time = int(re.sub(':', '', row[1]))
            if self.p_month < month and self.p_day < day and self.p_time < time:
                return i
        print("No new entries")
        return 100


    #TODO: change this so that it writes to sql server
    #writes data to csv
    def write_database(self, data, , option):
                
        
        
        f = None
        my_file = Path(loc_name)
        if my_file.is_file():
            f = open(loc_name, option)
        else:
            f = open(loc_name, 'w')
            f.write('Error History\n')
            f.write('Date, Time, Position, Level, Code, Content\n')
        for row in data:
            msg = row[0] + ', ' + row[1] + ', ' + row[2] + ', ' + row[3] + ', ' + row[4] + ', ' + row[5] + '\n'
            f.write(msg)
        f.close()

    # TODO: may be deprecated?
    #stores latest 100 lines of data
    def cache(self, data):
        self.write(data, 'cache.csv', 'w')

    #udates the latest time that was read
    def update_p(self, data):
        p_row = data[len(data) - 1]
        last = p_row[0].split('.')
        self.p_month = err_parser.month_dict[last[0]]
        self.p_day = int(last[1])
        self.p_time = int(re.sub(':', '', p_row[1]))

    #runs all of the above functions. Run this to start the program.
    def run(self):
        while True:
            data = self.load(self.op_dir)
            data = self.merge_content(data)
            self.cache(data)
            start_index = self.start(data)
            self.update_p(data)
            data = data[start_index:]
            self.write(data, self.sto_dir, 'a')
            data = []
            time.sleep(self.inter)
