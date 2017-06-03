# -*- coding: utf-8 -*-

from WindPy import *
import datetime


if __name__ == "__main__":
    
    #today = "2016-07-12"
    today = str(datetime.date.today())

    w.start()    
    d = w.wset("SectorConstituent","date=" + today + ";sectorId=a001010100000000;field=wind_code")
    
    file_name = "all_stock_codes.txt"
    f = open(file_name, "w")
    for code in d.Data[0]:
        f.write(code + "\n")
    
    f.close()