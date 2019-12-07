## A window size method to extract and evaluate the strength of supports and resistances of Forex and stocks prices for a given period "t"


### Description

The goal of this work is to extract the supports (S) and resistances (R) statistically using a method that I call it
"Window size method." After obtaining S and R, their strengths are evaluated using a statistical indicator. Support or
 resistance strength represents the possibility that the price is not able
to exceed. If the S or R is strong, the probability that the price will reverse at this point is high. Otherwise, we say S or R is weak.

for a given forex or stock signal

```
f: f=[id:int, d: date,O: open float,H: high float,L:Low float,C: close float,V: volume int]
```

where id is a unique value for each row

I assume that the signal `f` has `n` data points which represent the total number of candles. 
For a given time period (`t: int`) which represents the number of considered candles I choose
windows that will be shifted through the data starting from the latest value to the value `n-t`.
I calculate the highest and lowest prices that are visited at the considered `window_i`. If the price
reveres when reaching those prices, I consider those prices as strong prices.

Inputs:
* filename: CSV file that contains the data.
* number_of_candles: how many candles that the method considers when extracting the resistances and the supports. The technique counts the considered candles from the current candle
* minimum_window_size: the smaller the window is, the more local the results are.
* maximum_window_size: the larger the window is, the more global the results are.
* tolerance: to consider the price differences between bid and buy.
    
outputs: 
* Supports and resistances list
* The strengths of the supports and the resistances scaled between 0 and 100%
