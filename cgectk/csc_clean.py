"""
Correct unreasonable Chinese spell errors in CGEC input & reference sentences given the manual annotation results.
"""

import os
import json
import argparse


def main(args):
    assert args.annotation_file.endswith(".jsonl")
    csc_annotation = {}
    f_annotation = open(args.annotation_file)
    for line in f_annotation:
        line = json.loads(line.strip())
        src = line["source"]
        corrected_src = line["verified"]
        if src not in csc_annotation:
            csc_annotation[src] = corrected_src
        else:
            assert corrected_src == csc_annotation[src]
    f_annotation.close()
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    for file_name in args.file_names.split(","):
        all_cnt = 0
        src_csc_cnt = 0
        tgt_csc_cnt = 0
        data_path = os.path.join(args.data_dir, file_name)
        out_path = os.path.join(args.out_dir, file_name)
        f_data = open(data_path)
        f_out = open(out_path, "w")
        for line in f_data:
            line = line.strip().split("\t")
            idx = line[0]
            src = line[1]
            tgts = line[2:]
            new_tgts = []
            if src in csc_annotation:
                src = csc_annotation[src]
                src_csc_cnt += 1
            for tgt in tgts:
                if tgt in csc_annotation:
                    tgt = csc_annotation[tgt]
                    tgt_csc_cnt += 1
                new_tgts.append(tgt)
            all_cnt += 1
            print(idx, src, "\t".join(tgts), sep="\t", file=f_out)
        print(f'{file_name}: Correct {src_csc_cnt}/{all_cnt} input sentences that exist unreasonable csc errors.')
        print(f'{file_name}: Correct {tgt_csc_cnt}/{all_cnt} reference sentences that exist unreasonable csc errors.')
        f_data.close()
        f_out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", help="dir of all datasets needed processing", required=True)
    parser.add_argument("--out_dir", help="dir of all output datasets", required=True)
    parser.add_argument("--file_names", help="CGEC file names, split by english comm", required=True)
    parser.add_argument("--annotation_file", help="manual CSC annotation results", required=True)
    args = parser.parse_args()
    main(args)
