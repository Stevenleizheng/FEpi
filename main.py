import os
import sys
import argparse
import subprocess
from utilis import Timer

def argument():
    """Parse command line arguments for binary classification prediction
    
    Returns:
        tuple: (fasta_path, strgpu, batch_size, threshold, data_path, output)
            - fasta_path: Path to the fasta file.
            - strgpu: GPU device numbers
            - batch_size: Batch size for inference
            - threshold: Classification probability cutoff
            - data_path: Directory containing input data
            - output: Results output directory
    """
    parser = argparse.ArgumentParser(description='Binary task prediction')
    parser.add_argument('-i', '--fasta_data', type=str, help='fasta file path')
    parser.add_argument('-g', '--gpu', type=str, default='None', help="the number of GPU,(eg. '1')")
    parser.add_argument('-b', '--batch_size', type=int, default=2, help='batch size,(eg. 2)')
    parser.add_argument('-t', '--threshold', type=float, default=0.5, help='threshold,(eg. 0.5)')
    parser.add_argument('-d', '--data_path', type=str, default=os.path.join(os.getcwd(), 'data/'), help='data file path')
    parser.add_argument('-o', '--output', type=str, default=os.path.join(os.getcwd(), 'result/'), help='output,(eg. result)')
    args = parser.parse_args()
    fasta_path = args.fasta_data
    strgpu = args.gpu
    batch_size = args.batch_size
    threshold = args.threshold
    data_path = args.data_path
    output = args.output
    return fasta_path, strgpu, batch_size, threshold, data_path, output

def main():
    """Main execution function for the FEpi pipeline.
    
    This function orchestrates the two main stages of the FEpi pipeline:
    1. Data preparation and tokenization
    2. Binary prediction using the trained model
    """
    fasta_path, strgpu, batch_size, threshold, data_path, output = argument()
    cmds = [
            ['python', f'{sys.path[0]}/1.data_preparation.py', '-i', f'{fasta_path}', '-d', f'{data_path}'],
            ['python', f'{sys.path[0]}/2.binary_prediction.py', '-g', f'{strgpu}', '-b', f'{batch_size}', '-t', f'{threshold}', '-d', f'{data_path}', '-o', f'{output}'],
    ]
    sens =[
        'Data preparation(token) has been done.',
        'Binary prediction has been done.'
        ]
    for cmd, sen in zip(cmds,sens):    
        timer = Timer()
        subprocess.run(cmd)
        print(sen)
        timer.stop()
        timer.sum()
    print('All finished.')

if __name__ =="__main__":
    main()