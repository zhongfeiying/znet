#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 导入模块
import support
import sys
import math
import os;

print sys.argv

content = dir(math)

print content

# 现在可以调用模块里包含的函数了
support.print_func("zgb")


print "Hello, Python!";
aa = 9
print aa


if True:
    print "True"
else:
  print "False"
 

list = [ 'runoob', 786 , 2.23, 'john', 70.2 ]
tinylist = [123, 'john']
 
print list               # 输出完整列表
 
 
fruits = ['banana', 'apple',  'mango']
for fruit in fruits:        # 第二个实例
   print '当前水果 :', fruit 
   
s = '当前水果 :'
print s.decode("utf-8").encode("gbk") 

#str = raw_input("input please:");
 
#print str;

fo = open("foo.txt", "w")
fo.write( "www.runoob.com!\nVery good site!\n")
 
# 关闭打开的文件
fo.close()

document = open("testfile.txt", "w+");
print "name: ",document.name;
document.write("ooooooo\nwelcome!");
print document.tell();
#输出当前指针位置
document.seek(os.SEEK_SET);
#设置指针回到文件最初
context = document.read();
print context;
document.close();




