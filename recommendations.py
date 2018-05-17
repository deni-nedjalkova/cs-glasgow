# This program makes personalised book recommendations using
# a similarity algorithm to predict which books a user is likely
# to enjoy reading based on his/her sample ratings.
# ---
# books.txt includes a list of 55 books in an <author>,<title> format, one entry per line
# ratings.txt includes usernames to represent users of the service followed by a list of 55 integers, each
# representing a rating for each book from books.txt, in the same order. The file is structured using the
# following format: <user_a>\n<user_a_rating_1> ... <user_a_rating_55> \n
# ---
# A program can calculate how similar two users are by treating each of their ratings 
# as a vector and calculating the dot product of these two vectors.
# ---
# Once you have calculated the pair-wise similarity between User A and every other user, 
# you can then identify whose ratings are most similar to User A’s. 
# In this case, User B is most similar to User A, so we would recommend to User A 
# the top books from User B’s list that User A hasn't already read.


import random

def read_books():
	book_list = []
	with open ('books.txt', 'r') as file_books:
		line = file_books.readline()[:-1] # omit the newline character
		while line != "":
			line = line.split(',') # ['author', 'title']
			book_list.append(line) # [['a', 't'], ['a', 't']]
			line = file_books.readline()[:-1] # continue reading
	return book_list

book_list = read_books() #[['author', 'title']] - make it a global variable
ALL_BOOKS = 55 # number of books

def read_users():
	users_dict = {} # dictionary: ratings assigned to a person
	with open ('ratings.txt', 'r') as file_users:
		line_1 = file_users.readline()[:-1]
		line_2 = file_users.readline()[:-2].split(" ") # split at spaces
		while line_1 != "":
			users_dict.update({line_1: line_2}) # {'user': ['r1', 'r2'..]}
			line_1 = file_users.readline()[:-1]
			line_2 = file_users.readline()[:-2].split(" ") # continue reading
	return users_dict

def dot_product_list(all_users, user_ratings_list):
	dot_product = 0
	similarity_values = [] # store in a dictionary
	for user_name in all_users.keys(): # iterate over every person in the record
		for i in range (len(user_ratings_list)): # for every rating
			dot_product = dot_product + int(user_ratings_list[i])*int(all_users[user_name][i])
		similarity_values.append((dot_product, user_name)) # list of tuples
		dot_product = 0 # make it zero after every iteration
	similarity_values.sort(reverse = True) # big --> small
	#returns the list of tuples
	return similarity_values

def get_recommendation_dict(all_users, rating_list, sim_scores, recommended_quantity):
	recommendations = {} # {"Alice": [books]}
	checkList = [] # accumulates recommended books
	current_person_id = 0
	while len(checkList) < recommended_quantity:
		for current_rating_index in range(ALL_BOOKS): # iterates over ratings: 0 --> 54
			current_recommender_name = sim_scores[current_person_id][1] # second in the tuple
			user_not_read_book = rating_list[current_rating_index] == '0' # boolean
			recommender_pos_rating = int(all_users[current_recommender_name][current_rating_index]) > 1 # boolean
			book_not_recommended_yet = book_list[current_rating_index] not in checkList # boolean
			if user_not_read_book and recommender_pos_rating and book_not_recommended_yet: # necessary conditions
				if current_recommender_name not in recommendations.keys():
					recommendations[current_recommender_name] = book_list[current_rating_index] 
					# whoRecommends: [author, book]
				else:
					recommendations[current_recommender_name].extend(book_list[current_rating_index]) 
					# who_recommends: [a, b, a, b] - concatenates lists
				checkList.append(book_list[current_rating_index]) # [[], []]
				if len(checkList) == recommended_quantity: # check after every book
					return recommendations
		current_person_id += 1 # outer shell
	return recommendations

def get_new_rating_list():
	new_record = [] # like everyone else: a list
	for n in range (ALL_BOOKS):
		new_record.append('0')
	for i in range (int(0.2*ALL_BOOKS)):
		order = random.randint(0, ALL_BOOKS-1) #inclusive
		book_to_rate = book_list[order]
		print("Please rate", book_to_rate, ': ')
		rating = str(input())
		new_record[order] = rating # specific place
	return new_record

def print_recommendations(recommended_dict):
	with open ('output.txt', 'w') as output_file:
		for recommender in recommended_dict:
			line_1 = "Recommended by user {0}:\n".format(recommender)
			output_file.write(line_1)
			print(line_1[:-1]) # omit the newline character
			suggested_books = recommended_dict[recommender]
			book_details_i = 0
			while book_details_i < len(suggested_books):
				line_2 = "	{0}, {1} \n".format(suggested_books[book_details_i], suggested_books[book_details_i+1])
				output_file.write(line_2)
				print(line_2[:-1])
				book_details_i = book_details_i + 2

def integer_exception():
	try:
		how_many = int(input("How many recommendations do you want to get? "))
	except:
		print("Invalid name, default value 10 is set")
		how_many = 10
	finally:
		return how_many

def control_panel():
	name_check = str(input("Enter your username: "))
	full_record = read_users() # {'user': ['r1', 'r2'..]} - ratings per name
	how_many_to_recommend = integer_exception()
	if name_check in full_record.keys(): # if exists in a database
		similarity_scores = dot_product_list(full_record, full_record[name_check])
		i = 0
		while i < len(similarity_scores):
			if similarity_scores[i][1] == name_check:
				del(similarity_scores[i]) # stay on the same value of i
			else:
				i += 1
		# print(similarity_scores)
		recommended_books = get_recommendation_dict(full_record, full_record[name_check], similarity_scores, how_many_to_recommend)
	else:
		new_user_ratings = get_new_rating_list()
		similarity_scores = dot_product_list(full_record, new_user_ratings)
		# print(similarity_scores)
		recommended_books = get_recommendation_dict(full_record, new_user_ratings, similarity_scores, how_many_to_recommend)
	print(recommended_books)
	print_recommendations(recommended_books)

control_panel()