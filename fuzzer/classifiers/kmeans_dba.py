'''
from alexminnaar GitHub
changes:
- renamed to State_Detector
- added dba method
- added predict method
- added save & load centroids method
'''

from __future__ import division
import matplotlib.pylab as plt
import numpy as np
from progress.bar import Bar
import os
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce

class KmeansDBA(object):
	def __init__(self,num_clust):
		'''
		num_clust is the number of clusters for the k-means algorithm
		assignments holds the assignments of data points (indices) to clusters
		centroids holds the centroids of the clusters
		'''
		self.num_clust=num_clust
		self.assignments={}
		self.centroids=[]

	def load_centroids(self, path):
		self.centroids = []
		for centroid in os.listdir(path):
			self.centroids.append(np.loadtxt(path+'/'+centroid, delimiter=','))
		print("Loaded centroids from %s" % path)
		self.assignments = list(range(len(self.centroids)))

	def save_centroids(self, path):
		if self.createFolder(path):
			i=0
			for centroid in self.centroids:
				np.savetxt(path + '/' + str(i), centroid, delimiter=',')
				i+=1
			print("Saved centroids to %s" % path)	

	def createFolder(self, directory):
		try:
			if not os.path.exists(directory):
				os.makedirs(directory)
			return 1
		except OSError:
			print('Error: Creating directory. ' +  directory)
			return 0	

	def k_means_clust(self,data,num_iter,w,progress=False, dba_sample=100):
		'''
		k-means clustering algorithm for time series data.  dynamic time warping Euclidean distance
			used as default similarity measure. 
		'''
		idx= np.random.choice(data.shape[0], self.num_clust)
		self.centroids= data[idx]

		for n in range(num_iter):
			#assign data points to clusters
			self.assignments={}
			for ind,i in enumerate(data):
				min_dist=float('inf')
				closest_clust=None
				for c_ind,j in enumerate(self.centroids):
					if self.LB_Keogh(i,j,5)<min_dist:
						cur_dist=self.DTWDistance(i,j,w)
						if cur_dist<min_dist:
							min_dist=cur_dist
							closest_clust=c_ind
				if closest_clust in self.assignments:
					self.assignments[closest_clust].append(ind)
				else:
					self.assignments[closest_clust]=[]

			#recalculate centroids of clusters using DBA, only take a sample (otherwise too expensive)
			for key in self.assignments:				
				#series = data[np.random.choice(self.assignments[key], dba_sample)]
				series = data[self.assignments[key]]
				if len(series) != 0:
					self.centroids[key] = performDBA(series)
				else:
					self.centroids[key] = 0


	def classify(self, response):
		""" calculate dist to each clust, return closest """
		dist = {key:None for key in self.assignments}

		for key in self.assignments:
			dist[key] = self.DTWDistance(response, self.centroids[key])

		return min(dist, key=dist.get)

	def get_centroids(self):
		return self.centroids
		
	def get_assignments(self):
		return self.assignments
		
	def plot_centroids(self):
		plt.figure(figsize=(15,12))
		for i in self.centroids:
			plt.plot(i)
		plt.savefig('../Documents/figs/dba.png')
		
	def DTWDistance(self,s1,s2,w=None):
		'''
		Calculates dynamic time warping Euclidean distance between two
		sequences. Option to enforce locality constraint for window w.
		'''
		DTW={}

		if w:
			w = max(w, abs(len(s1)-len(s2)))

			for i in range(-1,len(s1)):
				for j in range(-1,len(s2)):
					DTW[(i, j)] = float('inf')
			
		else:
			for i in range(len(s1)):
				DTW[(i, -1)] = float('inf')
			for i in range(len(s2)):
				DTW[(-1, i)] = float('inf')
		
		DTW[(-1, -1)] = 0

		for i in range(len(s1)):
			if w:
				for j in range(max(0, i-w), min(len(s2), i+w)):
					dist= (s1[i]-s2[j])**2
					DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])
			else:
				for j in range(len(s2)):
					dist= (s1[i]-s2[j])**2
					DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])
			
		return np.sqrt(DTW[len(s1)-1, len(s2)-1])
		
	def LB_Keogh(self,s1,s2,r):
		'''
		Calculates LB_Keough lower bound to dynamic time warping. Linear
		complexity compared to quadratic complexity of dtw.
		'''
		LB_sum=0
		for ind,i in enumerate(s1):
			
			lower_bound=min(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
			upper_bound=max(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
			
			if i>upper_bound:
				LB_sum=LB_sum+(i-upper_bound)**2
			elif i<lower_bound:
				LB_sum=LB_sum+(i-lower_bound)**2
		
		return np.sqrt(LB_sum)
	
	def performDBA(self, series, n_iterations=10):
		n_series = len(series)
		max_length = reduce(max, map(len, series))

		cost_mat = np.zeros((max_length, max_length))
		delta_mat = np.zeros((max_length, max_length))
		path_mat = np.zeros((max_length, max_length), dtype=np.int8)

		medoid_ind = self.approximate_medoid_index(series,cost_mat,delta_mat)
		center = series[medoid_ind]

		for i in range(0,n_iterations):
			center = self.DBA_update(center, series, cost_mat, path_mat, delta_mat)

		return center

	def approximate_medoid_index(self, series,cost_mat,delta_mat):
		if len(series)<=50:
			indices = range(0,len(series))
		else:
			indices = np.random.choice(range(0,len(series)),50,replace=False)

		medoid_ind = -1
		best_ss = 1e20
		for index_candidate in indices:
			candidate = series[index_candidate]
			ss = self.sum_of_squares(candidate,series,cost_mat,delta_mat)
			if(medoid_ind==-1 or ss<best_ss):
				best_ss = ss
				medoid_ind = index_candidate
		return medoid_ind

	def sum_of_squares(self, s,series,cost_mat,delta_mat):
		return sum(map(lambda t:self.squared_DTW(s,t,cost_mat,delta_mat),series))

	def DTW(self, s,t,cost_mat,delta_mat):
		return np.sqrt(self.squared_DTW(s,t,cost_mat,delta_mat))

	def squared_DTW(self, s,t,cost_mat,delta_mat):
		s_len = len(s)
		t_len = len(t)
		length = len(s)
		self.fill_delta_mat_dtw(s, t, delta_mat)
		cost_mat[0, 0] = delta_mat[0, 0]
		for i in range(1, s_len):
			cost_mat[i, 0] = cost_mat[i-1, 0]+delta_mat[i, 0]

		for j in range(1, t_len):
			cost_mat[0, j] = cost_mat[0, j-1]+delta_mat[0, j]

		for i in range(1, s_len):
			for j in range(1, t_len):
				diag,left,top =cost_mat[i-1, j-1], cost_mat[i, j-1], cost_mat[i-1, j]
				if(diag <=left):
					if(diag<=top):
						res = diag
					else:
						res = top
				else:
					if(left<=top):
						res = left
					else:
						res = top
				cost_mat[i, j] = res+delta_mat[i, j]
		return cost_mat[s_len-1,t_len-1]

	def fill_delta_mat_dtw(self, center, s, delta_mat):
		slim = delta_mat[:len(center),:len(s)]
		np.subtract.outer(center, s,out=slim)
		np.square(slim, out=slim)

	def DBA_update(self, center, series, cost_mat, path_mat, delta_mat):
		options_argmin = [(-1, -1), (0, -1), (-1, 0)]
		updated_center = np.zeros(center.shape)
		n_elements = np.array(np.zeros(center.shape), dtype=int)

		center_length = len(center)
		for s in series:
			s_len = len(s)
			self.fill_delta_mat_dtw(center, s, delta_mat)
			cost_mat[0, 0] = delta_mat[0, 0]
			path_mat[0, 0] = -1

			for i in range(1, center_length):
				cost_mat[i, 0] = cost_mat[i-1, 0]+delta_mat[i, 0]
				path_mat[i, 0] = 2

			for j in range(1, s_len):
				cost_mat[0, j] = cost_mat[0, j-1]+delta_mat[0, j]
				path_mat[0, j] = 1

			for i in range(1, center_length):
				for j in range(1, s_len):
					diag,left,top =cost_mat[i-1, j-1], cost_mat[i, j-1], cost_mat[i-1, j]
					if(diag <=left):
						if(diag<=top):
							res = diag
							path_mat[i,j] = 0
						else:
							res = top
							path_mat[i,j] = 2
					else:
						if(left<=top):
							res = left
							path_mat[i,j] = 1
						else:
							res = top
							path_mat[i,j] = 2

					cost_mat[i, j] = res+delta_mat[i, j]

			i = center_length-1
			j = s_len-1

			while(path_mat[i, j] != -1):
				updated_center[i] += s[j]
				n_elements[i] += 1
				move = options_argmin[path_mat[i, j]]
				i += move[0]
				j += move[1]
			assert(i == 0 and j == 0)
			updated_center[i] += s[j]
			n_elements[i] += 1

		return np.divide(updated_center, n_elements)
