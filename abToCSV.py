import argparse


def sep_strip(data, space=False, sep=':'):
    res = data.split(sep)[1].strip()
    if space:
        res = res.split(' ')[0]
    return res


def ab_to_dict(input):
    ab_dict = {}
    ab_dict['server'] = sep_strip(input[0])
    ab_dict['host'] = sep_strip(input[1])
    ab_dict['port'] = sep_strip(input[2])
    ab_dict['path'] = sep_strip(input[4])
    ab_dict['doc_len'] = sep_strip(input[5], True)
    ab_dict['conc'] = sep_strip(input[7])
    ab_dict['time'] = sep_strip(input[8], True)
    ab_dict['r_comp'] = sep_strip(input[9])
    ab_dict['r_fail'] = sep_strip(input[10])
    ab_dict['rps'] = sep_strip(input[13], True)
    ab_dict['tpr'] = sep_strip(input[14], True)
    ab_dict['tpr_all'] = sep_strip(input[15], True)

    i = -1
    for j in range(15, len(input)):
        if '50%' in input[j]:
            i = j
            break

    sep = '%'
    ab_dict['50'] = sep_strip(input[i], sep=sep)
    ab_dict['66'] = sep_strip(input[i + 1], sep=sep)
    ab_dict['75'] = sep_strip(input[i + 2], sep=sep)
    ab_dict['80'] = sep_strip(input[i + 3], sep=sep)
    ab_dict['90'] = sep_strip(input[i + 4], sep=sep)
    ab_dict['95'] = sep_strip(input[i + 5], sep=sep)
    ab_dict['98'] = sep_strip(input[i + 6], sep=sep)
    ab_dict['99'] = sep_strip(input[i + 7], sep=sep)
    ab_dict['100'] = sep_strip(input[i + 8], True, sep=sep)

    return ab_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser('ab to CSV')
    in_grp = parser.add_mutually_exclusive_group(required=True)
    in_grp.add_argument('--inp', help='Input file')
    parser.add_argument('--out', required=True, help='Output file')
    parser.add_argument('-a', action='store_true', help='Append to input file')
    in_grp.add_argument('--stdin', action='store_true', help='Input from stdin')

    args = parser.parse_args()

    if args.stdin:
        data = []
        while True:
            try:
                line = input()
                data.append(line)
            except EOFError:
                break
    else:
        with open(args.inp, 'r') as f:
            data = f.readlines()

    mode = 'a' if args.a else 'w'
    with open(args.out, mode) as f:
        abd = ab_to_dict(data[7:])
        csv_str = ''
        if not args.a:
            csv_str = ','.join(abd.keys())
            csv_str += '\n'
        csv_str += ','.join(abd.values())
        csv_str += '\n'
        f.write(csv_str)
