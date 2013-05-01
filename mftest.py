#=*- coding:utf-8 -*-

from numpy import array,matrix,linalg,fliplr,zeros
import random

#read atuhors
def authors():
	counter = -1
	authors_dict = dict()
	datas = open('Author.csv','r')
	for line in datas.readlines():
		line = line.strip().split(',')
		try:
			aid = int(line[0])
			counter += 1
			authors_dict.setdefault( aid,[line[1].lower(),counter] )
		except:
			pass
	datas.close()

	return authors_dict#dictionary

def papers():
	
	papers_dict = []
	datas = open('Paper.csv','r')
	for line in datas.readlines():
		line = line.strip().split(',')
		try:
			pid = int(line[0])
			if type(pid) is int:
				papers_dict.append(line[0])
		except:
			pass
	datas.close()
	return papers_dict#a list containing the paper id

if __name__ == '__main__':
	author_csv = authors()#return the authors dictionary
	total_authors = len(author_csv)
	paper_id = papers()
	total_papers = len(paper_id)

	author_matrix = zeros((total_authors,total_authors))
	author_paper = zeros((total_papers,total_papers))

	

