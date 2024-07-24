# NaSGEC-v1
For detailed information about the NaSGEC dataset, please refer to this repository: [HillZhang1999/NaSGEC](https://github.com/HillZhang1999/NaSGEC).

## File Directory Introduction
+ **```NaSGEC/```**: We open-source the NaSGEC dataset for the first time.
    + Please add the ```--bpe``` option when evaluate nasgec.[exam/media/thesis].test.m2 using ChERRANT, this option is not required for all other datasets.
+ **```FCGEC/```**: We collect the [FCGEC](https://github.com/xlxwalex/FCGEC/tree/main/data) dataset and convert each instance (e.g., 2 references) in it into the following para format: ```idx \t input_sentence \t reference-1 \t reference-2```
    + We process FCGEC to remove duplicates. First, we merged all references under the identical input sentence. Then, we deduplicated the references for identical input sentence.
        + For example, consider the following two instances:
            ```
            1 \t input_sentence-1 \t reference-1 \t reference-2
            2 \t input_sentence-1 \t reference-2 \t reference-3
            ```
        + will be turned into the following format: 
            ```
            1 \t input_sentence-1 \t reference-1 \t reference-2 \t reference-3
            ```
    + 2. In the first official release of the FCGEC training dataset, there were input sentences that were identical to those in the development and test sets: https://github.com/xlxwalex/FCGEC/issues/26. We utilized the officially released filtered version [FCGEC_train_filtered.json](https://github.com/xlxwalex/FCGEC/blob/main/data/FCGEC_train_filtered.json) as our source for the training set, which had removed these leaked instances from the original training data.

+ **```NaCGEC/```**: We collect the [NaCGEC](https://github.com/masr2000/NaCGEC) dataset and turn it into para format. Due to the very small number of instances in NaCGEC-Dev, we merged NaCGEC-Dev and NaCGEC-Test to create ```nacgec.para```, which we are using as a new test set.
