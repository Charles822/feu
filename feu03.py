#!/usr/bin/env python3

# Exercise 4. Sudoku

import argparse

import sys
import threading

threading.stack_size(67108864)
sys.setrecursionlimit(5000)


def file_exist(file):
	try: 
		return open(file, "r")
	except FileNotFoundError:
		raise argparse.ArgumentTypeError(f"error, {file} is not in this directory")
	

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process a file, with our sudoku board.')
    parser.add_argument('sudoku_file', type=file_exist, help='the sudoku board.')
    args = parser.parse_args()
    return args.sudoku_file


def read_file(file_name):
	return file_name.read()
	

def valid_content(file_content):
	for char in file_content:
		if char in ".\n0123456789":
			pass
		else:
			print(f"error, your sudoku baord contains invalid characters")
			exit()
	return True


def create_rows(file_content):
	formatted_input = []
	temp_row = []
	file_content = file_content.split("\n")
	for item in file_content:
		for char in item:
			temp_row.append(char)
		formatted_input.append(temp_row)
		temp_row = []
	return formatted_input


def valid_board_format(sudoku_rows):
	if len(sudoku_rows) == 9:
		for item in sudoku_rows:
			if len(item) != 9:
				print(f"error, your sudoku baord is not a 9x9 format")
				exit()
			else:
				pass


def create_columns(sudoku_rows):
	sudoku_columns = []
	temp_column = []
	n = 0
	while n < 9:
		for item in sudoku_rows:
			temp_column.append(item[n])
		sudoku_columns.append(temp_column)
		temp_column = []
		n += 1
	return sudoku_columns

		
def create_squares(sudoku_rows):
	sudoku_squares = []
	temp_square = []
	for n in range(0,9,3):
		for i in range(0,9,3):
			for row in sudoku_rows[n:n + 3]:
				temp_square.append(row[i:i + 3])
			sudoku_squares.append(temp_square)
			temp_square = []
	return sudoku_squares


def format_squares(sudoku_squares): #format sudoku_squares to iterate more easily into it
	new_squares = []
	temp_square = []
	for item in sudoku_squares:
		for row in item:
			temp_square += row
		new_squares.append(temp_square)
		temp_square = []
	return new_squares


def check_if_completed(sudoku_columns):
	for i in range(0,9):
		for case in sudoku_columns[i]:
			if case == ".":
				return False
	else:
		return True


def all_values(sudoku_columns):
	all_values = []
	for item in sudoku_columns:
		all_values += item
	return all_values


# identify the remaining possibilities in a column
def get_remaining_possibilities(column):
    possibilities = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for char in column:
        if char in possibilities:
            possibilities.remove(char)
    return possibilities


# here is the logic to update the solutions in a square
def update_sudoku_squares(sudoku_squares, column_index, empty_case_index, case_solution): #here is the logic to update a square once we found the solution to a case
    if column_index in (0, 1, 2):
        if empty_case_index in (0, 1, 2):
            sudoku_squares[0][empty_case_index * 3 + column_index] = case_solution
        elif empty_case_index in (3, 4, 5):
            sudoku_squares[3][(empty_case_index - 3) * 3 + column_index] = case_solution
        elif empty_case_index in (6, 7, 8):
            sudoku_squares[6][(empty_case_index - 6) * 3 + column_index] = case_solution
    elif column_index in (3, 4, 5):
        if empty_case_index == 0:
            sudoku_squares[1][column_index - 3] = case_solution
        elif empty_case_index == 1:
            sudoku_squares[1][column_index] = case_solution
        elif empty_case_index == 2:
            sudoku_squares[1][column_index + 3] = case_solution
        elif empty_case_index == 3:
            sudoku_squares[4][column_index - 3] = case_solution
        elif empty_case_index == 4:
            sudoku_squares[4][column_index] = case_solution
        elif empty_case_index == 5:
            sudoku_squares[4][column_index + 3] = case_solution   
        elif empty_case_index == 6:
            sudoku_squares[7][column_index - 3] = case_solution
        elif empty_case_index == 7:
            sudoku_squares[7][column_index] = case_solution
        elif empty_case_index == 8:
            sudoku_squares[7][column_index + 3] = case_solution
    elif column_index in (6, 7, 8):
        if empty_case_index == 0:
            sudoku_squares[2][column_index - 6] = case_solution
        elif empty_case_index == 1:
            sudoku_squares[2][column_index - 3] = case_solution
        elif empty_case_index == 2:
            sudoku_squares[2][column_index] = case_solution
        elif empty_case_index == 3:
            sudoku_squares[5][(column_index - 6)] = case_solution
        elif empty_case_index == 4:
            sudoku_squares[5][column_index - 3] = case_solution
        elif empty_case_index == 5:
            sudoku_squares[5][column_index] = case_solution 
        elif empty_case_index == 6:
            sudoku_squares[8][column_index - 6] = case_solution
        elif empty_case_index == 7:
            sudoku_squares[8][column_index - 3] = case_solution
        elif empty_case_index == 8:
            sudoku_squares[8][column_index] = case_solution


