# CMCGEC
We realise **CMCGEC** (**C**leaned **M**ulti-reference Datasets for **C**hinese **G**rammatical **E**rror **C**orrection) in this repository.

## Raw Data

We decide to officially open source all the raw data of MuCGEC and NaSGEC. In addition, we also collect the data of FCGEC and NaCGEC. We convert all datasets into the following formats:
```
[idx][\t][src][\t][tgt][\t][tgt] ...
```
The source and description of each dataset can be found in their respective README.

## Data Processing
We perform the following processing steps: 
- Get para file from M2 file of MuCGEC-Test
- Remove special tag in MuCGEC, NaSGEC and NaCGEC
- Handle data leakage problem for native speaker CGEC datasets
- Correct unreasonable csc error for FCGEC-Dev and NaSGEC-Exam

Please refer to [process_cgec_data.sh](process_cgec_data.sh) for details of the processing procedure for converting ```raw_cgec``` to ```cmcgec```.