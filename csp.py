"""
Eight Variables: A, B, C, D, E, F, G, H
Domain: {1, 2, 3, 4}
Constraints:
- A > G [len 7] x
- A <= H [len 8] x
- |F - B| = 1 [len 6] x
- G < H [len 8] x
- |G - C| = 1 [len 7] x
- |H - C| % 2 == 0 (is even) [len 8] x
- H != D [len 8] x
- D > G [len 7] x
- D != C [len 4] x
- E != C, [len 5] x
- E < D - 1 [len 5] x
- E != H - 2 [len 8] x
- G != F [len 7] x
- H != F [len 8] x
- C != F [len 6] x
- D != F [len 6] x
- |E - F| % 2 != 0 (is odd) [len 6] x
"""

variables = ['B', 'C', 'D', 'E', 'F', 'G', 'H']
domain = [1, 2, 3, 4]

stack = [list(('A', 1)),
         list(('A', 2)),
         list(('A', 3)),
         list(('A', 4))]

solutions = []

global failedBranches
failedBranches = 0

def incFailedBranches():
    global failedBranches
    failedBranches += 1

#[A1 B3 C5 D7 E9 F11 G13 H15]
def checkIfGood(solution):
    # With our constraint ordering, can't know choices are bad until 4th variable
    if 0 <= (len(solution)/2) < 4:
        return True
    elif (len(solution)/2) == 4:
        return solution[7] != solution[5]
    elif (len(solution)/2) == 5:
        return solution[9] != solution[5] and solution[9] < (solution[7] - 1)
    elif (len(solution)/2) == 6:
        return abs(solution[11] - solution[3]) == 1 and solution[5] != solution[11] and solution[7] != solution[11] and (abs(solution[9] - solution[11]) % 2) != 0
    elif (len(solution)/2) == 7:
        return solution[1] > solution[13] and abs(solution[13] - solution[5]) == 1 and solution[7] > solution[13] and solution[13] != solution[11]
    elif (len(solution)/2) == 8:
        return solution[1] <= solution[15] and solution[13] < solution[15] and (abs(solution[15] - solution[5]) % 2) == 0 and solution[15] != solution[7] and solution[9] != (solution[15] - 2) and solution[15] != solution[11]



def solve(variables, domain, stack, solutions, constraint, failedBranches):
    """
    Solves a CSP with a single domain and n variables using a generative DFS
    :param variables: list of the n - 1 other variables to
    :param domain: the domain for each variable (this function can only solve single domain CSPs)
    :param stack: stack with current "paths" found on DFS
    :param solutions: list that our solutions will be output to
    :param constraint: function used to test path for goodness prior to its addition back to the stack
    :return:
    """

    # Base case: only completed paths reach here
    if len(variables) == 0:
        while len(stack) > 0:
            solutions.append(stack.pop())
        return

    newstack = []

    while len(stack) > 0:
        path = stack.pop()
        if len(variables) > 0:
            for option in domain:
                opt = list(path) + list((variables[0], option))

                # We only want to append a path if none of the variables seen so far are in conflict with constraints
                if constraint(opt):
                    newstack.append(opt)
                else:
                    incFailedBranches()

            # remove one variable for the next recursive call
            solve(variables[1:len(variables)], domain, newstack, solutions, constraint, failedBranches)


solve(variables, domain, stack, solutions, checkIfGood, failedBranches)

f = open("dump.txt", 'w')

for solution in solutions:
    if checkIfGood(solution):
        f.write(str(solution))
        f.write("\n")

f.write("Failed branches: " + str(failedBranches))
f.close()
