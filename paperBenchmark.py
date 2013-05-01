#-*- coding:utf-8 -*-

BUFFER = 1024


#paper benchmark code
def paperBenchmark():
	paper = open('paper.csv','r')
	content = paper.readlines(BUFFER)
	sample = open('./samples/paperSample.txt','w')
	sample.write(''.join(content) )
	sample.close()
	paper.close()

#paper-auther benchmark code
def paper_authorBenchmark():
	paper_auther = open('PaperAuthor.csv','r')
	content = paper_auther.readlines(BUFFER)
	sample = open('./samples/paperAuthorSample.txt','w')
	sample.write(''.join(content) )
	sample.close()
	paper_auther.close()

#author benchmark code
def authorBenchmark():
	_author = open('Author.csv','r')
	content = _author.readlines(BUFFER)
	sample = open('./samples/AuthorSample.txt','w')
	sample.write(''.join(content))
	sample.close()
	_author.close()

def findYear(record):
	position = 0

	for index,value in enumerate(record[2:]):
		try:
			int(value)
			position = index + 2
			break
		except:
			pass
	return position

def paperNoise():
	paper = open('paper.csv','r')

	paper_db = dict()
	content = paper.readlines(BUFFER)
	counter = -1
	nosie_paper = 0

	while len(content) > 0:
		for record in content:
			counter += 1
			if counter % 100000 == 1:
				print counter
			record_copy = record.strip().split(',')

			try:
				pid = int(record_copy[0])
				#find the index of the 'year' attribute in the record
				yearPosition = findYear(record_copy)
				#reconstruct the title of paper
				title = ','.join(record_copy[1:yearPosition])
				title = title.replace('"','')
				title = title.lower()

				year = record_copy[yearPosition]
				#conferenct id
				conid = record_copy[yearPosition + 1]
				#journal id
				journalid = record_copy[yearPosition + 2]
				#keep the keywords
				keywords = record_copy[yearPosition + 3:]
				
				if title in paper_db:
					paper_db[title] += 1
				
				if title not in paper_db:
					paper_db[title] = 1

			except Exception as inst:
				pass
		content = paper.readlines(BUFFER)
	for title in paper_db:
		if paper_db[title] != 1:
			nosie_paper += 1
	print 'noise',nosie_paper,'records',counter

if __name__ == '__main__':
	#authorBenchmark()
	