#!/usr/bin/python3

"""Convert a CSV file to TPC using specified columns for coordinates"""

# CSV files are good for tabular data.  TPC is meant for storing
# tabular data plus metadata and distinguished, named sets of rows
# (tags).  This utility converts a CSV and allows some metadata fields
# to be set.  In most practical situations, the resulting TPC file
# would receive additional post-processing to add tag information, if
# needed.

import sys
import argparse
import re

import tpc
import csv

parser = argparse.ArgumentParser(description='Convert CSV to TPC')
parser.add_argument('input',help='Input filename (CSV)')
parser.add_argument('-o','--output',help='Output filename (TPC)')
parser.add_argument('-z','--compress',help='Force compression (default: off for stdout, based on filename otherwise)',action='store_true')
parser.add_argument('-f','--fields',nargs='+',help='Names of CSV columns (default: use row 1 entries)')
parser.add_argument('-v','--vector-components',nargs='+',help='Names of columns that give vector components (default: Field names of the form v%d)')
parser.add_argument('--description',help='Set description text in output metadata')
parser.add_argument('--space',help='Set space text in output metadata')
parser.add_argument('--keep-comments',help='Set space text in output metadata',action='store_true')
parser.add_argument('-d','--delimiter',help='Field delimiter of input file',default=',')
parser.add_argument('--allow-missing',help='Allow missing columns',action='store_true')
parser.add_argument('-u','--uuid',help='Apply a random UUID',action='store_true')
parser.add_argument('-t','--timestamp',help='Apply a timestamp',action='store_true')
parser.add_argument('--clobber',help='Overwrite existing file',action='store_true')

args = parser.parse_args()

if args.compress and not args.output:
    sys.stderr.write('ERROR: Gzip compression selected, but not supported for STDOUT output.  Use -o/--output to specify a filename instead.\n')
    sys.exit(1)

if args.vector_components:
    is_component = lambda x:(x in args.vector_components)
else:
    is_component = lambda x:re.match('v[0-9]+',f)

def coerce(x):
    try:
        return int(x)
    except ValueError:
        pass

    try:
        return float(x)
    except ValueError:
        pass

    return x

    
with open(args.input) as csvfile:
    reader = csv.DictReader((line for line in csvfile if not line.startswith('#')),fieldnames=args.fields,delimiter=args.delimiter)
    vfields = []
    afields = []
    for f in reader.fieldnames:
        if is_component(f):
            vfields.append(f)
        else:
            afields.append(f)
    if not args.vector_components:
        vfields.sort()
    d = len(vfields)
    T = tpc.TPC(dimension=d)
    for r in reader:
        if None in r.values() and not args.allow_missing:
            m = [ f for f in reader.fieldnames if r[f] == None ]
            spec = ''
            if len(m) == len(reader.fieldnames)-1:
                spec = '.  Suspect wrong delimiter or malformed file.'
            raise ValueError('Fields [%s] missing on input line %d' % (','.join(m),reader.line_num) + spec)
        v = [float(r[k]) for k in vfields]
        a = {k:coerce(r[k]) for k in afields}
        T.points.append(tpc.TaggedPoint(v,a,[]))

if args.keep_comments:
    comments=[]
    with open(args.input,mode='rt',encoding='utf-8') as csvfile:
        for line in csvfile:
            if not line.startswith('#'):
                continue
            comments.append(line[1:].strip())
    T.metadata['csv_comments'] = '\n'.join(comments)

if args.description:
    T.metadata['description'] = args.description
if args.space:
    T.metadata['description'] = args.space
if args.uuid:
    T.set_uuid()
if args.timestamp:
    T.set_timestamp()

if not args.output:
    # stdout
    T.savefp(sys.stdout)
else:
    # file
    T.zsavefn(args.output,force_compression=args.compress,clobber=args.clobber)
