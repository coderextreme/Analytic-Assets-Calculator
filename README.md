# Analytic Assets Calculator

## A Pictures or Results

### Mostly Crypto Currencies Altcoins and Bitcoin, but that's unimportent, because it can be everything, also gold barren, oil cans, food prices, any ressources on the market, stock prices, several indexes of stocks or your created index of anything you want to create an index of

### all-start-at-100-percent ( because calculation command makes it, like a calculator you give formulas )
![alt text](/example-results/all-start-at-100-percent.png "all-start-at-100-percent")
### all-start-at-1-but-logscale-and-so-start-at-0
![alt text](/example-results/all-start-at-1-but-logscale-and-so-start-at-0.png "all-start-at-1-but-logscale-and-so-start-at-0.png")
### both-end-at-100-percent ( because calculation command makes it, like a calculator you give formulas )
![alt text](/example-results/both-end-at-100-percent.png "both-end-at-100-percent.png")
### diffuse2-operator: (all moving) Maximum, Minimum, Median, Average
![alt text](/example-results/diffuse2-operator.png "diffuse2-operator.png")
### diffuse-operator: (data points reducing) Maximum, Minimum, Median, Average
![alt text](/example-results/diffuse-operator.png "diffuse-operator.png")

## B About

Language: Python 3.6

Status: pre alpha, bleeding edge

## C What it is:
A Calculator for prices per timestamp, allowing:

+ unlimited formulas with brackets

+ unlimited amount calculations in one formula, because this means at the same amount:

+ unlimited graphs in a diagram (but yet no parallel computing)

## D What it can do:
Give you a chart diagram with the price of oil cans in gold barren instead of
a currency

Give you a chart diagram with the price of any Altcoin in the price any other
Altcoin instead having it in Bitcoin
And it can do a lot more!


Output: Linux GUI, text numbers stdout, text numbers for Web, web diagram

Input: one cli ( command line interace ) command
every syntax word must be seperated by whitespace, also brackets

+ Calculation objects can be a key value matrix: key is timestamp and value is a
price

+ it can be a matrix with one key and multiple values

+ it can be float numbers

+ it can be lists of float numbers for calculation with the same amount of
values having a key valueS matrix

+ statistical calculations, oszillators and indicators are to be implemented and partly already available, but all in the level of doing it by formula in its essence, like real math

+ create your own personal index, such as Dow Jones, with your desired needs, compare your index, divide any index or asset by any other "time and price chainching thing", to compare both, to get your desired chart in a diagram

There is no user friendly interface yet. For end users it is going to be better, not to know that there is a calculator like this behind, for what they want. End users is better to be given: a user interface, that does not overburden their mind. For example they better say they want the altcoin in the price of another altcoin instead to have to understand and know that this is just a division about one coin by another, whereat both must be given in the price bitcoin or in just the same price unit. This is like calculation in physics, because it is formulas with units.

## E Examples

examples for unix cli:
`
./CryGoldEVA.py monero-in-bitcoin.csv d0000-00-10_00:00 chart
`

### explanation:
CryGoldEVA.py is for direct cli mode
"chart" at the end is for unix GUI display of the diagram
"monero-in-bitcoin.csv" is a file in the same directory
may it be the price of the Monero altcoin in bitcoin
"d0000-00-10_00:00" means for 10 days until now

the csv file has in every line in its first column timestamps,
and the other columns have values, one line for example:
`
123455;10.5
`
that means the currency or whatsoever asset has the price of 10.5 whatsoever.

instead of the last parameter "chart", also possible is:
"stdout" or "none"
instead of "d0000-00-10_00:00" it is also possilbe:
"2019-01-01_10:10 2019-01-11_10:10" that is also 10 days, but in the past!
instead of
`
./CryGoldEVA.py monero-in-bitcoin.csv d0000-00-10_00:00 chart
`
it is also possible:
`
./CryGoldEVA.py 'monero-in-bitcoin.csv d0000-00-10_00:00' chart
`
or
`
./CryGoldEVA.py 'monero-in-bitcoin.csv d0000-00-10_00:00 chart'
`
this means, having brackets:
`
./CryGoldEVA.py \( monero-in-bitcoin.csv \) d0000-00-10_00:00 chart
`
or
`
./CryGoldEVA.py '( monero-in-bitcoin.csv ) d0000-00-10_00:00 chart'
so then escaping brackets is not needed!
`
### 2nd example:
`
./CryGoldEVA.py monero-in-bitcoin.csv mul bitcoin-in-dollar.csv mul dollar-in-euro.csv d0000-00-10_00:00 chart
`
for the next examples we look at just only that part:
`
monero-in-bitcoin.csv mul bitcoin-in-dollar.csv mul dollar-in-euro.csv
`
lets say all 3 csv's collected every prices (not exactly) every 5 minutes:
the result is the Monero Price in Euro
the price of Monero in Bitcoin multiplied by the price of Bitcoin in Dollar
multiplied by the price of Dollar in Euro. That is the price of Monero in
Euro.

