#coding=utf-8
#!/usr/bin/python
#
'''
zinan@outlook.com   @2019-0620
判断两个xml文件的结构是不是完全一样 tag+name的方式
'''


try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET

#import xml.etree.ElementTree as ET
import os
import sys

strfile 	= "clean_ui/strings.xml"
en_strfile 	= "clean_ui/strings_en.xml" 

def load_xml(xmlfilename):
	xmlstr = os.path.abspath(xmlfilename)
	try:
        tree = ET.parse(xmlstr)
        #print ("tree type:", type(tree))
    
        # 获得根节点
        return tree.getroot()
    except Exception as e:  #捕获除与程序退出sys.exit()相关之外的所有异常
        print ("parse %s fail!" % xmlstr)
        return None

def list_inter(lista,listb):
	ulist = list(set(a_list).union(set(b_list)))

	ret = [item for item in ulist if item not in lista or item not in listb]

	#print(ret)
	#
	return ret
	
def recurrent_check(nodea,nodeb):
		cnlvl_1 = [c.tag for c in rootcn]
    	enlvl_1 = [c.tag for c in rooten]

    	delta = list_inter(cnlvl_1,enlvl_1)

    	if(delta):
    		print("CN and EN string resouce file not match!==>")
    		print(delta)
    		return -3

    	for childa in nodea:
    		childa = nodeb.find(childa.tag)
    		if(not childb):
    			print("CN and EN string resouce file not match!==>")
    			print(childa.tag)
    		else:
    			return recurrent_check(childa,childb)


def integrity_check():
	xmlstr = os.path.abspath(strfile)
    en_xmlstr = os.path.abspath(en_strfile)
    
    rootcn = load_xml(strfile)
    rooten = load_xml(en_strfile)

    if(not rootcn or not rooten):
    	return -1

    result = 0
    try:
    	if(rootcn.tag != 'string' or rooten.tag != 'string'):
    		return -2;

		result = recurrent_check(rootcn,rooten)

   	except Exception as e:
   		return -99

   	
   	return result


if __name__ == "__main__":
	r = integrity_check()

	print("check result: %d" %r)
