#-*- coding:utf-8 -*-

def authors_list():
	authors_dict = []
	datas = open('Author.csv','r')
	for line in datas.readlines():
		line = line.strip().split(',')
		try:
			aid = int(line[0])
			authors_dict.append(line[0])
		except:
			pass
	datas.close()
	return authors_dict#dictionary

	valid = open('Valid.csv','r')
	authors = authors_list()

	for line in valid.readlines():
		line = line.strip().split(',')

		try:
			int(line[0])
			aid = line[0]
			if aid not in authors:
				print 'error'
				raw_input()
		except:
			pass
		#print line
		#raw_input()

def paperNoise():
	'''I found many odd results when statistic the number of co-authors for a paper.
	   It's impossible that there're over 100 co-authors for a paper.
	   There're a lot of noise in the PaperAuthor.csv file.
	   This function is wrotten to give some details about the noise.
	'''
	sample = ['1025077','1032521','2153264','1394813']

	datas = open('PaperAuthor.csv','r')
	sample_file = open('./plk/PaperAuthorSample.plk','wb')

	Buffer = 1024
	content = datas.readlines(Buffer)
	while  len(content) > 0:
		for line in content:
			record = line.strip().split(',')
			try:
				pid = record[0]
				if pid in sample:
					sample_file.write(line)
			except:
				print record
				raw_input()
				pass
		content = datas.readlines(Buffer)
	datas.close()
	sample_file.close()

	datas = open('./plk/paperAuthorSampleTitle.plk','w')
	paper = open('Paper.csv','r')
	content = paper.readlines(Buffer)
	while  len(content) > 0:
		for line in content:
			record = line.strip().split(',')
			try:
				pid = record[0]
				if pid in sample:
					datas.write(line)
			except:
				pass
		content = paper.readlines(Buffer)
	datas.close()
	paper.close()

if __name__ == '__main__':
	paperNoise()

print 'ok'