# update the list of possibilities within a square
def remove_items_from_square_remaining(square_remaining, items):
    for item in items:
        if item in square_remaining.copy():
            square_remaining.remove(item)
    return square_remaining


# this function triggers the square, columns and rows update
def update_solution_and_related_vars(solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities):
    sudoku_columns[column_index][position] = case_solution
    sudoku_rows[position][column_index] = case_solution
    update_sudoku_squares(sudoku_squares, column_index, position, case_solution)
    remaining_possibilities.remove(case_solution)
    square_remaining = remaining_possibilities.copy()
    solution = []
    return sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution


# a more sophiticated way to find the solution if we can't find it via a simple check in the column, row and square
def check_conditions_and_update(potential, sudoku_columns, column_index, position, sudoku_rows, square_remaining, remaining_possibilities, sudoku_squares):
    solution = square_remaining
    case_solution = []
    update_needed = False

    if column_index in (0, 3, 6):
        if position in (0, 3, 6):
            # check the if the potential solution is in the adjacent columns
            condition1 = (potential in sudoku_columns[column_index + 1] or "." not in sudoku_columns[column_index + 1][position:position + 3])
            condition2 = (potential in sudoku_columns[column_index + 2] or "." not in sudoku_columns[column_index + 2][position:position + 3])
            condition3 = (potential in sudoku_rows[position + 1] or sudoku_columns[column_index][position + 1] != ".")
            condition4 = (potential in sudoku_rows[position + 2] or sudoku_columns[column_index][position + 2] != ".")
            
            if condition1 and condition2 and condition3 and condition4:
                case_solution = potential
                update_needed = True
            
            # check the if the potential solution is in the adjacent rows
            condition5 = (potential in sudoku_rows[position + 1] or "." not in sudoku_rows[position + 1][position:position + 3])
            condition6 = (potential in sudoku_rows[position + 2] or "." not in sudoku_rows[position + 2][position:position + 3])
            condition7 = (potential in sudoku_columns[column_index + 1] or sudoku_columns[column_index + 1][position] != ".") 
            condition8 = (potential in sudoku_columns[column_index + 2] or sudoku_columns[column_index + 2][position] != ".")

            if condition5 and condition6 and condition7 and condition8:
                case_solution = potential
                update_needed = True
                
        elif position in (1, 4, 7):

            condition1 = (potential in sudoku_columns[column_index + 1] or "." not in sudoku_columns[column_index + 1][position - 1:position + 2]) or (potential in sudoku_rows[position - 1] and "." not in sudoku_columns[column_index + 1][position:position + 2])
            condition2 = (potential in sudoku_columns[column_index + 2] or "." not in sudoku_columns[column_index + 2][position - 1:position + 2]) or (potential in sudoku_rows[position - 1] and "." not in sudoku_columns[column_index + 2][position:position + 2])
            condition3 = (potential in sudoku_rows[position - 1] or sudoku_columns[column_index][position - 1] != ".")
            condition4 = (potential in sudoku_rows[position + 1] or sudoku_columns[column_index][position + 1] != ".")

            if condition1 and condition2 and condition3 and condition4:
                case_solution = potential
                update_needed = True

            condition5 = (potential in sudoku_rows[position - 1] or "." not in sudoku_rows[position - 1][position - 1:position + 2])
            condition6 = (potential in sudoku_rows[position + 1] or "." not in sudoku_rows[position + 1][position - 1:position + 2])
            condition7 = (potential in sudoku_columns[column_index + 1] or sudoku_columns[column_index + 1][position] != ".")
            condition8 = (potential in sudoku_columns[column_index + 2] or sudoku_columns[column_index + 2][position] != ".")

            if ((condition5 and condition6) and (condition7 and condition8)):
                case_solution = potential
                update_needed = True

        elif position in (2, 5, 8):

            condition1 = (potential in sudoku_columns[column_index + 1] or "." not in sudoku_columns[column_index + 1][position - 2:position + 1])
            condition2 = (potential in sudoku_columns[column_index + 2] or "." not in sudoku_columns[column_index + 2][position - 2:position + 1])
            condition3 = (potential in sudoku_rows[position - 2] or sudoku_columns[column_index][position - 2] != ".")
            condition4 = (potential in sudoku_rows[position - 1] or sudoku_columns[column_index][position - 1] != ".")

            if condition1 and condition2 and condition3 and condition4:
                case_solution = potential
                update_needed = True

            condition5 = (potential in sudoku_rows[position - 2] or "." not in sudoku_rows[position - 2][position - 2:position + 1])
            condition6 = (potential in sudoku_rows[position - 1] or "." not in sudoku_rows[position - 1][position - 2:position + 1]) 
            condition7 = (potential in sudoku_columns[column_index + 1] or sudoku_columns[column_index + 1][position] != ".")
            condition8 = (potential in sudoku_columns[column_index + 2] or sudoku_columns[column_index + 2][position] != ".")

            if condition5 and condition6 and condition7 and condition8:
                case_solution = potential
                update_needed = True

    elif column_index in (1, 4, 7):
    	if position in (0, 3, 6):
    		condition1 = (potential in sudoku_columns[column_index - 1] or "." not in sudoku_columns[column_index - 1][position:position + 3])
    		condition2 = (potential in sudoku_columns[column_index + 1] or "." not in sudoku_columns[column_index + 1][position:position + 3])
    		condition3 = (potential in sudoku_rows[position + 1] or sudoku_columns[column_index][position + 1] != ".")
    		condition4 = (potential in sudoku_rows[position + 2] or sudoku_columns[column_index][position + 2] != ".")

    		if condition1 and condition2 and condition3 and condition4:
    			case_solution = potential
    			update_needed = True

    		condition5 = (potential in sudoku_rows[position + 1] or "." not in sudoku_rows[position + 1][position:position + 3])
    		condition6 = (potential in sudoku_rows[position + 2] or "." not in sudoku_rows[position + 2][position:position + 3])
    		condition7 = (potential in sudoku_columns[column_index - 1] or sudoku_columns[column_index - 1][position] != ".")
    		condition8 = (potential in sudoku_columns[column_index + 1] or sudoku_columns[column_index + 1][position] != ".")

    		if condition5 and condition6 and condition7 and condition8:
    			case_solution = potential
    			update_needed = True

    	elif position in (1, 4, 7):
    		condition1 = (potential in sudoku_columns[column_index - 1] or "." not in sudoku_columns[column_index - 1][position - 1:position + 2]) or (potential in sudoku_rows[position - 1] and "." not in sudoku_columns[column_index - 1][position:position + 2])
    		condition2 = (potential in sudoku_columns[column_index + 1] or "." not in sudoku_columns[column_index + 1][position - 1:position + 2]) or (potential in sudoku_rows[position - 1] and "." not in sudoku_columns[column_index + 1][position:position + 2])
    		condition3 = (potential in sudoku_rows[position - 1] or sudoku_columns[column_index][position - 1] != ".")
    		condition4 = (potential in sudoku_rows[position + 1] or sudoku_columns[column_index][position + 1] != ".")

    		if condition1 and condition2 and condition3 and condition4:
    			case_solution = potential
    			update_needed = True

    		condition5 = (potential in sudoku_rows[position - 1] or "." not in sudoku_rows[position - 1][position - 1:position + 2])
    		condition6 = (potential in sudoku_rows[position + 1] or "." not in sudoku_rows[position + 1][position - 1:position + 2])
    		condition7 = (potential in sudoku_columns[column_index - 1] or sudoku_columns[column_index - 1][position] != ".")
    		condition8 = (potential in sudoku_columns[column_index + 1] or sudoku_columns[column_index + 1][position] != ".")

    		if condition5 and condition6 and condition7 and condition8:
    			case_solution = potential
    			update_needed = True

    	elif position in (2, 5, 8):
    		condition1 = (potential in sudoku_columns[column_index - 1] or "." not in sudoku_columns[column_index - 1][position - 2:position + 1])
    		condition2 = (potential in sudoku_columns[column_index + 1] or "." not in sudoku_columns[column_index + 1][position - 2:position + 1])
    		condition3 = (potential in sudoku_rows[position - 2] or sudoku_columns[column_index][position - 2] != ".")
    		condition4 = (potential in sudoku_rows[position - 1] or sudoku_columns[column_index][position - 1] != ".")

    		if condition1 and condition2 and condition3 and condition4:
    			case_solution = potential
    			update_needed = True

    		condition5 = (potential in sudoku_rows[position - 2] or "." not in sudoku_rows[position - 2][position - 2:position + 1])
    		condition6 = (potential in sudoku_rows[position - 1] or "." not in sudoku_rows[position - 1][position - 2:position + 1])
    		condition7 = (potential in sudoku_columns[column_index - 1] or sudoku_columns[column_index - 1][position] != ".")
    		condition8 = (potential in sudoku_columns[column_index + 1] or sudoku_columns[column_index + 1][position] != ".")

    		if condition5 and condition6 and condition7 and condition8:
    			case_solution = potential
    			update_needed = True

    elif column_index in (2, 5, 8):
    	if position in (0, 3, 6):
    		condition1 = (potential in sudoku_columns[column_index - 2] or "." not in sudoku_columns[column_index - 2][position:position + 3])
    		condition2 = (potential in sudoku_columns[column_index - 1] or "." not in sudoku_columns[column_index - 1][position:position + 3])
    		condition3 = (potential in sudoku_rows[position + 1] or sudoku_columns[column_index][position + 1] != ".")
    		condition4 = (potential in sudoku_rows[position + 2] or sudoku_columns[column_index][position + 2] != ".")

    		if condition1 and condition2 and condition3 and condition4:
    			case_solution = potential
    			update_needed = True

    		condition5 = (potential in sudoku_rows[position + 1] or "." not in sudoku_rows[position + 1][position:position + 3])
    		condition6 = (potential in sudoku_rows[position + 2] or "." not in sudoku_rows[position + 2][position:position + 3])
    		condition7 = (potential in sudoku_columns[column_index - 2] or sudoku_columns[column_index - 2][position] != ".")
    		condition8 = (potential in sudoku_columns[column_index - 1] or sudoku_columns[column_index - 1][position] != ".")

    		if condition5 and condition6 and condition7 and condition8:
    			case_solution = potential
    			update_needed = True

    	elif position in (1, 4, 7):
    		condition1 = (potential in sudoku_columns[column_index - 2] or "." not in sudoku_columns[column_index - 2][position - 1:position + 2])
    		condition2 = (potential in sudoku_columns[column_index - 1] or "." not in sudoku_columns[column_index - 1][position - 1:position + 2])
    		condition3 = (potential in sudoku_rows[position - 1] or sudoku_columns[column_index][position - 1] != ".")
    		condition4 = (potential in sudoku_rows[position + 1] or sudoku_columns[column_index][position + 1] != ".")

    		condition5 = (potential in sudoku_rows[position - 1] or "." not in sudoku_rows[position - 1][position - 1:position + 2])
    		condition6 = (potential in sudoku_rows[position + 1] or "." not in sudoku_rows[position + 1][position - 1:position + 2])
    		condition7 = (potential in sudoku_columns[column_index - 2] or sudoku_columns[column_index - 2][position] != ".")
    		condition8 = (potential in sudoku_columns[column_index - 1] or sudoku_columns[column_index - 1][position] != ".")

    		if condition1 and condition2 and condition3 and condition4:
    			case_solution = potential
    			update_needed = True

    		elif condition5 and condition6 and condition7 and condition8:
    			case_solution = potential
    			update_needed = True
	    
    # if the potential solution is identified, we change it in the board
    if update_needed:
    	sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
    		solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)

    return sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution, update_needed


