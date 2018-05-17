# This program prints direct flights as well as flights with one change
# to fly from one airport to the other - both are specified by a user. It also shows
# the total cost of the tickets and the total duration of the flight. 


from math import *
import math
class Haversine:
    '''
    use the haversine class to calculate the distance between
    two lon/lat coordnate pairs.
    output distance available in kilometers, meters, miles, and feet.
    example usage: Haversine([lon1,lat1],[lon2,lat2]).feet
    
    '''
    def __init__(self,coord1,coord2):
        lon1,lat1=coord1
        lon2,lat2=coord2
        
        R=6371000                               # radius of Earth in meters
        phi_1=math.radians(lat1)
        phi_2=math.radians(lat2)

        delta_phi=math.radians(lat2-lat1)
        delta_lambda=math.radians(lon2-lon1)

        a=math.sin(delta_phi/2.0)**2+\
           math.cos(phi_1)*math.cos(phi_2)*\
           math.sin(delta_lambda/2.0)**2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        
        self.meters=R*c                         # output distance in meters
        self.km=self.meters/1000.0              # output distance in kilometers
        self.miles=self.meters*0.000621371      # output distance in miles
        self.feet=self.miles*5280               # output distance in feet

if __name__ == "__Haversine__":
    main()
#Haversine((-84.412977,39.152501),(-84.412946,39.152505)).miles 
#0.00168380561019642

def great_circle_distance(coordinates):
	coord_from = [float(coordinates['lat1']), float(coordinates['long1'])]
	coord_to = [float(coordinates['lat2']), float(coordinates['long2'])]
	sph_dist = Haversine(coord_from, coord_to).miles
	#print(sph_dist)
	return sph_dist

# great_circle_distance({'lat1': 51.5, 'long1': -0.13,'lat2': 50.1, 'long2':8.68}, 3.959)

def read_airports():
	air_dict = {}
	with open('2_airports.txt', 'r') as file1:
		line = file1.readline()[:-1]
		while line != "":
			line = line.split(', ')
			air_dict[line[1]] = [line[0]] + line[2:]
			line = file1.readline()[:-1]
	return air_dict

print(read_airports())
#{'MEL': ['Melbourne', '-37.814107', '144.963280'], 'FRA': ['Frankfurt', '50.110922', '8.682127'], 
#'LHR': ['London', '51.507351', '-0.127758'], 'IAD': ['Washington', '38.907192', '-77.03687'], 
#'CDG': ['Paris', '48.856614', '2.352222'], 'ICN': ['Seoul', '37.566535', '126.977969'], 
#'AMS': ['Amsterdam', '52.370216', '4.895168'], 'GLA': ['Glasgow', '55.864237', '-4.251806'], 
#'ATH': ['Athens', '37.983917', '23.729360'], 'DXB': ['Dubai', '25.204849', '55.270783']}
print('')

def put_coords_into_dict(from1, from2, to1, to2):
	c_dict = {}
	c_dict['lat1'] = from1
	c_dict['long1'] = from2
	c_dict['lat2'] = to1
	c_dict['long2'] = to2
	return c_dict

def read_routes():
	airports_info = read_airports()
	coords_dict = {}
	fly_from = {}
	with open('2_routes_and_prices.txt', 'r') as file2:
		line = file2.readline()[:-1]
		while line != "":
			fly_to = {} #empty every loop
			line = line.split('-')
			#---
			lat_from = airports_info[line[0]][1]
			long_from = airports_info[line[0]][2]
			lat_to = airports_info[line[1]][1]
			long_to = airports_info[line[1]][2]
			coords_dict = put_coords_into_dict(lat_from, long_from, lat_to, long_to)
			#---
			distance = great_circle_distance(coords_dict)
			#if line[0] not in fly_from.keys():
			#	fly_from[line[0]] = {}
			#	fly_from[line[0]][line[1]] = [distance, line[2]]
			#else:
			#	fly_from[line[0]].update({line[1]: [distance, line[2]]})
			fly_to[line[1]] = [distance, line[2]]
			if line[0] not in fly_from.keys():
				fly_from[line[0]] = fly_to
			else:
				fly_from[line[0]].update(fly_to)
			line = file2.readline()[:-1]
	return fly_from

print(read_routes())
#{'LHR': {'IAD': [5335.848628643641, '500'], 'FRA': [616.2462388181178, '150'], 
# 'MEL': [6261.8516683731605, '1000'], 'AMS': [352.12210644077516, '150'], 'ATH': [1881.4240435474894, '250']}, 
#'AMS': {'LHR': [352.12210644077516, '150'], 'ATH': [1615.7809900105601, '250']}, 
#'GLA': {'FRA': [977.6070807555215, '200'], 'LHR': [414.2964839175631, '100'], 'AMS': [676.4406834713594, '200']}}

def indirect(from_, to_):
	fly_from = read_routes()
	tot_dist = 0
	tot_price = 0
	for airport in fly_from[from_].keys():
		if airport in fly_from.keys():
			if to_ in fly_from[airport].keys():
				tot_dist = fly_from[from_][airport][0] + fly_from[airport][to_][0]
				tot_price = int(fly_from[from_][airport][1]) + int(fly_from[airport][to_][1])
				return (tot_dist, tot_price, airport)

def output():
	fly_from = read_routes()
#{'LHR': {'IAD': [5335.848628643641, '500'], 'FRA': [616.2462388181178, '150'], 
# 'MEL': [6261.8516683731605, '1000'], 'AMS': [352.12210644077516, '150'], 'ATH': [1881.4240435474894, '250']}, 
#'AMS': {'LHR': [352.12210644077516, '150'], 'ATH': [1615.7809900105601, '250']}, 
#'GLA': {'FRA': [977.6070807555215, '200'], 'LHR': [414.2964839175631, '100'], 'AMS': [676.4406834713594, '200']}}
	from_ = str(input('Enter airport to fly from (code): '))
	to_ = str(input('Enter airport to fly to (code): '))
	if to_ in fly_from[from_].keys():
		print('Fare: GPB{0}	In-flight duration: ?'.format(fly_from[from_][to_][1]))
	if indirect(from_, to_)[0] != 0:
		intermediate = indirect(from_, to_)[2]
		print('via {}'.format(intermediate))
		print('Fare: GPB{0}	In-flight duration: ?'.format(indirect(from_, to_)[1]))

output()
