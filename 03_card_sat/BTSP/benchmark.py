import signal
import time
from BTSP import *


def timeout(signum, frame):
    print('Signal handler called with signal',
          signum)
    raise OSError("timeout exceeded!")


def benchmark_time(time_limit, start_points, step):
    signal.signal(signal.SIGALRM, timeout)

    num_points = start_points
    try:
        while True:
            print(f'Points: {num_points}')
            solver = BTSPSolverSAT(util.random_points(num_points), 2)
            # Use binary search as it is most performant
            signal.alarm(time_limit)
            start = time.time()
            solver.solve(0)
            print(f'Time taken for {num_points} points: {time.time() - start}')
            signal.alarm(0)
            num_points += step
    except OSError as e:
        print(e)

    print(f'Biggest instance to solve in under {time_limit} sec: {num_points - step}, in {time.time() - start}')
    print(f'Failed at {num_points} points')


benchmark_time(300, 615, 5)
