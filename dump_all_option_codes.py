# -*- coding: utf-8 -*-

from WindPy import *
import datetime


if __name__ == "__main__":
    
    #today = "2016-07-12"
    today = str(datetime.date.today())

    w.start()    
    d = w.wset("optioncontractbasicinfo","exchange=sse;windcode=510050.SH;status=trading")
    
    file_name = "all_option_codes.txt"
    f = open(file_name, "w")
    for code in d.Data[0]:
        f.write(code + ".SH\n")
    
    f.close()