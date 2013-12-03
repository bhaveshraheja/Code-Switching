"""
Note:
A lot of this code is copied/borrowed/inspired by Constantine's work on the same subject available at https://github.com/ConstantineLignos/Codeswitchador/blob/master/wordlist.py

Consequently, the license & copyright information for the same follows
"""

# Copyright (c) 2012, Constantine Lignos
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""
Creates the wordlist
"""
import argparse
from collections import Counter
from string import punctuation
import codecs
import sys

PUNC = set(punctuation)
BINARY = ['\x00','\x03','\x19']

def _get_tokens(infile):
    for line in infile:
        for token in filter(lambda x: not(x in BINARY),line).split():
            if _good_token(token):
                yield _remove_punctuation(token.decode('utf-8')).lower()

def _remove_punctuation(token):
    return str(filter(lambda x: x not in PUNC, token))


def _good_token(token):
    return not(token.isdigit())


def make_counter(infile):
    return Counter(_get_tokens(infile))

def load_counts(infile):
    counts = Counter()
    for line in infile:
        word,count = line.split("\t")
        counts[word] = int(count)

    return counts

def output_counts(counts, outfile):
    for word,count in counts:
        print >> outfile, u"{0}\t{1}".format(word,count)

def main():
    """Create a wordlist from a data file"""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('infile',nargs='?', help='input file in UTF-8 format, or omit for stdin')
    parser.add_argument('outfile',nargs='?', help='output file to which counts need to be printed')
    args = parser.parse_args()

    infile = (codecs.open(args.infile, 'Ur','utf_8','ignore') if args.infile else
                codecs.getreader('utf-8')(sys.stdin))
    outfile = (open(args.outfile,'wb') if args.outfile else
                codecs.getwriter('utf-8')(sys.stdout))
    #infile = open(args.file, 'rb')
    counts = make_counter(infile)

    output_counts(counts.most_common(),outfile)

if __name__ == "__main__":
    main()

