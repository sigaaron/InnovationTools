#coding=utf-8
'''
zinan@outlook.com   @2019-0620
判断一个文件夹下的所有xml文件和另外一个文件夹下的所有xml文件是否一样
'''



import StringIntegrity as si

import os

cndir = "viewCfg16_10"
endir = "viewCfgEn16_10"

def res_check(cndir,endir):

    print(os.path.abspath(cndir))
    print(os.path.abspath(endir))
     
    cnfiles = [fname for fname in os.listdir(cndir)]
    enfiles = [fname for fname in os.listdir(endir)]

    #print(cnfiles)
    #print(enfiles)
    
    #for n in cnfiles:
    #    a = os.path.join(cndir,n)
    #   print(os.path.abspath(a))
    
    delta = si.list_inter(cnfiles,enfiles)
    if(len(delta)):
        print("CN/EN not match[2]=>",delta)
        return -1
    else:
        for n in cnfiles:
            xmlcn = os.path.join(cndir,n)
            xmlen = os.path.join(endir,n)
            
            if(si.integrity_check(xmlcn,xmlen) != 0):
                return -2
    return 0
    
if __name__ == "__main__":
    r = res_check(cndir,endir)

    print("check result: %d" %r)    
    
    
    
    
    