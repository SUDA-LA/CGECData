# The whole process from raw_cgec to gec_data_v3

# Build tmp dir 
mkdir -p gec_data_v3/tmp
cp raw_cgec/MuCGEC/mucgec.dev.para gec_data_v3/tmp/
cp raw_cgec/FCGEC/fcgec.train.filtered.para gec_data_v3/tmp/fcgec.train.para
cp raw_cgec/FCGEC/fcgec.dev.para gec_data_v3/tmp/
cp raw_cgec/FCGEC/fcgec.test.para gec_data_v3/tmp/
cp raw_cgec/NaSGEC/NaSGEC-Exam/nasgec.exam.para gec_data_v3/tmp/
cp raw_cgec/NaSGEC/NaSGEC-Media/nasgec.media.para gec_data_v3/tmp/
cp raw_cgec/NaSGEC/NaSGEC-Thesis/nasgec.thesis.para gec_data_v3/tmp/
cp raw_cgec/NaCGEC/nacgec.para gec_data_v3/tmp/
python scripts/m2_to_para.py \
    --m2_file raw_cgec/MuCGEC/mucgec.test.m2 \
    --input_file raw_cgec/MuCGEC/mucgec.test.input \
    --out_file gec_data_v3/tmp/mucgec.test.para \

# Remove special tag in MuCGEC, NaSGEC and NaCGEC
python scripts/remove_special_tag.py \
    --data_dir gec_data_v3/tmp \
    --out_dir gec_data_v3/tmp/remove_special_tag \
    --file_names mucgec.dev.para,mucgec.test.para,nasgec.exam.para,nasgec.media.para,nasgec.thesis.para,nacgec.para

# Handle data leakage problem for NS CGEC datasets
mv gec_data_v3/tmp/fcgec.train.para gec_data_v3/tmp/remove_special_tag/
mv gec_data_v3/tmp/fcgec.dev.para gec_data_v3/tmp/remove_special_tag/
mv gec_data_v3/tmp/fcgec.test.para gec_data_v3/tmp/remove_special_tag/
python scripts/handle_leakage.py \
    --data_dir gec_data_v3/tmp/remove_special_tag \
    --out_dir gec_data_v3/tmp/handle_leakage \
    --train_file fcgec.train.para \
    --extract_test_files nasgec.exam.para,nacgec.para  \
    --frozen_test_files fcgec.dev.para,fcgec.test.para

# Correct unreasonable csc error for FCGEC-Dev and NaSGEC-Exam & fcgec_refinement
mv gec_data_v3/tmp/remove_special_tag/fcgec.dev.para gec_data_v3/tmp/handle_leakage/
python scripts/csc_clean.py \
    --data_dir gec_data_v3/tmp/handle_leakage \
    --out_dir gec_data_v3/tmp/csc_clean \
    --file_names fcgec.dev.para,nasgec.exam.para \
    --annotation_file raw_cgec/data_refinement/all.labeled.v2024.06.24.jsonl

mv gec_data_v3/tmp/handle_leakage/fcgec.train.para gec_data_v3/tmp/csc_clean/
python scripts/fcgec_refine.py \
    --data_dir gec_data_v3/tmp/csc_clean \
    --out_dir gec_data_v3/tmp/fcgec_refine \
    --file_names fcgec.train.para,fcgec.dev.para \
    --annotation_file raw_cgec/data_refinement/fcgec_refine.2024.7.23.jsonl

# Move processed files to gec_data_v3
mv gec_data_v3/tmp/remove_special_tag/mucgec.dev.para gec_data_v3/
mv gec_data_v3/tmp/remove_special_tag/mucgec.test.para gec_data_v3/
mv gec_data_v3/tmp/fcgec_refine/fcgec.train.para gec_data_v3/
mv gec_data_v3/tmp/fcgec_refine/fcgec.dev.para gec_data_v3/
mv gec_data_v3/tmp/remove_special_tag/fcgec.test.para gec_data_v3/
mv gec_data_v3/tmp/csc_clean/nasgec.exam.para gec_data_v3/
mv gec_data_v3/tmp/remove_special_tag/nasgec.media.para gec_data_v3/
mv gec_data_v3/tmp/remove_special_tag/nasgec.thesis.para gec_data_v3/
mv gec_data_v3/tmp/handle_leakage/nacgec.para gec_data_v3/

# Remove tmp dir
rm -rf gec_data_v3/tmp
