from MIP import *
import statistics


def benchmark_average_time(num_points, iterations):
    times = list()
    for i in range(iterations):
        points = util.random_points(num_points)
        edges = util.all_edges_sorted(points)
        solver = BTSPSolverIP(points, edges)
        solver.model_bottleneck.setParam('LogToConsole', 0)
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
        try:
            last_solvable_instance, time_taken = solver.solve()
        except TimeoutError as e:
            print(e)
            break

        num_points += step

    print(f'Last solvable instance has {num_points - step} points, time taken: {time_taken}')
    draw_edges(last_solvable_instance)
    print(f'First unsolvable instance has {num_points} points:')


# benchmark_time_limit(10, 50, 10)
benchmark_average_time(50, 10)
