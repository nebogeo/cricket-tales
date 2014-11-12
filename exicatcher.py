#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
===================================================
exicatcher -- extract JPEGs from icatcher SFS files
===================================================



:Author:
         Richard Everson <R.M.Everson@exeter.ac.uk>
:Date:
         19 January 2013 
:Copyright:
         Copyright (c) Richard Everson, University of Exeter, 2013
:File:
         exicatcher.py
"""

from __future__ import division
from optparse import OptionParser
import sys, os
import struct
import csv


def find_start(data, offset=0):
    """
    Find the index of the start of a JPEG block in data[offset:] by looking for the JFIF string
    and magic numbers. Return -1 if it can't be found.n
    """
    JFIF = 'JFIF\x00'                               # JFIF identification string
    magic = '\xff\xd8'
    start = offset
    while True:
        try:
            start = data.index(JFIF, start)
            if data[start-6:start-4] == magic:
                return start - 6
            else:
                print 'False start at', start
        except ValueError:
            return -1

def extract_no_seek(file, stem):
    """
    Extract JPG blocks from file, writing them to stem-%d.jpg where %d is the
    number of the block in the file.

    This version doesn't know about the byte offsets of frames in the file and
    has to look for magic numbers signifying the start of the each JPEG frame.
    """
    with open(args[0], 'rb') as f:
        data = f.read()
        
    n = 0
    start = find_start(data)
    finished = False
    while not finished:
        end = find_start(data, start+10)               # Start of next one
        if end < 0:
            end = len(data)
            finished = True
        print n, start, end
        with open('%s-%05d.jpg' % (stem, n), 'wb') as f:
            f.write(data[start:end])
        start = end
        n += 1

    
def get_time(data):
    """
    Interpret a Windows SYSTEMTIME structure (16 bytes), returning a tuple of 
    (year, month, day_of_the_week, day, hour, minute, second, millisecond)
    """
    year, = struct.unpack_from('<H', data, offset=0)
    month, = struct.unpack_from('<H', data, offset=2)
    dow, = struct.unpack_from('<H', data, offset=4)
    day, = struct.unpack_from('<H', data, offset=6)   # Day of the month, 1 to 31
    hour, = struct.unpack_from('<H', data, offset=8)
    minute, = struct.unpack_from('<H', data, offset=10)
    second, = struct.unpack_from('<H', data, offset=12)
    millisecond, = struct.unpack_from('<H', data, offset=14)

    return year, month, dow, day, hour, minute, second, millisecond


def read_index(file, verbose=False):
    """
    Read an iCatcher index file and return a list of dictionaries describing the data
    """
    with open(file, 'rb') as f:
        data = f.read()

    header = data[:4]
    if verbose:
        print "Version", [str(b) for b in header]
    
    if (len(data) - 4) % 32 != 0:
        print 'Index file %s not multiple of 32 (+4)!' % file

    print 'There should be ', (len(data)-4)//32, 'frames'
    
    frames = []
    for n in range((len(data)-4)//32):
        start = 32*n + 4
        offset, = struct.unpack_from('<Q', data, offset=start+24)   # 8 bytes
        time = get_time(data[start+4:start+4+16])
        length, = struct.unpack_from('<L', data, offset=start+20)   # 4 bytes
        if verbose:
            print '--------- %d -----------' % n
            print 'Date:', time
            print 'Byte offset: ', offset
            print 'Frame size', length
        frames.append({'time' : time, 'length' : length, 'offset' : offset, 'number' : n})
    return frames
    

def extract(file, frames, stem, verbose, nowrite=False):
    """
    Extract from an iCatcher SFS file the frames listed in the `frames` list.
    Files are written to stem-%d.jpg where %d is the number of the block in
    the file.
    """
    JFIF = 'JFIF\x00'                               # JFIF identification string
    magic = '\xff\xd8'
    header_offset = 4               # Bytes starting the SFS file before video info

    bad = 0
    with open(file, 'rb') as f:
        for frame in frames:
            if verbose:
                print '%d offset %d  length %d' % (frame['number'], frame['offset'], frame['length'])
            f.seek(header_offset+frame['offset'])
            data = f.read(frame['length'])
            if data[:2] != magic or data[6:11] != JFIF:
                print >> sys.stderr, 'Wrong magic number or string for frame %d at offset %d' % (frame['number'], frame['offset'])
                print >> sys.stderr, 'First 11 bytes are', ''.join(['%x' % ord(x) for x in data[:11]])
                bad += 1
                if bad == 10:
                    print >> sys.stderr, 'Giving up after 10 bad frames'
                    return
                continue

            if nowrite:
                continue
            with open('%s-%05d.jpg' % (stem, frame['number']), 'wb') as w:
                w.write(data)
                

def write_csv(sfsfile, stem, frames):
    """
    Write details of the frames in `frames` to `stem`.csv as a CSV file.

    Format is:
    sfsfile, framenumber, year, month, day, hour, minute, second, millisecond, jpeg-name
    """
    with open("%s.csv" % stem, "wb") as f:
        writer = csv.writer(f, dialect=csv.excel)
        writer.writerow(["SFS file", "Frame", "Year", "Month", "Day", "Hour", "Minute", "Second", "Millisecond", "JPEG file"])
        for frame in frames:
            year, month, dow, day, hour, minute, second, millisecond = frame['time']
            row = [sfsfile, 
                   frame['number'],
                   year, month, day, hour, minute, second, millisecond,
                   '%s-%06d.jpg' % (stem, frame['number'])
                   ]
            writer.writerow(row)
    
def xslice(str, N):
    """
    Return a list with the the slice of range(N) corresponding to the slice
    expression in str. Always returns a list even if the slice is a
    single element or empty.
    
    xslice("3", 7) -->  [3]
    xslice(":4", 7) --> [0, 1, 3, 2]
    xslice("4:", 7) --> [4, 5, 6]
    """
    s = eval("x[%s]" % str, {"x": range(N)})
    if type(s) == int:
        s = [s]
    return s
                
     
if __name__ == "__main__":    
    usage = """%prog: extract JPEGs from icatcher SFS files.  The .index file must also be present.
    %prog [options] video.generic.sfs"""
    
    parser = OptionParser(usage=usage)
    
    parser.add_option("-s", "--stem", type="string", dest="stem", 
                      help="stem for output.  Default is the input file name with the .generic.sfs removed")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False)
    parser.add_option("--no-write", dest="nowrite", action="store_true", default=False,
                      help='Do not actually write the frames to disk')
    parser.add_option("--frames", dest="slice", type="string", default=":",
                      help="Python slice expression specifying frame indices")
    (opt, args) = parser.parse_args()
    if len(args) == 0:
        parser.print_usage()
        sys.exit(1)
        
    if not opt.stem:
        opt.stem = os.path.splitext(args[0])[0]

    root, ext = os.path.splitext(args[0])
    root, ext = os.path.splitext(root)
    
    frames = read_index(root+".index", opt.verbose)
    xframes = [frames[i] for i in xslice(opt.slice, len(frames))]
    extract(file, xframes, opt.stem, opt.verbose, opt.nowrite)
    write_csv(os.path.basename(args[0]), opt.stem, xframes)
