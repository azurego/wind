# -*- coding: utf-8 -*-
"""
Created on Wed May 04 14:01:37 2016

@author: azure
"""

import csv
import datetime
import gflags

gflags.DEFINE_string("ipo_date_file", "ipo_date.csv", "ipo data file")

FLAGS = gflags.FLAGS


def get_ipo_date():
    d = {}
    reader = csv.reader(file(FLAGS.ipo_date_file, "rb"))
    for row in reader:
        d[row[0]] = row[-1]
    return d

def str2datetime(str):
    date_time = datetime.datetime.strptime(str,'%Y-%m-%d')
    return date_time

def after_ipo_days(codes, date_now, n):
    """date_now is string format '%Y-%m-%d'"""
    ipo_dict = get_ipo_date()
    #print ipo_dict
    result = []
    for code in codes:
        if code not in ipo_dict:
            print "warning:", code, "not in", FLAGS.ipo_date_file
            continue

        datetime_now = str2datetime(date_now)
        datetime_ipo = str2datetime(ipo_dict[code])
        if (datetime_now - datetime_ipo).days > n:
            result.append(code)

    return result


if __name__ == "__main__":    
    
    print get_ipo_date()