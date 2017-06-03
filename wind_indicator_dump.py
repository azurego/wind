# -*- coding: utf-8 -*-
"""
    Wind不能一批取出过多数据
"""

from WindPy import *

import csv
import sys
import WindCode
import IPODate
import gflags

gflags.DEFINE_string("begin", "2011-01-01", "from date")
gflags.DEFINE_string("end", "2011-12-31", "to date")
gflags.DEFINE_string("indicator", "mf_amt_ratio", "Wind indicator name")
gflags.DEFINE_string("period", "D", "[D|W|M]")
gflags.DEFINE_string("priceAdj", None, "[N|F|B]")
gflags.DEFINE_boolean("code_from_wind", True, "get codes on the begin date from Wind")
gflags.DEFINE_boolean("file_year_by_year", True, "True: dump file year by year, False: one file for all")
gflags.DEFINE_boolean("code_year_by_year", True, "True: code from Wind each year, False: beginning code from all years")
gflags.DEFINE_integer("after_ipo_days", 0, "at least IPO days, no care if 0")

FLAGS = gflags.FLAGS

def get_range(begin, end):
    result = []     
    if FLAGS.file_year_by_year:    
        year_begin = int(begin.split("-")[0])
        year_end = int(end.split("-")[0])
        if year_begin == year_end:
            result.append((begin, end))
        else:
            result.append((begin, str(year_begin) + "-12-31"))    
            for year in range(year_begin + 1, year_end):                
                result.append((str(year) + "-01-01", str(year) + "-12-31"))
            result.append((str(year_end) + "-01-01", end))
    else:
        result.append((begin, end))

    return result 
        
def dump_range(codes, begin, end, indicator):
    option = "Period=" + FLAGS.period
    if FLAGS.priceAdj == "F" or FLAGS.priceAdj == "B":
        option += ";PriceAdj=" + FLAGS.priceAdj 

    d = w.wsd(codes, indicator, begin, end, option)      
    #print d
    if d.ErrorCode != 0:
        print "Wind Error:\n", d        
        sys.exit(1)    
    
    file_name = "_".join([d.Fields[0], begin, end, FLAGS.period, codes[0], str(len(codes))]) + ".csv"
    try:
        csv_file = file(file_name, "wb")
    except IOError, e:
        print "exception:", e
        sys.exit(2)

    csv_writer = csv.writer(csv_file)
    d.Codes.insert(0, "date")
    csv_writer.writerow(d.Codes)
    for i in range(len(d.Times)):
        row = [d.Times[i].strftime("%Y-%m-%d")]
        for j in range(len(d.Data)):
            row.append(d.Data[j][i])
        csv_writer.writerow(row)
    
    print len(codes), "code(s) in", file_name    
    csv_file.close()       

def dump(codes):

    for (begin, end) in get_range(FLAGS.begin, FLAGS.end):
        if FLAGS.code_from_wind and FLAGS.code_year_by_year:
            codes = WindCode.get_codes_from_wind(begin)
            if FLAGS.after_ipo_days > 0:
                codes = IPODate.after_ipo_days(codes, begin, FLAGS.after_ipo_days)

        for indicator in FLAGS.indicator.split(","):
            print "\ndumping indicator [", indicator, "] for", str(len(codes)), "code(s) in range", (begin, end)    
            dump_range(codes, begin, end, indicator)   

def ipo_days_filter(codes):
    if FLAGS.at_least_ipo_days == 0:
        return codes

    ipo_dict = IPODate.get_ipo_date()


if __name__ == "__main__":

    try:
        argv = FLAGS(sys.argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, sys.argv[0], FLAGS)
        sys.exit(1)
        
    print "start Wind ......"
    w.start()   
    print "Wind started"
    
    if FLAGS.code_from_wind:
        print "code from wind"
        codes = WindCode.get_codes_from_wind(FLAGS.begin)
    else:
        print "code from config"
        codes = WindCode.get_codes()

    dump(codes)       
    
    w.stop()
    print "bye"