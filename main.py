#!/usr/bin/env python3
import sys
import argparse
import yaml
import base64

#from src.Tiles import TilesRefsManager
#from src.UI import Window
#from src.Config import GlobalSettings

from PIL import Image, ImageDraw, ImageFont

# Constants
IMAGE_FULL_SIZE = (1000, 1000)
IMAGE_FINAL_SIZE = (128, 96)
IMAGE_BACKGROUND = (0,0,0,0)

COLOR_LOOKUP = {
    "AirlockCargoGlass": (140,140,0,255),
    "AirlockGlassShuttle": (140,140,0,255),
    "Grille": (80,80,80,255),
    "GrilleDiagonal": (80,80,80,255),
    "ReinforcedWindow": (0,100,255,255),
    "ReinforcedWindowDiagonal": (0,100,255,255),
    "WallReinforced": (10,10,10,255),
    "WallReinforcedDiagonal": (15,15,15,255),
    "WallSolid": (20,20,20,255)
    }


parser = argparse.ArgumentParser("map-yaml-to-image")
parser.add_argument('-i', '--input', help="Input file to parse", required=True)
args = parser.parse_args()

def unknown(loader, suffix, node):
    if isinstance(node, yaml.ScalarNode):
        constructor = loader.__class__.construct_scalar
    elif isinstance(node, yaml.SequenceNode):
        constructor = loader.__class__.construct_sequence
    elif isinstance(node, yaml.MappingNode):
        constructor = loader.__class__.construct_mapping
    data = constructor(loader, node)
    return data

yaml.add_multi_constructor('!', unknown, Loader=yaml.SafeLoader)


print("Accessing " + str(args.input))

with open(args.input, 'r') as mapfile:
    readin = yaml.safe_load(mapfile)

    tile_map = readin['tilemap']
    chunk_info = readin['entities'][0]['entities'][0]['components']
    # Get the tranform of the grid itself
    grid_transform= chunk_info[1]['pos']
    # Get the BASE64 encoded tile layout
    grid_layout_enc = chunk_info[2]['chunks']['0,0']['tiles']
    grid_layout_dec = base64.b64decode(grid_layout_enc)



    print('Starting Image Generator')
    new_image = Image.new('RGBA', IMAGE_FULL_SIZE, color=IMAGE_BACKGROUND)
    new_image_data = new_image.load()


    for entity in readin['entities'][1:]:
        item_name = entity['proto']

        for subentity in entity['entities']:
            item_comps = subentity['components'][0]
            if ('pos' in item_comps):
                pos = item_comps['pos']
                pos_tup = tuple(map(float, pos.split(',')))
                if (item_name in COLOR_LOOKUP):
                    print("Drawing " + item_name + " at " + str(pos_tup))
                    new_image_data[int(pos_tup[0]*2)+500, int(pos_tup[1]*2)+500] = COLOR_LOOKUP[item_name]


    new_image.save("output.png", format="png")


