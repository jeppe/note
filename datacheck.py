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

print 'ok'
