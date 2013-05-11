#-*- coding:utf-8 -*-

import csv
import keyphrase

def cjdict():
	cdata = open('Conference.csv','rb')
	cdata = csv.reader(cdata)
	conference = dict()

	for row in cdata:
		cid,sname,fname,hpage = row
		try:
			int(cid)
			if cid not in conference:
				conference[cid] = fname
		except:
			pass

	cdata = open('Journal.csv','rb')
	cdata = csv.reader(cdata)
	journal = dict()

	for row in cdata:
		cid,sname,fname,hpage = row
		try:
			int(cid)
			if cid not in journal:
				journal[cid] = fname
		except:
			pass
	
	return conference,journal

import warnings

if __name__ == '__main__':


    paper_tag = open('paperTag.csv','wb')
    paper_tag = csv.writer(paper_tag)

    paper_tag.writerow(['paperId','Tags'])

    #warnings.filterwarnings('ignore',category = Warning)
    
    paper = open('Paper.csv','rb')
    paper = csv.reader(paper)

    conference,journal = cjdict()
    #print conference,journal

    counter = 0
    for row in paper:
        pid,title,year,cid,jid,kwords = row
        counter += 1
        if counter % 10000 == 9999:
        	print counter
        try:
        	int(pid)
        	if cid != '0':
        		try:
        			cfname = conference[cid]
        			sentence = ' '.join([title,kwords,cfname])
        		except:
        			sentence = ' '.join([title,kwords])
        	elif jid != '0':
        		try:
        			cjname = journal[jid]
        			sentence = ' '.join([title,kwords,cjname])
        		except:
        			sentence = ' '.join([title,kwords])
        	else:
        		sentence = ' '.join([title,kwords])

        	sentence = sentence.strip()
        	if len(sentence) > 0:

	        	tokens = keyphrase.tokenize(sentence)
	        	
	        	try:
	        		tokens.remove('keywords')
	        		
	        	except:
	        		try:
	        			tokens.remove('keyword')
	        		except:
		        		pass

	        	tokens = '|'.join(tokens)
	        else:
	        	tokens = ''

        	paper_tag.writerow([pid,tokens])
        except:
        	pass