# Function that generates a matrix of correct size
# Functions that check if the the current solution is optimal
# Functions that determines where a pivot element is located
# Function that pivots about an element
# Functions to receive string input and insert float variables into matrix
# Functions to maximize and minimize the problem

# generate first table based on number of variables and contraints
# def generate_table(variables, constraints):
#     # table = np.zeros((constraints + 1, variables + constraints + 2))
#     print(table)
#     return table

def get_solution(table):
    return get_coeffs(table, len(table[0]) - 1, 0)


def get_coeffs(table, index, start):
    coeffs = [var[index] for var in table]
    return coeffs[start:]


def is_final_table(table):
    obj_func = table[0]
    for var in obj_func:
        if var < 0:
            return False

    return True


def get_entering_index(table):
    return table[0].index(min(table[0]))


def get_pivot(table):
    obj_func = table[0]
    entering_index = get_entering_index(table)
    # print(entering_var, entering_index)
    rhs_coeffs = get_coeffs(table, index=len(obj_func) - 1)
    pivot_coeffs = get_coeffs(table, index=entering_index, start=1)
    # print(rhs_coeffs)
    # print(pivot_coeffs)
    zipped_lists = zip(rhs_coeffs, pivot_coeffs)
    ratios = []
    for (rhs_var, pivot_var) in zipped_lists:
        if pivot_var == 0:
            ratios.append(0)
        else:
            ratios.append(rhs_var / pivot_var)
    exiting_index = ratios.index(min(ratios)) + 1
    return entering_index, exiting_index


def print_table(table):
    print("------------------------------")
    for row in table:
        for col in row:
            if col < 0:
                print(col, end=" |  ")
            else:
                print(col, end="  |  ")
        if table.index(row) == 0:
            print()
            print("------------------------------", end="")
        print()
    print("------------------------------")


# pivot and return new table
if __name__ == "__main__":
    # variables = int(input("Enter the number of variables: "))
    # constraints = int(input("Enter the number of constraints: "))
    # generate_table(variables, constraints)
    print("hi")
    t = [[-4, -3, 0, 0, 0], [1, 1, 1, 0, 40], [2, 1, 0, 1, 60]]
    t1 = [[-1, -2, -2, 0, 0, 0], [2, 1, 0, 1, 0, 8], [0, 0, 1, 0, 1, 10]]
    print(get_solution(t1))
    print_table(t)
    # a = np.array([[-4, -3, 0], [1, 1, 1], [2, 1, 0]])
    # b = np.array([0, 40, 60])
    # x = np.linalg.solve(a, b)
    # print(x)
# get number of towns
# enter average for each town
# enter position for each town
# for each town: 2 constraints
# 1 0 1 -1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 10
# 0 1 0 0 1 -1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 20
# 1 0 0 0 0 0 1 -1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 60
# 0 1 0 0 0 0 0 0 1 -1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 20
# 1 0 0 0 0 0 0 0 0 0 1 -1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 40
# 0 1 0 0 0 0 0 0 0 0 0 0 1 -1 0 0 0 0 0 0 0 0 0 1 0 0 30
# 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -1 0 0 0 0 0 0 0 0 1 0 80
# 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -1 0 0 0 0 0 0 0 1 60
