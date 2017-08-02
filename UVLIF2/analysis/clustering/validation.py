'''
This code file contains an implementation of the calinski-harabasz index. 

References 
----------

Milligan, Glenn W., and Martha C. Cooper. 
"An examination of procedures for determining the 
number of clusters in a data set." Psychometrika 50.2 (1985): 159-179.

Calinski, T. and Harabasz, J.: A dendrite method for
cluster analysis, Commun. Stat.-Theor. M., 3, 1-27,
doi:10.1080/03610927408827101, 1974
'''


from collections import Counter
from numpy import mean, zeros, where, array
from numpy.linalg import norm

def validation(data, clusterings, method = 'calinski-harabasz', index = False, threshold = False):

    """
    Evaluates particular clusterings of a set of N objects
    using the original dataset to calculate an index which is used
    to determine which of the given clusterings is 'best'.

    Parameters
    ----------

    data : ndarray
        The original N by D matrix that was clustered for
        example by the linkage function in
        scipy.cluster.hierarchy.

    clusterings : ndarray
        An S by N matrix. Where S is the number of solutions to
        be evaluated. The output from the 'extract' function is
        the intended input here.

    method : str
        A string indicating what type of validation criterion is to
        be used. Currently 'calinski-harabasz is the only available
        index.

    index : bool 
        Set equal to true if you would like to return indices for 
        each clustering instead of the number of clusters.
        
    threshold : bool 
        Set equal to true if you would like to ignore minority clusters
        i.e. those which are less than half the average cluster size.

    Returns
    -------
    number_of_clusters : int
        The 'optimal' number of clusters indicated by the solutions
        given. 


    index : ndarray 
        An array of the validation indices for each clustering.
    
        
    """

    N = len(data) # Number of objects
    m = mean(data, axis = 0) # mean of the data 
    CH = zeros(len(clusterings)) # vector for CH index
    SSWv = zeros(len(clusterings)) # vector for SSW
    SSBv = zeros(len(clusterings)) # vector for SSB
 
    # Go through all the clusterings one by one 

    for i, solution in enumerate(clusterings): 

        clusters = Counter(solution) # label -> size
        k = len(clusters) # Number of clusters
        SSB = 0 # Initial sum of squares between the clusters 
        SSW = 0 # Initial sum of squares within the clusters

        # For each of the clusters updates the within and between
        # sums of squares.

        if threshold: 
            limit = mean(list(clusters.items())) // 2
        else: 
            limit = 0 
        
        for label, size in clusters.items():
            if size > limit: 
            	cluster = data[where(solution == label)] 
            	cluster_mean = mean(cluster, axis = 0)
            	SSB += size * norm(m - cluster_mean) ** 2
            	SSW += sum(norm(cluster - cluster_mean, axis = 1) ** 2)


        # If the number of clusters is 1 the index should
        # return a value of infinity but instead we return 0
        # otherwise this will always be maximum.

        if method == 'calinski-harabasz':
            SSWv[i] = SSW
            SSBv[i] = SSB

            if k -1 == 0 or SSW == 0:
                CH[i] = 0

            else:
                CH[i] = SSB / SSW * (N - k) / (k-1) # Formula of the index.



    if method == 'calinski-harabasz':  
        if index: 
            return CH
        else: 
            return len(Counter(clusterings[where(CH == max(CH))][0]))






                               
     
