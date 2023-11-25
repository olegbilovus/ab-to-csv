import argparse


def sep_strip(data, space=False, sep=':'):
    res = data.split(sep)[1].strip()
    if space:
        res = res.split(' ')[0]
    return res


def ab_to_dict(data):
    ab_dict = {'server': sep_strip(data[0]),
               'host': sep_strip(data[1]),
               'port': sep_strip(data[2]),
               'path': sep_strip(data[4]),
               'doc_len': sep_strip(data[5], True),
               'conc': sep_strip(data[7]),
               'time': sep_strip(data[8], True),
               'r_comp': sep_strip(data[9]),
               'r_fail': sep_strip(data[10]),
               'rps': sep_strip(data[13], True),
               'tpr': sep_strip(data[14], True),
               'tpr_all': sep_strip(data[15], True)}

    i = -1
    for j in range(15, len(data)):
        if '50%' in data[j]:
            i = j
            break

    sep = '%'
    ab_dict['50'] = sep_strip(data[i], sep=sep)
    ab_dict['66'] = sep_strip(data[i + 1], sep=sep)
    ab_dict['75'] = sep_strip(data[i + 2], sep=sep)
    ab_dict['80'] = sep_strip(data[i + 3], sep=sep)
    ab_dict['90'] = sep_strip(data[i + 4], sep=sep)
    ab_dict['95'] = sep_strip(data[i + 5], sep=sep)
    ab_dict['98'] = sep_strip(data[i + 6], sep=sep)
    ab_dict['99'] = sep_strip(data[i + 7], sep=sep)
    ab_dict['100'] = sep_strip(data[i + 8], True, sep=sep)

    return ab_dict


def extra_data(data):
    values = data.split(' ')
    dir_values = {}
    for val in values:
        k, v = val.split('=')
        dir_values[k] = v

    return dir_values


def add_extra_data(e_data, out_csv):
    out_csv[0] = out_csv[0][:-1]
    out_csv[-1] = out_csv[-1][:-1]
    headers = out_csv[0].split(',')
    values = out_csv[-1].split(',')

    for k, v in e_data.items():
        try:
            i = headers.index(k)
        except ValueError:
            i = len(headers)
            headers.append(k)

        len_values = len(values)
        if i >= len_values:
            values.extend(['' for _ in range(i - len_values + 1)])
        values[i] = v

    out_csv[0] = ','.join(headers) + '\n'
    out_csv[-1] = ','.join(values)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('ab to CSV')
    in_grp = parser.add_mutually_exclusive_group(required=True)
    in_grp.add_argument('--inp', help='Input file')
    in_grp.add_argument('--stdin', action='store_true', help='Input from stdin')
    parser.add_argument('--out', required=True, help='Output file')
    parser.add_argument('-a', action='store_true', help='Append to input file')
    parser.add_argument('--extra_data', help='Add extra data. Format is the same as in Ansible for --extra-vars: '
                                             '"k1=v1 k2=v2"')

    args = parser.parse_args()

    if args.stdin:
        _data = []
        while True:
            try:
                line = input()
                _data.append(line)
            except EOFError:
                break
    else:
        with open(args.inp, 'r') as f:
            _data = f.readlines()

    mode = 'a' if args.a else 'w'
    with open(args.out, mode) as f:
        abd = ab_to_dict(_data[7:])
        csv_str = ''
        if not args.a:
            csv_str = ','.join(abd.keys())
            csv_str += '\n'
        csv_str += ','.join(abd.values())
        csv_str += '\n'
        f.write(csv_str)

    if args.extra_data:
        with open(args.out, 'r+') as f:
            f_data = f.readlines()
            ex_data = extra_data(args.extra_data)
            add_extra_data(ex_data, f_data)
            f.seek(0)
            f.write(''.join(f_data))
