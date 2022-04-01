```R
library(styleer)
```

# 1. 数据导入及清洗

## 1. 对抓取的龙虎榜数据进行清洗 

检测每一天的数据是否抓到最新


```R
b <- fread("./data/2022-01-27.csv", encoding = "UTF-8")
b[order(-date)
    ][1:5]
```


<div style = "overflow-x:scroll; overflow-y:scroll">
	<table width = "1200px" >
	<caption>A data.table: 5 × 6</caption>
	<thead>
		<tr><th scope=col>buy_inst_num</th><th scope=col>date</th><th scope=col>rank_reason</th><th scope=col>sell_inst_num</th><th scope=col>stock_name</th><th scope=col>stock_symbol</th></tr>
		<tr><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;date&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;int&gt;</th></tr>
	</thead>
	<tbody>
		<tr><td> 460.27</td><td>2022-01-26</td><td>有价格涨跌幅限制的日收盘价格涨幅达到15%的证券                </td><td> 709.01</td><td>建研设计</td><td>301167</td></tr>
		<tr><td>2009.31</td><td>2022-01-26</td><td>连续3个交易日内收盘价格跌幅较基准指数偏离值累计达到-30%的证券</td><td>9479.98</td><td>华宝股份</td><td>300741</td></tr>
		<tr><td>4907.75</td><td>2022-01-26</td><td>连续三个交易日内,涨幅偏离值累计达20%的证券                   </td><td>4232.23</td><td>深南股份</td><td>  2417</td></tr>
		<tr><td>   0.00</td><td>2022-01-26</td><td>日跌幅偏离值达7%的证券                                       </td><td>4220.17</td><td>岭南股份</td><td>  2717</td></tr>
		<tr><td>4406.32</td><td>2022-01-26</td><td>日跌幅偏离值达7%的证券                                       </td><td>3039.90</td><td>千红制药</td><td>  2550</td></tr>
	</tbody>
	</table>
</div>



合并所有数据集查看行数并导出为csv


```R
DTRank <- fbread(pattern = "*.csv", encoding = "UTF-8")
DTRank <- DTRank[, file_id := NULL, 
    ][, unique(.SD)
    ][, stock_symbol := str_pad(stock_symbol, width = 6, side = "left", pad = "0")
    ][order(-date, stock_symbol), .SD
    ]
DTRank[, .N]
fwrite(DTRank, "DTRank.csv")
```


    Error in fbread(pattern = "*.csv", encoding = "UTF-8"): 没有"fbread"这个函数
    Traceback:
    


## 2. 清洗合并各类股票数据

导入日收益率文件数据


```R
trading <- fbread(pattern = "*.txt", encoding = "UTF-8", path = "./data/Trading")
trading[, .N]
trading <- trading[, file_id := NULL
    ][, setnames(.SD, c("Stkcd", "Trddt"), c("stock_symbol", "date"))]
trading[1:5]
```


5730194



<table class="dataframe">
<caption>A data.table: 5 × 5</caption>
<thead>
	<tr><th scope=col>stock_symbol</th><th scope=col>date</th><th scope=col>Clsprc</th><th scope=col>Dnvaltrd</th><th scope=col>Dsmvosd</th></tr>
	<tr><th scope=col>&lt;int&gt;</th><th scope=col>&lt;date&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>1</td><td>2017-01-25</td><td>9.26</td><td>281976294</td><td>156660584</td></tr>
	<tr><td>1</td><td>2017-01-26</td><td>9.33</td><td>391844286</td><td>157844843</td></tr>
	<tr><td>1</td><td>2017-02-03</td><td>9.26</td><td>292617943</td><td>156660584</td></tr>
	<tr><td>1</td><td>2017-02-06</td><td>9.31</td><td>480441331</td><td>157506484</td></tr>
	<tr><td>1</td><td>2017-02-07</td><td>9.30</td><td>368755274</td><td>157337304</td></tr>
</tbody>
</table>



导入换手率文件数据


