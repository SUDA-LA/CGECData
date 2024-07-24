# CGECData
We open source MuCGEC and NaSGEC in this repository. In addition, we collect and process other mainstream Chinese GEC datasets, i.e., FCGEC and NaCGEC.

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

### MuCGEC
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

### NaSGEC
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

### MrGEC
```
@inproceedings{liu-etal-2024-towards,
    title = "{Towards Better Utilization of Multi-Reference Training Data for Chinese Grammatical Error Correction}",
    author = "Liu, Yumeng  and
      Li, Zhenghua  and
      Jiang, Haochen  and
      Zhang, Bo  and
      Li, Chen  and
      Zhang, Ji,
    booktitle = "Findings of ACL",
    year = "2024",
}
```

### FCGEC
```
@inproceedings{xu-etal-2022-fcgec,
    title = "{{FCGEC}: Fine-Grained Corpus for {C}hinese Grammatical Error Correction}",
    author = "Xu, Lvxiaowei  and
      Wu, Jianwang  and
      Peng, Jiawei  and
      Fu, Jiayu  and
      Cai, Ming",
    booktitle = "Findings of EMNLP",
    year = "2022",
    address = "Abu Dhabi, United Arab Emirates",
    url = "https://aclanthology.org/2022.findings-emnlp.137",
    pages = "1900--1918",
}
```

### NaCGEC
```
@inproceedings{ma-etal-2022-linguistic,
    title = "{Linguistic Rules-Based Corpus Generation for Native {C}hinese Grammatical Error Correction}",
    author = "Ma, Shirong  and
      Li, Yinghui  and
      Sun, Rongyi  and
      Zhou, Qingyu  and
      Huang, Shulin  and
      Zhang, Ding  and
      Yangning, Li  and
      Liu, Ruiyang  and
      Li, Zhongli  and
      Cao, Yunbo  and
      Zheng, Haitao  and
      Shen, Ying",
    booktitle = "Findings of EMNLP",
    year = "2022",
    address = "Abu Dhabi, United Arab Emirates",
    url = "https://aclanthology.org/2022.findings-emnlp.40",
    pages = "576--589",
}
```

## Contact
If you have any problems, please make an issue or contact us at liu.yumeng@foxmail.com / Jacob_Zhou@outlook.com. 
