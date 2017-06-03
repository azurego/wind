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

import pandas as pd
from pandas import DataFrame

import WindCode

gflags.DEFINE_string("begin", None, "from date")
gflags.DEFINE_string("end", None, "to date")
gflags.DEFINE_string("save_dir", ".", "save directory")

#gflags.DEFINE_string("begin", "2016-04-28", "from date")
#gflags.DEFINE_string("end", "2016-05-05", "to date")

FLAGS = gflags.FLAGS

def dump_k(code):  
    
    begin_time = FLAGS.begin + " 09:00:00"
    end_time= FLAGS.end + " 15:00:00"    
    
    fields = ("open","high","low","close","volume","amt")    
    
    r = w.wsi(code, ",".join(fields), begin_time, end_time, "PriceAdj=F")
    if r.ErrorCode != 0:
        print "w.wsi() ErrorCode:", r.ErrorCode
        sys.exit(1)
            
    df = DataFrame(r.Data).T
    #df.index = pd.to_datetime(r.Times)
    df.index = [x.strftime('%Y-%m-%d %H:%M:%S') for x in r.Times]
    df.index.name = "time"
    df.columns = fields

    file_name = "_".join(("kbar", code, FLAGS.begin, FLAGS.end))  + ".csv"
    file_path = os.path.join(FLAGS.save_dir, file_name)
    print "save k bar to", file_path        
    df.to_csv(file_path)


if __name__ == "__main__":    
    
    try:
        argv = FLAGS(sys.argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, sys.argv[0], FLAGS)
        sys.exit(1)
    
    if not os.path.exists(FLAGS.save_dir):
        print "path not exist:", FLAGS.save_dir
        sys.exit(1)

    r = w.start()    
    if r.ErrorCode != 0:
        print "w.start() ErrorCode:", r.ErrorCode
        sys.exit(1)    
     
    for code in WindCode.get_codes():
        dump_k(code)  
    
    w.stop()