"""
Correct unreasonable Chinese spell errors in CGEC input & reference sentences given the manual annotation results.
"""

from collections import defaultdict
import os
import json
import argparse


class Alignment:
    # Alignment adapted from: https://github.com/chrisjbryant/errant/blob/main/errant/alignment.py
    # Input 1: An original text string parsed by spacy
    # Input 2: A corrected text string parsed by spacy
    # Input 3: A flag for standard Levenshtein alignment
    def __init__(self, orig, cor):
        # Set orig and cor
        self.orig = orig
        self.cor = cor
        # Align orig and cor and get the cost and op matrices
        self.cost_matrix, self.op_matrix = self.align()
        # Get the cheapest align sequence from the op matrix
        self.align_seq = self.get_cheapest_align_seq()

    # Input: A flag for standard Levenshtein alignment
    # Output: The cost matrix and the operation matrix of the alignment
    def align(self):
        # Sentence lengths
        o_len = len(self.orig)
        c_len = len(self.cor)
        # Lower case token IDs (for transpositions)
        o_low = [o.lower() for o in self.orig]
        c_low = [c.lower() for c in self.cor]
        # Create the cost_matrix and the op_matrix
        cost_matrix = [[0.0 for j in range(c_len + 1)] for i in range(o_len + 1)]
        op_matrix = [["O" for j in range(c_len + 1)] for i in range(o_len + 1)]
        # Fill in the edges
        for i in range(1, o_len + 1):
            cost_matrix[i][0] = cost_matrix[i - 1][0] + 1
            op_matrix[i][0] = "D"
        for j in range(1, c_len + 1):
            cost_matrix[0][j] = cost_matrix[0][j - 1] + 1
            op_matrix[0][j] = "I"

        # Loop through the cost_matrix
        for i in range(o_len):
            for j in range(c_len):
                # Matches
                if self.orig[i] == self.cor[j]:
                    cost_matrix[i + 1][j + 1] = cost_matrix[i][j]
                    op_matrix[i + 1][j + 1] = "M"
                # Non-matches
                else:
                    del_cost = cost_matrix[i][j + 1] + 1
                    ins_cost = cost_matrix[i + 1][j] + 1
                    trans_cost = float("inf")
                    # Standard Levenshtein (S = 1)
                    sub_cost = cost_matrix[i][j] + 1

                    # Costs
                    costs = [trans_cost, sub_cost, ins_cost, del_cost]
                    # Get the index of the cheapest (first cheapest if tied)
                    l = costs.index(min(costs))
                    # Save the cost and the op in the matrices
                    cost_matrix[i + 1][j + 1] = costs[l]
                    if l == 0:
                        op_matrix[i + 1][j + 1] = "T" + str(k + 1)
                    elif l == 1:
                        op_matrix[i + 1][j + 1] = "S"
                    elif l == 2:
                        op_matrix[i + 1][j + 1] = "I"
                    else:
                        op_matrix[i + 1][j + 1] = "D"
        # Return the matrices
        return cost_matrix, op_matrix

    # Get the cheapest alignment sequence and indices from the op matrix
    # align_seq = [(op, o_start, o_end, c_start, c_end), ...]
    def get_cheapest_align_seq(self):
        i = len(self.op_matrix) - 1
        j = len(self.op_matrix[0]) - 1
        align_seq = []
        # Work backwards from bottom right until we hit top left
        while i + j != 0:
            # Get the edit operation in the current cell
            op = self.op_matrix[i][j]
            # Matches and substitutions
            if op in {"M", "S"}:
                align_seq.append((op, i - 1, i, j - 1, j))
                i -= 1
                j -= 1
            # Deletions
            elif op == "D":
                align_seq.append((op, i - 1, i, j, j))
                i -= 1
            # Insertions
            elif op == "I":
                align_seq.append((op, i, i, j - 1, j))
                j -= 1
            # Transpositions
            else:
                # Get the size of the transposition
                k = int(op[1:])
                align_seq.append((op, i - k, i, j - k, j))
                i -= k
                j -= k
        # Reverse the list to go from left to right and return
        align_seq.reverse()
        return align_seq


md_styles = {
    "ins": (
        f"<span style='color:blue;font-weight:700;border-bottom: 1.5px dotted black;'>",
        "</span>",
    ),
    "del": (
        f"<span style='color: rgb(255, 168, 168);text-decoration:line-through;text-decoration-thickness:from-font;border-bottom: 1.5px dotted black;'>",
        "</span>",
    ),
    "sub": (
        f"<span style='color:green;font-weight:700;border-bottom: 1.5px dotted black;'>",
        "</span>",
    ),
}

