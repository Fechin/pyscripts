#!/usr/bin/env python
# coding=utf-8
'''
@author Fechin
@version V 1.0
'''

import os
import os.path


origin = 'D:\input'
dest = 'D:\output'
log = 'D:\mzp_log.log'


# execute command, and return the output
def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

# write "data" to file-filename
def writeFile(filename, data):
    f = open(filename, "w")
    f.write(data)
    f.close()

# walk dir
def walkDir(rootdir):
    lst = []
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            lst.append(filename)
            # lst.append(filename[:filename.find('.')])
    return lst

# start writting
def start():
    for filename in walkDir(origin):
        cmd = 'wacmd create -o %s\%s.mzp -add %s\%s /' % (dest,filename[:filename.find('.')], origin, filename)
	
	result = execCmd(cmd)
	writeFile(log,result)
	
	if result.find('100%') > 0:
            print '%s Writting done !'%filename
	    continue
        else:
            print 'Error log : %s \n %s' %(log,result) 
            break
        
if __name__ == '__main__':
    start()
