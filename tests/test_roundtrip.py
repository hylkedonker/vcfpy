# -*- coding: utf-8 -*-
"""Roundtrip-test: read in VCF file and write out again
"""

import os

import pytest

from vcfpy import reader
from vcfpy import writer

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@bihealth.de>'


def test_vcf_roundtrip(tmpdir_factory):
    # open reader with VCF file to read from
    in_path = os.path.join(os.path.dirname(__file__), 'vcfs/full_vcf43.vcf')
    r = reader.VCFReader.from_path(in_path)
    # open temporary file and setup the VCFWriter with header info from reader
    out_path = tmpdir_factory.mktemp('write_header').join('out.vcf')
    w = writer.VCFWriter.from_path(r.header, r.samples, out_path)
    # copy records to output file
    for rec in r:
        w.write_record(rec)
    r.close()
    w.close()
    # compare actual result with expected
    RESULT = out_path.read()
    EXPECTED = open(in_path, 'rt').read()
    assert EXPECTED == RESULT