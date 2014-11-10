import os

files = ['20130608.generic',
         '20130617.generic',
         '20130618.generic',
         '20130619.generic',
         '20130620.generic',
         '20130621.generic',
         '20130622.generic',
         '20130623.generic',]

def run(cmd):
    print(cmd)
    os.system(cmd)

for f in files:
    run("./exicatcher.py "+f+".sfs")
    run("ffmpeg -i "+f+"-%05d.jpg -vf vflip "+f+".mp4")
    run("ffmpeg -i "+f+"-%05d.jpg -vf vflip "+f+".ogg")
    run("ffmpeg -i "+f+"-%05d.jpg -vf vflip "+f+".webm")
    run("rm *.jpg")
