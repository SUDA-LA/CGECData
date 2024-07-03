# CMCGEC
We realise **CMCGEC** (**C**leaned **M**ulti-reference Datasets for **C**hinese **G**rammatical **E**rror **C**orrection) in this repository.

## Raw Data

We decide to officially open source all the raw data of MuCGEC and NaSGEC. In addition, we also collect the data of FCGEC and NaCGEC. We convert all datasets into the following formats:
```
[idx][\t][src][\t][tgt][\t][tgt] ...
```
The source and description of each dataset can be found in their respective README.

## Data Processing
The shell script [process_cgec_data.sh](process_cgec_data.sh) is used to convert ```raw_cgec``` to ```cmcgec```.

We perform the following processing steps: 
- Remove special tag in MuCGEC, NaSGEC and NaCGEC
- Handle data leakage problem for native speaker CGEC datasets
- Correct unreasonable spelling error, which is mainly caused by OCR, for FCGEC-Dev and NaSGEC-Exam (A large number of spelling errors are omitted by human annotators)

Details of the hyperparameters and processing steps can be found in the script.
