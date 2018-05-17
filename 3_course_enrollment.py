# This is a course enrollment system.
# Chosen courses should not clash and the total amount of credits
# should not exceed 120

def loadCourseCatalogue():
	catalogue = {}
	with open('3_course_catalogue.txt', 'r') as file1:
		line = file1.readline()[:-1]
		while line != '':
			line = line.split(',')
			catalogue[line[0]] = line[1:]
			line = file1.readline()[:-1]
	print(catalogue)
	return catalogue

def clash(catalogue, course1, course2):
	clashes = True
	lectures1 = catalogue[course1][1:]
	lectures2 = catalogue[course2][1:]
	i = j = 0
	for i in range (0, len(lectures1), 2):
		for j in range (0, len(lectures2), 2):
			if lectures1[i] == lectures2[j]:
				if lectures1[i+1] == lectures2[j+1]:
					return clashes
	clashes = False
	return clashes

def choose_courses(catalogue):
	credits_tot = 0
	chosen = {}
	while credits_tot < 120:
		course = str(input('Type the course name: '))
		if course not in catalogue.keys():
			print('No such course')
		else:
			credit = int(catalogue[course][0])
			if credits_tot + credit > 120:
				print('Exceeds 120 credits')
			else:
				if course in chosen.keys():
					print('You\'ve been enrolled at this course')
				else:
					how_many_clashes = 0
					for already_chosen in chosen.keys():
						if_clashes = clash(catalogue, course, already_chosen)
						if if_clashes == True:
							how_many_clashes += 1
					if how_many_clashes > 0:
						print('Cannot enroll due to clashes')
					else:
						print('Successfully enrolled')
						chosen[course] = catalogue[course][1:]
						credits_tot = credits_tot + credit
	return chosen

def print_timetable(course_dict):
	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
	for day in days:
		print(day)
		to_sort = []
		for course in course_dict.keys():
			course_list = course_dict[course]
			for i in range (len(course_list)):
				if course_list[i] == day:
					to_sort.append((course_list[i+1], course))
		to_sort.sort()
		for item in to_sort:			
			print('{0}: {1}'.format(item[0], item[1]))

print_timetable(choose_courses(loadCourseCatalogue()))