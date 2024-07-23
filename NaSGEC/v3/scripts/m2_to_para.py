import argparse


def main(args):
    f_m2 = open(args.m2_file)
    f_input = open(args.input_file)
    f_out = open(args.out_file, "w")
    m2 = f_m2.read().strip().split("\n\n")
    data = f_input.read().strip().split('\n')
    for idx, (edits, line) in enumerate(zip(m2, data), start=1):
        tgts = []
        src = ""
        for edit in edits.split("\n"):
            if edit[0] == "S":
                src = "".join(edit.split(" ")[1:])
            if edit[0] == "T":
                tgts.append("".join(edit.split(" ")[1:]))
        try:
            assert src == line.split("\t")[1]
        except:
            assert src == line.split("\t")[1].replace("\u3000", "")
            raw_src = line.split("\t")[1]
            print(repr('raw src: ' + raw_src))
            if src == '我最喜欢的导演是"宫崎骏"20多年以前，我还是大学生，当时我看了他的第一个电影"风之谷"。':
                cleaned_src = raw_src.replace("\u3000", "，")
            else:
                cleaned_src = raw_src.replace("\u3000", "")
            print(repr('cleaned_src: ' + cleaned_src))
            src = cleaned_src
        print(idx, src, "\t".join(tgts), sep="\t", file=f_out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--m2_file", help="m2 file", required=True)
    parser.add_argument("--input_file", help="input sentences file path", required=True)
    parser.add_argument("--out_file", help="out file path", required=True)
    args = parser.parse_args()
    main(args)