so we only look at the calculation for now:

### 3rd example:
`
Monero-in-Bitcoin.csv div Litecoin-in-Bitcoin.csv
`
This is also like calculating in physics.
(monero / bitcoin ) / ( litecoin / bitcoin)
= monero / litecoin
the resulting chart diagram is going to be the price of monero in the price of litecoin

### 4th example
`
( Ethereum-in-Bitcoin.csv div Litecoin-in-Bitcoin.csv ) aswell ( Monero-in-Bitcoin.csv div Litecoin-in-Bitcoin.csv )
`
this is 2 charts in one diagram: the price Ethereum and Monero, but given in
the price of Litecoin!

You can have as much and deep using brackets as you want and you can calculate as
much calculations as you want!
You must escape brackets: \( if the calculation is not inside '' or "" !
behind and before every bracket must be white space as around every token in
the command!
You can use all 3 types of brackets: [] () {}, they are the same, but opening
and closing have to be done with the same type of bracket, this is for better
understanding like it is in mathematics.

### 5th example:

If you have a calculation result ( in between ) that mean more than one value,
the continuing calculation will calculate with both, so you are going to
calculate multiple calculations the same time:
`
( price-of-something.csv aswell price-of-somethingelse.csv ) mul 20
`
the result is both things multplied by 20

operators for calculations:

+ **add** - adds 2 things, numbers, key-valueS matrices, lists of numbers

+ **mul** - same for multiply

+ **div** -  division

+ **sub** - sustract

+ **log** - caclulate any logarithm for log scale, you could even senselessly use 2 matrices instead a matrix and a number as operands

+ **root** - like squareroot, if you do "bla.csv root 2" an laternative to log scale

+ **med** - moving median

+ **avg** - moving average

+ **max** - maximum of bunches of time set by given time span

+ **min** - same for minimum

+ **aswell** - things behind and in front of aswell are to things, so it is possible to have more than one graph for one diagram, and continue calculation after having more than one thing, mean to calculate more than one thing as next when putting a calculation as next after "aswell"

+ **diffuse** - making 4 charts out of one, but with much reduced data points, given by your time range

+ **diffuse2** - same as diffuse, but all values are now moving things, so not less datapoints

+ **pow** - the power of whatsoever

+ **begin** - give us the first value in our time range

+ **end** - give us the last

+ **vari** - variance ( statistics )

+ **stddevi** - standard deviation of statistics

some explanations:
diffuse and diffuse2 make one chart to 4 charts in one diagram, by reducing
the data points. example command: file.csv diffuse 4h
this makes that every data point in the time span of 4 hours will be made to
one data point and 4 values: the max,min,median,average in those 4 hours.
So we have less data, even we have 4 instead of 1 chart in one diagram
instead of 4 hours you can also have: 2d 3w 4m 1y for 2 days, 3 weeks, 4
months, one year, with diffuse2 you have moving values and not less data
points, moving average, moving median, moving max, moving min
`
2d or 3w or 4m or 1y
`
has to be given as a parameter not only for diffuse and diffuse2, but also
for:
max,min,avg,med, begin, end

med is median, avg is average, end is the really last, and begin the really
first value, 
### 6th example:
`
XMR-BTC.csv mul btc-eur.csv div \( XMR-BTC.csv mul btc-eur.csv begin 1d \) mul 100
`
this is the price of xmr alias Monero in Euro ( because of the multiplication
) divided by its price in the average of the beginning one day
So the beginning will be at 1, but you multiply by 100, so it starts at 100,
so that it looks like it starts by 100%

you can combine such calculations with the "aswell" operator, so that you can
compare multiple assets starting all at 100%

### 7th and 8th example:
`
XMR-BTC.csv log 7
`
`
XMR-BTC.csv root 2
`
this makes log scale or square root scale. You can chose any number to do the
calculation!

### 9th example:

XMR-BTC.csv avg 10d
this calculates the moving average for the span of 10 days. The span is for
making the chart more or less smooth

### 10th example:
`
( bestcoin-price.csv mul bestcoin-amountofAllexisting.csv ) add ( secondbestcoin-price.csv mul secondbestcoin-amountofAllexisting.csv )
`
the result is the top 2 of the best coins, because it is the sum of both coins
market capitalizations.
This is like a stock index, like Dow Jones or DAX.
You can create your own altcoin index like Dow Jones or DAX.

### 11th example:
`
dax.csv div ( dowjones.csv mul euro-in-dollar.csv )
`
Lets say you have the German Stock Index that is probably compared to Euro in
its evaluation. So we make the Dow Jones also in Euro.
If we divide each other that are compared both to Euro, the result is
the German Stock index in the price of Dow Jones scores.

So with the resulting chart we can compare both countries better.
We can compare everything with everything and anything with anything.

### 12th example:
`
OilCanprice.csv div goldbarrenPrice.csv
`
the resulting chart is the price of oil cans, not in a currency, but in the price of
gold barren!

### 13th example:
`
\( XMR-BTC.csv aswell LTC-BTC.csv \) div \( \[ XMR-BTC.csv end 1h \] aswell \[ LTC-BTC.csv end 1h \] \) mul 100
`
result:
both charts end at 100%
how?
XMR-BTC.csv aswell LTC-BTC.csv
make 2 lists per one timestamp of 2 altcoins
XMR-BTC.csv end 1h
bring one float number, the average of the ending of the last hour of XMR.
XMR-BTC.csv end 1h aswell \[ LTC-BTC.csv end 1h \]
so a list of two float numbers
so u have a matrix with one key and two values
and you have a list with 2 floats
dividing both from each other, is like dividing twice:
one values list is divided by a value
second values list is divided by a second value in the list of two values

the rest can be well understood, as I described similar things before, and
with some mathetmatical knowlege.
So we can have more than one calculation in one formula
if we divide or do whatever with the same amount of things (here 2 things), like in this
example with this division: the result will remain in two things
if we have a not equal amount of things, the result is going to have as much
things as the multiplication product of both amounts of things. For example 4
things div 3 things is making 12 things.
So next, we would calculate with 12 things, if we add another calculation.

### 14th example
`
stockwhatsoever.csv div its-index.csv
`
the whatsoever stock not in its price of its currency, but in the price of scores of the index the stock is a member of ( or not, but should better use the same currency as it ).

### 15th example
`
stock-in-one-exchange.csv div same-stock-in-another-exchange.csv
`
the resul is a chart that moves around the number 1, and shows differences of the same stock being traded at both exchanges


## F Bugs:


### Bug:
Sometimes the last and first value is not right calculated:
Solve:
Different types of solutions possible

### Bug:
average and all other diffuse2 operations are shifted in time, and shall
calculate all the middle, so that the moving average and moving median is in
the middle and not time shifted. Time Shifting in diffuse 1 is even worse.
There it is not near the middle, but in the end - thats totally wrong!

### Bug:
merging 2 charts to one chart to be just the combination of 2 charts in one
diagram with only one list of timestamps and not anymore 2 list of timestamps,
is not solved well, if both lists of timestamps are too different, than the
result can become very wrong and weired.

#### When does this bug happen:
when diffuse,diffuse2,max,min,avg,med shall be combined with "aswell" with
another chart, then the lists of timestamps are too much different, because
the 1 hour, 2 weeks (1h,2w) of diffuse and etc. lead to a very distorted
diagram of charts.

#### Why does this happen?:
The combination of 2 or more chart data with the result of having then only
one list of timestamps, merges the timestamps in finding the nearest timestamp
and calculate the middle of both timestamps.

Solving the issue that way seems logically. But we need more than one way of
merging timestamp lists to one list. If we 2 lists of timestamps, one with 10
and another with 100 timestamps, this merge makes a very distorted list of
timestamp.

#### solution:
explained by example:
list1
time;value
100;5
200;10

list2
time;value
50;5
102;7
150;3
198;12

resulting list with operation "aswell"
time;value1;value2
50;5;calculated value in between, delta calculation, relative value
101;5;7
150;3;that what should be here in between, delta, relative, whatsoever+
199;10;12

We could also have always lists of timestamps, that are always equal enough,
so that we do not need to solve such situations, but we also want diagrams
that have not so many datapoints, to have less data, for multiple reasons,
like speed, network traffic, and so on.

Now we are going to have 2 or more merging algorithms.
What shall make select which shall become the right merging algorithm?
This: After max or min,avg,med,diffuse,diffuse2 not only the resulting matrix
shall be put out, but a matrix with also extra data. So the new merging
algorithm will know that it is the right merging algorithm, because the data
shrunk because of diffuse,diffuse2 or max, min, avg, med.








## G Future Features:


+ for avg and med:
It the ending and beginning shall be not cut off.
This feature is already implemented, but caclulation could be done better.
For a moving average or moving median, the ending and beginning, shall be
painted even though less data points for calculation, as everywhere in the
middle. For example at second data point, we have only 2 data points for
calculation and anywhere in the middle we have as much data points as we
shall give them, for example 12: if we want one hour, and have a data point
every 5 minute.

+ Quantile Operators:
Yet, we have a moving median operator.
We also want a moving quantile operator, that do not only tell how far it
shall move ( one our or two weeks, etc.), but also which quanitle, that is not
only at 50% that it is having the median.
Then after implementing a quantile operator, a quantiles operator could also
be nice. We do not tell this operator, which quantile, we want to have, but
how many. For example 20 quantiles makes every a quantile at 5%, 10%, 15% ...
95%.
The result we get, is a stock chart or altcoin chart, that looks more like a
rainbow. Because stocks and cryptos are more about feeling, than about
rationality, such a diagram, that looks like a rainbow, tell us better about
the feelings, the traders have had trading this asset that we display.


+ moving correlation

+ moving (linear) regression

+ we have already moving standard deviation, next we can implement:

+ moving Kurtosis and moving Skewness, that bring us the possibility to make:

+ clustering possible, that is good for

+ calculate when events happen to a similar time

+ create a new char diagram: from time 1 to 4 the chart is a*x*x and time 5
to 10 it is a+b*x*x*x and from time 11 to 15 it is just a.

+ why this: that way we can create chart diagrams that can be more easily be
understood instead to have lots of flickering in any chart diagram. We can
have a chart diagram that looks really tidy and simple, and without any noise,
if we have a chart diagram, that consists of a set of forms, every timespan
another particular form, and the range of one timespan can be calculated by
Skewnesses with probabilit mathematics.

+ self created top 1-10 or 5-15, whatsoever of any altcoin market or stock
market. We just add the market capitalization of any altcoin or stock. The
market capitalization is calcluated be multiplying amount of all coins with
the price of one coin.

+ automatic bracket creation, so that multiplication is always calculated
before adding something a + ( b * c ), that "aswell" is like (calulation1) aswell
(calcluation2)

+ Operations with an arbitrary amount of operands, yet 2 operands work, and 1 and 3
is prepared to is going to work, but there is also prepared to have as much as
you want, but still that buggy, that it does not work yet.

+ Names of Altcoins shall become also an input, so that it can be displayed in
the output, or when the top 10 Types of Altcoins shall be listed for one day,
the name shall also be output, so that the name can be an input, to can be
output

+ using not anymore csv as a file format, but using database, best are key
value databases like lmdb, sql is not needed.

+ Caching of already calculated charts and diagrams, so that a new calculation
calculates only new values, that have had not been calculated yet.

+ when a part of a formular have had already been calculated in the whole
formular, but is still needed in another part of the formular, than it does
not need to be calculated more than once, but can be cached while calculating.
For example if you want the chart itself but also its moving median and moving
average, than you do need the chart 3 times, but loading it form database 3
times is not fast, or need to calculate it 3 times is not needed, for example
if the chart is calculated by div or mul of 2 other charts

+ multi core or multi cpu calculation: the abstract syntax tree of a long
fromular with brackets can be devided for different cores or cpus

+ multi core or multi cpu calculation: the calculation of one operation on one
chart diagram can be splitted in that many parts, that many cpu cores exist.

+ faster merging algorithm for combining 2 or more chart diagrams into one.
The whole program is that very slow now, because the algorithm is very precise
and bad at speed for combining two matrixes of chart diagram data points, and
because csv files are used and not a database.

+ all indicators and oszillators that can be used also for stocks ( there are maybe around 100 that exist )

+ UI for: any mobile phone, any smart watch, TV, website, Desktop Widget like
for KDE Plasma

+ create lots of Unit Test Cases

+ make it possible to compare branches of branches of branches of industries,
like real tree structures: Calculate not only with numbers, lists or matrices,
but also with trees, so that complex comparisions between industries of
diffrent countries can be achieved.

+ operation add number to every timestamp: needed for MACD, nothing more needed but this feature and the right formula and you get the MACD

+ better have everything able to be calculated that Probability theory mathematics consists of

+ like moving average or moving median or moving quantile, lets make anything be a moving whatsoever, that is technically possible, even it does not make sense, but we will see if it will make sense, though!
