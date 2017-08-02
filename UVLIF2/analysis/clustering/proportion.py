'''
Function that takes two flat clusterings 
and finds the percentage of points placed into the same cluster for both
clusterings. 

Flat clusterings are represented by lists or arrays of integers. 
Each element corresponds to a particular object and the value 
is the label for the cluster that object is placed in. 
For example if the second element is equal to 5 then this means 
that the second object is placed into the fifth cluster. 

Parameters 
----------
clustering_a : array like object of type int 
  The first flat clustering 
  
clustering_b : array like object of type int 
  The second flat clustering 

matching : bool 
  If set to true a matching matrix (also commonly referred to as a confusion
  matrix will be returned). Otherwise the proportion

Returns 
-------

proportion : float 
  The proportion of points which are placed into the same cluster for both 
  clusterings. This is calculated by dividing the sum of the diagonal by the sum
  of the matching (confusion) matrix. 

matching_matrix : ndarray of type int 
  The matching matrix or confusion matrix.
'''

from numpy import unique, zeros, argmax, array 

def proportion(clustering_a, clustering_b, matching = False): 

  number_of_objects = len(clustering_a)
  
  # Create a matching matrix. Here we assume that the 
  # number of clusters are sufficiently small that a
  # sparse matrix is not necessary. 
  
  # Array of cluster labels for both clusterings 
  cluster_labels_a = unique(clustering_a)
  cluster_labels_b = unique(clustering_b)
  
  # Number of clusters for both clusterings 
  number_of_clusters_a = len(cluster_labels_a)
  number_of_clusters_b = len(cluster_labels_b) 
  
  # Relabel the clusters from 0 to number_of_clusters -1 
  # this is so you don't have unnecessary rows/cols in the matching matrix
  
  relabel_a = dict(zip(cluster_labels_a, range(number_of_clusters_a)))
  relabel_b = dict(zip(cluster_labels_b, range(number_of_clusters_b)))
  
  # Populate a matching matrix 
  matching_matrix = zeros((number_of_clusters_a, number_of_clusters_b))
  
  # Loop through both clustersings 
  
  for i, j in zip(clustering_a, clustering_b): 
    label_a = relabel_a[i] # relabel the first cluster 
    label_b = relabel_b[j] # relabel the second cluster 
    matching_matrix[label_a, label_b] += 1 # Add 1 to the matching matrix
    
  # If matching matrix is requested then return 
  if matching:
    return(array(matching_matrix,  'int'))
  
  # otherwise figure out a percentage
  min_number_of_clusters = min(number_of_clusters_a, number_of_clusters_b)
  
  total = 0 # total number of points in matched clusters 
  
  for _ in range(min_number_of_clusters):
  
    # Find the location of the maximum 
    maximum_loc = argmax(matching_matrix) #element of maximum 
    i = maximum_loc // number_of_clusters_b # row of maximum 
    j = maximum_loc % number_of_clusters_b # column of maximum 
    
    # ADd maximal element to total 
    total += matching_matrix[i, j] 
    
    # Set the row and column to 0 i.e. remove it 
    matching_matrix[i, :] = 0
    matching_matrix[:, j] = 0
    
  return total / number_of_objects
    