# Here is the function to check within a 3 x 3 square
def check_square(remaining_possibilities, column_index, sudoku_columns, sudoku_squares, sudoku_rows): 
    square_remaining = remaining_possibilities.copy()
    solution = []
    position = -1
    for char in sudoku_columns[column_index]:
        position += 1
        if char == ".":
            if column_index in (0, 1, 2):
                if position in (0, 1, 2):
                    square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_rows[position])
                    
                    if len(square_remaining) == 1:
                        solution = square_remaining
                        case_solution = solution[0]
                        sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
                            solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
                    
                    else: 
                        square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_squares[0])
                        if len(square_remaining) == 1:
                            solution = square_remaining
                            case_solution = solution[0]
                            sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
                                solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
                        
                        elif len(square_remaining) > 1:
                        	for potential in square_remaining:
                        		sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution, update_needed = check_conditions_and_update(
                        			potential, sudoku_columns, column_index, position, sudoku_rows, square_remaining, remaining_possibilities, sudoku_squares)
                        	if update_needed == False:
                        		square_remaining = remaining_possibilities.copy()		
                
                elif position in (3, 4, 5):
                	square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_rows[position])

                	if len(square_remaining) == 1:
                		solution = square_remaining
                		case_solution = solution[0]
                		sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
                			solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)

                	else: 
                		square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_squares[3])
                		if len(square_remaining) == 1:
                			solution = square_remaining
                			case_solution = solution[0]
                			sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
                				solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)

                		elif len(square_remaining) > 1:
                			for potential in square_remaining:
                				sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution, update_needed = check_conditions_and_update(
                					potential, sudoku_columns, column_index, position, sudoku_rows, square_remaining, remaining_possibilities, sudoku_squares)
                			if update_needed == False:
                				square_remaining = remaining_possibilities.copy()

                elif position in (6, 7, 8):
                	square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_rows[position])
                	if len(square_remaining) == 1:
                		solution = square_remaining
                		case_solution = solution[0]
                		sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
                			solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
                	else: 
                		square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_squares[6])
                		if len(square_remaining) == 1:
                			solution = square_remaining
                			case_solution = solution[0]
                			sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
                				solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)

                		elif len(square_remaining) > 1:
                			for potential in square_remaining:
                				sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution, update_needed = check_conditions_and_update(
                					potential, sudoku_columns, column_index, position, sudoku_rows, square_remaining, remaining_possibilities, sudoku_squares)
                			if update_needed == False:
                				square_remaining = remaining_possibilities.copy()

            elif column_index in (3, 4, 5):
                if position in (0, 1, 2):
	                square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_rows[position])
	                
	                if len(square_remaining) == 1:
	                    solution = square_remaining
	                    case_solution = solution[0]
	                    sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
	                        solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
	                
	                else: 
	                    square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_squares[1])
	                    if len(square_remaining) == 1:
	                        solution = square_remaining
	                        case_solution = solution[0]
	                        sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
	                            solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
	                    
	                    elif len(square_remaining) > 1:
	                    	for potential in square_remaining:
	                    		sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution, update_needed = check_conditions_and_update(
	                    			potential, sudoku_columns, column_index, position, sudoku_rows, square_remaining, remaining_possibilities, sudoku_squares)
	                    	if update_needed == False:
	                    		square_remaining = remaining_possibilities.copy()		

                elif position in (3, 4, 5):
                	square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_rows[position])
                	if len(square_remaining) == 1:
                		solution = square_remaining
                		case_solution = solution[0]
                		sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
	            			solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)

                	else: 
                		square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_squares[4]) 
                		if len(square_remaining) == 1:
                			solution = square_remaining
                			case_solution = solution[0]
                			sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
                				solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
	            		
                		elif len(square_remaining) > 1:
                			for potential in square_remaining:
                				sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution, update_needed = check_conditions_and_update(
                					potential, sudoku_columns, column_index, position, sudoku_rows, square_remaining, remaining_possibilities, sudoku_squares)
                			if update_needed == False:
                				square_remaining = remaining_possibilities.copy()

                elif position in (6, 7, 8):
                	square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_rows[position])
                	if len(square_remaining) == 1:
                		solution = square_remaining
                		case_solution = solution[0]
                		sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
                			solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
	                else:  
	                	square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_squares[7])
	                	if len(square_remaining) == 1:
	                		solution = square_remaining
	                		case_solution = solution[0]
	                		sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
	                			solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
	                	elif len(square_remaining) > 1:
	                		for potential in square_remaining:
	                			sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution, update_needed = check_conditions_and_update(
	                				potential, sudoku_columns, column_index, position, sudoku_rows, square_remaining, remaining_possibilities, sudoku_squares)
                			if update_needed == False:
                				square_remaining = remaining_possibilities.copy()

            elif column_index in (6, 7, 8):
            	if position in (0, 1, 2):
            		square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_rows[position])
            		
            		if len(square_remaining) == 1:
            			solution = square_remaining
            			case_solution = solution[0]
            			sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
            				solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
	                
            		else: 
            			square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_squares[2])
            			if len(square_remaining) == 1:
            				solution = square_remaining
            				case_solution = solution[0]
            				sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
            					solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
	                    
            			elif len(square_remaining) > 1:
            				for potential in square_remaining:
            					sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution, update_needed = check_conditions_and_update(
            						potential, sudoku_columns, column_index, position, sudoku_rows, square_remaining, remaining_possibilities, sudoku_squares)
            				if update_needed == False:
            					square_remaining = remaining_possibilities.copy()		
	            
            	elif position in (3, 4, 5):
            		square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_rows[position])

            		if len(square_remaining) == 1:
	                	solution = square_remaining
	                	case_solution = solution[0]
	                	sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
	                		solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
	                
            		else: 
	                    square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_squares[5])
	                    if len(square_remaining) == 1:
	                        solution = square_remaining
	                        case_solution = solution[0]
	                        sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
	                            solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
	                    
	                    elif len(square_remaining) > 1:
	                    	for potential in square_remaining:
	                    		sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution, update_needed = check_conditions_and_update(
	                    			potential, sudoku_columns, column_index, position, sudoku_rows, square_remaining, remaining_possibilities, sudoku_squares)
	                    	if update_needed == False:
	                    		square_remaining = remaining_possibilities.copy()
	            
            	elif position in (6, 7, 8):
            		square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_rows[position])

            		if len(square_remaining) == 1:
            			solution = square_remaining
            			case_solution = solution[0]
            			sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
            				solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
	                
            		else:
	                    square_remaining = remove_items_from_square_remaining(square_remaining, sudoku_squares[8])
	                    if len(square_remaining) == 1:
	                        solution = square_remaining
	                        case_solution = solution[0]
	                        sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution = update_solution_and_related_vars(
	                            solution, case_solution, sudoku_columns, column_index, position, sudoku_rows, sudoku_squares, remaining_possibilities)
	                    
	                    elif len(square_remaining) > 1:
	                    	for potential in square_remaining:
	                    		sudoku_columns, sudoku_rows, sudoku_squares, remaining_possibilities, square_remaining, solution, update_needed = check_conditions_and_update(
	                    			potential, sudoku_columns, column_index, position, sudoku_rows, square_remaining, remaining_possibilities, sudoku_squares)
	                    	if update_needed == False:
	                    		square_remaining = remaining_possibilities.copy()