```R
tradingDev <- fbread(pattern = "*.txt", encoding = "UTF-8", path = "./data/TradingDev")
tradingDev[, .N]
tradingDev <- tradingDev[, setnames(.SD, c('TradingDate', 'Symbol'), c('date', 'stock_symbol'))
    ][, file_id := NULL]
tradingDev[1:5]
```


5730194



<table class="dataframe">
<caption>A data.table: 5 × 4</caption>
<thead>
	<tr><th scope=col>date</th><th scope=col>stock_symbol</th><th scope=col>ShortName</th><th scope=col>Turnover</th></tr>
	<tr><th scope=col>&lt;date&gt;</th><th scope=col>&lt;int&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>2016-01-25</td><td>1</td><td>平安银行</td><td>0.00319</td></tr>
	<tr><td>2016-01-26</td><td>1</td><td>平安银行</td><td>0.00549</td></tr>
	<tr><td>2016-01-27</td><td>1</td><td>平安银行</td><td>0.00482</td></tr>
	<tr><td>2016-01-28</td><td>1</td><td>平安银行</td><td>0.00256</td></tr>
	<tr><td>2016-01-29</td><td>1</td><td>平安银行</td><td>0.00461</td></tr>
</tbody>
</table>



合并两个文件

## 3. 将龙虎榜和股票交易数据合并


```R
stkcd_feature <- tradingDev[trading, on = .(date, stock_symbol)]
stkcd_feature[, stock_symbol := str_pad(stock_symbol, 6, side = "left", pad = "0")
    ][1:5]
```


<table class="dataframe">
<caption>A data.table: 5 × 7</caption>
<thead>
	<tr><th scope=col>date</th><th scope=col>stock_symbol</th><th scope=col>ShortName</th><th scope=col>Turnover</th><th scope=col>Clsprc</th><th scope=col>Dnvaltrd</th><th scope=col>Dsmvosd</th></tr>
	<tr><th scope=col>&lt;date&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>2017-01-25</td><td>000001</td><td>平安银行</td><td>0.00180</td><td>9.26</td><td>281976294</td><td>156660584</td></tr>
	<tr><td>2017-01-26</td><td>000001</td><td>平安银行</td><td>0.00249</td><td>9.33</td><td>391844286</td><td>157844843</td></tr>
	<tr><td>2017-02-03</td><td>000001</td><td>平安银行</td><td>0.00186</td><td>9.26</td><td>292617943</td><td>156660584</td></tr>
	<tr><td>2017-02-06</td><td>000001</td><td>平安银行</td><td>0.00305</td><td>9.31</td><td>480441331</td><td>157506484</td></tr>
	<tr><td>2017-02-07</td><td>000001</td><td>平安银行</td><td>0.00235</td><td>9.30</td><td>368755274</td><td>157337304</td></tr>
</tbody>
</table>




```R
stkcd_feature <- tradingDev[trading, on = .(date, stock_symbol)]
stkcd_feature[, stock_symbol := str_pad(stock_symbol, 6, side = "left", pad = "0")
    ][1:5]
```


<table class="dataframe">
<caption>A data.table: 5 × 7</caption>
<thead>
	<tr><th scope=col>date</th><th scope=col>stock_symbol</th><th scope=col>ShortName</th><th scope=col>Turnover</th><th scope=col>Clsprc</th><th scope=col>Dnvaltrd</th><th scope=col>Dsmvosd</th></tr>
	<tr><th scope=col>&lt;date&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>2017-01-25</td><td>000001</td><td>平安银行</td><td>0.00180</td><td>9.26</td><td>281976294</td><td>156660584</td></tr>
	<tr><td>2017-01-26</td><td>000001</td><td>平安银行</td><td>0.00249</td><td>9.33</td><td>391844286</td><td>157844843</td></tr>
	<tr><td>2017-02-03</td><td>000001</td><td>平安银行</td><td>0.00186</td><td>9.26</td><td>292617943</td><td>156660584</td></tr>
	<tr><td>2017-02-06</td><td>000001</td><td>平安银行</td><td>0.00305</td><td>9.31</td><td>480441331</td><td>157506484</td></tr>
	<tr><td>2017-02-07</td><td>000001</td><td>平安银行</td><td>0.00235</td><td>9.30</td><td>368755274</td><td>157337304</td></tr>
