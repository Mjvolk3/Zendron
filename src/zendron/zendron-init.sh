#!/usr/bin/env bash
eval "$(conda shell.bash hook)"
conda activate zendron
# TODO find a better option than clearing previous... cache should fix this.
python src/zendron/init.py
# don't need to see pod and should remove everytime
echo "Initialized, check conf/config.yaml"
