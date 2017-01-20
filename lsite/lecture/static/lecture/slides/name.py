from glob import glob
from os import system

def name(x):
    return '10/'+str(x)+'.jpg'

list = [int(x[3:-4]) for x in glob('10/*.jpg')]

for x in list:
    if x >= 1 and x < 49:
        system('mv '+name(x)+' '+name('1-'+str(x)))

for x in list:
    if x >= 49 and x < 69:
        system('mv '+name(x)+' '+name('2-'+str(x-48)))

for x in list:
    if x >= 69 and x < 80:
        system('mv '+name(x)+' '+name('3-'+str(x-68)))

for x in list:
    if x >= 80:
        system('mv '+name(x)+' '+name('4-'+str(x-79)))
