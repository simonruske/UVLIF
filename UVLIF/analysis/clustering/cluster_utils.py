'''
The purpose of this code file is to provide extra utility functions
for hierarchical agglomerative clustering. 

The function extract provides the same functionality as the
scipy.cluster.hierarchy.fcluster using the 'maxclust' setting, but the extract
function is much faster when dealing with more than 10 ** 4 particles. 

The standardisation function provides 7 different methods of standardisation
that are detailed in full in the following paper

Milligan, G. W. and Cooper, M. C.: A study of standardization
of variables in cluster analysis, 1988. 

'''

import numpy as np 

def extract(A, minclust = 1, maxclust = 1, K = None): 

  '''
  Extracts particular solutions from a linkage matrix. Will 
  extract all solutions from the number clusters specified 
  by the minclust parameter up to and including the maxclust 
  parameter. Alternatively which solutions to extract can be 
  specified using the parameter K.  
  
  Parameters 
  ----------
  
  A : ndarray 
    A :math:`n-1` by 4 matrix encoding the linkage 
    (hierarchical clustering). See ``linkage`` documentation 
    in scipy.cluster.hierarhcy for more information on its form. 
    
  minclust : int 
    The smallest nuimber of clusters to be extracted. 
    
  maxclust : int 
    The largest number of clusters to be extracted. 
    
  k : ndarray 
    Used as an alternative to the minclust and maxclust parameters. 
    If specified the function will extract clusterings based on this array. 
    Each element should be a number of clusters. 
    
  Returns 
  -------
  
  Solution : ndarray 
    A matrix where each row represents the ith clustering as 
    given by `k`. For each row the jth element is the cluster 
    in which the jth object is placed. 
    
  Examples 
  --------
  
  Both of the following lines of code will return a matrix containing
  the clusterings for 1 to 5 clusters. 
  
  > extract(A, K = range(1, 6))
  > extract(A, maxclust = 5)

  Notes 
  -----
  
  This is intended as a faster alternative to scipy.cluster.hierarchy.fcluster
  using the 'maxclust' setting. 
  
  '''
  
  # If K not specified create it from minclust and maxclust 
  
  if K == None: 
    K = range(minclust, maxclust + 1) 
    
  # Creates a dictionary for the intial clustering 
  n = len(A) + 1
  d = {i:[i] for i in range(n)} 
  
  # Merges clusters until the required solutions are reached 
  
  clusterings = [] # the output for the function 
  
  for k, rows in enumerate(A): 
  
    # If solution is required
    if n-k in K:
    
      # create a vector to store the clusterings 
      clustering = np.zeros(n)
      
      # For each object update the clustering vector with
      # the label of the cluster it belongs to 
      
      for cluster, i in enumerate(d): 
        for obj in d[i]: 
          clustering[obj] = cluster + 1 
          
      clusterings.insert(0, clustering)
      
    # If finished return the clusterings   
    if n-k < np.min(K) + 1:
      return np.array(clusterings)
        
    # Otherwise, merge the clusters specified by 'rows'
      
    d[n+k] = d.pop(rows[0]) + d.pop(rows[1])
      
  # If this point is reached th4en the trivial 1 cluster
  # clustering is required so add this and return
  # the clustering matrix. 
  
  clusterings.insert(0, np.ones(n))
  
  return np.array(clusterings) 

def standardise(data, method): 

  """
  Standardises a dataset. 
  
  Parameters 
  ----------
  
  data : ndarray 
    The original dataset. 
    
  method : str
    One of the following methods 
    
    0) No standardisation
    1) z-score 
    2) divide by standard deviation 
    3) divide by max 
    4) subtract min divide by range 
    5) divide by range 
    6) divide by sum 
    7) Repalce each data point with its rank
    
    For further details on these method consult the citation at the 
    begining of this document. 
    
  Returns 
  -------
  
  new_data : ndarray 
    The standardised dataset
  """
  
  if method == 0 or 'unstandardised': 
    new_data = data

  if method == 1 or method == 'zscore':
    new_data = (data - np.mean(data, axis = 0)) / np.std(data, axis = 0)

  if method == 2 or method == 'std': 
    new_data = data / np.std(data, axis = 0)

  if method == 3 or method == 'max': 
    new_data = data / np.max(data, axis = 0) 

  if method == 4 or method == 'minrange': 
    new_data = (data - np.min(data, axis = 0)) /(np.max(data, axis = 0) - np.min(data, axis = 0))
        
  if method == 5 or method == 'range': 
    new_data = data / (np.max(data, axis = 0) - np.min(data, axis =0))

  if method == 6 or method == 'sum': 
    new_data = data / np.sum(data, axis = 0)
                                                   
  if method == 7 or method == 'rank': 
    d = len(data[0])
    N = len(data)
    new_data = np.zeros((N, d))
    for i in range(d):
      new_data[:,i] = data[:,i].argsort().argsort()

  return new_data
