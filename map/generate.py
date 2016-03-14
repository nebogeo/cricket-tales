from PIL import Image
from PIL import ImageDraw
import numpy as np
from matplotlib import pyplot as plt
import random

def gen_square(map_size,src_size,src_list,trees_list):
    im = Image.new("RGB", (map_size,map_size), "black")

    size_tiles = map_size/src_size
    print(size_tiles)
    tile_scale = (map_size/size_tiles)/float(src_size)
    print(tile_scale)


    empty_image = Image.open("map/orig_tiles/6.png")

    images = map(lambda i: Image.open("map/orig_tiles/"+i+".png"), src_list)
    ts = int(src_size*tile_scale)+1
    images = map(lambda i: i.resize((ts,ts), Image.ANTIALIAS), images)
    empty_image = empty_image.resize((ts,ts), Image.ANTIALIAS)
    t_images = map(lambda i: Image.open("map/orig_tiles/"+i+".png"), trees_list)
    ts = int(src_size*tile_scale)+1
    t_images = map(lambda i: i.resize((ts,ts), Image.ANTIALIAS), t_images)

    empties = []

    for x in range(0, size_tiles):
        for y in range(0, size_tiles):
            if random.random()<0.5:
                px = int(x*src_size*tile_scale)
                py = int(y*src_size*tile_scale)
                im.paste(empty_image,(px,py))
                empties.append([(px/float(map_size)-0.5)*360.0,
                                (py/float(map_size)-0.5)*180.0,
                                ((px+src_size*tile_scale)/float(map_size)-0.5)*360.0,
                                ((py+src_size*tile_scale)/float(map_size)-0.5)*180.0])
            elif random.random()<0.1:
                im.paste(random.choice(t_images),(int(x*src_size*tile_scale),
                                                int(y*src_size*tile_scale)))
            else:
                im.paste(random.choice(images),(int(x*src_size*tile_scale),
                                                int(y*src_size*tile_scale)))

    im.save("map/out.jpg")
    return empties
