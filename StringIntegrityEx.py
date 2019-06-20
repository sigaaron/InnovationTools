#coding=utf-8

#!/usr/bin/python
#

#coding=utf-8

try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET

#import xml.etree.ElementTree as ET
import os
import sys

strfile     = "strings.xml"
en_strfile  = "strings_en.xml" 

def load_xml(xmlfilename):
    xmlstr = os.path.abspath(xmlfilename)
    try:
        tree = ET.parse(xmlstr)
        #print ("tree type:", type(tree))
        return tree.getroot()
    except Exception as e:
        print ("parse %s fail!" % xmlstr)
        return None

def has_value_attr(node):
    if node is not None and node.attrib is not None and node.attrib.has_key('value'):
        return True
    return False



def recurrent_extract(nodea,nodeb):
    

    for c_a in nodea:
        #print(c_a.tag)
        c_b = nodeb.find(c_a.tag)
        if(c_b is not None):
            if has_value_attr(c_a) and has_value_attr(c_b):
                print("%s;%s;%s" %(c_a.tag,c_a.attrib['value'],c_b.attrib['value']))
            if has_value_attr(c_a) and not has_value_attr(c_b):
                print("%s;%s; " %(c_a.tag,c_a.attrib['value']))
            if not has_value_attr(c_a) and has_value_attr(c_b):
                print("%s; ;%s" %(c_a.tag,c_b.attrib['value']))
        else:
            print(c_a.tag,c_a.attrib['value'],"")
            
        recurrent_extract(c_a,c_b)
        
    #return 0
    

def integrity_extract(strfile,en_strfile):
    xmlstr = os.path.abspath(strfile)
    en_xmlstr = os.path.abspath(en_strfile)
    print(xmlstr,en_xmlstr)
    
    rootcn = load_xml(strfile)
    rooten = load_xml(en_strfile)

    if(rootcn is None or rooten is None):
        return -1

    result = 0
    try:
        #if(rootcn.tag != 'strings' or rooten.tag != 'strings'):
        #    return -2;
        return recurrent_extract(rootcn,rooten)
    except Exception as e:
        print(e)
        return -99

''' '''
if __name__ == "__main__":
    #a="测试"
    #b = u"测试"
    #print(b.encode('utf-8'))
    r = integrity_extract(strfile,en_strfile)

    #print("check result: %d" %r)
