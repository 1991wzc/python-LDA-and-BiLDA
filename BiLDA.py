#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import random
import re
import sys

class BiLDA:
	#documents
	M_en=0
	M_ja=0
	N_en=0
	N_ja=0
	#documents=[[]*N]*M
	documents_en=0
	documents_ja=0

	#vocabulary size
	V_en=0
	V_ja=0

	#number of topics
	K=0

	#Dirichlet parameter

	alpha=0.0

	beta=0.0

	#topic assignments for each word
	#z=[[]*N]*M
	z_en=[]
	z_ja=[]

	#nw[i][j] number of instances of word i (term?) assigned to topic j
	#nw=[[]*V]*K
	nw_en=[]
	nw_ja=[]

	#nd[i][j] number of words in document i assigned to topic j
	#nd=[[]*M]*K
	nd_en=[]
	nd_ja=[]

	#nwsum[j] total number of words assigned to topic j
	#nwsum=[]*K
	nwsum_en=[]
	nwsum_ja=[]

	#ndsum[i] total number of words in document i
	#ndsum=[]*M
	ndsum_en=[]
	ndsum_ja=[]

	#theta(document-topic distribution)
	#theta=[[]*M]*K
	theta=[]

	#phi(topic-word distribution)
	#phi=[[]*M]*V
	phi=[]
	psy=[]

	#size of statistics
	numstats=0

	#number of iteration
	iteration=0

	#dicitionary
	dic_wordTonum_en={}
	dic_numToword_en={}
	dic_wordTonum_ja={}
	dic_numToword_ja={}

	#config parameters
	def config(self,alpha,beta,K,iteration):
		self.alpha=alpha
		self.beta=beta
		self.K=K
		self.iteration=iteration

	#read file
	def readData(self,filename_en,filename_ja):
		f_en=open(filename_en,'r')
		wordmap_en=open('wordmap-'+filename_en,'w')
		f_ja=open(filename_ja,'r')
		wordmap_ja=open('wordmap-'+filename_ja,'w')

		#English file
		full_en=f_en.read()

		full_en=full_en.strip()

		wordList_en=''
		wordID_en=0

		#get documents size
		doc_en=full_en.split('\n')
		self.M_en=len(doc_en)
		#print self.M
		self.z_en=[0]*self.M_en
		
		self.nwsum_en=[0]*self.K
		self.ndsum_en=[0]*self.M_en
		self.nd_en=[[0]*self.K for row in range(self.M_en)]
		self.documents_en=[0]*self.M_en

		self.theta=[[0]*self.K for row in range(self.M_en)]
		#print len(self.theta)

		for m in range(self.M_en):
			#replace words by number
			text=doc_en[m]
			#print text
			text=text.replace('\n','')
			#text=text.decode(encoding='utf-8')
			words=text.split(' ')

			self.N_en=len(words)

			self.documents_en[m]=[0]*self.N_en


			for n in range(self.N_en):
				
				#print self.N
				if words[n] in wordList_en:
					continue
				else:
					self.dic_wordTonum_en[words[n]]=wordID_en
					self.dic_numToword_en[wordID_en]=words[n]
					wordList_en=wordList_en+str(wordID_en)+' '+words[n]+'\n'
					wordID_en+=1
					if wordID_en % 1000==0:
						print 'Have read '+str(wordID_en)+' English words.'	
				
				self.documents_en[m][n]=self.dic_wordTonum_en[words[n]]

		print 'Total '+str(wordID_en)+' English words.'
		self.V_en=wordID_en
		#print wordID
		self.nw_en=[[0]*self.K for row in range(self.V_en)]

		self.phi=[[0]*self.V_en for row in range(self.K)]


		for m in range(self.M_en):

			self.N_en=len(self.documents_en[m])
			self.z_en[m]=[0]*self.N_en
			

			for n in range(self.N_en):
				#randomly initiate
				topic=int(random.random()*self.K)
				self.z_en[m][n]=topic
				#documents[m][n] 是第m个doc中的第n个词  
				self.nw_en[self.documents_en[m][n]][topic]+=1
				#number of words in document i assigned to topic j
				self.nd_en[m][topic]+=1
				#total number of words assigned to topic j
				self.nwsum_en[topic]+=1		

				#total number of words in document i 
				self.ndsum_en[m]=self.N_en

		
		#creat wordmap file
		wordmap_en.write(wordList_en)

		f_en.close()
		wordmap_en.close()

		#Japanese file
		full_ja=f_ja.read()

		full_ja=full_ja.strip()

		#fullDoc=full.replace('\n','')
		#fullWord=fullDoc.split()
		wordList_ja=''
		wordID_ja=0

		#get documents size
		doc_ja=full_ja.split('\n')
		self.M_ja=len(doc_ja)
		#print self.M
		self.z_ja=[0]*self.M_ja
		
		self.nwsum_ja=[0]*self.K
		self.ndsum_ja=[0]*self.M_ja
		self.nd_ja=[[0]*self.K for row in range(self.M_ja)]
		self.documents_ja=[0]*self.M_ja

		#self.thetasum_ja=[[0]*self.K for row in range(self.M_ja)]
		#print len(self.theta)

		for m in range(self.M_ja):
			#replace words by number
			text=doc_ja[m]
			#print text
			text=text.replace('\n','')
			#text=text.decode(encoding='utf-8')
			words=text.split(' ')

			self.N_ja=len(words)

			self.documents_ja[m]=[0]*self.N_ja


			for n in range(self.N_ja):
				
				#print self.N
				if words[n] in wordList_ja:
					continue
				else:
					self.dic_wordTonum_ja[words[n]]=wordID_ja
					self.dic_numToword_ja[wordID_ja]=words[n]
					wordList_ja=wordList_ja+str(wordID_ja)+' '+words[n]+'\n'
					wordID_ja+=1
					if wordID_ja % 1000==0:
						print 'Have read '+str(wordID_ja)+' Japanese words.'	
				
				self.documents_ja[m][n]=self.dic_wordTonum_ja[words[n]]

		print 'Total '+str(wordID_ja)+' Japanese words.'
		self.V_ja=wordID_ja
		#print wordID
		self.nw_ja=[[0]*self.K for row in range(self.V_ja)]

		self.psy=[[0]*self.V_ja for row in range(self.K)]


		for m in range(self.M_ja):

			self.N_ja=len(self.documents_ja[m])
			self.z_ja[m]=[0]*self.N_ja
			

			for n in range(self.N_ja):
				#randomly initiate
				topic=int(random.random()*self.K)
				self.z_ja[m][n]=topic
				#documents[m][n] 是第m个doc中的第n个词  
				self.nw_ja[self.documents_ja[m][n]][topic]+=1
				#number of words in document i assigned to topic j
				self.nd_ja[m][topic]+=1
				#total number of words assigned to topic j
				self.nwsum_ja[topic]+=1		

				#total number of words in document i 
				self.ndsum_ja[m]=self.N_ja

		
		#creat wordmap file
		wordmap_ja.write(wordList_ja)

		f_ja.close()
		wordmap_ja.close()

		#print self.M_ja
		#print self.M_en

	def sampler(self):
		print 'Start sampling!'
		for i in range(self.iteration):
			#for all z_i
			for m in range(len(self.z_en)):
				#print m
				#for english word
				for n in range(len(self.z_en[m])):					
					#(z_i = z[m][n])  
					#sample from p(z_i|z_-i, w)
					topic = self.z_en[m][n]
					self.nw_en[self.documents_en[m][n]][topic]-=1
					self.nd_en[m][topic]-=1
					self.nwsum_en[topic]-=1
					self.ndsum_en[m]-=1

					p=[0]*self.K

					#print 'do multinomial sampling via cumulative method'
					#do multinomial sampling via cumulative method
					for k in range(self.K):
						#nw 是第i个word被赋予第j个topic的个数  
						#在下式中，documents[m][n]是word id，k为第k个topic  
						#nd 为第m个文档中被赋予topic k的词的个数
						p[k] = (self.nw_en[self.documents_en[m][n]][k] + self.beta) / (self.nwsum_en[k] + self.V_en * self.beta) * (self.nd_en[m][k] + self.nd_ja[m][k] + self.alpha) / (self.ndsum_en[m] + self.ndsum_ja[m] + self.K * self.alpha)
					
					#print 'cumulate multinomial parameters'
					#cumulate multinomial parameters				
					for k in range(len(p)):
						if k!=0:
							p[k]+=p[k-1]

					#print 'scaled sample because of unnormalised p[]'
					#scaled sample because of unnormalised p[]
					u=random.random()*p[self.K-1]
					for topic in range(len(p)):
						if(u<p[topic]):
							break

					self.nw_en[self.documents_en[m][n]][topic]+=1
					self.nd_en[m][topic]+=1
					self.nwsum_en[topic]+=1
					self.ndsum_en[m]+=1						

					self.z_en[m][n] = topic

				#print len(self.z_ja[m])
				#for japanese word
				for n in range(len(self.z_ja[m])):
					#(z_i = z[m][n])  
					#sample from p(z_i|z_-i, w)
					topic = self.z_ja[m][n]
					self.nw_ja[self.documents_ja[m][n]][topic]-=1
					self.nd_ja[m][topic]-=1
					self.nwsum_ja[topic]-=1
					self.ndsum_ja[m]-=1

					p=[0]*self.K

					#print 'do multinomial sampling via cumulative method'
					#do multinomial sampling via cumulative method
					for k in range(self.K):
						#nw 是第i个word被赋予第j个topic的个数  
						#在下式中，documents[m][n]是word id，k为第k个topic  
						#nd 为第m个文档中被赋予topic k的词的个数
						p[k] = (self.nw_ja[self.documents_ja[m][n]][k] + self.beta) / (self.nwsum_ja[k] + self.V_ja * self.beta) * (self.nd_en[m][k] + self.nd_ja[m][k] + self.alpha) / (self.ndsum_en[m] + self.ndsum_ja[m] + self.K * self.alpha)
					
					#print 'cumulate multinomial parameters'
					#cumulate multinomial parameters				
					for k in range(len(p)):
						if k!=0:
							p[k]+=p[k-1]

					#print 'scaled sample because of unnormalised p[]'
					#scaled sample because of unnormalised p[]
					u=random.random()*p[self.K-1]
					for topic in range(len(p)):
						if(u<p[topic]):
							break

					self.nw_ja[self.documents_ja[m][n]][topic]+=1
					self.nd_ja[m][topic]+=1
					self.nwsum_ja[topic]+=1
					self.ndsum_ja[m]+=1						

					self.z_ja[m][n] = topic

			#if i%100==0:
			print str(i+1)+' iterations completed!'
		print 'Sampling completed!'

	def updateParameter(self):	
		for m in range(len(self.documents_en)):
			for k in range(self.K):				
				self.theta[m][k] =(self.nd_en[m][k] + self.nd_ja[m][k] + self.alpha) / (self.ndsum_en[m] + self.ndsum_ja[m] + self.K * self.alpha)

		for k in range(self.K):
			for w in range(self.V_en):
				self.phi[k][w] = (self.nw_en[w][k] + self.beta) / (self.nwsum_en[k] + self.V_en * self.beta)

		for k in range(self.K):
			for w in range(self.V_ja):
				self.psy[k][w] = (self.nw_ja[w][k] + self.beta) / (self.nwsum_ja[k] + self.V_ja * self.beta)

	def creat_file(self):
		print 'Creating theta file.'
		f_theta=open('theta.txt','w')
		f_theta.write('')
		f_theta=open('theta.txt','a')
		for m in range(len(self.documents_en)):
			f_theta.write('\n')
			#text+='\n'
			for k in range(self.K):	
				f_theta.write(str(self.theta[m][k])+' ')
				#text+=str(self.theta[m][k])+' '
		#f_theta.write(text)
		f_theta.close()
		print 'Complete!'

		#english
		print 'Creating phi file.'
		f_phi=open('phi.txt','w')
		f_phi.write('')
		f_phi=open('phi.txt','a')		
		#text=''
		for k in range(self.K):
			f_phi.write('\n')
			#text+='\n'
			for w in range(self.V_en):
				#text+=str(self.phi[k][w])+' '
				f_phi.write(str(self.phi[k][w])+' ')
		#f_phi.write(text)
		f_phi.close()
		print 'Complete!'

		#japanese
		print 'Creating psy file.'
		f_psy=open('psy.txt','w')
		f_psy.write('')
		f_psy=open('psy.txt','a')
		#text=''
		for k in range(self.K):
			#text+='\n'
			f_psy.write('\n')
			for w in range(self.V_ja):
				#text+=str(self.psy[k][w])+' '
				f_psy.write(str(self.psy[k][w])+' ')
		#f_psy.write(text)
		f_psy.close()
		print 'Complete!'

		print 'Creating topic_word file.'
		f_topic_word=open('topic_word.txt','w')
		f_topic_word.write('')
		f_topic_word=open('topic_word.txt','a')
		#text=''
		for k in range(self.K):
			dic_en=dict()
			dic_ja=dict()
			f_topic_word.write('Topic '+str(k+1)+':\n')
			#text+='Topic '+str(k+1)+':\n'
			for w in range(self.V_en):
				dic_en[w]=self.phi[k][w]
			dic_en=sorted(dic_en.iteritems(), key=lambda d:d[1], reverse = True)

			for w in range(self.V_ja):
				dic_ja[w]=self.psy[k][w]
			dic_ja=sorted(dic_ja.iteritems(), key=lambda d:d[1], reverse = True)

			for i in range(100):
				f_topic_word.write(str(self.dic_numToword_en[dic_en[i][0]])+' '+str(dic_en[i][1])+' '+str(self.dic_numToword_ja[dic_ja[i][0]])+' '+str(dic_ja[i][1])+'\n')
				#text+=str(self.dic_numToword_en[dic_en[i][0]])+' '+str(dic_en[i][1])+' '+str(self.dic_numToword_ja[dic_ja[i][0]])+' '+str(dic_ja[i][1])+'\n'

		#f_topic_word.write(text)
		f_topic_word.close()
		print 'Complete!'


#start

reload(sys)
sys.setdefaultencoding('utf8')  

bilda=BiLDA()
bilda.config(0.2,0.5,200,1000)
bilda.readData('en.txt','ja.txt')
bilda.sampler()
bilda.updateParameter()
bilda.creat_file()