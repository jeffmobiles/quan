# -*- coding: utf-8 -*-

# General syntax to import specific functions in a library: 
##from (library) import (specific library function)
from pandas import DataFrame, read_csv

# General syntax to import a library but no functions: 
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number
import os

#folder = "E:\\python\\F4838\\data\\all_temp\\"
folder = "E:\\python\\F4838\\data\\sz002405\\"
filelist = os.listdir(folder)
print(filelist)
print ("日期-00-00.csv","power"+"\t"+"成交量"+"\t"+"连续买入量"+"\t"+"连续卖出量"+"\t"+"小单差"+"\t"+"小单买入量"+"\t"+"四个点的价格"+"\t"+"小单比例")         
       
for file in filelist:
    df = pd.read_csv(folder+file,encoding="gbk",sep="\t")
    #print (df.columns)
    #Index(['成交时间', '成交价', '价格变动', '成交量(手)', '成交额(元)', '性质'], dtype='object')
    power = 0
    small_bill_buy = 0;
    small_bill_sell = 0
    small_bill_cha = 0;
    p_index = 0;
    p_all_vol = 0;
    
    # 4个区间价格
    m_b=0
    m_e=0
    a_b=0
    a_e=0
    
    # 连续买入变量 
    lianxu_buy = 0;
    lianxu_buy_vol = 0;
    lianxu_sell = 0;
    lianxu_sell_vol = 0;
    all_sell_vol = 0;
    all_buy_vol = 0;
    
    mf = 0;
    all_amount = 0;
    ic = 0; 
    if (df.size > 10):
        for index,row in df.iterrows():
            v_date = row['成交时间']
            open_date = v_date.split(":")[0]+v_date.split(":")[1]
            v_price = row['成交价']
            v_change = row['价格变动']
            if v_change == "--" :
                v_change = "0" 
            v_vol = row['成交量(手)']
            v_amount = row['成交额(元)']
            v_type = row['性质']
            
            p_all_vol += v_vol;
            #1-------------power--------------------
            this_power = float(v_change) * v_vol
            if open_date != "0925":
                power +=this_power
                
            if v_amount <= 40000 :
                if v_type == "买盘" :
                   small_bill_buy +=v_vol
                if v_type == "卖盘" :
                   small_bill_sell +=v_vol
           #3------------总笔数--------------------
            p_index = p_index + 1
            #4-------------4个区价格
            cj_date = v_date.split(":")[0]+v_date.split(":")[1]+v_date.split(":")[2];
            #print(cj_date)
            if open_date == "0925":
               m_b = v_price
            if open_date == "1130":
                m_e = v_price
            if open_date == "1400":
                a_b = v_price
            if open_date == "1500":
                a_e = v_price
                
            #5 --连续买入
            if v_type == "买盘" :  
                lianxu_buy = lianxu_buy + 1
                lianxu_buy_vol += v_vol
                if (lianxu_sell >=5):
                    lianxu_sell = 0;
                    all_sell_vol += lianxu_sell_vol
                    lianxu_sell_vol  = 0
            if v_type == "卖盘" :
                lianxu_sell = lianxu_sell + 1
                lianxu_sell_vol += v_vol
                if (lianxu_buy >=5):
                    lianxu_buy = 0;
                    all_buy_vol += lianxu_buy_vol
                    lianxu_buy_vol = 0
            #6 ---mf，资金流净额:资金流金额。正表示流入、负表示流出 
            #7ic，资金流信息含量:abs（资金流净额/交易额）。ic>10%表明指标的信息含量较高。         
            #8mfp，资金流杠杆倍数:abs（流通市值/资金流净额）。用于衡量资金流的撬动效应。
            if float(v_change) > 0 :
               mf = mf + v_amount
            if float(v_change) < 0:
               mf = mf - v_amount
            all_amount += v_amount   
        small_bill_cha = small_bill_buy - small_bill_sell           
        small_rate = (small_bill_buy + small_bill_sell )/p_all_vol
        ic = mf / all_amount;        
        #print (small_bill_cha)  
        #if power > 0 :
        print (file,str(power) + "\t"+str(mf)+"\t"+str(ic)+"\t"+ str(p_all_vol) +"\t"+str(all_buy_vol)+"\t"+str(all_sell_vol)+"\t"+ "\t"+ str(small_bill_cha) + "\t"+str(small_bill_buy)+"\t ["+str(m_b)+","+str(m_e)+","+str(a_b)+","+str(a_e)+"]" +str(small_rate)) 
        