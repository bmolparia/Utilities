#!/usr/bin/env python
# Copyright (C) 2015-2016  Bhuvan Molparia
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import re, argparse
from itertools import tee, imap

class SAM_Header(object):
    """
    Separates out sam parsing from iterating over headerrecords.
    Maybe add more functionality later
    """
    def __init__(self, sam_line_arr):
         
        self.sam_list = sam_line_arr
        self.header_type, self.header_tags = sam_line_arr[0], sam_line_arr[1:] 
    
    def __str__(self):
        
        return ('\t').join(self.sam_list) + '\n'
 
             
class SAM_Data(object):
    """
    Separates out sam parsing from iterating over records.
    """
    def __init__(self, sam_line_arr):
        
        self.sam_list = sam_line_arr
        self.qname, self.flag, self.rname, self.pos, self.mapq, self.cigar, self.rnext, self.pnext, self.tlen, self.seq, self.qual = sam_line_arr[0:11]
        self.flag = int(self.flag)
        self.tlen = int(self.tlen)

        try:
            self.alignment = sam_line_arr[11]
        except IndexError:
            self.alignment = None

    def __str__(self):
        
        return ('\t').join(self.sam_list) + '\n'
 

class SAM_Parser(object):

    def __init__(self,filepath):
        self.fin = open(filepath,'r')
    
    def __iter__(self):
        return self

    def next(self):
        fin = self.fin
        line = fin.readline()
        if line == '':
            fin.close()
            raise StopIteration
        
        line = line.replace('\n','').split('\t')
        if line[0].startswith('@'):
            data = SAM_Header(line) 
        else:
            data = SAM_Data(line)

        return data

