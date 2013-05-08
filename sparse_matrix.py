#=*- coding:utf-8 -*-

from numpy import array,matrix,linalg,fliplr,zeros,dot
import random,cPickle
import time
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
	author_id = authors_list()#return the authors dictionary
	total_authors = len(author_id)
	paper_id = papers()
	total_papers = len(paper_id)


	cPickle.dump(author_id,open('./plk/map_author_id.plk','w'))
	cPickle.dump(paper_id,open('./plk/map_paper_id.plk','w'))
	print 'save the author and paper id map'

	BUFFER = 1024 #buffer for reading the large files
	#import the paper-author relation
	paper_author = dict()
	pa_datas = open('PaperAuthor.csv','r')

	buffer_content = pa_datas.readlines(BUFFER)
	#initial the paper_author dict
	counter = 0
	author_dict = dict()
	for i,v in enumerate(author_id ):
		author_dict[v] = i

	while len(buffer_content) > 0:
		for record in buffer_content:
			record = record.strip().split(',')
			try:
				int(record[0])#judge whether it's a valiable paperId
				pid = record[0]
				aid = record[1]
				if pid not in paper_author:
					paper_author[pid] = []
				#there are some authors in the paperAuthors.csv but not in the author.csv
				if aid in author_dict:
					counter += 1
					if counter % 100000 == 1:
						print counter
					author_index = author_dict[aid]
					paper_author[pid].append(author_index)
			except:
				pass
		buffer_content = pa_datas.readlines(BUFFER)
	pa_datas.close()	
	print 'saving the paper_author dictionary variable'
	new_pada = open('./plk/paper_author.plk','wb')

	for paper in paper_author:
		seg = ''
		seg += paper
		for author in paper_author[paper]:
			seg += '	'
			seg += author_id[author]
		seg += '\n'
		new_pada.write(seg)
	new_pada.close()

	print 'finish'
	#initilize the author matrix
	
	sparse_matrix = dict()
	paper_counter = 0 	#used to point out how many papers have been scaned
	sparse_nodes = 0

	print 'program run for %d , there are %d papers' %(time.clock(),len(paper_author) )
	timeSpan = 0.
	interval = 0.
	for paper in paper_author:
		paper_counter += 1

		if paper_counter % 1000000 == 1:
			interval = time.clock() - timeSpan
			timeSpan += interval
			print 'searching paper %d authors,spend %d m'%(paper_counter,interval / 60.)
			print 'sparse matrix has ',sparse_nodes

		authors = paper_author[paper]

		#print 'paper %s has authors %d'%(paper,len(authors) )
		for i in range(0,len(authors) - 1):
			
			#there are some authors in the paperAuthors.csv but not in the author.csv
			index_i = authors[i]

			for j in range(i+1,len(authors) ):
				
				#return the continue index
				index_j = authors[j]
#build a upper triangle matrix
				if index_i < index_j:
					
					if index_i not in sparse_matrix:
						sparse_matrix[index_i] = {index_j:1}
						sparse_nodes += 1
					elif index_j not in sparse_matrix[index_i]:
						sparse_matrix[index_i][index_j] = 1
						sparse_nodes += 1
					else:
						sparse_matrix[index_i][index_j] += 1

				elif index_i > index_j:

					
					if index_j not in sparse_matrix:
						sparse_matrix[index_j] = {index_j:1}
						sparse_nodes += 1
					elif index_i not in sparse_matrix[index_j]:
						sparse_matrix[index_j][index_i] = 1
						sparse_nodes += 1
					else:
						sparse_matrix[index_j][index_i] += 1
	
	days = timeSpan / (3600. * 24)
	print 'spend %d days finish initialing the sparse matrix' %days

	del paper_author
#save the triangle matrix


	print 'save the triangle matrix'


	amatrix = open('author_matrix.data','w')
	amatrix.write('%sparse matrix market format file')

	seg = str(len(author_id)) + '	'+ str(len(author_id)) + '	' + str(sparse_nodes ) + '\n'
	amatrix.write(seg)

	for author in sparse_matrix:
		co_authors = sparse_matrix[author]
		for co_author in co_authors:
			seg = str(author)
			seg += '	'
			seg += str(co_author)
			seg += '	'
			seg += str(co_authors[co_author])
			seg += '\n'
			amatrix.write(seg)
			seg = str(co_author)
			seg += '	'
			seg += str(author)
			seg += '	'
			seg += str(co_authors[co_author])
			seg += '\n'
			amatrix.write(seg)

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