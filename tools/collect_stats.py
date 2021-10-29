import os
from posixpath import basename
import sys
import shutil

script_path = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
dest_path = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else None

if len(sys.argv) <= 2:
    print("usage: collect_stats.py <output_folder> <destination_folder>")
    exit(1)


if output_path is None:
    print("No folder provided to process")
    exit(1)

if dest_path is None:
    print("No destination folder provided")
    exit(1)
    
if not os.path.exists(output_path):
    print(f'path not found: {output_path}')

if not os.path.exists(dest_path):
    print(f'destination path not found: {dest_path} ')

os.system(f"python {script_path}/collate_stats.py {output_path}")

experiment_name = os.path.basename(output_path)

shutil.copy(os.path.join(output_path,'stats.json'), os.path.join(dest_path, f'{experiment_name}.json'))
print(f" Collected stats from {os.path.basename(output_path)} => {os.path.join(dest_path, f'{experiment_name}.json')}")