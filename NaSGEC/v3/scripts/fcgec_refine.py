"""
FCGEC Refinement: manual correct annotation errors:
https://github.com/xlxwalex/FCGEC/issues/25
https://github.com/xlxwalex/FCGEC/issues/40
and other annotation errors
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
        error_input = line["error_input"]
        correct_instance = line["correct_instance"]
        if error_input not in fcgec_annotation:
            fcgec_annotation[error_input] = correct_instance

    f_annotation.close()
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    for file_name in args.file_names.split(","):
        cnt = 0
        data_path = os.path.join(args.data_dir, file_name)
        out_path = os.path.join(args.out_dir, file_name)
        f_data = open(data_path)
        f_out = open(out_path, "w")
        for line in f_data:
            line = line.strip()
            idx = line.split("\t")[0]
            src = line.split("\t")[1]
            if src in fcgec_annotation:
                correct_instance = '\t'.join(fcgec_annotation[src])
                cnt += 1
                print(idx, correct_instance, sep="\t", file=f_out)
            else:
                print(line, file=f_out)
        if args.verbose:
            print(f'{file_name}: Correct {cnt} instances that have annotation errors.')
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
