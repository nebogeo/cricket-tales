import os
import exicatcher
import datetime
import dbadd

srcdir = "/home/dave/projects/crickets/fakedisk/"

# palm:oil:chaos

print "hello"

def examine_index(path):
    frames = exicatcher.read_index(path)
    print len(frames)    
    last = ""
    f = open(path+".freq","w")
    for i,frame in enumerate(frames):
        t = frame["time"]
        dt = datetime.datetime(t[0],t[1],t[3],t[4],t[5],t[6],t[7])
        tot = 0
        if i!=0:
            delta = dt-last
            secs = delta.total_seconds()
            tot+=secs
            f.write(str(secs)+"\n")

        last = dt         
    tot/=len(frames)
    print 1/tot
    f.close()

def run(cmd):
    print(cmd)
    os.system(cmd)

def run_converter(f):
    f = "media/movies/"+f
    run("avconv -i frames/frame-%05d.jpg -vf vflip -c:v libx264 "+f+".mp4")
    run("avconv -i frames/frame-%05d.jpg -vf vflip "+f+".ogg")
    run("avconv -i frames/frame-%05d.jpg -vf vflip "+f+".webm")

def delete_frames():
    run("rm frames/*.jpg")

def renamer(start,frames):
    if start>0:
        for i in range(0,frames):
            run("mv frames/frame-%05d.jpg frames/frame-%05d.jpg"%(i+start,i))

def chop_video(path,subdir,start,frames):
    sf = os.path.splitext(path)
    moviename = sf[0]+".generic.sfs"
    print("extracting "+moviename+" starting "+str(start))
    exicatcher.extract(moviename, frames, "frames/frame", False)
    renamer(start,len(frames))
    so = os.path.splitext(os.path.basename(path))
    outname = subdir+"/"+so[0]+"-"+str(start)
    print(outname)
    run_converter(outname)
    delete_frames()
    dbadd.add_movie_django("Fred",outname)



def chop_index(duration,fps,path,subdir):
    frames = exicatcher.read_index(path)
    num_frames = len(frames)
    seg_length = int(round(duration*fps))
    num_segs = num_frames/seg_length
    # todo - what to do with the offcuts??
    print("seg length:"+str(seg_length))
    print("num segs:"+str(num_segs))

    for segnum in range(0,num_segs):
        start = segnum*seg_length
        chop_video(path,subdir,start,frames[start:start+seg_length])


def search_videos(path,duration,fps):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            sf = os.path.splitext(filename)
            if sf[1]==".index":
                # todo get subdir from path...
                chop_index(duration,fps,dirpath+"/"+filename,"IP101")
                


search_videos(srcdir,10,10)


