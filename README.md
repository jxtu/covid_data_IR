# COVID Open Research Dataset Indexing and Visualization

## Data preparation
You can find all COVID19-related datasets [here](https://pages.semanticscholar.org/coronavirus-research).
I am using [Metadata file](https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-27/metadata.csv) and 
[Commercial use subset](https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-27/comm_use_subset.tar.gz) (click to download).

Make sure you have a `raw_data/` folder to hold all your data files.

## Getting set up
Make sure your elasticsearch and kibana have the same version.
I am testing on MacOS with version 7.5.0. After install the elastic packages, run:

```
./bin/elasticsearch
./bin/kibana
```

## Inspect your single json doc:

```
./inspect.sh
```


## Parse Meta data and Build Elasticseach index

```
./build_index.sh
```

