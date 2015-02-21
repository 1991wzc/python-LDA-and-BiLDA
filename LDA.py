#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import random
import re
import sys

class LDA:
	#documents
	M=0
	N=0
	#documents=[[]*N]*M
	documents=0

	#vocabulary size
	V=0

	#number of topics
	K=0

	#Dirichlet parameter

	alpha=0.0

	beta=0.0

	#topic assignments for each word
	#z=[[]*N]*M
	z=[]

	#nw[i][j] number of instances of word i (term?) assigned to topic j
	#nw=[[]*V]*K
	nw=[]

	#nd[i][j] number of words in document i assigned to topic j
	#nd=[[]*M]*K
	nd=[]

	#nwsum[j] total number of words assigned to topic j
	#nwsum=[]*K
	nwsum=[]

	#ndsum[i] total number of words in document i
	#ndsum=[]*M
	ndsum=[]

	#theta(document-topic distribution)
	#theta=[[]*M]*K
	theta=[]

	#phi(topic-word distribution)
	#phi=[[]*M]*V
	phi=[]

	#size of statistics
	numstats=0

	#number of iteration
	iteration=0

	#dicitionary
	dic_wordTonum={}
	dic_numToword={}

	#config parameters
	def config(self,alpha,beta,K,iteration):
		self.alpha=alpha
		self.beta=beta
		self.K=K
		self.iteration=iteration

	#read file
	def readData(self,filename):
		f=open('C:\Users\ZICHUN\Desktop\python lda\\'+filename,'r')
		wordmap=open('C:\Users\ZICHUN\Desktop\python lda\wordmap-'+filename,'w')

		full=f.read()

		full=full.strip()

		#fullDoc=full.replace('\n','')
		#fullWord=fullDoc.split()
		wordList=''
		wordID=0

		#get documents size
		doc=full.split('\n')
		self.M=len(doc)
		#print self.M
		self.z=[0]*self.M
		
		self.nwsum=[0]*self.K
		self.ndsum=[0]*self.M
		self.nd=[[0]*self.K for row in range(self.M)]
		self.documents=[0]*self.M

		self.theta=[[0]*self.K for row in range(self.M)]
		#print len(self.theta)

		for m in range(self.M):
			#replace words by number
			text=doc[m]
			#print text
			text=text.replace('\n','')
			#text=text.decode(encoding='utf-8')
			words=text.split(' ')

			self.N=len(words)

			self.documents[m]=[0]*self.N


			for n in range(self.N):
				
				#print self.N
				if words[n] in wordList:
					continue
				else:
					self.dic_wordTonum[words[n]]=wordID
					self.dic_numToword[wordID]=words[n]
					wordList=wordList+str(wordID)+' '+words[n]+'\n'
					wordID+=1
					if wordID % 1000==0:
						print 'Have read '+str(wordID)+' words'	
				
				self.documents[m][n]=self.dic_wordTonum[words[n]]


		self.V=wordID
		#print wordID
		self.nw=[[0]*self.K for row in range(self.V)]

		self.phi=[[0]*self.V for row in range(self.K)]


		for m in range(self.M):

			self.N=len(self.documents[m])
			self.z[m]=[0]*self.N
			

			for n in range(self.N):
				#randomly initiate
				topic=int(random.random()*self.K)
				self.z[m][n]=topic
				#documents[m][n] 是第m个doc中的第n个词  
				self.nw[self.documents[m][n]][topic]+=1
				#number of words in document i assigned to topic j
				self.nd[m][topic]+=1
				#total number of words assigned to topic j
				self.nwsum[topic]+=1		

				#total number of words in document i 
				self.ndsum[m]=self.N

		
		#creat wordmap file
		wordmap.write(wordList)

		f.close()
		wordmap.close()

	def LDAsampler(self):
		print 'Start sampling!'
		for i in range(self.iteration):
			#for all z_i
			for m in range(len(self.z)):
				for n in range(len(self.z[m])):
					#(z_i = z[m][n])  
					#sample from p(z_i|z_-i, w)
					topic = self.z[m][n]
					self.nw[self.documents[m][n]][topic]-=1
					self.nd[m][topic]-=1
					self.nwsum[topic]-=1
					self.ndsum[m]-=1

					p=[0]*self.K

					#do multinomial sampling via cumulative method
					for k in range(self.K):
						#nw 是第i个word被赋予第j个topic的个数  
						#在下式中，documents[m][n]是word id，k为第k个topic  
						#nd 为第m个文档中被赋予topic k的词的个数
						p[k] = (self.nw[self.documents[m][n]][k] + self.beta) / (self.nwsum[k] + self.V * self.beta) * (self.nd[m][k] + self.alpha) / (self.ndsum[m] + self.K * self.alpha)
					
					#cumulate multinomial parameters				
					for k in range(1,len(p)):
						#print k
						p[k]+=p[k-1]

					#scaled sample because of unnormalised p[]
					u=random.random()*p[self.K-1]
					for topic in range(len(p)):
						if(u<p[topic]):
							break

					self.nw[self.documents[m][n]][topic]+=1
					self.nd[m][topic]+=1
					self.nwsum[topic]+=1
					self.ndsum[m]+=1						

					self.z[m][n] = topic

			#if i%100==0:
			print str(i+1)+' iterations completed!'
		print 'Sampling completed!'

	def updateParameter(self):		
		for m in range(len(self.documents)):
			for k in range(self.K):				
				self.theta[m][k] +=(self.nd[m][k] + self.alpha) / (self.ndsum[m] + self.K * self.alpha)

		for k in range(self.K):
			for w in range(self.V):
				self.phi[k][w] = (self.nw[w][k] + self.beta) / (self.nwsum[k] + self.V * self.beta)

	def creat_file(self):
		print 'Creating theta file.'
		f_theta=open('theta.txt','w')
		f_theta.write('')
		f_theta=open('theta.txt','a')
		for m in range(len(self.documents)):
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
			for w in range(self.V):
				#text+=str(self.phi[k][w])+' '
				f_phi.write(str(self.phi[k][w])+' ')
		#f_phi.write(text)
		f_phi.close()
		print 'Complete!'

		print 'Creating topic_word file.'
		f_topic_word=open('topic_word.txt','w')
		f_topic_word.write('')
		f_topic_word=open('topic_word.txt','a')
		#text=''
		for k in range(self.K):
			dic=dict()
			f_topic_word.write('Topic '+str(k+1)+':\n')
			#text+='Topic '+str(k+1)+':\n'
			for w in range(self.V):
				dic[w]=self.phi[k][w]
			dic=sorted(dic.iteritems(), key=lambda d:d[1], reverse = True)

			for i in range(100):
				f_topic_word.write(str(self.dic_numToword[dic[i][0]])+' '+str(dic[i][1])+'\n')
				#text+=str(self.dic_numToword_en[dic_en[i][0]])+' '+str(dic_en[i][1])+' '+str(self.dic_numToword_ja[dic_ja[i][0]])+' '+str(dic_ja[i][1])+'\n'

		#f_topic_word.write(text)
		f_topic_word.close()
		print 'Complete!'

reload(sys)
sys.setdefaultencoding('utf8')  

en=LDA()
en.config(0.2,0.1,100,10)
en.readData('en_test.txt')
en.LDAsampler()
en.updateParameter()
en.creat_file()
