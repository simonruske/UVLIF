
#!/usr/bin/env Rscript

# load the cluster index package
library(clusterCrit)

args = commandArgs(trailingOnly=TRUE)

load_file <- function(filename, m, n, byrow){
  return(matrix(scan(filename, sep = ',', skip = '\n'), nrow<-m, ncol<-n, byrow = byrow))
}

test <- function(data, cl, index)
{
tryCatch({
res <- vector()


for(k in 2:10)
{
  clustering <- as.integer(cl[,k])
  res <-c(res, as.numeric(intCriteria(data, clustering, index)))
}

idx <- bestCriterion(as.numeric(res), index) + 1
print(c(index, "Best clustering found for ", idx))
},
error = function(e){print(clust_idx)})
}




# main code

# load the data and flat clusterings
data <- load_file(args[2], as.integer(args[3]), as.integer(args[4]), byrow = TRUE)
cl <- load_file(args[1], as.integer(args[6]), as.integer(args[5]), byrow = FALSE)

# get the names of the different clustering indices
start.time <- Sys.time()
names <- getCriteriaNames(isInternal = TRUE)
for(index in c("calinski_harabasz", "GDI23", "PBM", "silhouette"))
{
test(data, cl, index)
}
end.time <- Sys.time()
time.taken <- end.time - start.time
print(time.taken)


