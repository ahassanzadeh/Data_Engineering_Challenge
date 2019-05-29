#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import os

order_data=[]# use to store the order_product data read from the order_products.csv file
order_title=1 # use to skip the first title line in the .csv file
product_data=[] # use to store the product data read from the products.csv file
product_title=1 # use to skip the first title line in the .csv file
report_data=[] # use to output data and then store it in the report.csv
order_data_add_department_id=[] # use this list to store the order_product.csv file plus one more colunm to store the department_id from product.csv file

testpath1=os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'insight_testsuite/tests/test_1/input/order_products.csv')
testpath2=os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'insight_testsuite/tests/test_1/input/products.csv')
testpath3=os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'insight_testsuite/tests/test_1/output/report.csv')
    
bigtestpath1=os.path.join(os.path.abspath(os.pardir), 'input/order_products.csv')
bigtestpath2=os.path.join(os.path.abspath(os.pardir), 'input/products.csv')
bigtestpath3=os.path.join(os.path.abspath(os.pardir), 'output/report.csv')
    
#os.path.dirname(os.path.abspath(os.curdir))
path1=bigtestpath1
path2=bigtestpath2
path3=bigtestpath3

#os.path.abspath(os.pardir)

def read_data(order_title,product_title):
    print("read_data")
    
    
    start=time.time()
    #, encoding="utf8"
    with open(path1, 'r') as order_csv:
    #read from csv line by line, rstrip helps to remove '\n' at the end of line
        lines_order = [line_order.rstrip() for line_order in order_csv]   
        for line_order in lines_order:
            if order_title < 1:
                words=line_order.split(',')
                order_data.append([int(words[0]),int(words[1]),int(words[2]),int(words[3])])
                #tup = list(map(int, line_order.split(',')))
                #order_data.append(tup)
            else:
                order_title=0
                print(line_order.split(',')) # print the title
     
    end=time.time()
    print("time cost for reading order_products.csv = ", -(start-end)) 

    start=time.time()
    #, encoding="utf8"    
    with open(path2, 'r') as product_csv:
    #read from csv line by line, rstrip helps to remove '\n' at the end of line
        lines_product = [line_product.rstrip() for line_product in product_csv]   
        for line_product in lines_product:
            if product_title < 1:
                words=line_product.split(',')
                product_data.append([ int(words[0]), words[1], int(words[len(words)-2]), int(words[len(words)-1])] )
            else:
                product_title=0
                print(line_product.split(','))
                
    end=time.time()
    print("time cost for reading products.csv = ", -(start-end))
                
def write_data( ):
    print("write_data")
    with open(path3, 'w') as out_file:
        # write the header first
        out_file.write('department_id'+','+'number_of_orders'+','+'number_of_first_orders'+','+'percentage'+'\n')
        for data in report_data: 
            
            for i in range(0,len(data)):
                if i<len(data)-1:
                    out_file.write(str(data[i])+',')
                else:
                    out_file.write(str(data[i])+'\n')
            """
            for item in data:
                if item==data[len(data)-1]:
                    out_file.write(str(item)+',')
                else:
                    out_file.write(str(item)+'\n')  
                    """
            #out_file.write('\n')
        out_file.close()
# this function search the products.csv file to generate the new file, which is adding department id into order_products.csv file
def search_product_id():
    print("search_product_id")
  
    
    # order_product_data and product_data are all sorted, and has been stored back
    start=time.time()
    
    order_data.sort(key=lambda order_data: order_data[1])
    
    end=time.time()
    print("time cost for sorting order_products.csv = ", -(start-end)) 

    start=time.time()
    
    product_data.sort(key=lambda product_data:product_data[0])
    
    end=time.time()
    print("time cost for sorting products.csv = ", -(start-end))
    # the code after this line is only for visulization purpose
      # for test purpose to check the type of order_data
    #for d1 in order_data:
        #print("single value from order_data = ",d1[0])
        #print(d1)
    #for d2 in product_data:
        #print("single value from product_data= ",d2[0])
        #print(d2)
    
    #order_data_add_department_id=[] # use this list to store the order_product.csv file plus one more colunm to store the department_id from product.csv file
    start=time.time()
    
    temp=order_data[0]
    index=binarySearch(product_data,0, 0,temp[1])
    #index=normalSearch(product_data,0,0,temp[1])
    order_data_add_department_id.append((temp[0],temp[1],temp[2],temp[3],product_data[index][3]))
    #print("first generated data= ",order_data_add_department_id[0])
    for data in order_data[1:]:
        #print("data in loop= ",data)
        if data[1]!=temp[1]:
            index=binarySearch(product_data,index+1, 0,data[1]) # search if the current data record is in product.csv file
            #index=normalSearch(product_data,index+1, 0, data[1])
            #print("index = ", index)
            temp=data # need to update temp
        if index > -1:
            order_data_add_department_id.append((data[0],data[1],data[2],data[3],product_data[index][3]))
        else:
            print("Could not find product_id in products.csv file!")
            
    end=time.time()
    print("time cost for binary search products.csv = ", -(start-end))
    print("generated new data file ")
    #for dd in order_data_add_department_id:
        #print(dd)
    order_data_add_department_id.sort(key=lambda order_data_add_department_id:order_data_add_department_id[4])  
    print("generated SORTED new data file ")
    #for dd in order_data_add_department_id:
        #print(dd)
    print("generated SORTED new data file  DONE")

