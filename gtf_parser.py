#!/usr/bin/env python
# Copyright (C) 2012-2013  Collin Tokheim
# Copyright (C) 2015-2016  Bhuvan Molparia
#
# Original code - https://github.com/ctokheim/PrimerSeq/blob/master/gtf.py
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

"""
The GTF Format

seqname - name of the chromosome or scaffold; chromosome names can be given with
          or without the 'chr' prefix. Important note: the seqname must be one
          used within Ensembl, i.e. a standard chromosome name or an Ensembl
          identifier such as a scaffold ID, without any additional content such
          as species or assembly. See the example GFF output below.
source  - name of the program that generated this feature, or the data source
          (database or project name)
feature - feature type name, e.g. Gene, Variation, Similarity
start   - Start position of the feature, with sequence numbering starting at 1.
end     - End position of the feature, with sequence numbering starting at 1.
score   - A floating point value.
strand  - defined as + (forward) or - (reverse).
frame   - One of '0', '1' or '2'. '0' indicates that the first base of the
          feature is the first base of a codon, '1' that the second base is the
          first base of a codon, and so on..

attributes - Another dictionary with the attributes as KEYS
"""

import re, argparse
from itertools import tee
import functools
import sys

class GtfData(object):
    """
    Separates out gtf parsing from iterating over records.
    """

    class Attribute(object):
        def __init__(self,attr_line,ftype):
            self.atl = attr_line
            self.ftp = ftype
            self.att = self.parse_atl(ftype)

        def parse_atl(self,ftype):

            if ftype == 'gtf':
                try:
                    # convert attrs to dict
                    attributes = dict(
                        map(lambda x: re.split('\s+', x.replace('"', '')),
                            re.split('\s*;\s*', self.atl.strip().strip(';'))))
                except ValueError:
                    print(self)
                    print('Error: Badly formatted attributes')
                    sys.exit()
            elif ftype == 'gff':
                try:
                    attributes = dict(
                        map(lambda x: re.split('=', x),
                            re.split('\s*;\s*', self.atl.strip().strip(';'))))
                except ValueError:
                    print(self)
                    print('Error:Badly formatted attributes')
                    sys.exit()

            return attributes

        def __str__(self):

            ftype = self.ftp
            if ftype == 'gff':
                return ('; ').join( map( lambda x:x[0]+'='+x[1],
                        [(key,value) for key,value in self.att.iteritems()] ) )
            elif ftype == 'gtf':
                return ('; ').join( map( lambda x:x[0]+' "'+x[1]+'"',
                    [(key,value) for key,value in self.att.iteritems()] ) )+';'
            else:
                raise TypeError('File type not supported')



    def __init__(self, gtf_line_arr, ftype):

        self.gtf_list = gtf_line_arr
        # These indexes are defined by the GTF spec
        (self.seqname, self.source, self.feature, self.start, self.end,
            self.score, self.strand, self.frame, self.attributes) = gtf_line_arr
        self.gtf_list = [self.seqname, self.source, self.feature, self.start,
                 self.end, self.score, self.strand, self.frame, self.attributes]
        self.attr_object = GtfData.Attribute(self.attributes,ftype)
        self.attributes = self.attr_object.att
        self.start, self.end = int(self.start) , int(self.end)

        try:
            self.score = float(self.score)
        except ValueError:
            self.score = 0.0

    def __str__(self):

        gtf_list = map(str,[self.seqname, self.source, self.feature, self.start,
               self.end, self.score, self.strand, self.frame, self.attr_object])
        return ('\t').join(gtf_list) + '\n'


class GTF_Parser(object):

    def __init__(self,filepath,ftype):
        self.fin = open(filepath,'r')
        self.ftp = ftype

    def __iter__(self):
        return self

    def __next__(self):
        fin = self.fin
        line = fin.readline()
        if line == '':
            fin.close()
            raise StopIteration
        elif line.startswith('#'):
            return self.next()
        else:
            line = line.replace('\n','').split('\t')
            data = GtfData(line,self.ftp)
            return data


def get_gtf_attr(gtfline,var):

    if 'attributes' in var:
        att_types = var.split(':')[1].split(';')
        return [getattr(gtfline,'attributes')[att_type] for att_type in att_types]
    else:
        return getattr(gtfline,var)


