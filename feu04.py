#!/usr/bin/env python3

# Exercise 5. Trouver le plus grand carré/ Find the biggest square

import argparse


def file_exist(file):
	try: 
		return open(file, "r")
	except FileNotFoundError:
		raise argparse.ArgumentTypeError(f"error, {file} is not in this directory")
	

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process a file, with a board.')
    parser.add_argument('board_file', type=file_exist, help='the board generator file.')
    args = parser.parse_args()
    return args.board_file


def read_file(board_file):
	return board_file.read()
	

def create_rows(board_file):
	board_rows = []
	temp_row = []
	board_file = board_file.split("\n")
	for item in board_file:
		for char in item:
			temp_row.append(char)
		board_rows.append(temp_row)
		temp_row = []
	return board_rows

# detect potential errors in the symbol paramters (obstacle, empty, full etc)
def error_symbols_parameters(symbol_parameters):
	compare = symbol_parameters.copy()
	for index, parameter in enumerate(symbol_parameters):
		if parameter in compare[index + 1:]:
			print("Board parameters are invalid, your board symbols must be all different")
			exit()

# check if the length parameters and board lenght matches
def error_map_size(board_rows, number_of_rows):
	if len(board_rows) != number_of_rows:
		print("Board size parameters is not equal to the board size")
		exit()

# function to access all parameters independantly
def read_map_parameters(board_parameters):
	full_symbol = board_parameters[-1]
	obstacle_symbol = board_parameters[-2]
	empty_symbol = board_parameters[-3]
	number_of_rows = board_parameters[-4::-1]
	coverted_number_of_rows = ""
	for number in number_of_rows:
		coverted_number_of_rows += number
	number_of_rows = int(coverted_number_of_rows)
	return full_symbol, obstacle_symbol, empty_symbol, number_of_rows

# make sure the board has at least 1 ligne and 1 box
def valid_board_format(board_rows, symbol_parameters):
	if len(board_rows) == 0:
			print("Your board must contain at least 1 row and 1 case")
			exit()
	for row in board_rows:
		if len(row) != len(board_rows[0]):
			print("Your board contain rows with different lengths")
			exit()			
		for case in row:
			if case not in symbol_parameters:
				print("Your board contain invalid symbols")
				exit()


def create_columns(board_rows):
	board_columns = []
	temp_column = []
	n = 0
	while n < len(board_rows[0]):
		for item in board_rows:
			temp_column.append(item[n])
		board_columns.append(temp_column)
		temp_column = []
		n += 1
	return board_columns

# logic to compute the potential side of a square
def compute_side(index_top, index_bottom, board_rows):
	square_side = 0
	if index_top == 0 or index_bottom == len(board_rows) - 1:
		square_side = (index_bottom - index_top) + 1
	else:
		square_side = index_bottom - index_top
	return square_side

# main logic to find a square based on the position of an "x"
def find_potential_square(board_rows, board_columns, first_x_index_column, first_x_position, index_column, \
	squares_list, obstacle_symbol):
	index_top = 0
	index_bottom = len(board_rows) - 1
	case_position = 0
	square_side = compute_side(index_top, index_bottom, board_rows)

	for index, column in enumerate(board_columns[index_column + 1:]):
		for case in column[index_top:index_bottom + 1]:
			if case == obstacle_symbol and (index_top <= case_position) and (case_position <= first_x_position): 
				index_top = case_position
				square_side = compute_side(index_top, index_bottom, board_rows)
			elif case == obstacle_symbol and ((index_bottom >= case_position) and (case_position >= first_x_position)): 
				if ((index + index_column + 1) - first_x_index_column) == square_side:
					squares_list.append((first_x_index_column + 1, index_top, square_side))
				else:
					index_bottom = case_position
					square_side = compute_side(index_top, index_bottom, board_rows)
			case_position += 1
		case_position = 0
		compute_side(index_top, index_bottom, board_rows)
	return squares_list

# logic to find "Xs" position in the board
def find_x(board_rows, board_columns, obstacle_symbol):
	squares_list = []
	first_x_position = 0
	for index_column, column in enumerate(board_columns):
		for case in column:
			if case == obstacle_symbol:
				first_x_index_column = index_column
				find_potential_square(board_rows, board_columns, first_x_index_column, first_x_position, \
					index_column, squares_list, obstacle_symbol)
			first_x_position += 1
		first_x_position = 0
	return squares_list	

# serve as a parameter for the select square function in case we have several squares in the board
def take_side(square_param):
	return square_param[2]

# serve as a parameter for the select square function in case we have several squares in the board
def take_index_column(square_param):
	return square_param[0]

# if we have several square this function help us to get the biggest one. 
def select_square(squares_list):
	squares_list.sort(key=take_side, reverse=True)
	for square_param in squares_list:
		biggest_side = squares_list[0][2]
		if square_param[2] != biggest_side:
			squares_list.remove(square_param)
	# If there are several with the same size, we take the one that is the most on the upper left		
	squares_list.sort(key=take_index_column)
	if len(squares_list) >= 1:
		return squares_list[0]
	else:
		print("There is no square in this board")
		exit()

# function to draw our result on the board
def draw_square(square_coordinates, board_rows, board_columns, full_symbol):
	start_index, start_position, square_side = square_coordinates
	end_index = start_index + square_side
	end_position = start_position + square_side
	result_board = []
	temp_row = []

	for index_column, row in enumerate(board_columns):
		for index_case, case in enumerate(row):
			if index_column in range(start_index, end_index - 1) and index_case in range(start_position, end_position - 1):
				temp_row.append(full_symbol)
			else:	
				temp_row.append(case)
		result_board.append(temp_row)
		temp_row = []	
	return result_board
	

def display_result_board(result_board):
	formatted_result_board = []
	temp_column = ""
	case_position = 0
	
	while case_position < len(result_board[0]):
		for item in result_board:
			temp_column += item[case_position]
		formatted_result_board.append(temp_column)
		temp_column = ""
		case_position += 1
	return formatted_result_board


def main():
	# Handling errors and Parsing
	board_file = parse_arguments()
	board_file = read_file(board_file)
	board_rows = create_rows(board_file)
	board_parameters = board_rows[0]
	symbol_parameters = board_parameters[-1:-4:-1] # all parameters except the number of rows
	error_symbols_parameters(board_parameters)
	full_symbol, obstacle_symbol, empty_symbol, number_of_rows = read_map_parameters(board_parameters)
	board_rows = board_rows[1:]
	error_map_size(board_rows, number_of_rows)
	valid_board_format(board_rows, symbol_parameters)
	board_columns = create_columns(board_rows)
	
	# Resolution
	squares_list = find_x(board_rows, board_columns, obstacle_symbol) #find the first Xs and potential squares
	square_coordinates = select_square(squares_list) # select the biggest square on the upper left side 
	result_board = draw_square(square_coordinates, board_rows, board_columns, full_symbol) # add the full symbol to draw the final square
	formatted_result_board = display_result_board(result_board)

    # Display
	print(*formatted_result_board, sep="\n")

if __name__ == "__main__":
    main()
