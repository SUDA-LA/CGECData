"""
from https://github.com/ymliucs/MrGEC/blob/main/utils/handle_data_leakage_tool/handle_leakage.py
1: Merge sentences from the same source in the test set into the training set 
(ignore same reference, merge different reference into the same source, and use similar source as new samples)
2: Remove sentences from the training set that are cognate (identical or similar) to the test set
Input: one training set, several test sets, format: idx \t src \t tgt1 \t tgt2 ...
Output: one training set, several test sets after processing data leakage
--extract_test_files and --frozen_test_files are optional, give at least one
example:
python handle_leakage.py --data_dir data/ns_original --out_dir data/ns_leakage_processed --train_file FCGEC_train_filtered.para --extract_test_files nasgec.exam.para,nacgec.all.para  --frozen_test_files fcgec.dev.para,fcgec.test.para
or
python handle_leakage.py --data_dir data/ns_original --out_dir data/ns_leakage_processed --train_file FCGEC_train_filtered.para --extract_test_files nasgec.exam.para
or
python handle_leakage.py --data_dir data/ns_original --out_dir data/ns_leakage_processed --train_file FCGEC_train_filtered.para --frozen_test_files nasgec.exam.para
"""

import os
import argparse
from tqdm import tqdm
from decimal import Decimal
from fastbm25 import fastbm25
from string import punctuation
from collections import OrderedDict
from sacrebleu import sentence_bleu


