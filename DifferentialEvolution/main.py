import subprocess as sp
from defaults import NUMBER_OF_CANDIDATES, NUMBER_OF_COUNTS, DISPLAY
from misc import write_to_cands, write_header, write_to_log, search_best, strip_line, display, get_info
from de import initialize, evaluation, mutation, mutation_mute
from datetime import datetime


def main():
    origin = datetime.now()

    filename = datetime.today().strftime('logs/log_%Y%m%d%H%M%S.csv')
    logfile = filename.replace(".csv", "_sub")
    cands_file = filename.replace(".csv", "_cands")

    elapse = datetime.now() - origin
    header = f" \033[93mSTART SIMULATION: [{datetime.now()}] [{datetime.now() - origin}] (+{elapse}) \033[m"
    print(header)
    info = f'#{get_info()}'
    print(info)
    sp.call(f'echo "{info}" >> {filename}', shell=True)
    # Log files in log directory
    write_header(filename)

    # Early stages of D.E.
    elapse = datetime.now() - origin
    header = f" \033[31m[{datetime.now()}] [{datetime.now() - origin}] (+{elapse}) "
    print(f" \033[31m\nINITIALIZATION  : {header}\033[m")
    candidates = initialize()
    elapse = datetime.now() - origin
    header = f" \033[92m[{datetime.now()}] [{datetime.now() - origin}] (+{elapse}) "
    print(f" \033[92m\nFIRST EVALUATION: {header}\033[m")
    evaluation(candidates)
    print()

    # Start mutation
    best = {}
    elapse = datetime.now() - origin
    for count in range(1, NUMBER_OF_COUNTS + 1):
        start = datetime.now()
        if count == 1:
            swap_num = 0
        write_to_cands(cands_file, count, candidates, swap_num)
        header = f" \033[96mMUTATION&UPDATE : [{datetime.now()}] [{datetime.now() - origin}] (+{elapse}) "
        if count > 0:
            header += f" ITERATION NO.{count}, LAST: {swap_num}/{NUMBER_OF_CANDIDATES}\033[m"
            print(header)
            sp.call(f'echo "{header}" >> {logfile}', shell=True)
        else:
            print(header, "\033[m")
        if DISPLAY:
            strip_line()
            swap_num = mutation(candidates)
        else:
            swap_num = mutation_mute(candidates, logfile)
        best = search_best(candidates)
        write_to_log(filename, count, best, swap_num)
        sp.call(f'echo "BEST:{display(best, echo=False)}\n" >> {logfile}', shell=True)
        if DISPLAY:
            scrolls = NUMBER_OF_CANDIDATES + 1
        else:
            scrolls = 1
        if swap_num > 0 and count < NUMBER_OF_COUNTS:
            print("\n \033[41m BEST:\033[m")
            strip_line(space=False)
            display(best)
            print(f"\033[m\033[5F\033[2K", end='')
            for _ in range(scrolls):
                print(f"\033[2K\033[F", end='')
        else:
            break
        end = datetime.now()
        elapse = end - start
    print(f"\n \033[41mBEST OUT OF {count} ITERATION(S)\033[m")
    strip_line(space=False)
    display(best)


main()
