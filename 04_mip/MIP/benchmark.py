from MIP import *
import statistics
import random


def benchmark_average_time(num_points, iterations, use_greedy=False):
    times = list()
    for i in range(iterations):
        points = util.random_points(num_points)
        edges = util.all_edges_sorted(points)
        solver = BTSPSolverIP(points, edges)
        solver.model_bottleneck.setParam('LogToConsole', 0)
        if use_greedy:
            start, bottleneck = Greedy_Btsp(points).solve()
            sol, time_taken = solver.solve(start, bottleneck)
        else:
            sol, time_taken = solver.solve()
        times.append(time_taken)
    average_time = statistics.mean(times)
    print(f'Average time: {average_time}')


def benchmark_time_limit(time_limit, start_points, step):
    num_points = start_points
    last_solvable_instance = []
    time_taken = 0

    while True:
        print(f'Number of points: {num_points}')
        points = util.random_points(num_points)
        edges = util.all_edges_sorted(points)
        solver = BTSPSolverIP(points, edges)
        solver.model_bottleneck.setParam('TimeLimit', time_limit)
        solver.model_bottleneck.setParam('LogToConsole', 0)
        try:
            last_solvable_instance, time_taken = solver.solve()
            print(f'Time taken for {num_points} points: {time_taken}')
        except TimeoutError as e:
            print(e)
            break

        num_points += step

    print(f'Last solvable instance has {num_points - step} points, time taken: {time_taken}')
    draw_edges(last_solvable_instance)
    print(f'First unsolvable instance has {num_points} points:')


# benchmark_time_limit(300, 205, 5)
random.seed('123456')
benchmark_average_time(num_points=100, iterations=5, use_greedy=False)
print('############################')
random.seed('123456')
benchmark_average_time(num_points=100, iterations=5, use_greedy=True)
