# -*- coding: utf-8 -*-

from WindPy import *
import gflags
import pandas as pd
from pandas import DataFrame
import datetime
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

gflags.DEFINE_string("wind_code", "IF.CFE", "wind code")
gflags.DEFINE_string("begin", "2016-09-16", "begin date")
gflags.DEFINE_string("end", "2016-10-24", "end date")
gflags.DEFINE_string("save_dir", ".", "save directory")
gflags.DEFINE_integer("batch", 28, "how many days for one batch, regarding to Wind limitation")

FLAGS = gflags.FLAGS

def get_date_range():
    begin = datetime.datetime.strptime(FLAGS.begin, "%Y-%m-%d")
    end = datetime.datetime.strptime(FLAGS.end, "%Y-%m-%d")
    n = (end - begin).days / FLAGS.batch
    if n == 0:
        return [(begin,end)]

    r = []
    for i in range(n):
        new_begin = begin + datetime.timedelta(days = i * FLAGS.batch)
        new_end = new_begin + datetime.timedelta(days = FLAGS.batch - 1)
        r.append((new_begin, new_end))
    
    if new_end < end:
        r.append((new_end + datetime.timedelta(days = 1), end))

    return r


def get_data(begin, end):
    d = w.wset("futureoi","startdate=%s;enddate=%s;varity=%s;wind_code=all;member_name=all;sorder_by=long" % \
        (begin, end, FLAGS.wind_code))
    df = DataFrame(d.Data).T
    df.columns = d.Fields
    df_filter = df.ix[df["member_name"] == u'\u524d\u4e8c\u5341\u540d\u5408\u8ba1',]    # 前二十名合计
    return df_filter


if __name__ == "__main__":  

    try:
        argv = FLAGS(sys.argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, sys.argv[0], FLAGS)
        sys.exit(1)

    w.start()

    df = DataFrame()  
    for begin, end in get_date_range():
        print "get range:", begin, end
        df = df.append(get_data(begin, end))

    # long_position,long_position_increase,long_potion_rate,short_position,short_position_increase,short_position_rate
    out = df.ix[:,(3,4,5,6,7,8)]
    out.index = [x.strftime('%Y-%m-%d') for x in df.ix[:,0]]
    out.index.name = "date"

    file_name = "_".join(("futureoi", FLAGS.wind_code, FLAGS.begin, FLAGS.end))  + ".csv"
    file_path = os.path.join(FLAGS.save_dir, file_name)
    print "save to file:", file_path
    out.to_csv(file_path)

    w.stop()