# Coco-Pack Verse (Coco-Pack-R)

This package contains tidyverse-style R code for Coco-Pack.

To use this code in R, you can either:

1. Source the individual scripts from this repo:

```R
if (!require(pacman)) {install.packages("pacman")}
pacman::p_load('devtools', 'glue')

repo_url <- 'https://raw.githubusercontent.com/ColinConwell/Coco-Pack/refs/heads/main'
remotes::source_url(glue('{repo_url}/verse/cocopack.R'))
```

 1. Install the standalone package ([Coco-Pack-R](https://github.io/ColinConwell/Coco-Pack-R)):

```R
devtools::install_github('colinconwell/Coco-Pack-R')
```
