#!/usr/bin/env python3
# Author: Bhuvan Molparia

# This module checks for overlaps between two sets of bins within a continuous
# array. Example usage: Finding overlaps between a CNVs and genes

class Overlap(object):

	def __init__(self, arr1_start,arr2_start,arr1_end,arr2_end):
	''' Two sets of start and end sites. Each start and end define the
	various bins '''
		self.a1s = arr1_start
		self.a2s = arr2_start
		self.a1e = arr1_end
		self.a2e = arr2_end

	def main(self):

		a1s = self.a1s
		a2s = self.a2s
		a1e = self.a1e
		a2e = self.a2e

		overlap_array = self.overlapCounts(a1s,a2s,a1e,a2e)
		return overlap_array

	def overlapCounts(self,a1s,a2s,a1e,a2e):

	## Function to calculate overlaps for every tag with virtual tags -
	## Find the closest island in the other sample
	## 1 - Tags
	## 2 - CNVs

		OverlapingTags = []
		i = 0
		while i < len(a1s):

			beg1 = a1s[i]
			end1 = a1e[i]
			seqL1 = float(end1-beg1+1)

			indx = self.insert_pos(a2s,a2s,beg1)
			try:
				beg2 = a2s[indx]
				end2 = a2e[indx]

				overlap = self.overlapNumber(beg1,end1,beg2,end2)
				if overlap != 0.0:
					OverlapingTags.append((beg1,end1,beg2,end2))

			except IndexError:

				pass
			i += 1

		return OverlapingTags


	def insert_pos(self,arrI,arr,value):

	## arrI - to get the final index
	## arr  - the array to work on, same as arrI

		if len(arr) == 1:
			if value < arr[0]:
				return arrI.index(arr[0])-1
			else:
				return arrI.index(arr[0])
		else:
			arr_mid = len(arr)/2
			arrLow  = arr[:arr_mid]
			arrHigh = arr[arr_mid:]

			if value>arrLow[-1]:
				out = self.insert_pos(arrI,arrHigh,value)
			else:
				out = self.insert_pos(arrI,arrLow,value)
		return out

	def overlapNumber(self,s1,e1,s2,e2):

		seqL1 = float(e1-s1+1)
		seqL2 = float(e2-s2+1)

		if (s1<=s2) and (e1<e2) and (e1>=s2):
			overlap = float(e1-s2+1)
		elif (s1<=s2) and (e1>=e2):
			overlap = seqL2
		elif (s1>s2) and (s1<=e2) and (e1>=e2):
			overlap = float(e2-s1+1)
		elif (s1>s2) and (e1<e2):
			overlap = seqL1
		else:
			overlap = 0.0

		return overlap


if __name__ == "__main__":

	a1s = range(50,10000,100)
	a1e = range(55,10000,100)
	a2s = range(0,10000,500)
	a2e = range(100,10000,500)

	print a1s
	print a1e
	print a2s
	print a2e,'\n'

	o = Overlap(a1s,a2s,a1e,a2e)
	t = o.main()
	print t
