#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Insight Challenge: Purchase-Analytics
Author: Ali Hassanzadeh
Data: 2/28/2019
"""

#import time
import os

order_data=[]# use to store the order_product data read from the order_products.csv file
product_data=[] # use to store the product data read from the products.csv file
report_data=[] # use to output data and then store it in the report.csv
order_data_add_department_id=[] # use this list to store the order_product.csv file plus one more colunm for department_id from product.csv file

testpath1=os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'insight_testsuite/tests/test_1/input/order_products.csv')
testpath2=os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'insight_testsuite/tests/test_1/input/products.csv')
testpath3=os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'insight_testsuite/tests/test_1/output/report.csv')
    
bigtestpath1=os.path.join(os.path.abspath(os.pardir), 'input/order_products.csv')
bigtestpath2=os.path.join(os.path.abspath(os.pardir), 'input/products.csv')
bigtestpath3=os.path.join(os.path.abspath(os.pardir), 'output/report.csv')
    
path1=bigtestpath1
path2=bigtestpath2
path3=bigtestpath3

def read_data( ):
    """
    This function is used to read data from order_products.csv and products.csv and store them in order_data and product_data lists,
    also change the data type from string to integer based on the content in the table.
    order_data <--order_products.csv
    product_data<--products.csv
    """
    
    order_title=1 # use to skip the first header line in the .csv file
    product_title=1 # use to skip the first header line in the .csv file
    
    #start=time.time()    
    with open(path1, 'r') as order_csv: # run on submission link but not on PC
    #with open(path1, 'r',  encoding="utf8" ) as order_csv: # run on PC           
        lines_order = [line_order.rstrip() for line_order in order_csv]   
        for line_order in lines_order:
            if order_title < 1:
                words=line_order.split(',')
                order_data.append([int(words[0]),int(words[1]),int(words[2]),int(words[3])])
            else:
                order_title=0
                #print(line_order.split(',')) # print the header line   
    #end=time.time()
    #print("time cost for reading order_products.csv = ", -(start-end)) 

    #start=time.time()  
    with open(path2, 'r') as product_csv: # run on submission link but not on PC
    #with open(path2, 'r',  encoding="utf8" ) as product_csv: # run on PC but not the submission link
        lines_product = [line_product.rstrip() for line_product in product_csv]   
        for line_product in lines_product:
            if product_title < 1:
                words=line_product.split(',')
                product_data.append([ int(words[0]), words[1], int(words[len(words)-2]), int(words[len(words)-1])] )
            else:
                product_title=0
                #print(line_product.split(',')) # use to print out the header line               
    #end=time.time()
    #print("time cost for reading products.csv = ", -(start-end))
                
def write_data( ):
    """
    This function is used to write the final data list, report_data, to report.csv file,
    and also change the data type from integer, float to string.
    """
    
    with open(path3, 'w') as out_file:
        # write the header first
        out_file.write('department_id'+','+'number_of_orders'+','+'number_of_first_orders'+','+'percentage'+'\n')
        for data in report_data:             
            for i in range(0,len(data)):
                if i<len(data)-1:
                    out_file.write(str(data[i])+',')
                else:
                    out_file.write(str(data[i])+'\n')           
        out_file.close()

# this function search the products.csv file to generate the new file, which is adding department id into order_products.csv file
def search_product_id():
    """
    This function is used to search the corresponding department_id for each product_id, 
    then add the found department_id to the end of each order record, 
    in order to not change the data structure in the original order_products.csv(order_data) file, 
    a new data list order_data_add_department_id was generated to store this data.

    In order to save search time for large amount of data, 
    both order_data and product_data have been sorted in ascending order based on product_id before the search starts.
    
    Search Procedure:
        1, look into order_data from the first row based on their product_id (which is also the smallest one based on product_id), 
        2, then go to the product_data to find rows have the same product_id
        (those rows should be at the first begining of product_data because all data here has also been sorted acendingly based on their product_id)
        3, rows have the same product_id in order_data will not need to be researched,  the same department_id will be used
    
    Search Algorithems:
        1, binary search, time complexity is O(n)
        2, sequence search, time complexity is 0(logn).
        
    Search Tip:
        During each search, the starting index of product_data will be updated to the next unsearched row,
        the search efficiency has been increased around 50%, from 50s decrease to 25s. 
        And with this technique, there is no performance difference from binary search and normal search, both cost around 25s.
    """
    
    #start=time.time()    
    order_data.sort(key=lambda order_data: order_data[1])
    #end=time.time()
    #print("time cost for sorting order_products.csv = ", -(start-end)) 

    #start=time.time()
    product_data.sort(key=lambda product_data:product_data[0])
    #end=time.time()
    #print("time cost for sorting products.csv = ", -(start-end)) 
        
    #start=time.time()    
    temp=order_data[0]
    index=binarySearch(product_data,0, 0,temp[1])
    #index=sequenceSearch(product_data,0,0,temp[1])
    order_data_add_department_id.append((temp[0],temp[1],temp[2],temp[3],product_data[index][3]))
    for data in order_data[1:]:
        if data[1]!=temp[1]:
            index=binarySearch(product_data,index+1, 0,data[1]) # search if the current data record is in product.csv file
            #index=sequenceSearch(product_data,index+1, 0, data[1])
            temp=data # need to update temp
        if index > -1:
            order_data_add_department_id.append((data[0],data[1],data[2],data[3],product_data[index][3]))
        else:
            print("Could not find product_id in products.csv file!")            
    #end=time.time()
    #print("time cost for binary search products.csv = ", -(start-end))
    
    

def calculate_report_data():
    """
    This function is used to count total order numbers and first time order numbers seperately from order_data_add_department_id data,
    and save all data into report_data.
    In order to save search time, again, all data in order_data_add_department_id has been sorted ascendingly based on their department_id.
    count_total <--So the total order numbers should be counted by rows has same department_id 
    count_zero  <--the total first time order numbers should be counted by rows has 0 marks in reorder column(in the range of same department_id).
    
    """
    #print("generated new data file ")
    order_data_add_department_id.sort(key=lambda order_data_add_department_id:order_data_add_department_id[4])  
    #print("generated SORTED new data file  DONE")
    
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
        index+=1
        if data[4]!=temp[4]:                       
            if count_total==0: 
                print("ratio calculation error!")
            else:
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
            if index==len(order_data_add_department_id):
                report_data.append((data[4], count_total, count_zero, round(float(count_zero)/float(count_total),2) ))
                                
def sequenceSearch(datalist, start, col, target):
    
    length=len(datalist)    
    for i in range(start,length):        
        if i < length:
            if datalist[i][col]==target:
                return i
        else:
            return -1                                

def binarySearch(datalist, start, col, target): # col use to indecate which coloum is being searched
    
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


if __name__=="__main__":
    
    #start1=time.time() # use to check the whole program running time
    
    read_data()     
    search_product_id()    
    #start=time.time()    
    calculate_report_data()    
    #end=time.time()
    #print("time cost for calculating the report data = ",-(start-end))
    
    #start=time.time()    
    write_data()    
    #end=time.time()
    #print("time cost for writing the report data = ",-(start-end))
    
    #end1=time.time() #use to check the whole program running time
    #print("time cost for total project = ", (end1-start1))
    
"""        
    use to check the whole length for total order numbers and total first orders in order to quantitatively compare with the final report data
    for testing the order_products_prior.csv 
    the total order number = 32434489
    the total first time order number = 13307953

    print("length = ", len(order_data))
    
    count=0 # use to count total first order number
    for dd in order_data:
        if dd[3]==0:
            count+=1
    print("zero numbers = ", count)
    
  """  
