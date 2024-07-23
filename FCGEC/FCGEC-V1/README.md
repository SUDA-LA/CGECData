FCGEC-V1 和 [FCGEC](https://github.com/xlxwalex/FCGEC/tree/main/data) 官方在 GitHub 发布的数据完全一样，我们将数据处理成了如下的 para 形式：

```
[idx][\t][src][\t][tgt][\t][tgt] ...
```

Note:
1. 我们对数据进行了去重处理，首先合并了相同 src 下的所有 tgt，其次对相同 src 的 tgt 进行了去重。
    例如如下的两个样本
    ```
    1   src1   tgt1   tgt2
    2   src1   tgt2   tgt3
    ```
    合并后变为
    ```
    1   src1   tgt1   tgt2   tgt3
    ```
2. FCGEC 官方发布的第一版 train 数据，存在和 dev 和 test 完全相同的 src 的情况，我们使用了官方发布的过滤版本，从训练集删去了这些样本 