def calculate_report_data():
    #data=order_data_add_department_id
    
    count_total=0 # use to store the total order number from the order_data_add_department_id 
    count_zero=0  # use to store the first order number from the order_data_add_department_id
    index=1 # use to store the index change of the for loop
    temp=order_data_add_department_id[0]
    count_total=1
    if temp[3]==0:
        count_zero=1
    else:
        count_zero=0
        
    for data in order_data_add_department_id[1:]: 
        #print(data)
        index+=1
        if data[4]!=temp[4]:                       
            if count_total==0: 
                print("ratio calculation error!")
            else:
                #int(count_zero/count_total*100)/100+0.1 
                #round((count_zero/count_total),2)
                report_data.append((temp[4],count_total, count_zero, round(float(count_zero)/float(count_total),2) ))
            
            count_total=1
            if data[3]==0:                
                count_zero=1
            else:
                count_zero=0
            temp=data # update temp
        else:
            count_total+=1
            if data[3]==0:
                count_zero+=1 
            #if data==order_data_add_department_id[len(order_data_add_department_id)-1]:
            if index==len(order_data_add_department_id):
                report_data.append((data[4], count_total, count_zero, round(float(count_zero)/float(count_total),2) ))
        
                     
    print("report_data")
    #for dd in report_data:
        #print(dd)

def normalSearch(datalist, start, col, target):
    
    length=len(datalist)
    
    for i in range(start,length):
        
        if i < length:
            if datalist[i][col]==target:
                return i
        else:
            return -1
            
            
        

def binarySearch(datalist, start, col, target): # col use to indecate which coloum is being searched
    """
    datalist=[]
    if len(product_data)!=0:
        
        for ddd in product_data:
        #x=ddd[0]
        #print(x)
            datalist.append(ddd[col])
        #datalist.append(d[col])
     """   

    lo, hi = start, len(datalist) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if datalist[mid][col] < target:
            lo = mid + 1
        elif target < datalist[mid][col]:
            hi = mid - 1
        else:
            return mid
    return -1

"""
    
    if(len(datalist)==0):
        return -1
    else:
        mid=len(datalist)//2
        if(datalist[mid][col]==target):
            return mid
        else:
            if target<datalist[mid][col]:
                return binarySearch(datalist[:mid], col, target)
            else:
                return binarySearch(datalist[mid+1:], col, target)

"""
if __name__=="__main__":
    start1=time.time()
    
    read_data(order_title, product_title)
    
    search_product_id()
    
    start=time.time()
    
    calculate_report_data()
    
    end=time.time()
    print("time cost for calculating the report data = ",-(start-end))
    
    start=time.time()
    
    write_data()
    
    end=time.time()
    print("time cost for writing the report data = ",-(start-end))
    
    end1=time.time()
    print("time cost for total project = ", (end1-start1))
    
    
"""        
d = {}
with open('your_file.csv', 'rb') as f:
    for line in f:
        line = line.split()
        for i in line[1:]:
            key = (line[0])
            d.setdefault(key, []).append(int(i))
x = sorted(d.keys())
y = sorted(d.values())
lst = zip(x,y)
print (lst)

import time

start = time.time()
print("hello")
end = time.time()
print(end - start)


def binarysearch1(sequence, value):
    lo, hi = 0, len(sequence) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sequence[mid] < value:
            lo = mid + 1
        elif value < sequence[mid]:
            hi = mid - 1
        else:
            return mid
    return None


def binarySearch2 (arr, l, r, x): 
  
    # Check base case 
    if r >= l: 
  
        mid = l + (r - l)/2
  
        # If element is present at the middle itself 
        if arr[mid] == x: 
            return mid 
          
        # If element is smaller than mid, then it  
        # can only be present in left subarray 
        elif arr[mid] > x: 
            return binarySearch(arr, l, mid-1, x) 
  
        # Else the element can only be present  
        # in right subarray 
        else: 
            return binarySearch(arr, mid + 1, r, x) 
  
    else: 
        # Element is not present in the array 
        return -1
"""
