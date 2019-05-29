#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python
# use Python3
work_path=$(dirname $0)

cd ${work_path}/src/

python purchase_analytics.py
#python ./src/purchase_analytics.py ./input/order_products.csv ./input/products.csv

