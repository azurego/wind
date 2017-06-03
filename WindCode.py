# -*- coding: utf-8 -*-
"""
Created on Wed May 04 14:01:37 2016

@author: azure
"""

import WindPy
import gflags

gflags.DEFINE_string("code_list", "000001.SZ,000002.SZ", "code list")
gflags.DEFINE_string("code_file", None, "code file having code list")

FLAGS = gflags.FLAGS

def get_codes_from_wind(date):
	"""Wind must be started already"""
	d = WindPy.w.wset("SectorConstituent","date=" + date + ";sectorId=a001010100000000;field=wind_code")
	#print d.Data[0]
	return d.Data[0]

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
    

if __name__ == "__main__":    
    
    pass