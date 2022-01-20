library(styleer)
library(mongolite)
mongo_client <- mongo(collection = 'post_info', db = 'GubaFuture', url = 'mongodb://localhost')
post_info <- mongo_client$find() %>% as.data.table()
post_info

