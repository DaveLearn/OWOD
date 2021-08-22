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
cd "$(dirname ${BASH_SOURCE[0]})"

# Python Weibull distribution is only defined for > 0, the Test phase can fail due to -ve values when calculating log prob. We set this to skip checks.
export PYTHONOPTIMIZE=TRUE

task_1 () {
    # Task 1
    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52125' --config-file ./configs/OWOD/t1/t1_train.yaml OUTPUT_DIR "./output/t1"

    # No need to finetune in Task 1, as there is no incremental component.

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52133' --config-file ./configs/OWOD/t1/t1_val.yaml OWOD.TEMPERATURE 1.5 OUTPUT_DIR "./output/t1_final" MODEL.WEIGHTS "./output/t1/model_final.pth"

    python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t1/t1_test.yaml  OUTPUT_DIR "./output/t1_final" MODEL.WEIGHTS "./output/t1/model_final.pth"
}

task_2 () {
    # Task 2
    cp -r ./output/t1 ./output/t2

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52127' --config-file ./configs/OWOD/t2/t2_train.yaml OUTPUT_DIR "./output/t2" MODEL.WEIGHTS "./output/t2/model_final.pth"

    cp -r ./output/t2 ./output/t2_ft

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52126' --config-file ./configs/OWOD/t2/t2_ft.yaml OUTPUT_DIR "./output/t2_ft" MODEL.WEIGHTS "./output/t2_ft/model_final.pth"

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52133' --config-file ./configs/OWOD/t2/t2_val.yaml OWOD.TEMPERATURE 1.5 OUTPUT_DIR "./output/t2_final" MODEL.WEIGHTS "./output/t2_ft/model_final.pth"

    python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t2/t2_test.yaml OUTPUT_DIR "./output/t2_final" MODEL.WEIGHTS "./output/t2_ft/model_final.pth"
}

task_3 () {
    # Task 3
    cp -r ./output/t2_ft ./output/t3

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52127' --config-file ./configs/OWOD/t3/t3_train.yaml OUTPUT_DIR "./output/t3" MODEL.WEIGHTS "./output/t3/model_final.pth"

    cp -r ./output/t3 ./output/t3_ft

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52126' --config-file ./configs/OWOD/t3/t3_ft.yaml OUTPUT_DIR "./output/t3_ft" MODEL.WEIGHTS "./output/t3_ft/model_final.pth"

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52133' --config-file ./configs/OWOD/t3/t3_val.yaml OWOD.TEMPERATURE 1.5 OUTPUT_DIR "./output/t3_final" MODEL.WEIGHTS "./output/t3_ft/model_final.pth"

    python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t3/t3_test.yaml OUTPUT_DIR "./output/t3_final" MODEL.WEIGHTS "./output/t3_ft/model_final.pth"
}

task_4 () {
    # Task 4
    cp -r ./output/t3_ft ./output/t4

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52127' --config-file ./configs/OWOD/t4/t4_train.yaml OUTPUT_DIR "./output/t4" MODEL.WEIGHTS "./output/t4/model_final.pth"

    cp -r ./output/t4 ./output/t4_ft

    python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52126' --config-file ./configs/OWOD/t4/t4_ft.yaml OUTPUT_DIR "./output/t4_ft" MODEL.WEIGHTS "./output/t4_ft/model_final.pth"

    python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t4/t4_test.yaml OUTPUT_DIR "./output/t4_final" MODEL.WEIGHTS "./output/t4_ft/model_final.pth"
}

task_1
task_2
task_3
task_4
