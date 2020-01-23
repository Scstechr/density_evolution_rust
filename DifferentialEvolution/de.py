import subprocess as sp
import numpy as np
import sys
from tqdm import tqdm
from rands import random_dist, random_name
from defaults import NUMBER_OF_CANDIDATES, SOURCE_FILE, RELEASE_FILE, MUTATION_FACTOR, OFFSET
from misc import swap, display


def initialize():
    lst = []
    for i in tqdm(range(NUMBER_OF_CANDIDATES)):
        lst.append({'i': str(i + 1), 't': 0.0, 'd': 0.0,
                    'g': 150, 'dist': random_dist()})
    return lst


def evaluate(candidate):
    name = random_name()
    lst = map(str, candidate['dist'])
    pmf = ','.join(lst)
    string = f"""
pub const PMF: [f64; 21] = [{pmf}];
"""
    sp.call(f"echo '{string}' >| {SOURCE_FILE}", shell=True)
    sp.call(f"cargo build --quiet --release", shell=True)
    sp.call(f"mv {RELEASE_FILE} temp/{name}", shell=True)
    # print(f"temp/{name} {candidate['g']}")
    start = candidate['g'] - OFFSET
    if start < 100:
        start = 100
    output = sp.getoutput(f"temp/{name} {start}")
    # print(output)
    try:
        candidate['g'] = int(output.split("\n")[-1].split(',')[0])
        candidate['d'] = float(output.split("\n")[-1].split(',')[1])
        candidate['t'] = float(output.split("\n")[-1].split(',')[2])
    except:
        print(output)
        sys.exit(1)
    # print(candidate)
    sp.call(f"rm temp/{name}", shell=True)
    return random_name


def evaluation(candidates):
    for candidate in tqdm(candidates):
        evaluate(candidate)
        # display(candidate)


def mutate(idx, candidate, candidates):
    idxs = [i for i in range(NUMBER_OF_CANDIDATES) if i != idx]
    selected = np.random.choice(idxs, 3, replace=False)
    a = candidates[selected[0]]
    b = candidates[selected[1]]
    c = candidates[selected[2]]
    mutant = []
    for idxx in range(21):
        r = abs(a['dist'][idxx] + MUTATION_FACTOR *
                (b['dist'][idxx] - c['dist'][idxx]))
        if np.random.rand() > 0.5:
            mutant.append(r)
        else:
            mutant.append(candidate['dist'][idxx])
    mutant = [m / sum(mutant) for m in mutant]
    mutant = {'g': candidate['g'], 'd': 0.0, 't': 0.0, 'dist': mutant}
    evaluate(mutant)
    return mutant


def mutation_mute(candidates, logfile):
    swap_num = 0
    idx = 0
    for candidate in tqdm(candidates):
        mutant = mutate(idx, candidate, candidates)
        if mutant['t'] > candidate['t']:
            swap_num += 1
            swap(candidate, mutant)
            sp.call(
                f'echo "{display(candidate, echo = False)}" >> {logfile}', shell=True)
        idx += 1
    return swap_num


def mutation(candidates):
    swap_num = 0
    for idx, candidate in enumerate(candidates):
        mutant = mutate(idx, candidate, candidates)
        if mutant['t'] > candidate['t']:
            swap_num += 1
            swap(candidate, mutant)
            print("\033[93m", end='')
            display(candidate)
            print("\033[m", end='')
        else:
            display(candidate)
    return swap_num


if __name__ == "__main__":
    [display(l) for l in initialize()]
