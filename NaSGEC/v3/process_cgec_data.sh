# set -o nounset
# set -o errexit
# set -o pipefail

{

# The whole process from nasgec_v1 to nasgec_v3

# Build tmp dir 
mkdir -p nasgec_v3/tmp
mkdir -p nasgec_v3/log
cp ../v1-ACL23/FCGEC/fcgec.train.filtered.para nasgec_v3/tmp/fcgec.train.para
cp ../v1-ACL23/FCGEC/fcgec.dev.para nasgec_v3/tmp/
cp ../v1-ACL23/FCGEC/fcgec.test.para nasgec_v3/tmp/
cp ../v1-ACL23/NaSGEC/NaSGEC-Exam/nasgec.exam.para nasgec_v3/tmp/
cp ../v1-ACL23/NaSGEC/NaSGEC-Media/nasgec.media.para nasgec_v3/tmp/
cp ../v1-ACL23/NaSGEC/NaSGEC-Thesis/nasgec.thesis.para nasgec_v3/tmp/
cp ../v1-ACL23/NaCGEC/nacgec.para nasgec_v3/tmp/

# Remove special tag in NaSGEC and NaCGEC
python scripts/remove_special_tag.py \
    --data_dir nasgec_v3/tmp \
    --out_dir nasgec_v3/tmp/remove_special_tag \
    --file_names nasgec.exam.para,nasgec.media.para,nasgec.thesis.para,nacgec.para \
    --verbose

# Handle data leakage problem for NS CGEC datasets
mv nasgec_v3/tmp/fcgec.train.para nasgec_v3/tmp/remove_special_tag/
mv nasgec_v3/tmp/fcgec.dev.para nasgec_v3/tmp/remove_special_tag/
mv nasgec_v3/tmp/fcgec.test.para nasgec_v3/tmp/remove_special_tag/
python scripts/handle_leakage.py \
    --data_dir nasgec_v3/tmp/remove_special_tag \
    --out_dir nasgec_v3/tmp/handle_leakage \
    --train_file fcgec.train.para \
    --extract_test_files nasgec.exam.para,nacgec.para \
    --frozen_test_files fcgec.dev.para,fcgec.test.para \
    --verbose | tee nasgec_v3/log/handle_leakage.log

# Correct unreasonable csc error for FCGEC-Dev and NaSGEC-Exam
mv nasgec_v3/tmp/remove_special_tag/fcgec.dev.para nasgec_v3/tmp/handle_leakage/
python scripts/csc_clean.py \
    --data_dir nasgec_v3/tmp/handle_leakage \
    --out_dir nasgec_v3/tmp/csc_clean \
    --file_names fcgec.dev.para,nasgec.exam.para \
    --annotation_file data_refinement/all.labeled.v2024.06.24.jsonl \
    --verbose \
    --generate_report | tee nasgec_v3/log/csc_clean.log

# Correct annotation error for FCGEC-Train and FCGEC-Dev
mv nasgec_v3/tmp/handle_leakage/fcgec.train.para nasgec_v3/tmp/csc_clean/
python scripts/fcgec_refine.py \
    --data_dir nasgec_v3/tmp/csc_clean \
    --out_dir nasgec_v3/tmp/fcgec_refine \
    --file_names fcgec.train.para,fcgec.dev.para \
    --annotation_file data_refinement/fcgec_refine.2024.7.24.jsonl \
    --verbose

# Move processed files to nasgec_v3
mv nasgec_v3/tmp/remove_special_tag/fcgec.test.para nasgec_v3/
mv nasgec_v3/tmp/remove_special_tag/nasgec.media.para nasgec_v3/
mv nasgec_v3/tmp/remove_special_tag/nasgec.thesis.para nasgec_v3/

mv nasgec_v3/tmp/fcgec_refine/fcgec.train.para nasgec_v3/
mv nasgec_v3/tmp/fcgec_refine/fcgec.dev.para nasgec_v3/

mv nasgec_v3/tmp/handle_leakage/nacgec.para nasgec_v3/

mv nasgec_v3/tmp/csc_clean/nasgec.exam.para nasgec_v3/

mv nasgec_v3/tmp/csc_clean/*.para.cleaning_report.md nasgec_v3/log/

# Clean-up tmp dir
rm -rf nasgec_v3/tmp

}
