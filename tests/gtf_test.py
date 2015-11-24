""" Tests for the gtf parser """

import sure
import sys
sys.path.insert(0,'..')

from gtf_parser import GTF_Parser

def test_parser():
    
    test_file = 'test.gtf'
    gtf_p_obj = GTF_Parser(test_file)

    for i in gtf_p_obj:
        gtf_data = i
        break

    gtf_data.should.have.property("seqname").being.equal("chr1")
    gtf_data.should.have.property("source").being.equal("hg38_rmsk")
    gtf_data.should.have.property("feature").being.equal("exon")
    gtf_data.should.have.property("start").being.equal(67108754)
    gtf_data.should.have.property("end").being.equal(67109046)
    gtf_data.should.have.property("score").being.equal("1892.000000")
    gtf_data.should.have.property("strand").being.equal("+")
    gtf_data.should.have.property("frame").being.equal(".")
    gtf_data.should.have.property("attribute")

    gtf_data.attribute.should.have.key("gene_id").being.equal("L1P5")
    gtf_data.attribute.should.have.key("transcript_id").being.equal("L1P5")

