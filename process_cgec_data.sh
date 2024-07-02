# The whole process from raw_cgec to cmcgec

# Build tmp dir 
mkdir -p cmcgec/tmp
cp raw_cgec/MuCGEC/mucgec.dev.para cmcgec/tmp/
cp raw_cgec/FCGEC/fcgec.train.filtered.para cmcgec/tmp/fcgec.train.para
cp raw_cgec/FCGEC/fcgec.dev.para cmcgec/tmp/
cp raw_cgec/FCGEC/fcgec.test.para cmcgec/tmp/
cp raw_cgec/NaSGEC/NaSGEC-Exam/nasgec.exam.para cmcgec/tmp/
cp raw_cgec/NaSGEC/NaSGEC-Media/nasgec.media.para cmcgec/tmp/
cp raw_cgec/NaSGEC/NaSGEC-Thesis/nasgec.thesis.para cmcgec/tmp/
cp raw_cgec/NaCGEC/nacgec.para cmcgec/tmp/
python cgectk/m2_to_para.py \
    --m2_file raw_cgec/MuCGEC/mucgec.test.m2 \
    --input_file raw_cgec/MuCGEC/mucgec.test.input \
    --out_file cmcgec/tmp/mucgec.test.para \

# Remove special tag in MuCGEC, NaSGEC and NaCGEC
python cgectk/remove_special_tag.py \
    --data_dir cmcgec/tmp \
    --out_dir cmcgec/tmp/remove_special_tag \
    --file_names mucgec.dev.para,mucgec.test.para,nasgec.exam.para,nasgec.media.para,nasgec.thesis.para,nacgec.para

# Handle data leakage problem for NS CGEC datasets
mv cmcgec/tmp/fcgec.train.para cmcgec/tmp/remove_special_tag/
mv cmcgec/tmp/fcgec.dev.para cmcgec/tmp/remove_special_tag/
mv cmcgec/tmp/fcgec.test.para cmcgec/tmp/remove_special_tag/
python cgectk/handle_leakage.py \
    --data_dir cmcgec/tmp/remove_special_tag \
    --out_dir cmcgec/tmp/handle_leakage \
    --train_file fcgec.train.para \
    --extract_test_files nasgec.exam.para,nacgec.para  \
    --frozen_test_files fcgec.dev.para,fcgec.test.para

# Correct unreasonable csc error for FCGEC-Dev and NaSGEC-Exam
mv cmcgec/tmp/remove_special_tag/fcgec.dev.para cmcgec/tmp/handle_leakage/
python cgectk/csc_clean.py \
    --data_dir cmcgec/tmp/handle_leakage \
    --out_dir cmcgec/tmp/csc_clean \
    --file_names fcgec.dev.para,nasgec.exam.para \
    --annotation_file raw_cgec/csc_annotation/all.labeled.v2024.06.24.jsonl

# Move processed files to cmcgec
mv cmcgec/tmp/remove_special_tag/mucgec.dev.para cmcgec/
mv cmcgec/tmp/remove_special_tag/mucgec.test.para cmcgec/
mv cmcgec/tmp/handle_leakage/fcgec.train.para cmcgec/
mv cmcgec/tmp/csc_clean/fcgec.dev.para cmcgec/
mv cmcgec/tmp/remove_special_tag/fcgec.test.para cmcgec/
mv cmcgec/tmp/csc_clean/nasgec.exam.para cmcgec/
mv cmcgec/tmp/remove_special_tag/nasgec.media.para cmcgec/
mv cmcgec/tmp/remove_special_tag/nasgec.thesis.para cmcgec/
mv cmcgec/tmp/handle_leakage/nacgec.para cmcgec/

# Remove tmp dir
rm -rf cmcgec/tmp
