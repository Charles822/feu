#!/usr/bin/env python3

# Exercise 6. Trouver le chemin le plus court/ Find the shortest path

import argparse


def file_exist(file):
	try: 
		return open(file, "r")
	except FileNotFoundError:
		raise argparse.ArgumentTypeError(f"error, {file} is not in this directory")
	

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process a file, with a map.')
    parser.add_argument('map_file', type=file_exist, help='the map generator file.')
    args = parser.parse_args()
    return args.map_file


def read_file(map_file):
	return map_file.read()
	

def create_rows(map_file):
	map_rows = []
	temp_row = []
	map_file = map_file.split("\n")
	for item in map_file:
		for char in item:
			temp_row.append(char)
		map_rows.append(temp_row)
		temp_row = []
	return map_rows

# handling symbol errors (obstacle, empyt, entrance, exit etc)
def error_symbols_parameters(map_parameters):
	compare = map_parameters[-1:-6:-1].copy() # checking key symbol parameters to read the map
	for index, parameter in enumerate(map_parameters[-1:-6:-1]):
		if parameter in compare[index + 1:]:
			print("Map parameters are invalid, your map symbols must be all different")
			exit()

# checking if map rows & column are equal to parameters
def error_map_size(map_rows, map_parameters):
	size_parameters = map_parameters[:-5]
	col_size = size_parameters[:size_parameters.index("x")]
	row_size = size_parameters[size_parameters.index("x") + 1:]
	col_size_converted = ""
	row_size_converted = ""
	if "x" not in size_parameters:
		print("Map size parameters are invalid")
		exit()
	for number in col_size:
		col_size_converted += number
	for number in row_size:
		row_size_converted += number
	if int(col_size_converted) != len(map_rows) or int(row_size_converted) != len(map_rows[1]):
			print("Map size parameters are invalid")
			exit()


def read_map_parameters(map_parameters):
	exit_symbol = map_parameters[-1]
	entrance_symbol = map_parameters[-2]
	path_symbol = map_parameters[-3]
	empty_symbol = map_parameters[-4]
	obstacle_symbol = map_parameters[-5]
	return exit_symbol, entrance_symbol, path_symbol, empty_symbol, obstacle_symbol


def entry_coordinates(map_rows, entrance_symbol):
	row_entrance = 0
	column_entrance = 0
	for index_row, row in enumerate(map_rows):
		for index_case, case in enumerate(row):
			if case == entrance_symbol: 
				row_entrance = index_row
				column_entrance = index_case
	return row_entrance, column_entrance


def player_start_position(entrance, map_rows):
	initial_position = ()
	if entrance[1] == 0:
		initial_position = entrance[0], entrance[1] + 1
	elif entrance[1] == len(map_rows[0]) - 1:
		initial_position = entrance[0], entrance[1] - 1			
	elif entrance[0] == 0:
		initial_position = entrance[0] + 1, entrance[1]
	elif entrance[0] == len(map_rows) - 1:
		initial_position = entrance[0] - 1, entrance[1]
	return initial_position	
	
			
def end_coordinates(map_rows, exit_symbol):
	exits = []
	row_exit = 0
	column_exit = 0
	for index_row, row in enumerate(map_rows):
		for index_case, case in enumerate(row):
			if case == exit_symbol: 
				row_exit = index_row
				column_exit = index_case
				exit = row_exit, column_exit
				exits.append(exit)	
	return exits


def player_end_position(exit, map_rows):
	final_position = ()
	if exit[1] == 0:
		final_position = exit[0], exit[1] + 1
	elif exit[1] == len(map_rows[0]) - 1:
		final_position = exit[0], exit[1] - 1			
	elif exit[0] == 0:
		final_position = exit[0] + 1, exit[1]
	elif exit[0] == len(map_rows) - 1:
		final_position = exit[0] - 1, exit[1]
	return final_position	

# logic to select the first vertical and lateral directions that will take based on the entrance and exit we are targeting
def set_directions(entrance, exit):
	if entrance[0] < exit[0]:
		first_direction = "down"
	else:
		first_direction = "up"
	if entrance[1] < exit[1]:
		secondary_direction = "right"
	else:
		secondary_direction = "left"

	return first_direction, secondary_direction

