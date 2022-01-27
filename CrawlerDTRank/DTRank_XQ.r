library(styleer)
trading <- fread("./CrawlerDTRank/TRD_Dalyr.txt", encoding = "UTF-8")
setnames(trading, 1:2, c("stock_symbol", "date"))
dtrank <- fread("./CrawlerDTRank/DTRank.csv", encoding = "UTF-8")
dtanly <- dtrank[trading, on = .(stock_symbol, date)
    ][order(stock_symbol, date), .SD
    ][, stock_symbol := str_pad(stock_symbol, 6, side = "left", pad = "0")
    ][, ret := Clsprc/shift(Clsprc) - 1, by = .(stock_symbol)
    ][!is.na(ret), .SD
    ][ret > 0.09 & buy_inst_num > sell_inst_num, .SD
    ]