</tbody>
</table>




```R
DTanalysis <- DTRank[stkcd_feature, on = .(date, stock_symbol)]
DTanalysis[1:5]
```


<table class="dataframe">
<caption>A data.table: 5 × 11</caption>
<thead>
	<tr><th scope=col>buy_inst_num</th><th scope=col>date</th><th scope=col>rank_reason</th><th scope=col>sell_inst_num</th><th scope=col>stock_name</th><th scope=col>stock_symbol</th><th scope=col>ShortName</th><th scope=col>Turnover</th><th scope=col>Clsprc</th><th scope=col>Dnvaltrd</th><th scope=col>Dsmvosd</th></tr>
	<tr><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;date&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>NA</td><td>2017-01-25</td><td>NA</td><td>NA</td><td>NA</td><td>000001</td><td>平安银行</td><td>0.00180</td><td>9.26</td><td>281976294</td><td>156660584</td></tr>
	<tr><td>NA</td><td>2017-01-26</td><td>NA</td><td>NA</td><td>NA</td><td>000001</td><td>平安银行</td><td>0.00249</td><td>9.33</td><td>391844286</td><td>157844843</td></tr>
	<tr><td>NA</td><td>2017-02-03</td><td>NA</td><td>NA</td><td>NA</td><td>000001</td><td>平安银行</td><td>0.00186</td><td>9.26</td><td>292617943</td><td>156660584</td></tr>
	<tr><td>NA</td><td>2017-02-06</td><td>NA</td><td>NA</td><td>NA</td><td>000001</td><td>平安银行</td><td>0.00305</td><td>9.31</td><td>480441331</td><td>157506484</td></tr>
	<tr><td>NA</td><td>2017-02-07</td><td>NA</td><td>NA</td><td>NA</td><td>000001</td><td>平安银行</td><td>0.00235</td><td>9.30</td><td>368755274</td><td>157337304</td></tr>
</tbody>
</table>



## 4. 策略1
对机构介入的、上了龙虎榜的股，不管是否涨跌停，只要机构净买入占总成交额比＞1.5％或者机构净买额占总成交额比（A％），换手率（B％），A×B＞＝20的股；选出来，再第二天的涨跌幅±2％内的股，判第三天的涨幅。第三天累积涨跌幅±3％的股，判第四天涨幅。第五天累积涨跌幅±3％的股，判第六天涨幅。


```R
DTanalysis_DT <- DTanalysis[order(stock_symbol, date), .SD # 首先根据股票和日期排序
    ][, net_buy_inst_num := buy_inst_num - sell_inst_num # 看机构净买入量
    ][, ret := Clsprc/shift(Clsprc, type = "lag", n = 1L) - 1, by = .(stock_symbol) # 计算每天的收益率
    ][, ret_2nd := shift(Clsprc, type = "lead", n = 1L)/Clsprc - 1, by = .(stock_symbol)# 计算第2天的收益率
    ][, ret_3rd := shift(Clsprc, type = "lead", n = 2L)/shift(Clsprc, type = "lead", n = 1L) - 1, by = .(stock_symbol)# 计算第3天的收益率
    ][, ret_4th := shift(Clsprc, type = "lead", n = 3L)/shift(Clsprc, type = "lead", n = 2L) - 1, by = .(stock_symbol)# 计算第4天的收益率
    ][, ret_5th := shift(Clsprc, type = "lead", n = 4L)/shift(Clsprc, type = "lead", n = 3L) - 1, by = .(stock_symbol)# 计算第5天的收益率
    ][, ret_6th := shift(Clsprc, type = "lead", n = 5L)/shift(Clsprc, type = "lead", n = 4L) - 1, by = .(stock_symbol)# 计算第6天的收益率
    ][, ret_7th := shift(Clsprc, type = "lead", n = 6L)/shift(Clsprc, type = "lead", n = 5L) - 1, by = .(stock_symbol)# 计算第7天的收益率       
    ][!is.na(buy_inst_num), .SD
    ]
DTanalysis_DT[1:5]
```


