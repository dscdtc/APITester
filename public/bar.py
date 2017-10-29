# -*- coding: utf_8 -*-
import sys,os
from time import sleep

def Progress(x,y):
    rate = (x*100)/y + 1
    sys.stdout.write(' '*rate + '\r')
    sys.stdout.flush()
    sys.stdout.write('   ' + str(rate) + '%  '+ '>'*rate + '-'*(100-rate) + '\r')
    #os.write(1,'   ' + str(rate) + '%  '+ '>'*rate + '-'*(100-rate) + '\r')
    sys.stdout.flush()