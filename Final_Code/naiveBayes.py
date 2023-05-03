# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    correct_arr = [0] * len(kgrid)
    n = len(trainingData)
    for l in range(len(kgrid)): 
      k = kgrid[l]
      dict = {}

      for feature in self.features:
        list0 = [0] * len(self.legalLabels)
        list1 = [0] * len(self.legalLabels)
        for i in range(len(trainingData)):
          feature_array = trainingData[i]
          label = trainingLabels[i]
          pixel = feature_array.__getitem__(feature)
          if pixel == 1:
            list1[label] += 1
          else:
            list0[label] += 1
        finallist = [list0,list1]
        dict[feature] = finallist
      
      p_y = [0] * len(self.legalLabels)
      for entry in trainingLabels:
        p_y[entry] += 1/n
      
      self.p_y = p_y

      self.dict_p = {}

      for coord in dict.keys():
        list0_p = [0] * len(self.legalLabels)
        list1_p = [0] * len(self.legalLabels)
        for i in range(len(self.legalLabels)):
          val0 = dict[coord][0][i]
          val1 = dict[coord][1][i]
          list0_p[i] = (val0 + k) / (val0 + val1 + 2*k)
          list1_p[i] = (val1 + k) / (val0 + val1 + 2*k)
        finallist_p = [list0_p,list1_p]
        self.dict_p[coord] = finallist_p
      
      guesses = self.classify(validationData)
      correct = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
      correct_arr[l] = correct
    
    print("CORRECT ARR")
    print(correct_arr)

    max_value = max(correct_arr)
    max_index = correct_arr.index(max_value)

    final_k = kgrid[max_index]
    dict = {}

    for feature in self.features:
      list0 = [0] * len(self.legalLabels)
      list1 = [0] * len(self.legalLabels)
      for i in range(len(trainingData)):
        feature_array = trainingData[i]
        label = trainingLabels[i]
        pixel = feature_array.__getitem__(feature)
        if pixel == 1:
          list1[label] += 1
        else:
          list0[label] += 1
      finallist = [list0,list1]
      dict[feature] = finallist
    
    p_y = [0] * len(self.legalLabels)
    for entry in trainingLabels:
      p_y[entry] += 1/n
    
    self.p_y = p_y

    self.dict_p = {}

    for coord in dict.keys():
      list0_p = [0] * len(self.legalLabels)
      list1_p = [0] * len(self.legalLabels)
      for i in range(len(self.legalLabels)):
        val0 = dict[coord][0][i]
        val1 = dict[coord][1][i]
        list0_p[i] = (val0 + final_k) / (val0 + val1 + 2*final_k)
        list1_p[i] = (val1 + final_k) / (val0 + val1 + 2*final_k)
      finallist_p = [list0_p,list1_p]
      self.dict_p[coord] = finallist_p
        
    
        
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior)
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    logJoint = util.Counter()
    
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    # print(self.dict_p)
    pval_arr = [0] * len(self.legalLabels)
    for i in range(len(self.legalLabels)):
      sum = math.log(self.p_y[i])
      for key in datum.keys():
        value = datum[key]
        prelog = self.dict_p[key][value][i]
        sum = sum + math.log(prelog)
      pval_arr[i] = sum
    
    max_value = max(pval_arr)
    max_index = pval_arr.index(max_value)
    return max_index

    
    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []
       
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    return featuresOdds
    

    
      
