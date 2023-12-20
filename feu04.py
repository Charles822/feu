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

"""
def valid_board_format(board_rows):
	#les lignes ont toute la même longueur, il y a au moins une ligne d’une case, les lignes sont séparées d’un retour à la ligne, les caractères présents dans la carte sont uniquement ceux de la première ligne

"""

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

def compute_side(index_top, index_bottom, board_rows):
	square_side = 0
	if index_top == 0 or index_bottom == len(board_rows) - 1:
		square_side = (index_bottom - index_top) + 1
		print(square_side)
	else:
		square_side = index_bottom - index_top
		print(square_side)

	return square_side



def find_potential_square(first_x_index_column, first_x_position, index_column, squares_list):
	index_top = 0
	#top_found = False
	index_bottom = len(board_rows) - 1
	#bottom_found = False
	case_position = 0
	square_side = compute_side(index_top, index_bottom, board_rows)
	print(square_side)
	"""
	if first_x_position == index_top:
		index_top = True
	elif first_x_position == index_bottom:
		index_bottom -= 1
		bottom_found = True
	else: 
	"""	
	for index, column in enumerate(board_columns[index_column + 1:]):
		print("column: ", index + index_column + 1)
		for case in column[index_top:index_bottom + 1]:
			if case == "x" and (index_top <= case_position) and (case_position <= first_x_position): # if there are several X in the same column
				index_top = case_position
				square_side = compute_side(index_top, index_bottom, board_rows)
				print("index top = ", index_top, "side = ", square_side)
			elif case == "x" and ((index_bottom >= case_position) and (case_position >= first_x_position)): #il faut que je deal avec le cas ou le x est sur la meme ligne
				print((index_bottom > case_position) and (case_position > first_x_position))
				if ((index + index_column + 1) - first_x_index_column) == square_side:
					print(index + index_column + 1, " - ", first_x_index_column, " = ", square_side)
					squares_list.append((first_x_index_column + 1, index_top, square_side))
					print("square trouve")
				else:
					index_bottom = case_position
					square_side = compute_side(index_top, index_bottom, board_rows)
					print("index bottom = ", index_bottom, "index top = ", index_top, "side = ", square_side) 
			case_position += 1
		case_position = 0
		compute_side(index_top, index_bottom, board_rows)
	return squares_list


def find_x(board_columns):
	squares_list = []
	first_x_position = 0
	for index_column, column in enumerate(board_columns):
		for case in column:
			if case == "x":
				first_x_index_column = index_column
				print("coordonne X: ", first_x_index_column, first_x_position)
				find_potential_square(first_x_index_column, first_x_position, index_column, squares_list)
			first_x_position += 1
		first_x_position = 0
	return squares_list	


def take_side(square_param):
	return square_param[2]

def take_index_column(square_param):
	return square_param[0]


def select_square(squares_list):
	squares_list.sort(key=take_side, reverse=True)
	#return squares_list
	for square_param in squares_list:
		biggest_side = squares_list[0][2]
		if square_param[2] != biggest_side:
			squares_list.remove(square_param)
	squares_list.sort(key=take_index_column)
	if len(squares_list) >= 1:
		return squares_list[0]
	else:
		print("There is no square in this board")
		exit()

"""
def convert_into_rows(result_board):
	result_board_rows = []
	temp_row = []
	for i in range(0, len(result_board[0])):
		for column in result_board:
			temp_row.append(column[i])
		result_board_rows.append(temp_row)
		temp_row = []
	return result_board_rows
"""	


def draw_square(square_coordinates, board_rows, board_columns):
	start_index, start_position, square_side = square_coordinates
	end_index = start_index + square_side
	end_position = start_position + square_side
	result_board = []
	temp_row = []
	for index_column, row in enumerate(board_columns):
		for index_case, case in enumerate(row):
			if index_column in range(start_index, end_index - 1) and index_case in range(start_position, end_position - 1):
				temp_row.append("o")
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


board_file = parse_arguments()
board_file = read_file(board_file)
board_rows = create_rows(board_file)
board_param = board_rows[0]
board_rows = board_rows[1:]
board_columns = create_columns(board_rows)
squares_list = find_x(board_columns)
square_coordinates = select_square(squares_list)
result_board = draw_square(square_coordinates, board_rows, board_columns)
formatted_result_board = display_result_board(result_board)

print(board_param)
print("ROWS", board_rows)
print("COLUMNS", board_columns)
print(squares_list)
print(square_coordinates)
print(result_board)
print(*formatted_result_board, sep="\n")


