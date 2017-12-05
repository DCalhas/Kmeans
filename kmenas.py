import os
import numpy
import random

#number of clusters arg 1

def meanPoint(cluster, points):
	meanPoint = []
	i = 0
	while i < len(cluster)-1:
		meanPoint = numpy.sum([points[cluster[i]], points[cluster[i+1]]], axis = 0).tolist()
		i += 2
	#divide every position
	for i in range(0, len(meanPoint)):
		meanPoint[i] = meanPoint[i] / len(cluster)
	return meanPoint

class kmeans:

	def __init__(self, arg, points, k):
		self.arg = arg
		self.k = k
		self.points = points


		minDistance = -1
		centroids = []
		clusters = []
		for i in range(0, k):
			clusters += [[]]

		self.clusters = clusters
		#compute every combination of centroids
		self.centroids = self.getCentroids(k)
		print(self.centroids)

	def getPoints(self):
		return self.points

	def run(k):
		return k

	def distance(p1, p2):
		sum = 0.0
		for i in range(0, len(p1)):
			sum = numpy.sum((p1[i] - p2[i]) ** 2)
		return numpy.sqrt(sum)

	def getCentroids(self, k):
		centroids = []
		for i in range(0, k):
			c = random.randint(0, len(self.points) - 1)
			while c in centroids:
				c = random.randint(0, len(self.points) - 1)
			centroids += [c]
		return centroids

	def computeMeanCentroids(self):
		distanceClusters = []
		self.clusterMeans = []
		for i in range(0, len(self.centroids)):
			self.clusterMeans += [self.points[self.centroids[i]]]
			self.clusters[i] += [self.centroids[i]]
		for i in range(0, len(self.points)):
			if not i in self.centroids:
				for j in range(0, len(self.centroids)):
					distanceClusters += [kmeans.distance(self.points[self.centroids[j]], self.points[i])]
				index = -1
				minDist = -1
				for j in range(0, len(distanceClusters)):
					if index == -1:
						index = j
						minDist = distanceClusters[j]
					elif minDist > distanceClusters[j]:
						index = j
						minDist = distanceClusters[j]

				self.clusters[index] += [i]
				self.clusterMeans[index] = meanPoint(self.clusters[index], self.points)

			distanceClusters = []

	def computeDistances(self):
		self.clusterDistances = []
		for i in range(0, len(self.centroids)):
			self.clusterDistances += [[]]
		for i in range(0, len(self.points)):
			for j in range(0, len(self.clusterDistances)):
				self.clusterDistances[j] +=  [kmeans.distance(self.points[i], self.clusterMeans[j])]

	def arrangeClusters(self):
		changed = True
		while changed:
			newClusters = []
			for i in range(0, len(self.clusters)):
				newClusters += [[]]

			changed = False
			for i in range(0, len(self.points)):
				minCluster = -1
				minV = -1
				for j in range(0, len(self.clusterDistances)):
					if minV == -1:
						minV = self.clusterDistances[j][i]
						minCluster = j
					elif minV > self.clusterDistances[j][i]:
						minV = self.clusterDistances[j][i]
						minCluster = j
				#check if is the same cluster
				if not i in self.clusters[minCluster]:
					changed = True

				#update newClusters
				newClusters[minCluster] += [i]

			self.clusters = newClusters
			#compute the means again

			self.clusterMeans = []
			for i in range(0, len(self.clusters)):
				self.clusterMeans += [meanPoint(self.clusters[i], self.points)]
			#compute clusters means

			self.computeDistances()

data = open("Lymphoma45x4026+2classes.arff")

lines = data.readlines()

points = []

for line in lines:
	missing_values = False
	if not missing_values and not "@RELATION" in line and not "@ATTRIBUTE" in line and not "@DATA" in line and line != "\n" and line != "" and line != " ":
		values = line.split(",")[:-1]
		for i in range(0, len(values)):
			if values[i] == "?":
				missing_values = True
			else:
				values[i] = float(values[i])
		if not missing_values:
			points.append(values)


km = kmeans(1, points, 2)
km.computeMeanCentroids()
km.computeDistances()
km.arrangeClusters()
print("The clusters computed are: ")
print(km.clusters)
#find furthest samples

minDistance = -1
centroids = []
clusters = [[],[]]
#TODO: use random in this bitch
for i in range(0, 2):
	c = random.randint(0, len(points))
	while c in centroids:
		c = random.randint(0, len(points))
	centroids += [c]

print(centroids)
#initialize array
distanceClusters = []
clusterMeans = []
clusterMeans += [points[centroids[0]]]
clusterMeans += [points[centroids[1]]]
clusters[0] += [centroids[0]]
clusters[1] += [centroids[1]]
#compute means
for i in range(0, len(points)):
	distanceClusters += [kmeans.distance(points[centroids[0]], points[i])]
	distanceClusters += [kmeans.distance(points[centroids[1]], points[i])]
	if distanceClusters[0] < distanceClusters[1]:
		if i != centroids[0] and i != centroids[1]:
			clusters[0] += [i]
			clusterMeans[0] = meanPoint(clusters[0], points)
	else:
		if i != centroids[0] and i != centroids[1]:
			clusters[1] += [i]
			clusterMeans[1] = meanPoint(clusters[1], points)
	#reinitialize array
	distanceClusters = []

#compute clusters means

clusterDistances = [[], []]
for i in range(0, len(points)):
	clusterDistances[0] += [kmeans.distance(points[i], clusterMeans[0])]
	clusterDistances[1] += [kmeans.distance(points[i], clusterMeans[1])]

#rearrange clusters
changed = True
while changed:
	newClusters = [[], []]
	changed = False
	for i in range(0, len(points)):
		minCluster = -1
		minValue = -1
		for j in range(0, len(clusterDistances)):
			if minValue == -1:
				minValue = clusterDistances[j][i]
				minCluster = j
			elif minValue > clusterDistances[j][i]:
				minValue = clusterDistances[j][i]
				minCluster = j
		#check if is the same cluster
		if not i in clusters[minCluster]:
			changed = True

		#update newClusters
		newClusters[minCluster] += [i]

	clusters = newClusters
	#compute the means again

	clusterMeans = [meanPoint(clusters[0], points), meanPoint(clusters[1], points)]

	#compute clusters means

	clusterDistances = [[], []]
	for i in range(0, len(points)):
		clusterDistances[0] += [kmeans.distance(points[i], clusterMeans[0])]
		clusterDistances[1] += [kmeans.distance(points[i], clusterMeans[1])]

print("The clusters computed are: ")
print(clusters)