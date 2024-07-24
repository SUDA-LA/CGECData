"""
Remove special annotation tag
Example: ["没有错误", "噪音数据", "句意不明", "无法标注", "歧义句"] in NaSGEC and ["error。"] in NaCGEC
"""

import os
import argparse


def main(args):
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    for file_name in args.file_names.split(","):
        all_cnt = 0
        remove_tgt_cnt = 0
        data_path = os.path.join(args.data_dir, file_name)
        out_path = os.path.join(args.out_dir, file_name)
        f_data = open(data_path)
        f_out = open(out_path, "w")
        idx = 1
        for line in f_data:
            line = line.strip().split("\t")
            src = line[1]
            tgts = line[2:]
            new_tgts = []
            for tgt in tgts:
                if tgt in ["噪音数据", "句意不明", "无法标注", "歧义句", "error。"] or "[缺失成分]" in tgt:
                    remove_tgt_cnt += 1
                    continue
                if tgt == "没有错误":
                    tgt = src
                new_tgts.append(tgt)
                all_cnt += 1
            if len(new_tgts) == 0:
                continue
            print(idx, src, "\t".join(new_tgts), sep="\t", file=f_out)
            idx += 1
        if args.verbose:
            print(f'{file_name}: Remove {remove_tgt_cnt}/{all_cnt} reference sentences labeled with special tag.')
        f_data.close()
        f_out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", help="dir of all datasets needed processing", required=True)
    parser.add_argument("--out_dir", help="dir of all output datasets", required=True)
    parser.add_argument("--file_names", help="CGEC file names, split by english comm", required=True)
    parser.add_argument("--verbose", action="store_true", help="print log")
    args = parser.parse_args()
    main(args)