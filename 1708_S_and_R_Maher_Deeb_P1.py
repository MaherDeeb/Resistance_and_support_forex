# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 20:08:17 2017, prepared by Spyder

@author: Maher Deeb
@ Warning: the author is not responsible for any losts of money or any type of losts because of using this program or its result. The user is completely responsible for all the
consequences. the program and the results are only for educational purposes.

@Title:
   A window size method to extract and evaluate the strength of supports and resistances of a forex or stock time history signal for a given period "t"
@keywords:
    window size method, supports and resistances,forex,stock,statistical,probabilistic

@description

The goal of this work is to extract the supports (S) and resistances (R) statistically using a method that I will call it "Window size method". After extracting
S and R their strengths will be evaluated using a statistical indicator. Support or resistance strength represents the possibility that the price is not able
to exceed. If the S or R is strong, the probability that the price will reverse at this point is high. Otherwise we say S or R is weak.

for a given forex or stock signal f: f=[id::int,d::date,O::float,H::float,L::Low,C::float,V::int] where id is a unique value for each , d present the date
O is the open price, H is the highest price of the candle, L is the lowest price of the candle, the C is the close price and V is the volume. We assume that
the signal f has l data points which represnets the total number of candles.
for a given time period t::int which represents the number of candles that should be included we are going to choose windows that will be shifted through the data
starting from the latest value to the value l-t.

Inputs: f, t, ws_min,ws_max
outputs: S,R

the implementation will be done in Python using pandas

"""
#1.Import libraries

import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
#==============================================================================

#2.read csv file (4h time frame will be used for this example)

f=pd.read_csv('USDCHF240.csv',header=None)
#2.1give names to the columns
f.columns=['date','time','O','H','L','C','V']
#2.3the amount of the data
l=len(f['H'])
#==============================================================================
# 4. inputs
#4.1 considered periods = number of days * 5 candles per day
t=20*5
#4.2 the minimum and the maximum size of the window that will explore the data
ws_min,ws_max=3,75
#4.2 Initial values of the R and S
R=defaultdict(list)
S=defaultdict(list)
#==============================================================================
#5. process:
for ws in range(ws_min,ws_max+1):
    for t_i in range(l-t,l-ws+2):
        top=max(f['H'][t_i:t_i+ws+1])
        low=min(f['L'][t_i:t_i+ws+1])
        # be sure that the values are unique
        if top not in R[ws]:
            R[ws].append(top)
        if low not in S[ws]:
            S[ws].append(low)
#==============================================================================
#6. For visualization purposes only the R and S values close to the current price will be presented
#6.1 current price is the close of the last candle
cur= f['C'][len(f['C'])-1]
#6.2 define the range of presenting the data based on the range of price movement which is the difference between the highest and lowest value of each candle
df_h_l=f['H']-f['L']
#6.2.1 Histogram of the price movement can be checked to understand the results.
#plt.hist(df_h_l)
fig = plt.figure()
#6.3 plot the result (this is the primary results but they are enough for the first impression) green from R, red from S, blue is the current price
ax = fig.add_subplot(111)
for ws in range(ws_min,ws_max+1):
    ax.plot([ws for i in range(len(R[ws]))],R[ws],'go')
    ax.plot([ws for i in range(len(S[ws]))],S[ws],'ro')
ax.plot(list(range(ws_min,ws_max+1)),[cur]*(ws_max-ws_min+1))
ax.set_ylim(cur-df_h_l.mean(), cur+df_h_l.mean())
#==============================================================================
#... next step is prepare a professional plot and present the method to evaluate the strength of R and S
# Best regards
#Maher Deeb