# Here is the main function to solve the sudoku, activating the necessary sub-functions
def solve_sudoku(sudoku_rows, sudoku_columns, sudoku_squares):
    for column_index in range(0, 9):
    	remaining_possibilities = get_remaining_possibilities(sudoku_columns[column_index])
    	if remaining_possibilities == []:
    		pass
    	elif len(remaining_possibilities) == 1: #means we have find the solution for this case
            empty_case_index = sudoku_columns[column_index].index(".")
            case_solution = remaining_possibilities[0]
            update_sudoku_squares(sudoku_squares, column_index, empty_case_index, case_solution)
            sudoku_rows[empty_case_index][column_index] = case_solution 
            sudoku_columns[column_index][empty_case_index] = case_solution 
    	else:
        	#need to check row and square possibilities
        	check_square(remaining_possibilities, column_index, sudoku_columns, sudoku_squares, sudoku_rows)
        	remaining_possibilities = remaining_possibilities.copy()
    
    if check_if_completed(sudoku_columns) == True:
        return sudoku_columns
    else:
    	return solve_sudoku(sudoku_rows, sudoku_columns, sudoku_squares)
    

def display_completed_sudoku(sudoku_columns):
	completed_sudoku_rows = []
	temp_row = ""
	n = 0
	while n < 9:
		for item in sudoku_columns:
			temp_row += item[n]
		completed_sudoku_rows.append(temp_row)
		temp_row = ""
		n += 1
	return completed_sudoku_rows


def main():
    # Handling errors and Parsing
    sudoku = parse_arguments()
    sudoku = read_file(sudoku)
    valid_content(sudoku)
    sudoku_rows = create_rows(sudoku)
    valid_board_format(sudoku_rows)
    sudoku_columns = create_columns(sudoku_rows)
    sudoku_squares = create_squares(sudoku_rows)
    sudoku_squares = format_squares(sudoku_squares)
    
    # Resolution
    # Here is the main function to solve the sudoku, activating the necessary sub-functions
    sudoku_columns = solve_sudoku(sudoku_rows, sudoku_columns, sudoku_squares)
    #reformatting before displaying the result
    completed_sudoku_rows = display_completed_sudoku(sudoku_columns)    

    # Display
    print(*completed_sudoku_rows, sep="\n")

if __name__ == "__main__":
    main()
