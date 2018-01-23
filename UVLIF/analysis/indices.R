#!/usr/bin/env Rscript

# load the cluster index package
library(clusterCrit)

args = commandArgs(trailingOnly=TRUE)

load_file <- function(filename, m, n, byrow){
  return(matrix(scan(filename, sep = ',', skip = '\n'), nrow<-m, ncol<-n, byrow = byrow))
}

test <- function(data, cl, clust_idx)
{
tryCatch({
index <- getCriteriaNames(isInternal = TRUE)[clust_idx]
print(c("Trying clustering index ", index))
res <- vector()


for(k in 2:10)
{
  print(c("Considering ", k, " clusters"))
  clustering <- as.integer(cl[,k])
  res <-c(res, as.numeric(intCriteria(data, clustering, index)))
}

idx <- bestCriterion(as.numeric(res), index) + 1
print(res)
print(c("Best clustering found for ", idx))
},
error = function(e){print(clust_idx)})
}




# main code

# load the data and flat clusterings
data <- load_file(args[2], as.integer(args[3]), as.integer(args[4]), byrow = TRUE)
cl <- load_file(args[1], as.integer(args[6]), as.integer(args[5]), byrow = FALSE)
print(data[1,])
print(cl[,1])

# get the names of the different clustering indices
names <- getCriteriaNames(isInternal = TRUE)
for(clust_idx in 1:length(names))
{
test(data, cl, clust_idx)
}
