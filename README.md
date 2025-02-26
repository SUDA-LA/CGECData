# CGECData
We open source MuCGEC and NaSGEC in this repository. In addition, we collect and process other mainstream Chinese GEC datasets, i.e., FCGEC and NaCGEC.

## Data Access

Once you use the data from this repo, it means that you agree to the [data sharing agreement](2025.02.18_MuCGEC_NaSGEC_Sharing_Agreement.docx) of MuCGEC and NaSGEC. You can directly use MuCGEC and NaSGEC-Exam. If you need to obtain NaSGEC-Media and NaSGEC-Thesis, you need to sign the data sharing agreement and sent it to Zhenghua Li (zhli13@suda.edu.cn).

## File Directory Introduction

+ **`MuCGEC/`**:
  + **`v1-NAACL22/`**: We open source [MuCGEC-Test](MuCGEC/v1-NAACL22/mucgec.test.m2) in M2 format for the first time, which yields the same results as those obtained using the online [Tianchi](https://tianchi.aliyun.com/dataset/131328/submission) platform. 
+ **`NaSGEC/`**:
  + **`v1-ACL23/`**: We open source the NaSGEC dataset for the first time.
  + **`v2-ACL24/`**: We handle the data leakage issue for FCGEC, NaSGEC-Exam, and NaCGEC.
  + **`v3/`**: We conduct further cleaning on FCGEC, NaSGEC-Exam, and NaCGEC.

## Evaluation

We strongly recommend you use [ChERRANT](https://github.com/HillZhang1999/MuCGEC/tree/main/scorers/ChERRANT) for evaluation, which is proposed in our [MuCGEC](https://aclanthology.org/2022.naacl-main.227/) paper.

## Citation

If you find this repo is useful for your research, please selectively cite the following papers.

#### MuCGEC
```
@inproceedings{zhang-etal-2022-mucgec,
    title = "{{M}u{CGEC}: a Multi-Reference Multi-Source Evaluation Dataset for {C}hinese Grammatical Error Correction}",
    author = "Zhang, Yue  and
      Li, Zhenghua  and
      Bao, Zuyi  and
      Li, Jiacheng  and
      Zhang, Bo  and
      Li, Chen  and
      Huang, Fei  and
      Zhang, Min",
    booktitle = "Proceedings of NAACL",
    year = "2022",
    address = "Seattle, United States",
    url = "https://aclanthology.org/2022.naacl-main.227",
    pages = "3118--3130",
}
```

#### NaSGEC
```
@inproceedings{zhang-etal-2023-nasgec,
    title = "{{N}a{SGEC}: a Multi-Domain {C}hinese Grammatical Error Correction Dataset from Native Speaker Texts}",
    author = "Zhang, Yue  and
      Zhang, Bo  and
      Jiang, Haochen  and
      Li, Zhenghua  and
      Li, Chen  and
      Huang, Fei  and
      Zhang, Min",
    booktitle = "Findings of ACL,
    year = "2023",
    address = "Toronto, Canada",
    url = "https://aclanthology.org/2023.findings-acl.630",
    pages = "9935--9951",
}
```

#### MrGEC
```
@inproceedings{liu-etal-2024-towards-better,
    title = "{Towards Better Utilization of Multi-Reference Training Data for {C}hinese Grammatical Error Correction}",
    author = "Liu, Yumeng  and
      Li, Zhenghua  and
      Jiang, HaoChen  and
      Zhang, Bo  and
      Li, Chen  and
      Zhang, Ji",
    booktitle = "Findings of ACL",
    year = "2024",
    address = "Bangkok, Thailand and virtual meeting",
    url = "https://aclanthology.org/2024.findings-acl.180",
    pages = "3044--3052",
}
```

## Contact
If you have any problems, please make an issue or contact us at liu.yumeng@foxmail.com / Jacob_Zhou@outlook.com. 
