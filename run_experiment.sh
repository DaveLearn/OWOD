#!/usr/bin/env bash
# General flow: tx_train.yaml -> tx_ft -> tx_val -> tx_test

# tx_train: trains the model.
# tx_ft: uses data-replay to address forgetting. (refer Sec 4.4 in paper)
# tx_val: learns the weibull distribution parameters from a kept aside validation set.
# tx_test: evaluate the final model
# x above can be {1, 2, 3, 4}

# NB: Please edit the paths accordingly.
# NB: Please change the batch-size and learning rate if you are not running on 8 GPUs.
# (if you find something wrong in this, please raise an issue on GitHub)

# we use relative paths so ensure we are running from the correct directory.
cd "$(dirname "${BASH_SOURCE[0]}")" || exit

# Python Weibull distribution is only defined for > 0, the Test phase can fail due to -ve values when calculating log prob. We set this to skip checks.
export PYTHONOPTIMIZE=TRUE
export CUDA_HOME=~

SUFFIX=""

if [[ $1 = '--fast' ]]; then
    shift
    SUFFIX="_fast"
fi

OUTDIR=$1

if [[ -z $OUTDIR ]]; then
    echo "Usage run_experiment.sh [--fast] <outputfolder>"
    exit 1
fi

mkdir -p "$OUTDIR"


clean_folder () {
    rm -f "$1"/model_[0123456789]*   
}

collect_stats () {
    python tools/extract_stats.py < "$1"/log.txt > "$1"/stats.json
}

task_1 () {

    if [[ -e $OUTDIR/t1 ]] || [[ -e $OUTDIR/t1_final ]]; then
       echo "Task 1 folder already exists! - aborting"
       exit 1
    fi

    # Task 1
    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52125' --config-file ./configs/OWOD/t1/t1_train${SUFFIX}.yaml OUTPUT_DIR "$OUTDIR/t1"

    echo "Using code in commit: $(git log --pretty=oneline -n 1)" >> "$OUTDIR"/t1/log.txt
    # No need to finetune in Task 1, as there is no incremental component.
    clean_folder "$OUTDIR"/t1

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52133' --config-file ./configs/OWOD/t1/t1_val.yaml OWOD.TEMPERATURE 1.5 OUTPUT_DIR "$OUTDIR/t1_final" MODEL.WEIGHTS "$OUTDIR/t1/model_final.pth"
    #echo "Using code in commit: $(git log --pretty=oneline -n 1)" >> ./output/t1_final/log.txt

    python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t1/t1_test.yaml  OUTPUT_DIR "$OUTDIR/t1_final" MODEL.WEIGHTS "$OUTDIR/t1/model_final.pth"

    collect_stats "$OUTDIR"/t1_final
}

task_2 () {

    if [[ -e $OUTDIR/t2 ]] || [[ -e $OUTDIR/t2_ft ]] || [[ -e $OUTDIR/t2_final ]]; then
       echo "Task 2 folder already exists! - aborting"
       exit 1
    fi

    # Task 2
    mkdir -p "$OUTDIR"/t2
    echo "Using code in commit: $(git log --pretty=oneline -n 1)" >> "$OUTDIR"/t2/log.txt

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52127' --config-file ./configs/OWOD/t2/t2_train${SUFFIX}.yaml OUTPUT_DIR "$OUTDIR/t2"

    clean_folder "$OUTDIR"/t2
    #cp -r -T "$OUTDIR"/t2 "$OUTDIR"/t2_ft

    #python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52126' --config-file ./configs/OWOD/t2/t2_ft${SUFFIX}.yaml OUTPUT_DIR "$OUTDIR/t2_ft" MODEL.WEIGHTS "$OUTDIR/t2_ft/model_final.pth"
    
    #clean_folder "$OUTDIR"/t2_ft

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52133' --config-file ./configs/OWOD/t2/t2_val.yaml OWOD.TEMPERATURE 1.5 OUTPUT_DIR "$OUTDIR/t2_final" MODEL.WEIGHTS "$OUTDIR/t2/model_final.pth"
    
    echo "Using code in commit: $(git log --pretty=oneline -n 1)" >> "$OUTDIR"/t2_final/log.txt
    python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t2/t2_test.yaml OUTPUT_DIR "$OUTDIR/t2_final" MODEL.WEIGHTS "$OUTDIR/t2/model_final.pth"

    collect_stats "$OUTDIR"/t2_final
}

task_3 () {

    if [[ -e $OUTDIR/t3 ]] || [[ -e $OUTDIR/t3_ft ]] || [[ -e $OUTDIR/t3_final ]]; then
       echo "Task 3 folder already exists! - aborting"
       exit 1
    fi

    # Task 3
    mkdir -p "$OUTDIR"/t3
    echo "Using code in commit: $(git log --pretty=oneline -n 1)" >> "$OUTDIR"/t3/log.txt
    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52127' --config-file ./configs/OWOD/t3/t3_train${SUFFIX}.yaml OUTPUT_DIR "$OUTDIR/t3"

    clean_folder "$OUTDIR"/t3
   # cp -r "$OUTDIR"/t3 "$OUTDIR"/t3_ft

   # python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52126' --config-file ./configs/OWOD/t3/t3_ft${SUFFIX}.yaml OUTPUT_DIR "$OUTDIR/t3_ft" MODEL.WEIGHTS "$OUTDIR/t3_ft/model_final.pth"
    
   # clean_folder "$OUTDIR"/t3_ft

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52133' --config-file ./configs/OWOD/t3/t3_val.yaml OWOD.TEMPERATURE 1.5 OUTPUT_DIR "$OUTDIR/t3_final" MODEL.WEIGHTS "$OUTDIR/t3/model_final.pth"

    echo "Using code in commit: $(git log --pretty=oneline -n 1)" >> "$OUTDIR"/t3_final/log.txt
    python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t3/t3_test.yaml OUTPUT_DIR "$OUTDIR/t3_final" MODEL.WEIGHTS "$OUTDIR/t3/model_final.pth"

    collect_stats "$OUTDIR"/t3_final
}

task_4 () {

    if [[ -e $OUTDIR/t4 ]] || [[ -e $OUTDIR/t4_ft ]] || [[ -e $OUTDIR/t4_final ]]; then
       echo "Task 4 folder already exists! - aborting"
       exit 1
    fi

    # Task 4
    mkdir -p "$OUTDIR"/t4
    echo "Using code in commit: $(git log --pretty=oneline -n 1)" >> "$OUTDIR"/t4/log.txt

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52127' --config-file ./configs/OWOD/t4/t4_train${SUFFIX}.yaml OUTPUT_DIR "$OUTDIR/t4"

    clean_folder "$OUTDIR"/t4
  #  cp -r "$OUTDIR"/t4 "$OUTDIR"/t4_ft

  #  python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52126' --config-file ./configs/OWOD/t4/t4_ft${SUFFIX}.yaml OUTPUT_DIR "$OUTDIR/t4_ft" MODEL.WEIGHTS "$OUTDIR/t4_ft/model_final.pth"
    
   # clean_folder "$OUTDIR"/t4_ft

    echo "Using code in commit: $(git log --pretty=oneline -n 1)" >> "$OUTDIR"/t4_final/log.txt
    python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t4/t4_test.yaml OUTPUT_DIR "$OUTDIR/t4_final" MODEL.WEIGHTS "$OUTDIR/t4/model_final.pth"
    
    collect_stats "$OUTDIR"/t4_final
}

task_1
task_2
task_3
task_4
