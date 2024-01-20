#!/usr/bin/env python3

# Exercise 3. Trouver une forme / Find a shape

import argparse


def file_exist(file):
	try: 
		return open(file, "r")
	except FileNotFoundError:
		raise argparse.ArgumentTypeError(f"error, {file} is not in this directory")
	

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process 2 file names, the board and the shape to find.')
    parser.add_argument('board_file', type=file_exist, help='the board.')
    parser.add_argument('shape_file', type=file_exist, help='the shape we are trying to find.')
    args = parser.parse_args()
    return args.board_file, args.shape_file


def read_file(file_name):
	return file_name.read()


def valid_content(file_content):
	for char in file_content:
		if char in " \n0123456789":
			pass
		else:
			print(f"error, {file_content} contains invalid characters")
			exit()
	return True


# Function to format the content of a file into a 2D list
def input_formatting(file_content):
	formatted_input = []
	temp_row = []
	file_content = file_content.split("\n")
	for item in file_content:
		for char in item:
			temp_row.append(char)
		formatted_input.append(temp_row)
		temp_row = []
	return formatted_input


# Function to create the first variation of the shape's row
def create_first_variation(row, board_table_sublist):
	row_variations = []
	temp_row = []
	row_lenght = len(row) - 1
	board_row_lengths = len(board_table_sublist[0]) - 1
	i = 0
	while i <= row_lenght :
		temp_row.append(row[i])
		i += 1
	while i > row_lenght and i <= board_row_lengths:
		temp_row.append("-")
		i += 1
	row_variations.append(temp_row)
	temp_row = []
	return row_variations


# generate the remaining row variations 
def generate_other_variations(row_variations, board_table_sublist, shape_table_sublist):
	dummy_row = ["-" for i in range(len(max(board_table_sublist)))]
	temp_row = dummy_row.copy()
	additional_variations = len(max(board_table_sublist)) - len(max(shape_table_sublist))
	for index in range(0, additional_variations):
		for i, item in enumerate(row_variations[index]):
			if item != "-": 
				temp_row[i + 1] = item
		row_variations.append(temp_row)
		temp_row = dummy_row.copy()
	return row_variations


# Function to generate all variations for the shape
def generate_variations(shape_table_sublist, board_table_sublist):
	variations = {}
	i = 1
	for row in shape_table_sublist:
		row_variations = create_first_variation(row, board_table_sublist)
		row_variations = generate_other_variations(row_variations, board_table_sublist, shape_table_sublist)
		variations[i] = row_variations
		i += 1
	return variations


# Function to check if a row from the board matches a row variation
def check_row_equal(item, row):
	for i in range(0, len(item)):
		if row[i] == "-" or row[i] == " ":
			pass
		elif row[i] == item[i]:
			pass
		else:
			return False
	return True


# Function to find if the shape is in the board
def shape_in_board(board_table_sublist, variations): 
	dummy_row = ["-" for i in range(len(max(board_table_sublist)))]
	temp_result = []
	board_result = []
	
	for index_board, item in enumerate(board_table_sublist):
		dict_item = 1
		
		for index_shape, row in enumerate(variations[dict_item]): 
			
			if check_row_equal(item, row) is True and len(variations) == 1:
				board_result.append(row)
				diff = len(board_table_sublist) - len(board_result)
				for i in range(0, diff):
					board_result.append(dummy_row)
				return "Trouvé" , board_result
		
			elif check_row_equal(item, row) is True and len(variations) > 1:
				if len(board_table_sublist[board_table_sublist.index(item):]) < len(variations):
					pass
				else: 
					temp_result.append(row)
					n = 1
					for _ in range(1, (len(variations) - dict_item) + 1):
						if check_row_equal(board_table_sublist[index_board + n], variations[dict_item + n][index_shape]) is True:
							temp_result.append(variations[dict_item + n][index_shape])	
						else:
							temp_result = [] 
						n += 1
				if temp_result != []:
					for row in temp_result:
						board_result.append(row)
					diff = len(board_table_sublist) - len(board_result)
					for i in range(0, diff):
						board_result.append(dummy_row)
					return "Trouvé !" , board_result
		
		else:
			board_result.append(dummy_row)
	return "Introuvable", board_result


# Function to exit if the shape is not found
def no_shape(result):
	if result == "Introuvable":
		print(result)
		exit()


# Function to calculate the coordinates of the shape
def coordinates(board_result):
	for item in board_result:
		for element in item:
			if element != "-":
				x = item.index(element)
				board_result.reverse()
				y = board_result.index(item)
				return x, y
	else:
		exit()
	

def display_board_result(board_result):
	board_result.reverse()
	final_result = ""
	for item in board_result:
		for i, __ in enumerate(item):
			final_result += item[i]
		final_result += "\n"
	return final_result[:-1]


def main():
	# Handling errors and Parsing
	board, shape = parse_arguments()
	board = read_file(board)
	valid_content(board)
	shape = read_file(shape)
	valid_content(shape)
	board_table_sublist = input_formatting(board)
	shape_table_sublist = input_formatting(shape)

	
	# Resolution
	variations = generate_variations(shape_table_sublist, board_table_sublist)
	result, board_result = shape_in_board(board_table_sublist, variations)
	no_shape(result)
	x, y = coordinates(board_result)
	final_result = display_board_result(board_result)

	# Display
	print(*(result, f"coordinates are: {x}, {y}", final_result), sep="\n")


if __name__ == "__main__":
    main()



