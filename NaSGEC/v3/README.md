与v2-ACL24相比，v3主要做了以下优化，参考脚本在这里[process_cgec_data.sh](process_cgec_data.sh)。
- 手动修复了FCGEC几条标注错误，参见https://github.com/xlxwalex/FCGEC/issues/25 和 https://github.com/xlxwalex/FCGEC/issues/40。
- 使用我们自己开发的先进的CSC模型找出FCGEC-Dev和NaSGEC-Exam里面不合理的错别字错误（比如离谱的OCR错误），并进行人工矫正
- 删除NaSGEC-Exam里的特殊标签句子，比如["没有错误", "噪音数据", "句意不明", "无法标注", "歧义句"] 等。