error_types = [
    '音似错别字',
    '形似错别字',
    '“的地得”误用',
    '繁体字/异体字',
    '其他错别字',
    '符号错误',
    '多字',
    '漏字',
    '字序',
    '人名错误',
    '专有名词错误',
    '句法错误',
]


def main(args):
    assert args.annotation_file.endswith(".jsonl")
    n_verified = 0
    n_correct = 0
    cleaning_report = defaultdict(list)
    csc_annotation = {}
    f_annotation = open(args.annotation_file)
    for line in f_annotation:
        item = json.loads(line.strip())
        src = item["source"].strip()
        corrected_src = item["verified"].strip()
        if "没有错误" in item['label']:
            csc_annotation[src] = src
            n_correct += 1
            continue
        # assert source not in csc_annotation, f'Duplicate source: {source}'
        if src in csc_annotation:
            assert corrected_src == csc_annotation[src], f"Duplicate source with different verified text: {src}, {corrected_src}, {csc_annotation[src]}"
            continue
        else:
            csc_annotation[src] = corrected_src
            n_verified += 1
            for error_type in item['label']:
                cleaning_report[error_type].append(item)
    f_annotation.close()
    if args.verbose:
        verification_summary = f"""
        Verification Summary
        ----------------------------------------------------------------
        - Number of Verified Sentences:            {n_verified}
        - Number of Correct Sentences:             {n_correct}

        """
        print(verification_summary)

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    for file_name in args.file_names.split(","):
        all_cnt = 0
        src_csc_cnt = 0
        tgt_csc_cnt = 0
        data_path = os.path.join(args.data_dir, file_name)
        out_path = os.path.join(args.out_dir, file_name)
        if args.verbose:
            print(f"Processing {data_path}...")
        n_changes = 0
        n_change_sources = 0
        n_change_targets = 0
        n_sentences = 0
        n_target_sentences = 0
        n_fail_to_find_by_humans = 0
        n_fail_to_find_by_all_humans = 0
        used_data = set()
        f_data = open(data_path)
        f_out = open(out_path, "w")
        for line in f_data:
            idx, *sentences = line.strip().split("\t")
            src, *tgts = sentences
            used_data.update(sentences)
            new_tgts = []
            if src in csc_annotation:
                new_src = csc_annotation[src]
                src_csc_cnt += 1
            else:
                new_src = src

            for tgt in tgts:
                if tgt in csc_annotation:
                    tgt = csc_annotation[tgt]
                    tgt_csc_cnt += 1
                new_tgts.append(tgt)
            all_cnt += 1
            new_line = f"{idx}\t{new_src}\t" + "\t".join(new_tgts)
            if new_line != line:
                n_changes += 1
            this_change_targets = len([1 for s, v in zip(tgts, new_tgts) if s != v])
            n_change_targets += this_change_targets
            if src != new_src:
                n_change_sources += 1
                if this_change_targets > 0:
                    n_fail_to_find_by_humans += 1
                if this_change_targets == len(tgts):
                    n_fail_to_find_by_all_humans += 1
            n_sentences += 1
            n_target_sentences += len(tgts)
            f_out.write(f"{new_line}\n")
        f_data.close()
        f_out.close()
        if args.verbose:
            changes_summary = f"""
            Changes Summary
            ----------------------------------------------------------------
            - Overall Changes:
                Number of Changes:                     {n_changes}
                Number of Sentences:                   {n_sentences}
                Percentage of Changes:                 {n_changes / n_sentences * 100:.2f}%
                
            - Source Changes:
                Number of Source Changes:              {n_change_sources}
                Percentage of Source Changes:          {n_change_sources / n_sentences * 100:.2f}%
                
            - Target Changes:
                Number of Target Changes:              {n_change_targets}
                Percentage of Target Changes:          {n_change_targets / n_target_sentences * 100:.2f}%
                
            - Failures to Find (by at least one human):
                Number:                                {n_fail_to_find_by_humans}
                Percentage:                            {n_fail_to_find_by_humans / n_change_sources * 100:.2f}%
                
            - Failures to Find (by all humans):
                Number:                                {n_fail_to_find_by_all_humans}
                Percentage:                            {n_fail_to_find_by_all_humans / n_change_sources * 100:.2f}%

            """

            print(changes_summary)

        if args.generate_report:
            print('Generating markdown report...')
            # clean up verified report for this file
            this_cleaning_report = {}
            for error_type in error_types:
                items = cleaning_report[error_type]
                new_items = []
                for item in items:
                    source = item['source']
                    if source in used_data:
                        new_items.append(item)
                this_cleaning_report[error_type] = new_items
            # generate markdown report
            report_path = os.path.join(args.out_dir, f'{file_name}.cleaning_report.md')
            with open(report_path, 'w') as writer:
                writer.write(f'# Refinement Report for __{file_name}__ Dataset\n')
                writer.write(f'- Instance: \n')
                writer.write(f'  - Number of instance: {n_sentences}\n')
                writer.write(f'  - Number of instance with spelling errors: {n_changes}\n')
                writer.write(f'  - Percentage of instance with spelling errors: {n_changes / n_sentences * 100:.2f}%\n\n')
                writer.write(f'- Source: \n')
                writer.write(f'  - Number of source sentences: {n_sentences}\n')
                writer.write(f'  - Number of source with spelling errors: {n_change_sources}\n')
                writer.write(f'  - Percentage of source with spelling errors: {n_change_sources / n_sentences * 100:.2f}%\n\n')
                writer.write(f'- Target: \n')
                writer.write(f'  - Number of target sentences: {n_target_sentences}\n')
                writer.write(f'  - Number of target with spelling errors: {n_change_targets}\n')
                writer.write(f'  - Percentage of target with spelling errors: {n_change_targets / n_target_sentences * 100:.2f}%\n\n')
                writer.write(f'- Human Verification: \n')
                writer.write(f'  - Number of simple text errors that failed to be identified by at least one human: {n_fail_to_find_by_humans}\n')
                writer.write(
                    f'  - Percentage of simple text errors that failed to be identified by at least one human: {n_fail_to_find_by_humans / n_change_sources * 100:.2f}%\n\n'
                )
                writer.write(f'  - Number of simple text errors that failed to be identified by all human: {n_fail_to_find_by_all_humans}\n')
                writer.write(
                    f'  - Percentage of simple text errors that failed to be identified by all human: {n_fail_to_find_by_all_humans / n_change_sources * 100:.2f}%\n\n'
                )
                writer.write('## Error Distribution\n')
                writer.write(f'| Error Type | Number of Refinements | Percentage |\n')
                writer.write(f'| --- | --- | --- |\n')
                for error_type in error_types:
                    items = this_cleaning_report[error_type]
                    writer.write(f'| <a href="#{error_type}">{error_type}</a> | {len(items)} | {len(items) / n_verified * 100:.2f}% |\n')
                writer.write('\n')
                for error_type in error_types:
                    items = this_cleaning_report[error_type]
                    if len(items) == 0:
                        continue
                    writer.write(f'<h2 id="{error_type}">{error_type}</h2>\n')
                    writer.write(f'Number of refinements: {len(items)}\n\n')
                    writer.write('### Refinements\n')
                    for i, item in enumerate(items):
                        id = item['source']
                        verified = item['verified']
                        pred_edits = Alignment(list(id), list(verified)).align_seq
                        writer.write(f'#### Refinement {i + 1}\n')
                        writer.write(f'> **Original**: {id}\n')
                        writer.write(f'> \n')
                        formatted_verified = ''
                        for t, s_b, s_e, t_b, t_e in pred_edits:
                            if t == 'M':
                                formatted_verified += verified[t_b:t_e]
                            elif t == 'S':
                                formatted_verified += md_styles['sub'][0] + verified[t_b:t_e] + md_styles['sub'][1]
                            elif t == 'I':
                                formatted_verified += md_styles['ins'][0] + verified[t_b:t_e] + md_styles['ins'][1]
                            elif t == 'D':
                                formatted_verified += md_styles['del'][0] + id[s_b:s_e] + md_styles['del'][1]
                        writer.write(f'> **Refined**:  {formatted_verified}\n\n')
                    writer.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", help="dir of all datasets needed processing", required=True)
    parser.add_argument("--out_dir", help="dir of all output datasets", required=True)
    parser.add_argument("--file_names", help="CGEC file names, split by english comm", required=True)
    parser.add_argument("--annotation_file", help="manual CSC annotation results", required=True)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--generate_report", action="store_true")
    args = parser.parse_args()
    main(args)
