#!/usr/bin/env bash
set -euo pipefail

python script/get_sub_meta_csv.py raw_data/metadata.csv raw_data/comm_use_subset/sub_meta.csv sha title abstract authors publish_time journal
python load_index.py covid_sample_index raw_data/comm_use_subset sub_meta.csv