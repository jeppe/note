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

if __name__ == '__main__':
	#authorBenchmark()
	paper = open('paper.csv','r')

	paper_db = dict()
	content = paper.readlines(BUFFER)
	counter = 0
	while len(content) > 0:
		for record in content:
			record = record.strip().split(',')
			try:
				pid = int(record[0])
				pid,title,year,conid,journalid,keywords = record
				title = title.lower()
				if title not in paper_db:
					paper_db[title] = 1
				else:
					#print title
					raw_input()
			except Exception as inst:
				#print len(record[0]),record[0]
				pass
		content = paper.readlines(BUFFER)
