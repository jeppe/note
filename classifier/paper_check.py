#-*- coding:utf-8 -*-

import csv

#read paper file and build a db for papers
paper = dict()

pp = open('Paper.csv','rb')
pp = csv.reader(pp)

for row in pp:
	pid,title,year,cid,jid,kwords = row
	try:
		int(pid)
		if pid not in paper:
			paper[pid] = row[1:]
	except:
		pass

train = open('Train.csv','rb')
train = csv.reader(train)
train_counter = 0
train_delete = 0
train_nin_counter = 0

for row in train:
	AuthorId,ConfirmedPaperIds,DeletedPaperIds = row

	try:
		int(AuthorId)
		ConfirmedPaperIds = ConfirmedPaperIds.split(' ')
		for cid in ConfirmedPaperIds:
			try:
				if paper[cid][0] == '' and paper[cid][2] == '0' and paper[cid][3] == '0' and paper[cid][4] == '':
					train_counter += 1
			except KeyError:
				train_nin_counter += 1
		DeletedPaperIds = DeletedPaperIds.split(' ')

		for cid in DeletedPaperIds:
			try:
				if paper[cid][0] == '' and paper[cid][2] == '0' and paper[cid][3] == '0' and paper[cid][4] == '':
					train_delete += 1
			except KeyError:
				train_nin_counter += 1			
	except:
		pass
print train_counter,train_nin_counter,train_delete

valid = open('Valid.csv','rb')
valid = csv.reader(valid)

valid_counter = 0
valid_nin_counter = 0

for row in valid:
	AuthorId,PaperIds = row

	try:
		int(AuthorId)
		PaperIds = PaperIds.split(' ')
		for cid in PaperIds:
			try:
				if paper[cid][0] == '' and paper[cid][2] == '0' and paper[cid][3] == '0' and paper[cid][4] == '':
					valid_counter += 1
			except KeyError:
				valid_nin_counter += 1			
	except:
		pass

print valid_counter,valid_nin_counter