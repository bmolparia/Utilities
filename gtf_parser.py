"""
This is a small parser object that will return a neat dictionary for every line in a GTF file with the following KEYS

seqname - name of the chromosome or scaffold; chromosome names can be given with or without the 'chr' prefix. Important note: the seqname must be one used within Ensembl, i.e. a standard chromosome name or an Ensembl identifier such as a
          scaffold ID, without any additional content such as species or assembly. See the example GFF output below.
source  - name of the program that generated this feature, or the data source (database or project name)
feature - feature type name, e.g. Gene, Variation, Similarity
start   - Start position of the feature, with sequence numbering starting at 1.
end     - End position of the feature, with sequence numbering starting at 1.
score   - A floating point value.
strand  - defined as + (forward) or - (reverse).
frame   - One of '0', '1' or '2'. '0' indicates that the first base of the feature is the first base of a codon, '1' that the second base is the first base of a codon, and so on..

attributes - Another dictionary with the attributes as KEYS
"""                                    

## transcribed_unprocessed_pseudogene gene    11869   14409   .   +   .   gene_id "ENSG00000223972"; gene_name "DDX11L1"; gene_source "havana"; gene_biotype "transcribed_unprocessed_pseudogene"; 
##  processed_transcript   transcript  11869   14409   .   +   .   gene_id "ENSG00000223972"; transcript_id "ENST00000456328"; gene_name "DDX11L1"; gene_sourc e "havana"; gene_biotype "transcribed_unprocessed_pseudogene"; transcript_name "DDX11L1-002"; transcript_source "havana";

class GTF_Parser(object):

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
        
        data = {}
        
        data['seqname'] = line[0]
        data['source']  = line[1]
        data['feature'] = line[2]
        data['start']   = int(line[3])
        data['end']     = int(line[4])
        data['score']   = float(line[5])
        data['strand']  = line[6]
        data['frame']   = line[7]

        attrsTm = line[8]
        attrsTm = attrsTm.split('; ')

        attrs = {}
        for i in attrsTm:
            i = i.replace('"','')
            
            if i != '':
                i = i.split(' ')
                attr_name = i[0]
                attr_val  = i[1]

                attrs[attr_name] = attr_val
        
        data['attributes'] = attrs

        return data

if __name__ == "__main__":

    gtf_file = 'test.gtf'
    for data in GTF_Parser(gtf_file):
        #pass
        print data
    
    
