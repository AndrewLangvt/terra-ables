#!/usr/bin/env python3

''' This script should be run from the cloud environment within a Terra workspace. 
Once files have been uploaded into a Terra workspace, this script will generate 
a sample table with pointers to all fastq.gz files in a provided directory.'''

import sys
import subprocess
from datetime import datetime as dt

location = sys.argv[1]

class reads:
    def __init__(self):
        self.read1 = ''
        self.read2 = ''

read_dict = {}
#print(f'gsutil ls {location}')
p = subprocess.run(f'gsutil ls {location}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
for line in p.stdout.split('\n'):
#       print(line)
        if '_R1_001.fastq.gz' in line:
                samplename = line.split('/')[-1].split('_')[0]
                print(f'found right read for {samplename}')
                if samplename in read_dict.keys():
                        sample = read_dict[samplename]
                else:
                        sample = reads()
                sample.read1 = line
                read_dict[samplename] = sample
        elif '_R2_001.fastq.gz' in line:
                samplename = line.split('/')[-1].split('_')[0]
                print(f'found left read for {samplename}')
                if samplename in read_dict.keys():
                        sample = read_dict[samplename]
                else:
                        sample = reads()
                sample.read2 = line
                read_dict[samplename] = sample
        else:
                pass
fname = f'_sampletable_{location.rstrip("/").split("/")[-1]}_{str(dt.now().strftime("%Y%m%d_%H%M%S"))}.tsv'
outfile = open(fname, 'w')
outfile.write('entity:sample_id\tread1\tread2\n')
for samplename, read_info in read_dict.items():
        outfile.write(f'{samplename}\t{read_info.read1}\t{read_info.read2}\n')
outfile.close()

print(f'copying {fname} to {location}')
subprocess.run(f'gsutil cp {fname} {location}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
