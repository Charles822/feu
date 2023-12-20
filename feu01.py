#!/usr/bin/env python3

# Exercise 2. Evaluer une expression / Evaluate an expression

import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process an expression in a string format and revert the result.')
    parser.add_argument('expression', help='the expression you wish to compute.')
    args = parser.parse_args()
    return args.expression


# step 1: remove the spaces in our string and convert it into a list
def extract_expression_parts(expression_elements):
	open_bracket = "("
	closing_bracket = ")"
	processed_expression = []
	temporary_sublist = []
	for element in expression_elements:
		if open_bracket in element:
			processed_expression.append(temporary_sublist)
			temporary_sublist = []
			temporary_sublist.append(element)
		elif closing_bracket in element:
			temporary_sublist.append(element)
			processed_expression.append(temporary_sublist)
			temporary_sublist = []
		else:
			temporary_sublist.append(element)
	processed_expression.append(temporary_sublist)
	if closing_bracket in expression_elements[-1][-1]:
		processed_expression.pop()
	if open_bracket in expression_elements[0][0]:
		processed_expression.pop(0)
	return processed_expression


# step 3: we separate the brackets from the numbers they are attached to within our sublists 
def split_brackets_in_sublists(bracket_separated_expression): 
	processed_sublists = []
	temporary_item = []
	for item in bracket_separated_expression:
		if "(" in item[0]:
			for character in item:
				if "(" in character:
					temporary_item.append("(")
					temporary_item.append(character[1:])
				elif ")" in character:
					temporary_item.append(character[:-1])
					temporary_item.append(")")
				else:
					temporary_item.append(character)
			processed_sublists.append(temporary_item)
			temporary_item = []
		else:
			processed_sublists.append(item)
	return processed_sublists


def add_multiplication_division_markers(expression_list): 
	processed_list = []
	for item in expression_list:
		if item in "+-":
			processed_list.append(["#", item, "#"])
		else:
			processed_list.append([item])
	return processed_list
 

def flatten_list(nested_list): 
	flattened = [item for sublist in nested_list for item in sublist]
	return flattened


# step 6: we isolate part of the expression with * and / and % operators into sublists
def isolate_multiplication_division(flattened_list): 
	marker_value = "#"
	result = []
	temporary_sublist = []
	for item in flattened_list:
		if item == marker_value:
			result.append(item)
			result.append(temporary_sublist)
			temporary_sublist = []
		else:
			temporary_sublist.append(item)
	result.append(temporary_sublist)
	return result


def remove_markers(processed_list): 
	marker_item = "#"
	marker_count = processed_list.count(marker_item) 
	for i in range(marker_count):
		processed_list.remove(marker_item)
	return processed_list


def perform_multiplication_division(clean_list): 
	marker_value = "#"
	final_list = []
	for item in clean_list:
		if "*" in item or "/" in item or "%" in item:
			count = 0
			if "(" in item: # We put this condition to handle the case where there is no + or - in the expression
				count = int(item[1])
			else:
				count = int(item[0])
			for i, sub_item in enumerate(item):
				if sub_item == "*":
					count *= int(item[i + 1])
				elif sub_item == "/":
					count /= int(item[i + 1])
				elif sub_item == "%":
					count %= int(item[i + 1])
				else:
					pass
			final_list.append([count])
		else:
			final_list.append(item)
	return final_list


def perform_final_computation(flat_list): 
	count = 0
	if flat_list[0] == "(":
		first_char = int(flat_list[1])
		count += first_char
	else:
		first_char = int(flat_list[0])
		count += first_char
	for i, item in enumerate(flat_list):
		if item == "+":
			count += int(flat_list[i + 1])
		elif item == "-":
			count -= int(flat_list[i + 1])
		else:
			pass
	return [str(count)]


#step 4: we compute the expressions into brackets and replace these elements in the list with their result
def compute_expression_in_brackets(ready_for_computation_expression): 
	processed_expression = []
	for item in ready_for_computation_expression:
		if "(" in item:
			# Step 4.1: we add a marker ("#") that will help us to isolate part of the expression with * and / and % operators
			item = add_multiplication_division_markers(item)
			# Step 4.2: we flatten our list to remove the subslists we created 
			flat_item = flatten_list(item)
			# Step 4.3: we isolate part of the expression with * and / and % operators into sublists
			regrouping = isolate_multiplication_division(flat_item)
			# Step 4.4: we remove the markers to clean our list 
			cleaning = remove_markers(regrouping)
			# Step 4.5: we compute parts of the expression with * and / and % first and replace them with their results
			no_mult = perform_multiplication_division(cleaning)
			# Step 4.6: we flatten our list to remove the subslists we created 
			flat_mult = flatten_list(no_mult)
			# Step 4.7: we compute the final parts of the expression with only + and - operators left
			result_bracket = perform_final_computation(flat_mult)
			# Step 4.8: we replace the expressions in brackets by their result 
			processed_expression.append(result_bracket)
		else:
			# if items in the list don't contain brackets, they are inserted as they are
			processed_expression.append(item)
	return processed_expression

#step 5: we compute the rest of the expression
def compute_remaining_expression(expression_without_brackets): 
	#step 5.1: we remove sublist created in the step 4.8
	flattened_expression = flatten_list(expression_without_brackets)
	# Step 5.2: we add a marker ("#") that will help us to isolate part of the expression with * and / and % operators
	item = add_multiplication_division_markers(flattened_expression)
	# Step 5.3: we remove sublist created in the step 5.2
	flat_item = flatten_list(item)
	# Step 5.4: we isolate part of the expression with * and / and % operators into sublists
	regrouping = isolate_multiplication_division(flat_item)
	# Step 5.5: we remove the markers to clean our list 
	cleaning = remove_markers(regrouping)
	# Step 5.6: we compute parts of the expression with * and / and % first and replace them with their results
	no_mult = perform_multiplication_division(cleaning)
	# Step 5.7: we remove sublist created in the step 5.6
	flat_mult = flatten_list(no_mult)
	# Step 5.8: we compute the final parts of the expression with only + and - operators left
	final_result = perform_final_computation(flat_mult)
	return final_result
	
def main():
	# Handling errors and Parsing
	expression = parse_arguments()
	
	# Resolution
	# step 1: remove the spaces in our string and convert it into a list
	expression_elements = expression.split()
	# step 2: we isolate the parts of the expression into brackets
	bracket_separated_expression = extract_expression_parts(expression_elements) 
	# step 3: we separate the brackets from the numbers they are attached to within our sublists 
	ready_for_computation_expression = split_brackets_in_sublists(bracket_separated_expression)
	#step 4: we compute the expressions into brackets and replace these elements in the list with their result
	expression_without_brackets = compute_expression_in_brackets(ready_for_computation_expression)
	#step 5: we compute the rest of the expression
	final_result = compute_remaining_expression(expression_without_brackets)
	
	# Display
	print(int(final_result[0]))

if __name__ == "__main__":
    main()
