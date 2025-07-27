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
IMAGE_FULL_SIZE = (1280, 1280)
IMAGE_FINAL_SIZE = (128, 96)
IMAGE_BACKGROUND = (0,0,0,0)
IMAGE_PIXELSIZE = 10

COLOR_LOOKUP = {
    "Airlock": (140,140,0,255),
    "AirlockCaptain": (140,140,0,255),
    "AirlockCaptainLocked": (140,140,0,255),
    "AirlockCargo": (140,140,0,255),
    "AirlockCargoGlass": (140,140,0,255),
    "AirlockCommand": (140,140,0,255),
    "AirlockCommandGlass": (140,140,0,255),
    "AirlockEngineering": (140,140,0,255),
    "AirlockExternal": (140,140,0,255),
    "AirlockExternalGlass": (140,140,0,255),
    "AirlockExternalGlassShuttleArrivals": (140,140,0,255),
    "AirlockGlass": (140,140,0,255),
    "AirlockGlassShuttle": (140,140,0,255),
    "AirlockHatch": (140,140,0,255),
    "AirlockMaint": (140,140,0,255),
    "AirlockMercenary": (140,140,0,255),
    "AirlockMercenaryGlass": (140,140,0,255),
    "AirlockMedical": (140,140,0,255),
    "AirlockMedicalGlass": (140,140,0,255),
    "AirlockScience": (140,140,0,255),
    "AirlockScienceGlass": (140,140,0,255),
    "AirlockShuttle": (140,140,0,255),
    "AirlockShuttleSyndicate": (140,140,0,255),
    "AirlockShuttleNfsdLocked": (140,140,0,255),
    "AirlockNfsdLocked": (140,140,0,255),
    "AirlockNfsdGlassLocked": (140,140,0,255),
    "AirlockExternalGlassNfsdLocked": (140,140,0,255),
    "Grille": (80,80,80,255),
    "GrilleDiagonal": (80,80,80,255),
    "ReinforcedWindow": (0,100,255,255),
    "ReinforcedWindowDiagonal": (0,100,255,255),
    "WallReinforced": (10,10,10,255),
    "WallReinforcedDiagonal": (15,15,15,255),
    "WallSolid": (20,20,20,255),
    "WallPlastitanium": (40,30,40,255),
    "WallPlastitaniumDiagonal": (40,30,40,255),
    "Window":(0,200,255,255),
    "WindowDirectional":(0,200,255,255),
    "WindowReinforcedDirectional":(0,128,255,255),
    "ReinforcedUraniumWindow":(0,128,0,128),
    "ReinforcedPlasmaWindow":(128,0,128,255),
    "PlasmaReinforcedWindowDirectional":(128,0,128,255),
    "PlasmaReinforcedWindow":(128,0,128,255),
    "PlasmaWindowDirectional":(128,0,128,255),
    "PlasmaWindow":(128,0,128,255),
    "PlastitaniumWindow":(128,0,128,128),
    "PlastitaniumWindowDiagonal":(128,0,128,128),
    "WeaponTurretCyrexa": (255,0,0,255),
    "WeaponTurretM25": (255,255,255,255),
    "WeaponTurretTarnyxReload": (200,0,0,255),
    "ComputerGunneryConsole": (0,128,64,128),
    "ComputerIFF": (0,128,128,128),
    "ComputerShuttle": (64,128,64,128),
    "ComputerRadar": (64,128,64,128),
    "ComputerCriminalRecords": (128,128,0,128),
    "ComputerPowerMonitoring": (128,128,0,128),
    "Catwalk": (128,128,128,64),
    }


parser = argparse.ArgumentParser("map-yaml-to-image")
parser.add_argument('-i', '--input', help="Input file to parse", required=True)
parser.add_argument('-o', '--output', help="Output file destination", required=True)
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
    components = readin['entities'][0]['entities'][0]['components']
    # Get the tranform of the grid itself
    #grid_transform= chunk_info['pos']
    # Get the BASE64 encoded tile layout
    for comp in components:
        if comp['type'] == "MapGrid":
            chunk_info = comp['chunks']
            for chunk in chunk_info:
                grid_layout_enc = chunk_info[chunk]['tiles']
                grid_layout_dec = base64.b64decode(grid_layout_enc)
                print("Number of values in grid " + str(chunk) + " is: "+ str(len(grid_layout_dec)))



    print('Starting Image Generator')
    new_image = Image.new('RGBA', IMAGE_FULL_SIZE, color=IMAGE_BACKGROUND)
    new_image_data = new_image.load()
    new_image_draw = ImageDraw.Draw(new_image)

    min_x = 1024
    min_y = 1024
    max_x = -1024
    max_y = -1024

    for entity in readin['entities'][1:]:
        item_name = entity['proto']

        for subentity in entity['entities']:
            item_comps = subentity['components'][0]
            if ('pos' in item_comps):
                pos = item_comps['pos']
                pos_tup = tuple(map(float, pos.split(',')))
                if (item_name in COLOR_LOOKUP):
                    print("Drawing " + item_name + " at " + str(pos_tup))
                    draw_pos_tup = ((int(pos_tup[0]*IMAGE_PIXELSIZE)+IMAGE_FULL_SIZE[0]/2), (int(pos_tup[1]*IMAGE_PIXELSIZE+IMAGE_FULL_SIZE[1]/2)))

                    min_x = draw_pos_tup[0] if (draw_pos_tup[0] < min_x) else min_x
                    min_y = draw_pos_tup[1] if (draw_pos_tup[1] < min_y) else min_y
                    max_x = draw_pos_tup[0] if (draw_pos_tup[0] > max_x) else max_x
                    max_y = draw_pos_tup[1] if (draw_pos_tup[1] > max_y) else max_y

                    new_image_draw.rectangle((draw_pos_tup[0]-IMAGE_PIXELSIZE / 2, draw_pos_tup[1]-IMAGE_PIXELSIZE / 2,draw_pos_tup[0]+IMAGE_PIXELSIZE/2,draw_pos_tup[1]+IMAGE_PIXELSIZE/2), fill=COLOR_LOOKUP[item_name])
                    #new_image_data[int(pos_tup[0]*2)+500, int(pos_tup[1]*2)+500] = COLOR_LOOKUP[item_name]

    crop_box = new_image.getbbox()
    cropped = new_image.crop(crop_box)
    cropped.thumbnail(IMAGE_FINAL_SIZE, Image.Resampling.LANCZOS)
    crop_box = cropped.getbbox()

    final_image = Image.new('RGBA', IMAGE_FINAL_SIZE, color=IMAGE_BACKGROUND)
    off_box = (int((IMAGE_FINAL_SIZE[0]- crop_box[2])/2), int((IMAGE_FINAL_SIZE[1] - crop_box[3])/2))
    final_image.paste(cropped, off_box)
    final_image.save(args.output, format="png")


