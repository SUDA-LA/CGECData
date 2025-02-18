# NaSGEC-v3

## 📢 Important Update

+ We delete the special label references in NaSGEC-Exam and NaCGEC, such as ```["没有错误", "噪音数据", "句意不明", "无法标注", "歧义句"]```, etc.
+ We use the same data leakage handling approaches as in NaSGEC-v2.
+ We use our advanced CSC model (https://aclanthology.org/2024.emnlp-main.966/) to find unreasonable spell errors (such as serious OCR errors) in FCGEC-Dev and NaSGEC-Exam, and perform manual annotation verification.
+ We manually correct some annotation errors in FCGEC, see https://github.com/xlxwalex/FCGEC/issues/25 and https://github.com/xlxwalex/FCGEC/issues/40.
+ The script for all processes is here [process_cgec_data.sh](process_cgec_data.sh).