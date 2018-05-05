
class Fragment:

	def __init__(self):
		self.predPerAttribute = list()
		self.applPerSite = list()
		self.MCRUD = dict()
		self.numSites = 0
		self.numAttributes = 0

	def createMCRUD(self):
		print ("Input number of sites")
		self.numSites = int(raw_input())

		print ("Enter number of attributes")
		self.numAttributes = int(raw_input())

		for attr in range(self.numAttributes):
			print ("Input number of predicates for attribute: ", attr)
			self.predPerAttribute.append(int(raw_input()))

		for site in range(self.numSites):
			print ("Input number of applications for site: ", site)
			self.applPerSite.append(int(raw_input()))
			for attributeIndex in range(len(self.predPerAttribute)):
				numPredicates = self.predPerAttribute[attributeIndex]
				matrix = [[0 for x in range(self.applPerSite[-1])] for y in range(numPredicates)]
				print ("Enter MCRUD matrix for site and attribute: ", site, attributeIndex)
				for pred in range(numPredicates):
					for appl in range(self.applPerSite[-1]):
						print(pred , appl)
						matrix[pred][appl] = raw_input()

				self.MCRUD[site, attributeIndex] = matrix


	def getSum(self, site, pred, attr):
		MCRUD = self.MCRUD
		mcrud_site_attr_pred = MCRUD[site, attr][pred]
		length = len(mcrud_site_attr_pred)
		sum_pred_site = 0
		for l in range(length):
			if "c" in mcrud_site_attr_pred[l]:
				sum_pred_site += 2
			if "r" in mcrud_site_attr_pred[l]:
				sum_pred_site += 1
			if "u" in mcrud_site_attr_pred[l]:
				sum_pred_site += 3
			if "d" in mcrud_site_attr_pred[l]:
				sum_pred_site += 2

		return sum_pred_site


	def createFragments(self):		
		self.sum_pred_site_dict = dict()
		ALP_attr_pred = dict()
		ALP_attr = [0 for x in range(self.numAttributes)]

		for attr in range(self.numAttributes):
			for pred in range(self.predPerAttribute[attr]):
				sum_pred_site_list = list()
				for site in range(self.numSites):
					sum_pred_site_list.append(self.getSum(site, pred, attr))
				self.sum_pred_site_dict[attr, pred] = sum_pred_site_list
				sum_max = max(sum_pred_site_list)
				print ("sum_max", sum_max)
				total_sum = sum(sum_pred_site_list)
				print ("total_sum", total_sum)
				ALP_attr_pred[attr, pred] = 2*sum_max - total_sum
				print ("alp_attr_pred", ALP_attr_pred[attr, pred])
				ALP_attr[attr] += ALP_attr_pred[attr, pred]

		self.max_attr_index = ALP_attr.index(max(ALP_attr))
		print self.max_attr_index
		print ALP_attr[self.max_attr_index]


	def countRead(self, attr, pred, sites_indices):
		MCRUD = self.MCRUD
		num_reads_list = list()

		for site in sites_indices:
			num_reads = 0
			for appl in range(self.applPerSite[site]):
				if("r" in MCRUD[site, attr][pred][appl]):
					num_reads = num_reads + 1
			num_reads_list.append(num_reads)
		num_reads_min_index = num_reads_list.index(min(num_reads_list))
		return num_reads_min_index


	def allocateFragments(self):
		numPredicates = self.predPerAttribute[self.max_attr_index]
		allocate = [-1 for x in range(numPredicates)]
		replicate = [-1 for x in range(numPredicates)]

		for pred in range(numPredicates):
			sum_pred_site_list = self.sum_pred_site_dict[self.max_attr_index, pred]
			max_sum_pred_site = max(sum_pred_site_list)
			max_indices = [i for i, x in enumerate(sum_pred_site_list) if x == max_sum_pred_site]
			if (len(max_indices) == 1):	
				allocate[pred] = max_indices[0]
			
			else:
				site_index_min = self.countRead(self.max_attr_index, pred, max_indices)
				allocate[pred] = site_index_min
				for site_index in max_indices:
					if site_index != site_index_min: 
						replicate[pred] = site_index

		for i in range(numPredicates):
			print("All tuples with predicate %d will be allocated to site %d" % (i, allocate[i]))
		
		for i in range(numPredicates):
			print("All tuples with predicate %d will be replicated to site %d" % (i, replicate[i]))


obj = Fragment()
obj.createMCRUD()
obj.createFragments()
obj.allocateFragments()