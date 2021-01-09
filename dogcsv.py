import csv

def readCsv(path, delimiter):
	lines =0
	dogs =[]
	with open(path) as file:
		reader  = csv.DictReader(file, delimiter =	delimiter)
		fields = reader.fieldnames if reader.fieldnames is not None else []
		for row in reader:
			lines+=1
			dogs.append(row)
				
		print(f'read  {lines} lines')
		return dogs, fields


def writeCsv(dogs, fields, path, delimiter):
	print('writing fields')
	print(fields)

	with open(path, 'w') as file:
		writer = csv.DictWriter(file, fieldnames = fields)
		writer.writeheader()
		writer.writerows(dogs)

		
def addDate(dogs, doglist, date):
	
	for name in doglist:
		print(f'handling {name}')
		if name != '':
			if len(dogs) > 0:
				dogIdx = findDogIndex(dogs,name)
				if dogIdx > -1:
					dogs[dogIdx][date] = name
					print(dogs[dogIdx].values())
				else:
					newDog = {f'{date}':f'{name}'}
					dogs.append(newDog)
					print(newDog)
			else:
				newDog = {f'{date}':f'{name}'}
				dogs.append(newDog)
				print(newDog)
			
			

	return dogs
	
	
def findDogIndex(dogs, name):
	if len(dogs) > 0:
		for idx, dog in enumerate(dogs):
			if name in dog.values():
				return idx
		return -1
	else:
		return -1