def gtf_compare_wrapper(Vars):
    """compare two lines of a GTF file to see if they are
    correctly sorted as "a" before "b".
    variables = sorting order """

    def gtf_compare(a, b):

        variables=Vars.split(',')
        tmp_list = [a, b]  # proposed sorted order
        try:
            # actual sorted order
            srt_list = sorted(tmp_list,
                     key=lambda x: [get_gtf_attr(x,y) for y in variables] )
        except AttributeError as e:
            print(str(e)+'\n')
            print("Please make sure the attribute/variable you are using to sort"
             "exists. List of legal variables - seqname, source, feature, start,"
             " end, score, strand, frame, attributes")
            sys.exit(1)

        # return flag for whether the two entries were in sorted order
        flag = (tmp_list == srt_list)
        return flag

    return gtf_compare


def is_sorted(iterable, compare):
    """Returns if iterable is sorted given the definition of
    a compare function"""
    a, b = tee(iterable)
    next(b, None)

    return  all(map(compare, a, b))


def is_gtf_sorted(file_name,ftype,variables):
    """Returns Boolean for if gtf is sorted."""
    mygtf_reader = GTF_Parser(file_name,ftype)
    gtf_compare  = gtf_compare_wrapper(variables)

    return is_sorted(mygtf_reader, gtf_compare)


def sort_gtf(file_name, ftype, output, variables):
    gtf_lists = {}
    for gtf_line in GTF_Parser(file_name,ftype):
        if gtf_line.seqname in gtf_lists:
            gtf_lists[gtf_line.seqname].append(gtf_line)
        else:
            gtf_lists[gtf_line.seqname] = [gtf_line]

    variables = variables.split(',')
    for seq in gtf_lists:
        gtf_list = gtf_lists[seq]
        gtf_list.sort(key=lambda x:  [get_gtf_attr(x,y) for y in variables] )

    # write the contents back to a file
    with open(output, 'w') as write_handle:
        for seq in sorted(gtf_lists):
            gtf_list = gtf_lists[seq]
            for gtf_obj in gtf_list:
                write_handle.write(str(gtf_obj))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Either performs proper "
    "sorting of GTF for PrimerSeq or checks if GTF is sorted. For Sorting GTF: "
    "python gtf_parser.py -i GTF_FILE_PATH -o OUTPUT_FILE_PATH -v "
    "VARIABLES_TO_SORT_BY(default: start position), For checking if GTF is "
    "sorted: python gtf_parser.py -c GTF_FILE_PATH -v VARIABLES_TO_SORT_BY")
    parser.add_argument('-i',
                        type=str,
                        default='',
                        dest='gtf',
                        action='store',
                        help='path to gtf file to sort')
    parser.add_argument('-f',
                        type=str,
                        default='gtf',
                        dest='ftype',
                        action='store',
                        help="File type. Valid options are 'gff' or 'gtf', default 'gtf'")
    parser.add_argument('-o',
                        type=str,
                        default='',
                        dest='output',
                        action='store',
                        help='Path name of properly sorted gtf')
    parser.add_argument('-c',
                        type=str,
                        default='',
                        dest='is_sorted',
                        action='store',
                        help='Path to gtf file to check if sorted correctly')
    parser.add_argument('-v',
                        type=str,
                        default='start',
                        dest='sort_vars',
                        action='store',
                        help='Comma separated list of vaiables to sort by, in '
                        'the order that is desired. Attributes to be used should'
                        ' be mentioned after the key word attributes separated '
                        'by a ":" and separated by a semicolon. For example - '
                        'start, source, attributes:gene_id;transcript_id')

    args = parser.parse_args()


    if args.gtf and args.output:

        sort_gtf(args.gtf, args.ftype, args.output, args.sort_vars)

    elif args.is_sorted:

        if is_gtf_sorted(args.is_sorted, args.ftype, args.sort_vars):
            print('{} is correctly sorted'.format(args.is_sorted))
        else:
            print('{} is not correctly sorted.'.format(args.is_sorted))

    else:
        print('You must enter either both the -i and -o options or just the '
              '-c option.')
