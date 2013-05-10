#-*- coding:utf-8 -*-

'''Rhadamanthus, who also was regarded as king and judge in the world of ghosts.
   Hope he could help the Academic Search Engine distinguish the real author.
'''

import filtering,apdb,cPickle

#input the valid data.
valid = open('Valid.csv','r')
v_set = dict()
valid_sequence = []
for line in valid.readlines():
	record = line.strip()
	record = record.split(',')
	try:
		int(record[0])
		target_author = record[0]
		valid_sequence.append(target_author)

		valid_papers = record[1].split(' ')

		v_set.setdefault(target_author,{'v_paper':[]})
		for p in valid_papers:
			v_set[target_author]['v_paper'].append([p,0.])
	except:
		pass

valid.close()
#define the similarity function
def sim(t,n):
	denominator = len(t)
	numerator    = 0.
	for v in n:
		if v in t:
			numerator += 1
	return numerator / denominator

#input the sparse_matrix,which describe the co-relationship between different authors

smatrix = open('author_matrix.data','r')
aco = dict() #instore the co-relationship between different authors,the data type of it is string.
for line in smatrix.readlines():
	record = line.strip()
	record = record.split('	')
	try:
		int(record[0])
		tid = apdb.author_dict[int(record[0]) ]#target author's id
		cid =  apdb.author_dict[int(record[1]) ]#co-author's id 
	
		if tid not in aco:
			aco[tid] = [cid]
		else:
			aco[tid].append(cid)
	except Exception as inst:
		print inst
smatrix.close()

#input the paper_author.plk file
paper_author = dict()
data = open('./plk/paper_author.plk','r')

content = data.readlines()
for line in content:
	record = line.strip().split('	')
	paper = record[0]
	authors = record[1:]
	paper_author[paper] = authors

data.close()
#begin prediction

badExample = []
print len(v_set)
counter = 0
for v_author in v_set:
	counter += 1
	print counter
	#initilize the co-author list for v_author
	if v_author not in aco:
		badExample.append(v_author)
		continue

	name_sim_authors = dict( filtering.fd_author(v_author) )

	for co in name_sim_authors:
		if co != v_author:
			try:
				similarity = sim(aco[v_author],aco[co])
			except:
				similarity = 0.
			if similarity != 0:
				name_sim_authors[co] = similarity

	for v in range(0,len(v_set[v_author]['v_paper']) ):
		p_valid = v_set[v_author]['v_paper'][v][0]
		authors_pvalid = paper_author[p_valid]

		#if v_author in authors_pvalid:
		#	print p_valid,v_author,authors_pvalid
		#	raw_input()
		#	v_set[v_author]['v_paper'][v][1] = 1.
		#else:
		pos = 0. #possibility of the same author
		for i in range(0,len(authors_pvalid)):
			if authors_pvalid[i] in name_sim_authors:
				try:
					s = name_sim_authors[authors_pvalid[i]]
				except:
					s = 0.
				if s > pos:
					pos = s
		v_set[v_author]['v_paper'][v][1] = pos
	#print v_set[v_author]['v_paper']
	#raw_input()
print badExample,len(badExample)

#for bad in badExample:
#end prediction
import csv

cPickle.dump(v_set,open('./plk/validSet.plk','wb') )
valid_result = open('./result/valid_result.csv','wb')
writer = csv.writer(valid_result,delimiter = ',')
header = ['AuthorIds','PaperIds']
writer.writerow(header)

for v_author in valid_sequence:
	p = v_set[v_author]['v_paper']
	p.sort( cmp = lambda x,y:cmp(y[1],x[1]) )
	print p
	raw_input()
	seg = ''
	#papers = []
	for pr in p:
		seg += pr[0]
		seg += ' '
	#	papers.append(pr[0])
	seg = seg.strip()
	writer.writerow([v_author,seg])
