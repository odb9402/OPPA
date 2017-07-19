#main function called by python.
py_spp <- function(file_name, control_name, fdr=0.01) {

library(parallel)
library(multicore)
library(spp)

options(spp.core = detectCores())

chip_data <- BAMTags()
chip_data$read(file=file_name)
chip_data$compute.cross.cor(srange=c(-100,500), bin=10)

control_data <- BAMTags()
control_data$read(file=control_name)
control_data$compute.cross.cor(sragne=c(-100,500), bin=10)

conf<- IPconf(ChIP=chip_data, Input=control_data)
conf$binding_position$set.param(fdr, method="tag.wtd", add_broad_peak_reg=TRUE)
conf$binding_position$identify()

#make output file name
output_name = substr(file_name, 0, nchar(file_name) - 4)
output_name = paste(output_name, ".narrowpeak", sep="")

conf$binding_position$write.narrowpeak(file=output_name)
}
