import subprocess as sp
from defaults import DECIMAL_PLACES, KMAX, NUMBER_OF_CANDIDATES, LIB_FILE
from sys import exit


if DECIMAL_PLACES % 2 != 0:
    print("Invalid decimal places:", DECIMAL_PLACES)
    exit(1)


def get_info():
    lst = []
    with open(LIB_FILE, 'r') as rf:
        for r in rf:
            if r.count('const'):
                r = r.strip().split(' ')
                r = {r[1]: r[4][:-1]}
                lst.append(r)
    string = '|'.join([f'{d}' for d in lst]).replace('{', '').replace('}', '')
    return string


def display(candidate, echo=True):
    disp = ['{:f}'.format(round(d, DECIMAL_PLACES))
            for d in candidate['dist'][2:KMAX + 1]]
    t = '{:.7f}'.format(candidate['t'], 7)
    d = '{:.2f}'.format(candidate['d'], 2)
    g = '{:.2f}'.format(candidate['g'] / 100, 2)
    if 'i' in candidate.keys():
        i = candidate['i'].rjust(len(str(NUMBER_OF_CANDIDATES)), ' ')
        if echo:
            print(f'[{i}/{NUMBER_OF_CANDIDATES}]', end=' ')
    string = ' '.join(['[\"' + '\", \"'.join(disp) + '\"]', g, d, t])
    if echo:
        print(string)
    return string


def strip_line(space=True):
    r = int(DECIMAL_PLACES / 2)
    bar = ''.join(['-' for _ in range(r)])
    num = NUMBER_OF_CANDIDATES
    numbers = '  '.join(
        [f" {bar}{str(s).rjust(2, ' ')}{bar} " for s in range(2, KMAX + 1)])
    numbers += '  - G- DEG. --- T ---'
    if space:
        spaces = ' ' + ''.join([' ' for _ in range(len(f'[{num}/{num}]'))])
    else:
        spaces = ''
    print(spaces, numbers)


def write_header(filename):
    disp = ','.join([f'dist{k}' for k in range(2, KMAX + 1)])
    string = f'count,{disp},g,t,swaps'
    sp.call(f'echo "{string}" >> {filename}', shell=True)
    return filename


def write_to_cands(filename, count, candidates, swap_num):
    for idx, candidate in enumerate(candidates):
        disp = ','.join(['{:f}'.format(round(d, DECIMAL_PLACES))
                         for d in candidate['dist'][2:KMAX + 1]])
        string = f'{disp},{candidate["g"]},{candidate["t"]}'
        if idx > 0:
            sp.call(f'echo "{string}" >> {filename}', shell=True)
        else:
            sp.call(f'echo "{string}" >| {filename}', shell=True)


def write_to_log(filename, count, candidate, swap_num):
    disp = ','.join(['{:f}'.format(round(d, DECIMAL_PLACES))
                     for d in candidate['dist'][2:KMAX + 1]])
    string = f'{count},{disp},{candidate["g"]},{candidate["t"]},{swap_num}'
    sp.call(f'echo "{string}" >> {filename}', shell=True)


def swap(c1, c2):
    c1['t'] = c2['t']
    c1['g'] = c2['g']
    c1['p'] = c2['p']
    c1['dist'] = [c for c in c2['dist']]


def search_best(candidates):
    max_c = {'t': 0.0, 'd': 0.0, 'g': 100, 'dist': []}
    for candidate in candidates:
        if candidate['t'] > max_c['t']:
            swap(max_c, candidate)
    return max_c