def remove_punct(line):
    chinese_punct = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～《》｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏．"
    english_punct = punctuation
    punct = set(chinese_punct + english_punct)
    punct |= set("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    line = ''.join([c for c in line if c not in punct])
    line = ''.join(line.split())
    return line


def remove_repetition(data_dir, data_file):
    """
    删除数据集内部的重复数据
    输入：文件路径
    输出：字典：{name:str,data:{{src:str,tgts:[str, str, ...]}}}
    """
    # if args.verbose:
    #     print(f"\n{data_file} remove repetition:")
    data = open(os.path.join(data_dir, data_file))
    src_cnt = 0
    tgt_cnt = 0
    new_src_cnt = 0
    new_tgt_cnt = 0
    new_data = OrderedDict()
    for line in data:
        line = line.strip().split("\t")
        src = line[1]
        tgts = line[2:]
        src_cnt += 1
        tgt_cnt += len(tgts)
        if src not in new_data.keys():
            new_src_cnt += 1
            new_data[src] = []
        for tgt in tgts:
            if tgt not in new_data[src]:
                new_tgt_cnt += 1
                new_data[src].append(tgt)
    if args.verbose:
        output_summary = f"""
        Original Data:
        ----------------------------------------------------------------
        - Source Sentences:                        {src_cnt}
        - Target Sentences:                        {tgt_cnt}

        Unique Sentences:
        ----------------------------------------------------------------
        - Source Sentences:                        {new_src_cnt}
        - Target Sentences:                        {new_tgt_cnt}

        """

        print(output_summary)

    return {"name": data_file, "data": new_data}


def extract_test_to_train(train, test, similarity_threshold=60):
    add_same_src_cnt = 0
    add_tgt_of_same_src_cnt = 0
    ignore_same_src_cnt = 0
    ignore_tgt_of_same_src_cnt = 0
    add_similar_src_cnt = 0
    add_tgt_of_similar_src_cnt = 0
    delect_same_src_cnt = 0
    delect_tgt_of_same_src_cnt = 0
    delect_similar_src_cnt = 0
    delect_tgt_of_similar_src_cnt = 0
    train_name, train_data = train["name"], train["data"]
    test_name, test_data = test["name"], test["data"]
    if args.verbose:
        print(f"\nExtract same or similar source sentences from {test_name} to {train_name}")
    test_srcs = [x for x in test_data.keys()]
    add_src_flag = False
    train_src_bm25 = fastbm25([remove_punct(x) for x in train_data.keys()])
    add_same_src_set = set()
    for test_src in tqdm(test_srcs):
        test_tgts = test_data[test_src]
        if test_src in train_data.keys():
            for test_tgt in test_tgts:
                if test_tgt not in train_data[test_src]:
                    add_tgt_of_same_src_cnt += 1
                    train_data[test_src].append(test_tgt)
                    add_src_flag = True
                else:
                    ignore_tgt_of_same_src_cnt += 1
            if add_src_flag:
                add_same_src_cnt += 1
                add_same_src_set.add(test_src)
            else:
                ignore_same_src_cnt += 1
            delect_same_src_cnt += 1
            delect_tgt_of_same_src_cnt += len(test_tgts)
            test_data.pop(test_src)
            add_src_flag = False
        else:
            top_k = train_src_bm25.top_k_sentence(remove_punct(test_src), k=100)
            for train_src, _, _ in top_k:
                bleu_score = sentence_bleu(" ".join(remove_punct(train_src)), [" ".join(remove_punct(test_src))]).score
                if bleu_score >= similarity_threshold:
                    train_data[test_src] = test_tgts
                    add_similar_src_cnt += 1
                    add_tgt_of_similar_src_cnt += len(test_tgts)
                    delect_similar_src_cnt += 1
                    delect_tgt_of_similar_src_cnt += len(test_tgts)
                    test_data.pop(test_src)
                    break
    new_train_src_cnt = len(train_data)
    new_train_tgt_cnt = 0
    new_test_src_cnt = len(test_data)
    new_test_tgt_cnt = 0
    for tgts in train_data.values():
        new_train_tgt_cnt += len(tgts)
    for tgts in test_data.values():
        new_test_tgt_cnt += len(tgts)
    add_src_cnt = add_same_src_cnt + add_similar_src_cnt
    add_tgt_cnt = add_tgt_of_same_src_cnt + add_tgt_of_similar_src_cnt
    add_avg_tgt_of_same_src = round(Decimal(str(add_tgt_of_same_src_cnt / add_same_src_cnt)), 2)
    add_avg_tgt_of_similar_src = round(Decimal(str(add_tgt_of_similar_src_cnt / add_similar_src_cnt)), 2)
    add_avg_tgt = round(Decimal(str(add_tgt_cnt / add_src_cnt)), 2)
    same_src_total_tgt_cnt = 0
    assert len(add_same_src_set) == add_same_src_cnt
    for src in add_same_src_set:
        same_src_total_tgt_cnt += len(train_data[src])
    same_src_avg_tgt = round(Decimal(str(same_src_total_tgt_cnt / add_same_src_cnt)), 2)
    if args.verbose:
        output = f"""
        Train Data: {train_name}
        ----------------------------------------------------------------
        - Same Source Sentences:
            Found:                                 {add_same_src_cnt + ignore_same_src_cnt}
            Merged:                                {add_same_src_cnt}
            Ignored (Repetition):                  {ignore_same_src_cnt}
            Added Target Sentences:                {add_tgt_of_same_src_cnt}
            Added Average Target Sentences:        {add_avg_tgt_of_same_src}
            Total Target Sentences:                {same_src_total_tgt_cnt}
            Total Average Target Sentences:        {same_src_avg_tgt}
            Ignored Target Sentences (Repetition): {ignore_tgt_of_same_src_cnt}
        - Similar Source Sentences:
            Added:                                 {add_similar_src_cnt}
            Added Target Sentences:                {add_tgt_of_similar_src_cnt}
            Added Average Target Sentences:        {add_avg_tgt_of_similar_src}
        - New Sentences:
            Added Source Sentences:                {add_src_cnt}
            Added Target Sentences:                {add_tgt_cnt}
            Added Average Target Sentences:        {add_avg_tgt}
        - Final Counts:
            Source Sentences:                      {new_train_src_cnt}
            Target Sentences:                      {new_train_tgt_cnt}

        Test Data: {test_name}
        ----------------------------------------------------------------
        - Same Source Sentences:
            Deleted:                               {delect_same_src_cnt}
            Deleted Target Sentences:              {delect_tgt_of_same_src_cnt}
        - Similar Source Sentences:
            Deleted:                               {delect_similar_src_cnt}
            Deleted Target Sentences:              {delect_tgt_of_similar_src_cnt}
        - Total Deleted:
            Source Sentences:                      {delect_same_src_cnt + delect_similar_src_cnt}
            Target Sentences:                      {delect_tgt_of_same_src_cnt + delect_tgt_of_similar_src_cnt}
        - Final Counts:
            Source Sentences:                      {new_test_src_cnt}
            Target Sentences:                      {new_test_tgt_cnt}

        """
        print(output)

    return {"name": train_name, "data": train_data}, {"name": test_name, "data": test_data}


def remove_train(train, test, similarity_threshold=60):
    delect_same_src_cnt = 0
    delect_tgt_of_same_src_cnt = 0
    delect_similar_src_cnt = 0
    delect_tgt_of_similar_src_cnt = 0
    train_name, train_data = train["name"], train["data"]
    test_name, test_data = test["name"], test["data"]
    if args.verbose:
        print(f"\nDelete same or similar source sentences between {train_name} and {test_name}")
    test_srcs = [x for x in test_data.keys()]
    train_srcs = [x for x in train_data.keys()]
    train_src_bm25 = fastbm25([remove_punct(x) for x in train_data.keys()])
    for test_src in tqdm(test_srcs):
        if test_src in train_data.keys():
            delect_same_src_cnt += 1
            delect_tgt_of_same_src_cnt += len(train_data[test_src])
            train_data.pop(test_src)
        else:
            top_k = train_src_bm25.top_k_sentence(remove_punct(test_src), k=100)
            for train_src, train_idx, _ in top_k:
                bleu_score = sentence_bleu(" ".join(remove_punct(train_src)), [" ".join(remove_punct(test_src))]).score
                if bleu_score >= similarity_threshold:
                    train_src_ori = train_srcs[train_idx]
                    assert remove_punct(train_src_ori) == remove_punct(train_src)
                    if train_src_ori in train_data.keys():
                        delect_similar_src_cnt += 1
                        delect_tgt_of_similar_src_cnt += len(train_data[train_src_ori])
                        train_data.pop(train_src_ori)
    new_train_src_cnt = len(train_data)
    new_train_tgt_cnt = 0
    for tgts in train_data.values():
        new_train_tgt_cnt += len(tgts)
    if args.verbose:

        train_data_deletion_summary = f"""
        Train Data: {train_name} Deletion Summary
        ----------------------------------------------------------------
        - Deleted Same Source Sentences:
            Source Sentences:                      {delect_same_src_cnt}
            Target Sentences:                      {delect_tgt_of_same_src_cnt}
        - Deleted Similar Source Sentences:
            Source Sentences:                      {delect_similar_src_cnt}
            Target Sentences:                      {delect_tgt_of_similar_src_cnt}
        - Total Deleted:
            Source Sentences:                      {delect_same_src_cnt + delect_similar_src_cnt}
            Target Sentences:                      {delect_tgt_of_same_src_cnt + delect_tgt_of_similar_src_cnt}
        - Final Counts:
            Source Sentences:                      {new_train_src_cnt}
            Target Sentences:                      {new_train_tgt_cnt}
        """

        print(train_data_deletion_summary)

    return {"name": train_name, "data": train_data}


def write_to_file(data, out_dir):
    out_path = os.path.join(out_dir, data["name"])
    data = data["data"]
    with open(out_path, "w") as f_out:
        for idx, (src, tgts) in enumerate(data.items(), start=1):
            print(idx, src, "\t".join(tgts), sep="\t", file=f_out)


def main(args):
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    if args.verbose:
        print("=" * 50 + " Data Remove Repetition " + "=" * 50)
    train = remove_repetition(args.data_dir, args.train_file)
    extract_tests = []
    frozen_tests = []
    new_extract_tests = []
    assert args.extract_test_files is not None or args.frozen_test_files is not None
    if args.extract_test_files is not None:
        for extract_test_file in args.extract_test_files.split(","):
            if args.verbose:
                print("Remove Repetition:", extract_test_file)
            extract_tests.append(remove_repetition(args.data_dir, extract_test_file))
    if args.frozen_test_files is not None:
        for frozen_test_file in args.frozen_test_files.split(","):
            if args.verbose:
                print("Remove Repetition:", extract_test_file)
            frozen_tests.append(remove_repetition(args.data_dir, frozen_test_file))
    if len(extract_tests) > 0:
        if args.verbose:
            print("\n" + "=" * 50 + " Extract Test Sentences " + "=" * 50)
        for extract_test in extract_tests:
            if args.verbose:
                print(f"Extract Test Sentences from {extract_test['name']} to {train['name']}")
            train, extract_test = extract_test_to_train(train, extract_test, args.similarity_threshold)
            new_extract_tests.append(extract_test)
    if len(extract_tests) > 0 or len(frozen_tests) > 0:
        if args.verbose:
            print("\n" + "=" * 50 + " Remove Train Sentences " + "=" * 50)
        for extract_test in new_extract_tests:
            write_to_file(extract_test, args.out_dir)
            if args.verbose:
                print(f"Remove Train Sentences between {train['name']} and {extract_test['name']}")
            train = remove_train(train, extract_test, args.similarity_threshold)
        for frozen_test in frozen_tests:
            if args.verbose:
                print(f"Remove Train Sentences between {train['name']} and {frozen_test['name']}")
            train = remove_train(train, frozen_test, args.similarity_threshold)
        write_to_file(train, args.out_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", help="dir of all datasets", default="./data")
    parser.add_argument("--train_file", help="train file name", required=True)
    parser.add_argument("--extract_test_files", help="extest file names needed extraction, split by english comma", default=None)
    parser.add_argument("--frozen_test_files", help="test file names purely for evaluation, split by english comma", default=None)
    parser.add_argument("--out_dir", help="output dir", default="./data_leakage_processed")
    parser.add_argument("--similarity_threshold", type=float, help="similarity threshold", default=60)
    parser.add_argument("--verbose", action="store_true", help="print log")
    args = parser.parse_args()
    main(args)