from PIL import Image
from PIL import ImageDraw
import numpy as np
from matplotlib import pyplot as plt
import random

def gen_square(map_size,src_size,src_list,trees_list):
    im = Image.new("RGB", (map_size,map_size), "black")
    tile_scale = 0.5

    size_tiles = int(map_size/(src_size*tile_scale))

    empty_image = Image.open("orig_tiles/6.png")

    images = map(lambda i: Image.open("orig_tiles/"+i+".png"), src_list)
    ts = int(src_size*tile_scale)+1
    images = map(lambda i: i.resize((ts,ts), Image.ANTIALIAS), images)

    empty_image = empty_image.resize((ts,ts), Image.ANTIALIAS)

    t_images = map(lambda i: Image.open("orig_tiles/"+i+".png"), trees_list)
    ts = int(src_size*tile_scale)+1
    t_images = map(lambda i: i.resize((ts,ts), Image.ANTIALIAS), t_images)

    for x in range(0, size_tiles):
        for y in range(0, size_tiles):
            if random.random()<0.5:
                im.paste(empty_image,(int(x*src_size*tile_scale),
                                      int(y*src_size*tile_scale)))
            elif random.random()<0.1:
                im.paste(random.choice(t_images),(int(x*src_size*tile_scale),
                                                int(y*src_size*tile_scale)))
            else:
                im.paste(random.choice(images),(int(x*src_size*tile_scale),
                                                int(y*src_size*tile_scale)))

    im.save("out.jpg")

gen_square(16384,1034,["1","2","3","4","5","7","8","9"],["t1","t1","t2","t4","t5"])
