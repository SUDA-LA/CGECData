"""
FCGEC Refinement: manual correct
https://github.com/xlxwalex/FCGEC/issues/25
https://github.com/xlxwalex/FCGEC/issues/40
"""

import os
import json
import argparse


def main(args):
    assert args.annotation_file.endswith(".jsonl")
    fcgec_annotation = {}
    f_annotation = open(args.annotation_file)
    for line in f_annotation:
        line = json.loads(line.strip())
        src = line["text"]
        corrected_src = line["correct"]
        if src not in fcgec_annotation:
            fcgec_annotation[src] = corrected_src
        else:
            assert corrected_src == fcgec_annotation[src]
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
            if src in fcgec_annotation:
                src = fcgec_annotation[src]
                src_csc_cnt += 1
            for tgt in tgts:
                if tgt in fcgec_annotation:
                    tgt = fcgec_annotation[tgt]
                    tgt_csc_cnt += 1
                new_tgts.append(tgt)
            all_cnt += 1
            print(idx, src, "\t".join(new_tgts), sep="\t", file=f_out)
        if args.verbose:
            print(f'{file_name}: Correct {src_csc_cnt}/{all_cnt} input sentences that have annotation errors.')
            print(f'{file_name}: Correct {tgt_csc_cnt}/{all_cnt} reference sentences that have annotation errors.')
        f_data.close()
        f_out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", help="dir of all datasets needed processing", required=True)
    parser.add_argument("--out_dir", help="dir of all output datasets", required=True)
    parser.add_argument("--file_names", help="CGEC file names, split by english comm", required=True)
    parser.add_argument("--annotation_file", help="manual FCGEC annotation results", required=True)
    parser.add_argument("--verbose", action="store_true", help="print log")
    args = parser.parse_args()
    main(args)
