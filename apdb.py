#-*- coding:utf-8 -*-

import cPickle

author_id = cPickle.load( open('./plk/map_author_id.plk','r') )#type : list
paper_id  = cPickle.load(open('./plk/map_paper_id.plk','r') )#type : list

author_dict = dict()#dictionary

for i,v in enumerate(author_id):
	author_dict[i] = v

datas = open('Author.csv','r')
author_name = dict()

for line in datas.readlines():
	line = line.strip().split(',')
	try:
		aid = int(line[0])
		author_name.setdefault(line[0],line[1])
	except:
		pass
datas.close()
