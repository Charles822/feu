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


board, shape = parse_arguments()


def read_file(file_name):
	return file_name.read()
	

board = read_file(board)
shape = read_file(shape)

print(board)
print(shape)

def valid_content(file_content):
	for char in file_content:
		if char in " \n0123456789":
			pass
		else:
			print(f"error, {file_content} contains invalid characters")
			exit()
	return True


valid_content(board)
valid_content(shape)


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

board_table_sublist = input_formatting(board)

shape_table_sublist = input_formatting(shape)

print(board_table_sublist)
print(shape_table_sublist)


# generate row variations 

# generate the first row variation 
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



def generate_variations(shape_table_sublist):
	variations = {}
	i = 1
	for row in shape_table_sublist:
		row_variations = create_first_variation(row, board_table_sublist)
		row_variations = generate_other_variations(row_variations, board_table_sublist, shape_table_sublist)
		variations[i] = row_variations
		i += 1
		print(row_variations)
	return variations

dictionnary = generate_variations(shape_table_sublist)

print(f'dictionnary: {dictionnary}')



def check_row_equal(item, row):
	for i in range(0, len(item)):
		if row[i] == "-" or row[i] == " ":
			pass
		elif row[i] == item[i]:
			pass
		else:
			return False
	return True


def shape_in_board(board_table_sublist, dictionnary): 
	dummy_row = ["-" for i in range(len(max(board_table_sublist)))]
	temp_result = []
	board_result = []
	
	for index_board, item in enumerate(board_table_sublist):
		dict_item = 1
		
		for index_shape, row in enumerate(dictionnary[dict_item]): 
			
			if check_row_equal(item, row) is True and len(dictionnary) == 1:
				board_result.append(row)
				diff = len(board_table_sublist) - len(board_result)
				for i in range(0, diff):
					board_result.append(dummy_row)
				return "Trouvé" , board_result
		
			elif check_row_equal(item, row) is True and len(dictionnary) > 1:
				if len(board_table_sublist[board_table_sublist.index(item):]) < len(dictionnary):
					pass
				else: 
					temp_result.append(row)
					print(temp_result)
					n = 1
					for _ in range(1, (len(dictionnary) - dict_item) + 1):
						if check_row_equal(board_table_sublist[index_board + n], dictionnary[dict_item + n][index_shape]) is True:
							temp_result.append(dictionnary[dict_item + n][index_shape])	
							print(temp_result)
						else:
							temp_result = [] 
							print(temp_result)
						n += 1
				if temp_result != []:#n == len(dictionnary) - dict_item:
					for row in temp_result:
						board_result.append(row)
						print(board_result)
					diff = len(board_table_sublist) - len(board_result)
					for i in range(0, diff):
						board_result.append(dummy_row)
					return "Trouvé" , board_result
		
		else:
			board_result.append(dummy_row)
			print(board_result)
	return "Introuvable", board_result


result, board_result = shape_in_board(board_table_sublist, dictionnary)


if result == "Introuvable":
	print(result)
	exit()
else:
	print(result)
	print(board_result)


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
	

x, y = coordinates(board_result)

print(f"coordinates are: {x}, {y}")



def display_board_result(board_result):
	board_result.reverse()
	final_result = ""
	for item in board_result:
		for i, __ in enumerate(item):
			final_result += item[i]
		final_result += "\n"
	return final_result[:-1]


print(display_board_result(board_result))

