import numpy as np


def get_solution(table):
    return get_coeffs(table, len(table[0]) - 1, 0)


def get_coeffs(table, index, start):
    coeffs = [var[index] for var in table]
    return coeffs[start:]


def is_final_table(table):
    obj_func = table[0][:len(table[0]) - 1]
    for var in obj_func:
        if var < 0:
            return False

    return True


def get_entering_index(table):
    return table[0].index(min(table[0][:len(table[0]) - 2]))


def get_pivot_in_iteration(table):
    obj_func = table[0]
    entering_index = get_entering_index(table)
    rhs_coeffs = get_coeffs(table, index=len(obj_func) - 1, start=1)
    pivot_coeffs = get_coeffs(table, index=entering_index, start=1)
    zipped_lists = zip(rhs_coeffs, pivot_coeffs)
    ratios = []
    for (rhs_var, pivot_var) in zipped_lists:
        if pivot_var == 0:
            ratios.append(0)
        else:
            ratios.append(rhs_var / pivot_var)
    positive_ratios = [i for i in ratios if i > 0]
    if len(positive_ratios) == 0:
        return "no pivot"
    exiting_index = ratios.index(min(positive_ratios)) + 1
    return entering_index, exiting_index


def do_pivot(table, entering_col, exiting_row, pivot):
    pivot_row = table[exiting_row]
    if pivot != 1:
        pivot_row = [(var / pivot) for var in pivot_row]
        table[exiting_row] = pivot_row
        pivot = table[exiting_row][entering_col]
    for r, row in enumerate(table):
        print("entering col", entering_col, sep=" ")
        multiplier = (-1) * row[entering_col]
        print("mult ", multiplier)
        for c, var in enumerate(row):
            if r != exiting_row:
                table[r][c] = var + multiplier * table[exiting_row][c]


def next_iteration(table):
    if get_pivot_in_iteration(table) == "no pivot":
        return "infeasible"
    entering_col, exiting_row = get_pivot_in_iteration(table)
    pivot_col = get_coeffs(table, index=entering_col, start=0)
    pivot = table[exiting_row][entering_col]
    do_pivot(table, entering_col, exiting_row, pivot)
    print_table(table)
    return table


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
    print()


def simplex_method(table):
    if is_final_table(table):
        print("Final table:")
        print_table(table)
        return
    while not is_final_table(table):
        table = next_iteration(table)
        if table == "infeasible":
            print("infeasible")
            break


def get_artificial_vars_pivot_positions(table, num_of_var, num_of_art_var):
    art_var_index = num_of_var - num_of_art_var
    row = 1
    positions = []
    for col in range(art_var_index, len(table[0]) - 1):
        if table[row][col] != 1:
            print("wrong format")
            return
        positions.append((row, col))
        row += 1
    return positions


def phase1(table, total_vars, total_art_vars):
    positions = get_artificial_vars_pivot_positions(table, total_vars, total_art_vars)
    if positions == "wrong format":
        print("wrong format")
        return "wrong format"
    for r, c in positions:
        pivot = table[r][c]
        do_pivot(table, pivot=pivot, entering_col=c, exiting_row=r)
    print_table(table)
    simplex_method(table)
    # return table


#         replace row 0 with objective function and remove art variables

# this function checks if phase 2 is possible
def is_phase2_ready(table, total_vars, total_art_vars):
    # TODO:    usually check if artificial vars are still in column 0 - if yes - infeasable else ready for phase 1
    # TODO: never mind - can just check if artifical vars are 1 in obj row and that z' is 0
    for i in range(total_vars - total_art_vars, len(table[0])):
        if i == len(table[0]) - 1:
            if table[0][i] != 0:
                return False
        elif table[0][i] != 1:
            return False
    return True


def two_phase_simplex(table, obj_func, total_vars, total_art_vars):
    phase1(table, total_vars, total_art_vars)
    print("phase 1 over")
    if is_phase2_ready(table, total_vars, total_art_vars):
        print("ready")
        phase2(table, obj_func, total_vars, total_art_vars)
    return


def make_ready_for_simplex(table):
    # get positions of pivots
    positions = []
    for col in range(0, len(table[0]) - 1):
        row = col + 1
        position = (row, col)
        positions.append(position)
    for (row, col) in positions:
        do_pivot(table, exiting_row=row, entering_col=col, pivot=table[row][col])


def phase2(table, obj_func, total_vars, total_art_vars):
    print("phase2")
    # replace the first row with the objective function and remove artificial variables
    new_table = np.array(table)
    new_table = np.delete(new_table, np.s_[total_vars - total_art_vars:len(table[0]) - 1], axis=1)
    new_table[0][0:len(new_table[0]) - 1] = obj_func
    new_table = new_table.tolist()
    # before simplex method need to make it ready - by pivoting
    print_table(new_table)
    make_ready_for_simplex(new_table)
    simplex_method(new_table)


if __name__ == "__main__":
    objective_func = [5, 1]
    z_prime = [0, 0, 1, 1, 0]
    first_table = [z_prime, [1, -3, 1, 0, 1], [2, -1, 0, 1, 3]]
    two_phase_simplex(first_table, obj_func=objective_func, total_art_vars=2, total_vars=4)

# variables = int(input("Enter the number of variables: "))
# constraints = int(input("Enter the number of constraints: "))
# generate_table(variables, constraints)

# TODO: organize start of main problem
# variables = ["d1", "d2", "d3", "d4"]
# artificial_variables = []
# const_num = 8
# z = [20, 30, 40, 25]
# t1 = [[-1, -2, -2, 0, 0, 0], [2, 1, 0, 1, 0, 8], [0, 0, 1, 0, 1, 10]]
# pb = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#       [1, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 10],
#       [0, 1, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 20],
#       [1, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 60],
#       [0, 1, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 20],
#       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 40],
#       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 30],
#       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 80],
#       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 60]]
# two_phase_simplex(table=pb, obj_func=[0, 0, 20, 20, 20, 20, 30, 30, 30, 30, 40, 40, 40, 40, 25, 25, 25, 25],
#                   total_vars=26, total_art_vars=8)
