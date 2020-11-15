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


def get_entering_index(table, skip):
    obj_row = table[0][:len(table[0]) - 2]
    pair = [(i, num) for i, num in enumerate(obj_row) if num < 0 and i not in skip]
    if len(pair) == 0:
        return "no pivot"
    min_pair = min(pair, key=lambda p: p[1])
    entering_index = min_pair[0]
    print("entering index ", entering_index)
    if entering_index is None:
        return "no pivot"
    return entering_index


# row_vars = ["x1", "x2", "a1", "a2"]
# artificial_vars = ["a1", "a2"]
# basic_vars = ["a1", "a2"]
row_vars = ["x", "y", "d1", "d2", "d3", "d4", "e1", "e2", "e3", "e4", "w1", "w2", "w3", "w4", "n1", "n2", "n3",
            "n4", "s1", "s2", "s3", "s4", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10", "a11", "a12"]
artificial_vars = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10", "a11", "a12"]
basic_vars = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10", "a11", "a12"]


def enter_exit_variable(table, entering_index, exiting_index):
    enter = row_vars[entering_index]
    exit = basic_vars[exiting_index - 1]
    basic_vars[exiting_index - 1] = enter
    print("enter " + row_vars[entering_index])
    print("exit " + exit)
    print(basic_vars)


def get_pivot_in_iteration(table, skip):
    obj_func = table[0]
    entering_index = get_entering_index(table, skip)
    if entering_index == "no pivot":
        return "no pivot"
    rhs_coeffs = get_coeffs(table, index=len(obj_func) - 1, start=1)
    pivot_coeffs = get_coeffs(table, index=entering_index, start=1)
    zipped_lists = zip(rhs_coeffs, pivot_coeffs)
    ratios = []
    for (rhs_var, pivot_var) in zipped_lists:
        if pivot_var <= 0:
            ratios.append("")
        else:
            if rhs_var == 0:
                ratios.append(rhs_var)
            else:
                ratios.append(rhs_var / pivot_var)
    # print("ratios ", ratios)
    positive_ratios = [i for i in ratios if i != "" and i >= 0]
    # print("positive ratios ", positive_ratios)
    while len(positive_ratios) == 0:
        count = 0
        if entering_index != len(table[0]) - 2:
            skip.add(entering_index)
            # print("skip ", skip)
        entering_index = get_entering_index(table, skip)
        if entering_index == "no pivot":
            return "no pivot"
        pivot_coeffs = get_coeffs(table, index=entering_index, start=1)
        zipped_lists = zip(rhs_coeffs, pivot_coeffs)
        ratios = []
        for (rhs_var, pivot_var) in zipped_lists:
            if pivot_var <= 0:  # check if denominator is neg or 0 if so skip
                ratios.append("")
            else:
                if rhs_var == 0:
                    ratios.append(rhs_var)
                    # print("appended 0 ", ratios)
                else:
                    ratios.append(rhs_var / pivot_var)
        # print("ratios ", ratios)
        positive_ratios = [i for i in ratios if i != "" and i >= 0]
        # print("positive ratios ", positive_ratios)
    enter_exit_variable(table, entering_index, ratios.index(min(positive_ratios)) + 1)
    print("el")
    print(ratios.index(min(positive_ratios)) + 1)
    print(table[ratios.index(min(positive_ratios)) + 1][entering_index])
    return entering_index, ratios.index(min(positive_ratios)) + 1


def do_pivot(table, entering_col, exiting_row, pivot):
    pivot_row = table[exiting_row]
    print("exiting ", exiting_row, "entering ", entering_col, "element ", table[exiting_row][entering_col])
    if pivot != 1:
        pivot_row = [(var / pivot) for var in pivot_row]
        table[exiting_row] = pivot_row
        pivot = table[exiting_row][entering_col]
    for r, row in enumerate(table):
        if row[entering_col] == 0:
            multiplier = 0
        else:
            multiplier = row[entering_col]
        for c, var in enumerate(row):
            if r != exiting_row:
                table[r][c] = var - (multiplier * table[exiting_row][c])


def next_iteration(table):
    skip = set()
    copy = table[0][:len(table[0]) - 2]
    if get_pivot_in_iteration(table, skip) == "no pivot":
        return "infeasible"
    entering_col, exiting_row = get_pivot_in_iteration(table, skip)
    pivot_col = get_coeffs(table, index=entering_col, start=0)
    pivot = table[exiting_row][entering_col]
    do_pivot(table, entering_col, exiting_row, pivot)
    print_table(table)
    return table


def print_table(table):
    print(
        "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for row in table:
        for col in row:
            if col < 0:
                print(col, end=" |  ")
            else:
                print(col, end="  |  ")
        if table.index(row) == 0:
            print()
            print(
                "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
                end="")
        print()
    print(
        "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
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
    for var in row_vars:
        if var in basic_vars:
            positions.append((basic_vars.index(var) + 1, row_vars.index(var)))
    # for col in range(0, len(table[0]) - 1):
    #     row = col + 1
    #     position = (row, col)
    #     positions.append(position)
    # print(positions)
    # print(row_vars)
    # print(basic_vars)
    for (row, col) in positions:
        # print(row, col, table[row][col], sep="  ")
        do_pivot(table, exiting_row=row, entering_col=col, pivot=table[row][col])
    # return positions


def phase2(table, obj_func, total_vars, total_art_vars):
    print("phase2")
    # replace the first row with the objective function and remove artificial variables
    new_table = np.array(table)
    new_table = np.delete(new_table, np.s_[total_vars - total_art_vars:len(table[0]) - 1], axis=1)
    new_table[0][0:len(new_table[0]) - 1] = obj_func
    new_table = new_table.tolist()
    # before simplex method need to make it ready - by pivoting
    print_table(new_table)
    make_ready_for_simplex(new_table)  # should make ready the basic variable (in first column)
    print("ready for simplex now")
    print_table(new_table)
    simplex_method(new_table)


if __name__ == "__main__":
    objective_func = [-5, -1]
    z_prime = [0, 0, 1, 1, 0]
    first_table = [z_prime, [1, -3, 1, 0, 1], [2, -1, 0, 1, 3]]

    # variables = int(input("Enter the number of variables: "))
    # constraints = int(input("Enter the number of constraints: "))
    # generate_table(variables, constraints)

    # TODO: organize start of main problem
    # variables = ["d1", "d2", "d3", "d4"]
    artificial_variables = []
    const_num = 8

    # two_phase_simplex(first_table, obj_func=objective_func, total_art_vars=2, total_vars=4)
    z = [0, 0, 20, 30, 40, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    z_prime = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               0]
    pb = [z_prime,
          # x, yd1 d2 d3d4 || e w n s
          [1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20],
          [1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 20],
          [1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 40],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 30],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 80],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 60],
          [0, 0, 1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
          [0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
          ]
    two_phase_simplex(table=pb, obj_func=z, total_vars=34, total_art_vars=12)
