from ortools.sat.python.cp_model import CpModel, CpSolver, IntVar, OPTIMAL, FEASIBLE
from typing import List, Optional
import itertools
import math

Partition = List[int]

class PartitionSolverCpSat():
    def __init__(self, integers: List[int]) -> None:
        self.integers = integers
    
    def solve(self, k: int) -> Optional[List[Partition]]:
        """
        Solve the k-partition problem with the integers associated with this solver.
        If a feasible solution exists, it is returned as a list of partitions (lists).
        Otherwise, 'None' is returned.
        """

        # create a CP model and solver
        m = CpModel()
        solver = CpSolver()

        # Create n boolean variables for every integer in the list.
        # These variables will be used to indicate to which partition/container each integer is assigned.
        partitions: List[List[IntVar]] = [
            [m.NewBoolVar(f"int_{i}_part_of_partition_{p}") for i in range(len(self.integers))] for p in range(k)
        ]

        # Only allow each integer to be assigned to exactly one partition.
        for i in range(len(self.integers)):
            variables = [p[i] for p in partitions]
            m.AddExactlyOne(variables) # equivalent to m.Add(sum(variables) == 1)

        # This constraint is a symmetry breaker. Without changing the validity of the partitions,
        # one single element can be assigned to one of the partitions. This is done to eliminate
        # "symmetrical" solutions, as solvers tend to take more time in solving problems with
        # these kinds of symmetries.
        m.Add(partitions[0][0] == 1)

        # Build the sums within each partition.
        # This is done by multiplying the variable's values (0 or 1) with the associated integers and summing them up.
        # Note: The variables are special objects that override the mathematical operators (+, *), which return
        # special LinearExpression objects, which can further be used to build mathematical/logical terms.
        sums = [sum(p[i] * self.integers[i] for i in range(len(self.integers))) for p in partitions]

        # Force the equality of all sums (sum[0] == sum[1] == sum[2] == ...).
        for sum1, sum2 in zip(sums, sums[1:]):
            m.Add(sum1 == sum2)
        
        # Call the solver, print solving statistics.
        status = solver.Solve(m)
        print(solver.ResponseStats())

        # Check the solution status.
        if status in (OPTIMAL, FEASIBLE):
            solution = list()
            for p in partitions:
                # Obtain the assigned values from the solver. An integer is contained in the partition if the associated
                # boolean value is 'True'
                values = [i for (i, v) in zip(self.integers, p) if solver.BooleanValue(v)]
                solution.append(sorted(values))
            return solution
        else:
            return None
