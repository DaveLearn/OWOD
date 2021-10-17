#!/bin/bash

$OUTDIR = /output/ncm-cutoff-no-norm/exp_$1
if [[ -e $OUTDIR ]]; then
       echo "$OUTDIR folder already exists! - aborting"
       exit 1
fi
mkdir -p $OUTDIR
python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t1/t1_test.yaml OUTPUT_DIR $OUTDIR MODEL.WEIGHTS ./output/ncm-cutoff-no-norm/t1/model_final.pth