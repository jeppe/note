#-*- coding:utf-8 -*-

'''
	There are much noise in the data sets.For example,the author called James Goe,whose name have two patterns,J. Goe and 
	James Goe.This model's purpose is to filter out the similar names from the authors database for the target author.
'''

import apdb

def fd_author(target):
	'''Given an author's ID,fd_author returns the authorID,whose name has the similar patterns with the target author
	'''
	tar_name = apdb.author_name[target]
	tar_name = tar_name.split(' ')

	similar_name = []

	if len(tar_name) >= 2:
		f_name = tar_name[0][0].lower()
		l_name = tar_name[-1].lower()
		for nauthor in apdb.author_name:
			if nauthor != target:
				name = apdb.author_name[nauthor].lower()
				name = name.split(' ')
				if len(name) >= 2:
					nf_name = name[0][0].lower()
					nl_name = name[-1].lower()
					if (nf_name == f_name) and (nl_name == l_name):
						similar_name.append([nauthor,0])
						#print apdb.author_name[target],apdb.author_name[nauthor]

	elif len(tar_name) == 1:
		l_name = tar_name[0].lower()
		for nauthor in apdb.author_name:
			if nauthor != target:
				name = apdb.author_name[nauthor].lower()
				name = name.split(' ')
				if len(name) == 1:
					nl_name = name[0].lower()
					if nl_name == l_name:
						similar_name.append([nauthor,0])

	return similar_name

if __name__ == '__main__':
	#print fd_author('426')
	pass