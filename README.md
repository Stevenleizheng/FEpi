# FEπ: Fine-tuned ESM2 for Peptidase identification
## Description
The primary goal of FEpi is to accurately identify peptidase in multiple predicted protein sequences. Currently, there is a lack of one-stop tools for specifically mining peptidases.We apply fine-tuned ESM2 to develop a specific peptide enzyme identification model universally applicable for users in need.

## Steps to predict
### Step 1: Prepare the environment
(1) Download the FEpi software from github

``git clone https://github.com/Stevenleizheng/FEpi/tree/main``

(2) Go to the directory of FEpi, for example:

``cd FEpi``

(3) Create a new conda environment and partial required softwares:

``conda env create -f fepi.yaml``

(4) Enter the conda environment

``conda activate fepi``

(5) Install the pytorch software

If you want to use the CPU version, please go to https://pytorch.org/get-started and get the pip install command or run 
``pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu``

If you want to use the GPU version, please go to https://pytorch.org/get-started and get the pip install command according to your device and demand.

### Step 2: Download the trained model
(1) Download the model (The working path is still 'FEpi'). The model parameter file is saved at: https://zenodo.org/records/14878564. The file size is 1.6 GB.

``wget -c https://zenodo.org/records/14878564/files/model_param.tar.gz``

or

``wget -c https://zenodo.org/records/14878564/files/model_param.tar.gz?download=1``

(2) Unpack the file

``tar xzvf model_param.tar.gz``

### (Optional) Step 3: Test the software
Run this command (a test prediction with 103 proteins) to see whether the software has installed correctly using CPU.

``python main.py -i Testset/demo.fasta -b 32``

If the software is installed correctly and completely, this step will finish in less than 10 minutes (might be longer if your device is too old) without any errors. The results of the test prediction will be saved in the result folder.

Run this command (a test prediction with 103 proteins) to see whether the software has installed correctly using GPU (e.g. NVIDIA A40).

``python main.py -i Testset/demo.fasta -g 0``

If the software is installed correctly and completely, this step will finish in less than 3 minutes (might be longer if your device is too old) without any errors. The results of the test prediction will be saved in the result folder.

### Step 4: Prediction

(1) Preparations

Your proteins in a fasta file (path: xxx.fa). A directory to save the output files (path: xxx/). If you want to use GPU(s), please prepare the IDs of the GPU(s) you want to use, for example, a single-GPU machine, here it is prepared to be 0; multi-GPU machine using only one GPU, here it is prepared as x (x is the GPU ID used); multi-GPU machine using multiple GPUs, here it is prepared as x1,x2,... (x1,x2,... are the GPU IDs you want to use).

(2) Prediction

CPU: python main.py -i xxx.fa 

single GPU machine: python main.py -i xxx.fa -g '0'

multi GPU machine, using one GPU: python main.py -i xxx.fa -g 'x'

multi GPU machine, using multi GPUs: python main.py -i xxx.fa -g 'x1,x2,...'

-o determines the output directory, -g determines the IDs of GPUs you want to use (not given -g, will use CPU)

If you want to change the batch size (default is 2), please use -b, please note that the batch size cannot be negative and should not be smaller than the number of GPUs used.

If you want to change the threshold of binary task (default is 0.5), please use -t. You can set the number between 0 and 1. Example commands:

Predict proteins in 'example.fasta', save the results to 'result/', and batch size is 64. The intermediate process data is saved in the 'data/' directory.

CPU: python main.py -i example.fa  -b 64 -d data/ -o result/

single GPU machine: python main.py -i example.fa -g '0' -b 64 -d data/ -o result/

multi GPU machine, using one GPU (ID:2): python main.py -i example.fa -g '2' -b 64 -d data/ -o result/

multi GPU machine, using eight GPUs (ID:0-7): python main.py -i example.fa -g '0,1,2,3,4,5,6,7' -b 16 -d data/ -o result/

The descriptions for the result files are in the 'binary_result.txt' file of the output directory.

The other parameter is -t, which controls the threshold for binary classification models (ranging from 0 to 1, default is 0.5). A higher value increases the confidence in the selected peptidases, while a lower value allows for the detection of more peptidases, but may also result in a higher rate of false positives.