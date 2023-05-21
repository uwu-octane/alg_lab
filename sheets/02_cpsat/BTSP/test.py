import threading
import time


def solver_test(time_limit, instance_limit, solver_class, param_generator, using_circle_constraints):
    results = []
    current_size = 0
    running_time = 0

    def target(param, using_circle_constraints):
        nonlocal current_size
        nonlocal running_time
        solver_instance = solver_class(param, using_circle_constraints)
        running_time = 0

        start = time.time()
        result = solver_instance.solve()
        end = time.time()

        running_time = end - start

        results.append(result)
        current_size = len(results)

    while len(results) < instance_limit and running_time <= time_limit:
        param = next(param_generator)
        t = threading.Thread(target=target, args=(param[1], ), kwargs={"using_circle_constraints": using_circle_constraints})
        print("solving instance: ", param[0])
        print("current size: ", current_size)
        t.start()
        t.join()

    return results
