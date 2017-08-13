# Resistance_and_support_forex
‣Created on Sun Aug 06 20:08:17 2017, prepared by Spyder

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