<table class="dataframe">
<caption>A data.table: 5 × 19</caption>
<thead>
	<tr><th scope=col>buy_inst_num</th><th scope=col>date</th><th scope=col>rank_reason</th><th scope=col>sell_inst_num</th><th scope=col>stock_name</th><th scope=col>stock_symbol</th><th scope=col>ShortName</th><th scope=col>Turnover</th><th scope=col>Clsprc</th><th scope=col>Dnvaltrd</th><th scope=col>Dsmvosd</th><th scope=col>net_buy_inst_num</th><th scope=col>ret</th><th scope=col>ret_2nd</th><th scope=col>ret_3rd</th><th scope=col>ret_4th</th><th scope=col>ret_5th</th><th scope=col>ret_6th</th><th scope=col>ret_7th</th></tr>
	<tr><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;date&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td> 8658.03</td><td>2017-07-11</td><td>日涨幅偏离值达7%的证券                    </td><td>    0.00</td><td>平安银行</td><td>000001</td><td>平安银行</td><td>0.02253</td><td>10.25</td><td>3842010171</td><td>173409394</td><td> 8658.03</td><td> 0.06882169</td><td> 0.008780488</td><td> 0.054158607</td><td> 0.000000000</td><td>-0.008256881</td><td> 0.022201665</td><td> 0.00361991</td></tr>
	<tr><td>28154.20</td><td>2021-02-25</td><td>日涨幅偏离值达7%的证券                    </td><td>22422.10</td><td>万科A   </td><td>000002</td><td>万科A   </td><td>0.02671</td><td>32.99</td><td>8382663604</td><td>320582082</td><td> 5732.10</td><td> 0.10003334</td><td> 0.003334344</td><td> 0.007552870</td><td>-0.001799100</td><td> 0.006308201</td><td>-0.024179104</td><td>-0.03517895</td></tr>
	<tr><td>  769.45</td><td>2021-06-09</td><td>连续三个交易日内,涨幅偏离值累计达20%的证券</td><td>  788.98</td><td>国华网安</td><td>000004</td><td>国华网安</td><td>0.11303</td><td>19.82</td><td> 246709411</td><td>  2281790</td><td>  -19.53</td><td> 0.09988901</td><td> 0.099899092</td><td> 0.100000000</td><td>-0.100083403</td><td>-0.066265060</td><td> 0.038213400</td><td>-0.05449331</td></tr>
	<tr><td>    0.00</td><td>2019-09-03</td><td>日涨幅偏离值达7%的证券                    </td><td>  527.69</td><td>世纪星源</td><td>000005</td><td>世纪星源</td><td>0.09123</td><td> 3.48</td><td> 330930683</td><td>  3681653</td><td> -527.69</td><td> 0.10126582</td><td> 0.100574713</td><td>-0.036553525</td><td>-0.035230352</td><td>-0.002808989</td><td>-0.008450704</td><td>-0.01136364</td></tr>
	<tr><td>    0.00</td><td>2020-10-14</td><td>日跌幅偏离值达7%的证券                    </td><td> 1080.73</td><td>深振业A </td><td>000006</td><td>深振业A </td><td>0.05205</td><td> 6.39</td><td> 462640390</td><td>  8615688</td><td>-1080.73</td><td>-0.10000000</td><td>-0.035993740</td><td> 0.006493506</td><td> 0.003225806</td><td>-0.006430868</td><td>-0.012944984</td><td> 0.00000000</td></tr>
</tbody>
</table>




```R

```
