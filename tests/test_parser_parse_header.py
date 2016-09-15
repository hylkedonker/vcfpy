# -*- coding: utf-8 -*-
"""Test parsing of full VCF header
"""

import io
import textwrap

import pytest

from vcfpy import parser

MEDIUM_HEADER = r"""
##fileformat=VCFv4.3
##fileDate=20090805
##source=myImputationProgramV3.1
##reference=file:///seq/references/1000GenomesPilot-NCBI36.fasta
##contig=<ID=20,length=62435964,assembly=B36,md5=f126cdf8a6e0c7f379d618ff66beb2da,species="Homo sapiens",taxonomy=x>
##phasing=partial
##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">
##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">
##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">
##FILTER=<ID=q10,Description="Quality below 10">
##FILTER=<ID=s50,Description="Less than 50% of samples have data">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
##FORMAT=<ID=HQ,Number=2,Type=Integer,Description="Haplotype Quality">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	NA00001	NA00002	NA00003
""".lstrip()

@pytest.fixture(scope='function')
def medium_header():
    return io.StringIO(MEDIUM_HEADER)


def test_parse_header(medium_header):
    p = parser.VCFParser(stream=medium_header, path='<builtin>')
    header = p.parse_header()
    assert header.lines
    assert len(header.lines) == 18
    EXPECTED = "VCFHeaderLine('fileformat', 'VCFv4.3')"
    assert str(header.lines[0]) == EXPECTED
    EXPECTED = (
        "VCFFormatHeaderLine('FORMAT', '<ID=HQ,Number=2,Type=Integer,"
        "Description=\"Haplotype Quality\">', OrderedDict([('ID', 'HQ'), "
        "('Number', 2), ('Type', 'Integer'), ('Description', "
        "'Haplotype Quality')]))")
    assert str(header.lines[-1]) == EXPECTED
    assert header.samples.names == ['NA00001', 'NA00002', 'NA00003']
