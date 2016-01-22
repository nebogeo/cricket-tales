#!/usr/bin/env python
# Copyright (C) 2016 Foam Kernow
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PIL import Image
from PIL import ImageDraw
import numpy as np
from matplotlib import pyplot as plt

import sys
import os

# return the topmost pixel position in y
def find_top(im):
    pixels=np.array(im)
    for y in range(0,im.size[1]):
        for x in range(0,im.size[0]):
            if pixels[y,x][3]>10:
                print pixels[y,x]
                return y
    return -1

def num_to_letter(n):
    if n==1: return "a"
    if n==2: return "b"
    if n==3: return "c"
    if n==4: return "d"
    if n==5: return "e"
    if n==6: return "f"
    if n==7: return "g"
    if n==8: return "h"
    return "?"

def short_filename(top,middle,bottom,colour):
    return num_to_letter(top)+\
        num_to_letter(middle)+\
        num_to_letter(bottom)+\
        num_to_letter(colour)+".png"

top_pos = {}

def get_top_pos(fn):
    global top_pos
    if fn not in top_pos:
        im = Image.open("resized/q/"+fn)
        top_pos[fn]=find_top(im)
    return top_pos[fn]

def build_filenames():
    out = []
    for top in range(1,9):
        for middle in range(1,9):
            for bottom in range(1,9):
                for col_num,colour in enumerate(["blue", "brown", "green", "grey", "orange", "pink", "purple", "yellow"]):
                    tfn = "house "+str(top)+" roof "+colour+".png"
                    mfn = "house "+str(middle)+" middle "+colour+".png"
                    bfn = "house "+str(bottom)+" ground "+colour+".png"
                    out.append([tfn,mfn,bfn,short_filename(top,middle,bottom,col_num+1)])
    return out

def alpha_composite(src, dst):
    '''
    Return the alpha composite of src and dst.

    Parameters:
    src -- PIL RGBA Image object
    dst -- PIL RGBA Image object

    The algorithm comes from http://en.wikipedia.org/wiki/Alpha_compositing
    '''
    # http://stackoverflow.com/a/3375291/190597
    # http://stackoverflow.com/a/9166671/190597
    src = np.asarray(src)
    dst = np.asarray(dst)
    out = np.empty(src.shape, dtype = 'float')
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    src_a = src[alpha]/255.0
    dst_a = dst[alpha]/255.0
    out[alpha] = src_a+dst_a*(1-src_a)
    old_setting = np.seterr(invalid = 'ignore')
    out[rgb] = (src[rgb]*src_a + dst[rgb]*dst_a*(1-src_a))/out[alpha]
    np.seterr(**old_setting)
    out[alpha] *= 255
    np.clip(out,0,255)
    # astype('uint8') maps np.nan (and np.inf) to 0
    out = out.astype('uint8')
    out = Image.fromarray(out, 'RGBA')
    return out

tweaks = {"house 1 middle":(0,-5),
          "house 4 middle":(0,-3),
          "house 8 middle":(0,-8)}


tweaks2 = {"house 5 ground":(5,0),
           "house 8 ground":(8,0),
           "house 5 middle":(-5,0),
           "house 3 ground":(5,0),
           "house 3 middle":(5,0),
           "house 8 middle":(3,0),
           "house 6 ground":(3,0),
           "house 7 roof":(-5,-3),
           "house 8 roof":(3,-3),
           "house 1 roof":(0,-3)}

def get_tweak(fn):
    global tweaks
    for v in tweaks.keys():
        if fn.startswith(v):
            return tweaks[v]
    else:
        return (0,0)

def get_tweak2(fn):
    global tweaks2
    for v in tweaks2.keys():
        if fn.startswith(v):
            return tweaks2[v]
    else:
        return (0,0)

# run over all houses and paste them in the big images
def batch_run(filenames):
    for house in filenames:
        top = Image.open("resized/q/"+house[0])
        mid = Image.open("resized/q/"+house[1])
        bot = Image.open("resized/q/"+house[2])

        if house[0].startswith("house 1 roof"):
            print ("rotating")
            top=top.rotate(1)

        width = top.size[0]
        height = top.size[1]
        mid_pos = get_top_pos(house[2])
        top_pos = get_top_pos(house[1])

        t = Image.new("RGBA", (width,height*3), (0,0,0,0))
        m = Image.new("RGBA", (width,height*3), (0,0,0,0))
        b = Image.new("RGBA", (width,height*3), (0,0,0,0))

        btweak = get_tweak(house[2])
        mtweak = get_tweak(house[1])
        ttweak = get_tweak(house[0])

        btweak2 = get_tweak2(house[2])
        mtweak2 = get_tweak2(house[1])
        ttweak2 = get_tweak2(house[0])

        print btweak2

        base_pos = btweak[1]+height*2
        offset = 155

        mp = mtweak[1]+(base_pos-height)+mid_pos+offset

        b.paste(bot,(btweak[0]+btweak2[0],btweak2[1]+base_pos))
        m.paste(mid,(mtweak[0]+mtweak2[0],mtweak2[1]+mp))
        t.paste(top,(ttweak[0]+ttweak2[0],ttweak2[1]+ttweak[1]+(mp-height)+top_pos+offset))

        ret = alpha_composite(m,b)
        ret = alpha_composite(t,ret)

        print(house[3])

        w, h = ret.size
        ret = ret.crop((0,height,w,h))
        ret.save("out/"+house[3])


print batch_run(build_filenames())

# are we the script that's being run?
# if __name__ == "__main__":
#     if sys.argv[1]=="batch":
#         batch_run(generate_quipu_list())
#     if sys.argv[1]=="sliced_entropy":
#         global_entropy_sliced(generate_quipu_list())
#     if sys.argv[1]=="global_entropy":
#         global_entropy_comp(generate_quipu_list())
#     if sys.argv[1]=="pairwise_entropy":
#         pairwise_entropy_comp(generate_quipu_list())
#     if sys.argv[1]=="json":
#         json_save(generate_quipu_list())
#     else:
#         run(sys.argv[1])
