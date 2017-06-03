# -*- coding: utf-8 -*-
"""
Created on Wed May 04 14:01:37 2016

@author: azure
"""

from WindPy import *
import sys
import os
import gflags
import datetime

gflags.DEFINE_string("begin", None, "from date")
gflags.DEFINE_string("end", None, "to date")
gflags.DEFINE_string("code_list", "150153.SZ,150201.SZ", "code list")
gflags.DEFINE_string("code_file", None, "code file having code list")
gflags.DEFINE_string("save_dir", ".", "save directory")

#gflags.DEFINE_string("begin", "2016-04-28", "from date")
#gflags.DEFINE_string("end", "2016-05-05", "to date")

FLAGS = gflags.FLAGS

def get_codes():
    codes = None;
    #configuration code_file priors to code_list
    if FLAGS.code_file:
        if os.path.isfile(FLAGS.code_file):
            codes = get_codes_from_file(FLAGS.code_file)
        else:
            print "FLAGS.code_file not exist!"
            sys.exit(1)
    else:
        codes = FLAGS.code_list.split(",")        
    
    return codes

def get_codes_from_file(file):
    codes = []
    f = open(file)
    for line in f.readlines():
        code = line.strip()
        if not code == "" and not code.startswith("#"):            
            codes.append(code)    
    return codes
    
# date is datetime type
def record_one_day(date, codes):  
    date_str = date.strftime("%Y-%m-%d")
    begin_time = date_str + " 09:00:00"
    end_time= date_str + " 15:00:00"    
    
    fields = "last,ask,bid,volume,amt,ask1,ask2,ask3,ask4,ask5,ask6,ask7,ask8,ask9,ask10,bid1,bid2,bid3,bid4,bid5,bid6,bid7,bid8,bid9,bid10,"
    fields += "asize1,asize2,asize3,asize4,asize5,asize6,asize7,asize8,asize9,asize10,bsize1,bsize2,bsize3,bsize4,bsize5,bsize6,bsize7,bsize8,bsize9,bsize10"
    field_len = len(fields.split(","))

    for code in codes:
        r = w.wst(code, fields, begin_time, end_time)
        if r.ErrorCode != 0:
            print "w.wst() ErrorCode:", r.ErrorCode
            continue
            
        file_name = code + "_" + date_str + ".csv"
        title = "code,time," + fields + "\n"
        file_path = os.path.join(FLAGS.save_dir, file_name)
        print "save tick to", file_path        
        
        f = open(file_path, "w")    
        f.write(title)
       
        for i in range(len(r.Times)):            
            f.write(code + ",")
            f.write(str(r.Times[i]) + ",")
            for field in range(field_len):
                f.write(str(r.Data[field][i]) + ",")
            f.write("\n")          
        
        f.close()


if __name__ == "__main__":    
    
    try:
        argv = FLAGS(sys.argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, sys.argv[0], FLAGS)
        sys.exit(1)
    
    if not os.path.exists(FLAGS.save_dir):
        print "path not exist:", FLAGS.save_dir
        sys.exit(1)
        
    codes = get_codes()
    today_datetime = datetime.datetime.now()
    
    begin = FLAGS.begin
    if begin is None:
        begin_datetime = today_datetime
    else:
        begin_datetime = datetime.datetime.strptime(begin, "%Y-%m-%d")
        
    end = FLAGS.end
    if end is None:
        end_datetime = today_datetime
    else:
        end_datetime = datetime.datetime.strptime(end, "%Y-%m-%d")
        
    r = w.start()    
    if r.ErrorCode != 0:
        print "w.start() ErrorCode:", r.ErrorCode
        sys.exit(1)
    
    r = w.tdays(begin_datetime, end_datetime)
    if r.ErrorCode != 0:
        print "w.tdays() ErrorCode:", r.ErrorCode
        sys.exit(1)
     
    #n = end_datetime - begin_datetime
    #datetime_list = [begin_datetime + datetime.timedelta(i) for i in range(n.days + 1)]
    datetime_list = r.Times    
    for date in datetime_list:
        print "\nrecord date:", date
        record_one_day(date, codes)  
    
    w.stop()