# here is our main function to move the player through the map
def move_players(initial_position, final_position, first_direction, secondary_direction, map_rows, empty_symbol, obstacle_symbol, exit_symbol):
	directions = {
	"up": (-1, 0),
	"down": (1, 0),
	"right": (0, 1),
	"left": (0, -1),
	}

	player_position = initial_position
	cds_list = []
	temp_path = [initial_position]
	max_attempts = pow(len(map_rows) * len(map_rows[0]), 2)
	first_round_attempts = max_attempts - 1
	attempt = 0
	# we create this switch a new condition after a "first round" of our while loop in order to test a more simple algorythm first
	main_direction_switch = False 


	while attempt < max_attempts:
		if attempt == first_round_attempts:
			cds_list = []	# CDS stands for CUL DE SAC				
			player_position = initial_position
			temp_path = [player_position]
			attempt = 0
			main_direction_switch = True 
			first_round_attempts = max_attempts + 1

		# check if veritcal direction (main) path is available, if yes, we follow it
		if map_rows[player_position[0] + directions[first_direction][0]][player_position[1]] == empty_symbol and \
		 ((player_position[0] + directions[first_direction][0], player_position[1]) not in cds_list) and \
		 ((player_position[0] + directions[first_direction][0], player_position[1]) not in temp_path):
			player_position = player_position[0] + directions[first_direction][0], player_position[1] + directions[first_direction][1]
			temp_path.append(player_position)
		# if not, we check our lateral direction (secondary) is avaialble, if yes, we follow it
		elif map_rows[player_position[0] + directions[first_direction][0]][player_position[1]] == obstacle_symbol or \
		(player_position[0] - 1, player_position[1] in cds_list): 
			if map_rows[player_position[0]][player_position[1] + directions[secondary_direction][1]] == empty_symbol and \
			((player_position[0], player_position[1] + directions[secondary_direction][1]) not in cds_list):
				player_position = player_position[0] + directions[secondary_direction][0], player_position[1] + directions[secondary_direction][1]
				temp_path.append(player_position)
				if player_position == final_position:
					return temp_path
			# if not we are going to check our secondary direction opposite 						
			elif map_rows[player_position[0]][player_position[1] + directions[secondary_direction][1]] in f"{obstacle_symbol}{exit_symbol}" or \
			(player_position[0], player_position[1] + directions[secondary_direction][1] in cds_list):
				if player_position == final_position:
					return temp_path
				else:
					if map_rows[player_position[0]][player_position[1] - directions[secondary_direction][1]] == empty_symbol and \
					((player_position[0], player_position[1] - directions[secondary_direction][1]) not in temp_path):
						player_position = player_position[0] + directions[secondary_direction][0], player_position[1] - directions[secondary_direction][1]
						temp_path.append(player_position)
						if player_position == final_position:
							return temp_path
					# if the opposite lateral direction is not empty, we trigger this new condition (after trying a more direct path in the first round)
					# to check the opposite main direction
					elif (map_rows[player_position[0] - directions[first_direction][0]][player_position[1]] == empty_symbol) and \
					((player_position[0] - directions[first_direction][0], player_position[1]) not in temp_path) and (main_direction_switch == True):
						player_position = player_position[0] - directions[first_direction][0], player_position[1]
						temp_path.append(player_position)
						if player_position == final_position:
							return temp_path
						
					else:
						cds_list.append(player_position)					
						player_position = initial_position
						temp_path = [player_position]

		attempt += 1				
	temp_path.append(player_position)
	return temp_path


def find_paths(exits, map_rows, entrance, initial_position, empty_symbol, obstacle_symbol, exit_symbol):
	all_paths = []
	for exit in exits:
		final_position = player_end_position(exit, map_rows)
		first_direction, secondary_direction = set_directions(entrance, exit)
		potential_path = move_players(initial_position, final_position, first_direction, secondary_direction, map_rows, empty_symbol, obstacle_symbol, exit_symbol)
		all_paths.append(potential_path)
	return all_paths


def clean_all_paths(all_paths, exits, map_rows):
	wrong_paths = 0
	final_positions = []
	remove_wrong_paths = []
	for exit in exits:
		final_position = player_end_position(exit, map_rows)
		final_positions.append(final_position)
	for final_position in final_positions:
		for path in all_paths: # checking if there is a viable path or not
			if final_position not in path:
				wrong_paths += 1
			else:
				remove_wrong_paths.append(path)
	if wrong_paths == len(all_paths) * len(final_positions):
		print("There is no viable path in this labyrinthe")
		quit()
	return remove_wrong_paths


def shortest_path(all_paths):
	if len(all_paths) == 1:
		return all_paths[0]
	elif len(all_paths) > 1:
		return min(all_paths, key=len)


def draw_final_path(final_path, map_rows):
	for coordinates in final_path:
		map_rows[coordinates[0]][coordinates[1]] = "o"
	return map_rows


def display_paths(paths, map_parameters):
	paths.insert(0, map_parameters)
	temp_row = ""
	formatted_result = []
	for row in paths:
		for case in row:
			temp_row += str(case)
		formatted_result.append(temp_row)
		temp_row = ""
	return formatted_result


def main():
	# Handling errors and Parsing
	map_file = parse_arguments()
	map_file = read_file(map_file)
	map_rows = create_rows(map_file)
	map_parameters = map_rows[0]
	exit_symbol, entrance_symbol, path_symbol, empty_symbol, obstacle_symbol = read_map_parameters(map_parameters)
	map_rows = map_rows[1:]
	error_symbols_parameters(map_parameters)
	error_map_size(map_rows, map_parameters)
	entrance = entry_coordinates(map_rows, entrance_symbol)
	# here we identify the coordinates from where the player will start its journey
	initial_position = player_start_position(entrance, map_rows)
	# here we identify all potential exits, the final position of the players will be identified in the all_path func 
	exits = end_coordinates(map_rows, exit_symbol) 
	
	# Resolution
	# here is our main function to move along the map and save potential paths
	all_paths = find_paths(exits, map_rows, entrance, initial_position, empty_symbol, obstacle_symbol, exit_symbol)
	# here, we remove all the wrong path that do not contain the final positions
	all_paths = clean_all_paths(all_paths, exits, map_rows) 
	# here we identify the shortes path, our solution
	final_path = shortest_path(all_paths)
	# here we replace the empty path with the path symbol from the map parameters 
	map_rows = draw_final_path(final_path, map_rows) 
	result = display_paths(map_rows, map_parameters)
	result.append(f"=> Exit found in {len(final_path)} steps !")

    # Display
	print(*result, sep="\n")

if __name__ == "__main__":
    main()




