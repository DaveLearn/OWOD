# Step 1) Copy the shared models to <your_location>/OWOD/output/ and
# Step 2) Copy the shared data to <your_location>/OWOD/datasets/VOC2007

# code expects CUDA_HOME to be defined but doesn't use it as far as i can tell.
export CUDA_HOME='~'

# Python Weibull distribution is only defined for > 0, the Test phase can fail due to negative values when calculating log prob. We set this to skip checks.
export PYTHONOPTIMIZE=TRUE


# Task 1: Start
python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52133' --config-file ./configs/OWOD/t1/t1_val.yaml OWOD.TEMPERATURE 1.5 OUTPUT_DIR "./output/t1_final"

python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t1/t1_test.yaml  OUTPUT_DIR "./output/t1_final"
# Task 1: End


# Task 2: Start
python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52133' --config-file ./configs/OWOD/t2/t2_val.yaml OWOD.TEMPERATURE 1.5 OUTPUT_DIR "./output/t2_final"

python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t2/t2_test.yaml OUTPUT_DIR "./output/t2_final"
# Task 2: End

# Task 3: Start
python tools/train_net.py --num-gpus 1 --dist-url='tcp://127.0.0.1:52133' --config-file ./configs/OWOD/t3/t3_val.yaml OWOD.TEMPERATURE 1.5 OUTPUT_DIR "./output/t3_final"

python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t3/t3_test.yaml OUTPUT_DIR "./output/t3_final"
# Task 3: End

# Task 4: Start
python tools/train_net.py --num-gpus 1 --eval-only --config-file ./configs/OWOD/t4/t4_test.yaml OUTPUT_DIR "./output/t4_final"
# Task 4: End