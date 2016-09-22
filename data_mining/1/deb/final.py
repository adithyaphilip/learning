# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 09:29:07 2016

@author: Debarati Das 
"""
#import os
import random
import csv
import operator
import math
import pandas as pd

# functions to create the matrix of distances from each element in the training set to other 

def func_find_min(distMatrix,fresult):
    ctr=0
    for i in distMatrix : 
        newlist=sorted(i, key=lambda x: x[1])

        print >>fresult, "For Element number in train dataset : "+str(ctr+1)
        print >>fresult, "Species of minimum distance element : "+str(newlist[1][0][4])
        print >>fresult, "Minimum distance element and distance : "+str(newlist[1])
        print >>fresult,"Species of Maximum distance element: "+str(newlist[len(newlist)-1][0][4])
        print >>fresult, "Maximum distance element and distance: "+str(newlist[len(newlist)-1])
        
        print >>fresult,'\n'
        
        ctr+=1
    
def calculateDistanceMatrixEuclid(trainingSet):
    #first create  a list of lists
    k=len(trainingSet) #what is the number of training data
    #print 'debug : Length of training set \n'    
    #print k 
    d = [[] for x in xrange(k)] # this is the list of lists
    length=len(trainingSet[0]) # we need this in distance calculation
    for y in range(k): # for each element, now create the list of distances
        testInstance= trainingSet[y]
        for x in range(len(trainingSet)):
            dist=euclideanDistance(testInstance, trainingSet[x], length)
            d[y].append((trainingSet[x], dist))
    return d

def calculateDistanceMatrixManhattan(trainingSet):
    #first create  a list of lists
    k=len(trainingSet) #what is the number of training data 
    d = [[] for x in xrange(k)] # this is the list of lists
    length=len(trainingSet[0]) # we need this in distance calculation
    for y in range(k): # for each element, now create the list of distances
        testInstance= trainingSet[y]        
        for x in range(len(trainingSet)):
            dist=manhattanDistance(testInstance, trainingSet[x], length)
            d[y].append((trainingSet[x], dist))
    return d

def calculateDistanceMatrixSupremum(trainingSet):
    #first create  a list of lists
    k=len(trainingSet) #what is the number of training data 
    d = [[] for x in xrange(k)] # this is the list of lists
    #length=len(trainingSet[0]) # we need this in distance calculation
    for y in range(k): # for each element, now create the list of distances
        testInstance= trainingSet[y]        
        for x in range(len(trainingSet)):
            dist=supremumDistance(testInstance, trainingSet[x])
            d[y].append((trainingSet[x], dist))
    return d


def getResponseFrom(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def deriveAccuracy(testSet, predictions):
	#debug 
	#print 'Inside accuracy function \n'
	correct = 0
	for x in range(len(testSet)):
		#print testSet[x][-1] #debug
		#print predictions[x] #debug	 
		if testSet[x][-1] == predictions[x]:
			correct += 1
	#print  'correct number is: %d' %(correct)
	#print 'Leaving accuracy function \n' 
	return (correct/float(len(testSet))) * 100.0


def euclideanDistance(instance1, instance2, length):
	distance = 0
     #length is the number of dimension and last dimension is class ( not required for distance)
	for x in range(length-1):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def manhattanDistance(instance1, instance2, length):
    distance = 0
    #length is the number of dimension and last dimension is class ( not required for distance)
    for x in range(length-1):
         distance += abs(instance1[x] - instance2[x])
    return distance

def supremumDistance(x,y):
    #print zip(x,y)
    return max(abs(a-b) for a,b in zip(x,y)[:4]) 
    # ignore all but first two values  


def getNeighborsEuclid(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getNeighborsManhattan(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = manhattanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getNeighborsSupremum(trainingSet, testInstance, k):
	distances = []
	#length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = supremumDistance(testInstance, trainingSet[x])
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors
 

def loadDataset(filename,data=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        #next(lines)  #as there is no header
        dataset = list(lines)
        for x in range(len(dataset)):
	        for y in range(4):
	           dataset[x][y] = float(dataset[x][y])
                data.append(dataset[x])
        print 'loaded data: ' + repr(len(data))    
         

####################################################################
# Assignment 
###############################################################

def assignment():    
    trainingSet=[] 
    testSet=[]
    predictions=[]
    trainList=[]
    testList=[]
    
#    testk=75  #use default values 
#    traink=75
   

    ######################################################################################
    #Step 1  
    #######################################################################################
   
    
    fresult=open('./DebaratiResult.txt', 'wt')
    
    
    print >>fresult,'Data Mining assignment# 1  By Debarati Das  USN : XXXXX'
    print "Test results are stored in the file resultfile.txt \n"
    
    print >>fresult,'\n' 
    print >>fresult,'====================================================='
    print >>fresult,'Results of Data Mining assignment# 1 Step#1'
    print >>fresult,'====================================================='
    print >>fresult,'\n' 
    
    testk = int(raw_input("Enter your number of records in test dataset: "))
    traink=150-testk
    print >> fresult,"You have entered TestSet count= %d \n" %(testk)
    print >> fresult,"Since it is 150 element dataset, Traincount= 150-Testcount= %d \n" %(traink)
    
   
    # open the three files from the current directory
     
    f  = open('iris.csv', 'rb')
    f1 = open('test.csv', 'wb')
    f2 =open('train.csv','wb')
    
    reader = csv.reader(f)
    writertest = csv.writer(f1)
    writertrain=csv.writer(f2)
    traincount=testcount=0  # this is to set the count of the records in train and test 

    print >>fresult,'====================================================='
    print >>fresult, 'We make the train and test data list by random number generation (used seed 31)'
    print >>fresult, 'We then arrange the dataset by looking up the the above list'
    print >>fresult,'====================================================='
    random.seed(31)   # we do seeding to ensure same series gets generated  
    while (traincount <traink):
      num=random.randint(1,150)
      if (num not in trainList):
          trainList.append(num)
          traincount +=1
          print >> fresult,"Traincount= %d storing in training set; iris.csv id :%d" %(traincount,num) #seek out this record & store
    print >> fresult, "=================Train data list of iris.csv record ID===================================\n"
    print >>fresult,trainList
    print >>fresult, "=====================================================================\n" 
    
#now keep generating the numbers till we find one not in this list 
# and we dont exceed the test count
        

    while (testcount < testk):
        num=random.randint(1,150)
        if (num not in trainList and num not in testList): # we do not need seeding as we just pick up the rest !! 
            testList.append(num)
            testcount +=1;
            print >> fresult,"Testcount= %d storing in test set;; iris.csv id : %d" %(testcount,num) #seek out this reco
    print >>fresult, "===================================Test data list of iris.csv record ID====================\n"
    print >>fresult,testList
    print >>fresult, "=====================================================================\n"
    print >>fresult,'====================================================='
    print >>fresult, 'Preparaing of the Train.csv and Test.csv......'
    print >>fresult,' Read from the iris.csv and write the record into train.csv and test.csv as per the above lists' 
    print >>fresult,'====================================================='
    
    traincount=testcount=0 
    count =1

    try:
            
        next(reader) #skip the header 
        for row in reader:
            #fresult.write ("row[0] is %s \n" %(row[0]))
            if (count in trainList):
                writertrain.writerow((row[1],row[2],row[3],row[4],row[5])) #note that we want to skip the ID as our function does NOT need
                traincount +=1
                count +=1
                #fresult.write("Train file recordnum=%s iris.csv record ID is = %s \n" %(traincount,row[0]))
            else:
                writertest.writerow((row[1],row[2],row[3],row[4],row[5]))  #note that we want to skip the ID as our function does NOT need 
                testcount +=1
                count +=1
                #fresult.write("Test file recordnum=%s iris.csv record ID ID is = %s\n" %(testcount,row[0]))
               
    finally:
        f.close()
        f1.close()
        f2.close()
        fresult.write("\n Train.csv and test.csv created\n")
    
    ######################################################################################
    #Step 2  
    #######################################################################################
    
    print >>fresult,'\n'    
    print >>fresult,'====================================================='
    print >>fresult,'Results of Data Mining assignment#1 Step#2 (descriptive statistics)'
    print >>fresult,'====================================================='
    print >>fresult,'\n' 
    DF = pd.read_csv("iris.csv", na_values=[" "]) #you need not replace na 
    
    #print DF descriptive statistics for full dataset

    print >>fresult,'====================================================='
    print >>fresult,'(step 2 : Part 1) Descriptive statistics of full datatset'
    print >>fresult,'====================================================='
    
    print  >>fresult, DF.describe(percentiles=None)
    
    print >>fresult,'\n' 
    print >>fresult,'====================================================='
    print >>fresult,'(step 2 : Part 1) Descriptive statistics of full datatset grouped by species'
    print >>fresult,'====================================================='
    print >>fresult, DF.groupby('Species').describe(percentiles=None)
    print >>fresult,'\n' 
    print >>fresult,'====================================================='
    print >>fresult,'Results of Data Mining assignment# 1 Step#2 Part #2 (distance computation)'
    print >>fresult,'====================================================='
    print >>fresult,'\n' 
  
    #First we load the train and test dataset into separate lists  
    #we reset the training and test dataset
    
    trainingSet=[] 
    testSet=[]
    print >>fresult, "Loading training data... \n"
    loadDataset('train.csv',trainingSet)
    print >>fresult, "Loading test data... \n"
    loadDataset('test.csv',testSet)
   
    
    
    print >>fresult,'====================================================='
    print >>fresult,'(step 2 : Part 2) Calculate different types of distance between any two points and find the minimum and maximum of those'
    print >>fresult,'====================================================='
    print >>fresult,'\n'     
    # all we have to do is : for each member of the training set, define it as testSetSingle while the rest 149 can be training set
    #calculate three kinds of distances in a for loop for each one with the other 149  
    # do euclideanDistance(instance1, instance2, length) etc.  
    k=len(trainingSet) #what is the number of training data 
    distMatrix = [[] for x in xrange(k)] # this is the list of lists
    print >>fresult,'====================================================='
    print >> fresult, "Distance matrix for Each Element of training set from each including itself ... \n"
    print >>fresult,'====================================================='    
    print >> fresult, "nxn distance matrix using Euclidean distance..............\n"
    print >>fresult,'====================================================='
    distMatrix=calculateDistanceMatrixEuclid(trainingSet)
    
#    for elem in distMatrix:
#        print >>fresult,elem
    
    #print "TESTING NEW FUNC LOL"
    print >>fresult, '\n'
    print >>fresult,'====================================================='    
    print >> fresult, "For each element(in train dataset) minimum and maximum distance(Euclidean) element & distance..............\n"
    print >>fresult,'====================================================='

    func_find_min(distMatrix,fresult)
    
    print >>fresult,'====================================================='
    print >> fresult, "nxn distance matrix using Manhattan distance..............\n"
    print >>fresult,'====================================================='
    distMatrix= calculateDistanceMatrixManhattan(trainingSet)
#    for elem in distMatrix:
#        print >>fresult,elem
    print >>fresult, '\n'    
    print >>fresult,'====================================================='    
    print >> fresult, "For each element (in train dataset) minimum and maximum distance(Manhattan) element & distance..............\n"
    print >>fresult,'====================================================='
    func_find_min(distMatrix,fresult)    
    
    print >>fresult,'====================================================='    
    print >> fresult, "nxn distance matrix using Supremum distance..............\n"
    print >>fresult,'====================================================='
    distMatrix= calculateDistanceMatrixSupremum(trainingSet)
#    for elem in distMatrix:
#        print >>fresult,elem
    print >>fresult, '\n'
    print >>fresult,'====================================================='    
    print >> fresult, "For each element(in train dataset) minimum and maximum distance(Supremum) element & distance..............\n"
    print >>fresult,'====================================================='
    
    func_find_min(distMatrix,fresult)

###########################################################################################################
#                     Step 3 
#########################################################################################################     

    print >>fresult,'====================================================='
    print >>fresult,'Assignment 1 : step 3 !!'
    print >>fresult,'====================================================='
    print >>fresult,'\n' 
    
    for k in range(1,6):	# thisis effectively k =1 to 5 	
		# generate predictions
		print >>fresult,'Classification using k nearest neighbour with k='+ str(k)
		print >>fresult,'=====================================================' 
		print >>fresult,'Classification using Euclidean distance !!'
		print >>fresult,'====================================================='
	 
		predictions=[]
		
		for x in range(len(testSet)):
			neighbors = getNeighborsEuclid(trainingSet, testSet[x], k)
			print >>fresult,"===========neighbours of ===========\n"
			print >> fresult,testSet[x]
			print >>fresult,"neighbors are :"
			print >>fresult,neighbors
			result = getResponseFrom(neighbors)
			predictions.append(result)
			print >> fresult,'> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1])
		accuracy = deriveAccuracy(testSet, predictions)
		print>> fresult,'Accuracy: ' + repr(accuracy) + '%'   
		
		print >>fresult,'\n' 
		print >>fresult,'====================================================='
		print >>fresult,'Classification using Manhattan distance !!'
		print >>fresult,'====================================================='
		
		
		predictions=[]
		
		for x in range(len(testSet)):
			neighbors = getNeighborsManhattan(trainingSet, testSet[x], k)
			print >>fresult,"===========neighbours of==========="
			print >> fresult,testSet[x]
			print >>fresult,"neighbors are :"
			print >>fresult,neighbors
			result = getResponseFrom(neighbors)
			predictions.append(result)
			print >> fresult,'> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1])
		accuracy = deriveAccuracy(testSet, predictions)
		print >> fresult,'Accuracy: ' + repr(accuracy) + '%'    
		
		
		print >>fresult,'====================================================='
		print >>fresult,'Classification using Supremum distance !!'
		print >>fresult,'====================================================='

		predictions=[]
	   
		for x in range(len(testSet)):
			neighbors = getNeighborsSupremum(trainingSet, testSet[x], k)
			print >>fresult,"===========neighbours of==========="
			print >> fresult,testSet[x]
			print >>fresult,"neighbors are :"
			print >>fresult,neighbors
			result = getResponseFrom(neighbors)
			predictions.append(result)
			print >> fresult,'> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1])
		accuracy = deriveAccuracy(testSet, predictions)
		print >> fresult,'Accuracy: ' + repr(accuracy) + '%'    
   
    
    #############################################################################################
    #close the result file 
    print >>fresult,'====================================================='
    print  >> fresult, "...Assignment 1 done...Check resultfile.txt for results ...\n"
    print >>fresult,'====================================================='
    fresult.close()
    print "...Assignment 1 done...Check resultfile.txt for results ...\n"

######################################################################

def main():

    assignment()
    
if __name__ == "__main__":
  main()

######################################################################## 
  
