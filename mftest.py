#=*- coding:utf-8 -*-

from numpy import array,matrix,linalg,fliplr,zeros,dot
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
			authors_dict.setdefault( line[0],[line[1].lower(),counter] )
		except:
			pass
	datas.close()

	return authors_dict#dictionary

def papers():
	datas = open('Paper.csv','r')

	papers_dict = []
	BUFFER = 1024
	content = datas.readlines(BUFFER)
	
	while len(content) > 0:
		for line in content:
			line = line.strip().split(',')
			try:
				pid = int(line[0])
				if type(pid) is int:
					papers_dict.append(line[0])
			except:
				pass
		content = datas.readlines(BUFFER)
	datas.close()

	return papers_dict#a list containing the paper id

def _init_paper_author(author_paper,author_csv,paper_id):

	paper_author = open('PaperAuthor.csv','r')

	BUFFER = 1024
	buffer_content = paper_author.readlines(BUFFER)
	#initial the author_paper matrix
	while len(buffer_content) > 0:
		for record in buffer_content:
			record = record.strip().split(',')
			try:
				int(record[0])#judge whether it's a valiable paperId
				pid = record[0]
				aid = record[1]

				pindex = paper_id.index(record[[0]])#hash the paperId to a sequential order
				aindex = author_csv[aid][1]#hash

				author_paper[aindex][pindex] += 1
			except:
				pass

		buffer_content = paper_author.readlines(BUFFER)
	paper_author.close()

	print 'finish initilizing paper_author matrix'
	return author_paper

def _init_author_matrix(author_matrix,author_paper,author_csv):
	num_paper = author_paper.shape[1]
	for j in range(0,len(author_csv) - 1):
		for i in range(j + 1,len(author_csv)):
			sum_paper = dot(author_paper[j],author_paper[i])
			author_matrix[i][j] = sum_paper
			author_matrix[j][i] = sum_paper

	print 'finish initilizing author_matrix'
	return author_matrix


if __name__ == '__main__':
	author_csv = authors()#return the authors dictionary
	total_authors = len(author_csv)
	paper_id = papers()
	total_papers = len(paper_id)

	author_matrix = zeros((total_authors,10))
	copy_matrix   = zeros((total_authors,10))
	print 'enough for author_matrix'

def matrix_mf():
	author_csv = authors()#return the authors dictionary
	total_authors = len(author_csv)
	paper_id = papers()
	total_papers = len(paper_id)

	author_matrix = zeros((total_authors,total_authors))
	author_paper = zeros((total_authors,total_papers))

	author_paper = _init_paper_author(author_paper,author_csv,paper_id)
	author_matrix = _init_author_matrix(author_matrix,author_paper,author_csv)
		
	evals,evec = linalg.eig(author_matrix)#return the eigenvalues and eigenvalues vectors
	print 'catching the eigenvalues and eigeenvectors'

	b = sort(evals)
	b.sort(cmp = lambda x,y:cmp(y,x))

	power = sum(b)
	sub_power = 0
	index = 0
	for i in range(0,len(b)):
			sub_power += b[i]
			index += 1
			if sub_power / power > 0.8:
				break

	idx = evals.argsort()
	evec = evec[:,idx]
	evec = fliplr(evec)[:,0:index]
	
	print 'mapping the author_matrix to a new vector space'
	new_user_matrix = dot(evec.T,author_matrix.T)

	new_user_matrix.dump('user_feature_matrix.plk')