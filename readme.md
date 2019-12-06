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

We assume that the signal f has n data points which represent the total number of candles. 
For a given time period (t: int) which represents the number of considered candles we choose
windows that will be shifted through the data starting from the latest value to the value l-t.

Inputs:

* f
* t 
* ws_min
* ws_max
    
outputs: 
* S
* R

"""