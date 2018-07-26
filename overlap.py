#!/usr/bin/env python3
# Author: Bhuvan Molparia

# This module checks for overlaps between two sets of bins within a continuous
# array. Example usage: Finding overlaps between a CNVs and genes

from sorted_collection import SortedCollection

class Overlap(object):

	def __init__(self, bin, overlapping_bins=None, overlap_amounts=None):

		self.bin = bin
		if overlapping_bins != None:
			self._obin = overlapping_bins
		else:
			self._obin = []

		if overlap_amounts != None:
			self._oamts = overlap_amounts
		else:
			self._oamts = []

	def __repr__(self):
		''' Defines the way this obejct is printed '''
		return '{} overlaps with:\n{}'.format(self.bin,
		'\n'.join('{}:{}'.format(x,y) for x,y in zip(self._obin, self._oamts)))

	@property
	def overlapping_bins(self):
		return self._obin

	@overlapping_bins.getter
	def overlapping_bins(self):
		''' Defines the get attribute function for overlapping bins.'''
		return list(zip(self._obin, self._oamts))

	@overlapping_bins.setter
	def overlapping_bins(self,value):
		''' Defines the set attribute function for overlapping bins. It will
		append any values that are being set to the original list '''

		raise AttributeError('Attribute cannot directly be set')

	def add_bin(self,bin,overlap_amt):
		''' A method to add an overlapping bin to the list'''

		self._obin.append(bin)
		self._oamts.append(overlap_amt)

def find_overlapping_bins(arr1, arr2):
	''' Function to calculate overlaps for every bin in array 1 against
	every bin in array 2. Accepts two arrays of tuples as inputs. Where each
	tuple is the start and end site of a bin within that array.

	Returns a list of Overlap objects for each bin in arr1. Each overlap
	object contains the indices of all the bins in arr2 that a given arr1
	bin overlaps with along with the amount of overlap represented as tuples.
	'''

	arr2_sc = SortedCollection(arr2, key = (lambda x: x[0]))
	overlapping_bins = []
	for bin in arr1:

		overlaps = Overlap(bin)
		bin_beg, bin_end = bin

		# Find the closest bin in array2
		try:
			closest_bin = arr2_sc.find_le(bin_beg)
			indx = arr2.index(closest_bin)
		except ValueError:
			closest_bin = arr2[0]
			indx = 0

		overlap_amt = get_overlap_amount(bin, closest_bin)
		if overlap_amt > 0:
			overlaps.add_bin(indx, overlap_amt)

		# Check bins after the closest for overlaps
		flag = True
		while flag:
			indx += 1
			try:
				next_bin = arr2[indx]
				overlap_amt = get_overlap_amount(bin, next_bin)
				if overlap_amt > 0:
					overlaps.add_bin(indx, overlap_amt)
				else:
					flag = False
			except IndexError:
				flag = False

		overlapping_bins.append(overlaps)

	return overlapping_bins

def get_overlap_amount(bin1,bin2):
	''' Given two bins, this function returns the amount points that overlap
	between the two '''

	s1,e1 = bin1
	s2,e2 = bin2
	seqL1 = e1-s1+1
	seqL2 = e2-s2+1

	if (s1<=s2) and (e1<e2) and (e1>=s2):
		overlap = e1-s2+1
	elif (s1<=s2) and (e1>=e2):
		overlap = seqL2
	elif (s1>s2) and (s1<=e2) and (e1>=e2):
		overlap = e2-s1+1
	elif (s1>s2) and (e1<e2):
		overlap = seqL1
	else:
		overlap = 0

	return overlap

if __name__ == "__main__":

	arr1 = [(5,15),(55,85),(106,127),(132,142)]
	arr2 = [(10,23),(41,48),(51,62),(80,82),(106,125)]

	t = find_overlapping_bins(arr1, arr2)
	for i in t:
		print(i.bin, i.overlapping_bins)

	# o = Overlap((10,30),[(5,14),(21,27),(30,33)],[5,7,1])
	# print(o.overlapping_bins)
	# o.overlapping_bins = []
