#!/usr/bin/env python3
# Author: Bhuvan Molparia

# This module checks for overlaps between two sets of bins within a continuous
# array. Example usage: Finding overlaps between a CNVs and genes

from sorted_collection import SortedCollection

def find_overlapping_bins(arr1, arr2):
	''' Function to calculate overlaps for every bin in array 1 against
	every bin in array 2. Accepts two arrays of tuples as inputs. Where each
	tuple is the start and end site of a bin within that array'''

	a1s,a1e = zip(*arr1)
	a2s,a2e = zip(*arr2)

	overlapping_bins = []
	i = 0
	while i < len(a1s):
		beg1 = a1s[i]
		end1 = a1e[i]
		seqL1 = float(end1-beg1+1)
		le_val = SortedCollection(a2s).find_le(beg1)
		indx = a2s.index(le_val)

		try:
			beg2 = a2s[indx]
			end2 = a2e[indx]
			overlap = overlap_amount(beg1,end1,beg2,end2)
			if overlap != 0.0:
				overlapping_bins.append((beg1,end1,beg2,end2))
		
		except IndexError:
			pass
		i += 1

	return overlapping_bins

def overlap_amount(s1,e1,s2,e2):
	''' Given two bins, this function returns the amount points that overlap
	between the two '''

	seqL1 = float(e1-s1+1)
	seqL2 = float(e2-s2+1)

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

	arr1 = [(10,23),(41,62),(80,82),(106,125)]
	arr2 = [(5,15),(55,85),(106,125)]
	print(arr1,'\n')
	print(arr2,'\n')


	t = find_overlapping_bins(arr1, arr2)
	print(t)
