prefix <- "http://cbio.ensmp.fr/~thocking/chip-seq-chunk-db"

## Download a table of meta-data, with 1 row for each annotated
## chunk/window.
load(url(sprintf("%s/chunks.RData", prefix)))

### Define what chunk and peaks to download.
set.name <- "H3K36me3_TDH_immune"
chunk.id <- 1
algorithm <- "hmcan.broad.trained"

### Download the data.
load(url(sprintf("%s/%s/%s/error/%s.RData", prefix, set.name, chunk.id, algorithm)))
load(url(sprintf("%s/%s/%s/peaks/%s.RData", prefix, set.name, chunk.id, algorithm)))
load(url(sprintf("%s/%s/%s/signal.RData", prefix, set.name, chunk.id)))
load(url(sprintf("%s/%s/%s/regions.RData", prefix, set.name, chunk.id)))
load(url(sprintf("%s/%s/%s/counts.RData", prefix, set.name, chunk.id)))

### Select the peaks.
show.param <- "5"
param.list <- split(error, error$param.name)
param.regions <- param.list[[show.param]]
param.peaks <- peaks[[show.param]]

### Compute the PeakError.
if(!require(PeakError)){
  library(devtools)
  install_github("tdhock/PeakError")
  library(PeakError)
}
peak.list <- split(param.peaks, param.peaks$sample.id)
region.list <- split(regions, regions$sample.id)
error.list <- split(param.regions, param.regions$sample.id)
for(sample.id in names(peak.list)){
  sample.peaks <- peak.list[[sample.id]]
  sample.regions <- region.list[[sample.id]]
  computed.error <- PeakErrorChrom(sample.peaks, sample.regions)
  ## Check that the error computed above is the same as the error
  ## below, which was downloaded from the benchmark web site.
  expected.error <- error.list[[sample.id]]
  stopifnot(expected.error$status == computed.error$status)
}

### Plot the signal, peaks, and show which regions contain errors.
library(ggplot2)
geom_tallrect <- function(mapping=NULL, data=NULL, stat="identity", position="identity", ...){
  require(proto)
  GeomTallRect <- proto(ggplot2:::GeomRect,{
    objname <- "tallrect"
    required_aes <- c("xmin", "xmax")
    draw <- draw_groups <- function(.,data,scales,coordinates,
                                    ymin=0,ymax=1,...){
      ymin <- grid::unit(ymin,"npc")
      ymax <- grid::unit(ymax,"npc")
      with(ggplot2:::coord_transform(coordinates, data, scales),
           ggname(.$my_name(), {
        rectGrob(xmin, ymin, xmax - xmin, ymax-ymin,
                 default.units = "native", just = c("left", "bottom"),
                 gp=gpar(
                   col=colour, fill=alpha(fill, alpha),
                   lwd=size * .pt, lty=linetype, lineend="butt"
                   )
                 )
      }))
    }
  })
  GeomTallRect$new(mapping = mapping, data = data, stat = stat,
                   position = position, ...)
}

ann.colors <-
  c(noPeaks="#f6f4bf",
    peakStart="#ffafaf",
    peakEnd="#ff4c4c",
    peaks="#a445ee")

ggplot()+
  geom_tallrect(aes(xmin=chromStart/1e3, xmax=chromEnd/1e3,
                    fill=annotation),
                data=param.regions)+
  geom_line(aes(chromStart/1e3, coverage),
            data=signal, color="grey50")+
  geom_segment(aes(chromStart/1e3, 0,
                   xend=chromEnd/1e3, yend=0),
               data=param.peaks, size=2, color="deepskyblue")+
  geom_point(aes(chromStart/1e3, 0),
             data=param.peaks,
             pch=1, size=2, color="deepskyblue")+
  geom_tallrect(aes(xmin=chromStart/1e3, xmax=chromEnd/1e3,
                    linetype=status),
                data=param.regions,
                fill=NA, color="black", size=1)+
  scale_fill_manual("annotation", values=ann.colors,
                    breaks=names(ann.colors))+
  scale_linetype_manual("error type",
                        values=c(correct=0,
                          "false negative"=3,
                          "false positive"=1))+
  theme_bw()+
  theme(panel.margin=grid::unit(0, "cm"))+
  facet_grid(sample.id ~ ., scales="free",
             labeller=function(var, val){
               sub("McGill0", "", val)
             })+
  scale_y_continuous("normalized coverage from bigWig files",
                     labels=function(x){
                       sprintf("%.1f", x)
                     },
                     breaks=function(limits){
                       limits[2]
                     })+
  xlab("position on chromosome (kilo base pairs)")+
  guides(linetype=guide_legend(order=2,
           override.aes=list(fill="white")))+
  ggtitle(sprintf("%s parameter=%s on %s chunk %d",
                  algorithm, show.param, set.name, chunk.id))

ggplot()+
  geom_tallrect(aes(xmin=chromStart/1e3, xmax=chromEnd/1e3,
                    fill=annotation),
                data=param.regions)+
  geom_line(aes(chromStart/1e3, coverage),
            data=counts, color="grey50")+
  geom_segment(aes(chromStart/1e3, 0,
                   xend=chromEnd/1e3, yend=0),
               data=param.peaks, size=2, color="deepskyblue")+
  geom_point(aes(chromStart/1e3, 0),
             data=param.peaks,
             pch=1, size=2, color="deepskyblue")+
  geom_tallrect(aes(xmin=chromStart/1e3, xmax=chromEnd/1e3,
                    linetype=status),
                data=param.regions,
                fill=NA, color="black", size=1)+
  scale_fill_manual("annotation", values=ann.colors,
                    breaks=names(ann.colors))+
  scale_linetype_manual("error type",
                        values=c(correct=0,
                          "false negative"=3,
                          "false positive"=1))+
  theme_bw()+
  theme(panel.margin=grid::unit(0, "cm"))+
  facet_grid(sample.id ~ ., scales="free",
             labeller=function(var, val){
               sub("McGill0", "", val)
             })
  scale_y_continuous("aligned read coverage from bedtools genomecov -bga",
                     labels=function(x){
                       sprintf("%.1f", x)
                     },
                     breaks=function(limits){
                       limits[2]
                     })+
  xlab("position on chromosome (kilo base pairs)")+
  guides(linetype=guide_legend(order=2,
           override.aes=list(fill="white")))+
  ggtitle(sprintf("%s parameter=%s on %s chunk %d",
                  algorithm, show.param, set.name, chunk.id))