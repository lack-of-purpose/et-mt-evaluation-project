import json
from PIL import Image, ImageDraw
import pathlib
import os
parent_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

### Mapping rectangulars of problematic words on screens ###

sets = [1,2,3,4,5,6,7,8,9,10]
screens = [1,2,3,4,5,6,7,8,9,10]
names = ['participant1', 'participant2', 'participant3', 'participant4', 'participant5', 'participant6', 'participant7', 'participant8']

for name in names:
    for setn in sets:
        for screen in screens:
            rects = parent_folder + r'\mappings\{}\set{}\corrected\fixations\h-processed-fix{}.json'.format(name,setn,screen)
            if not pathlib.Path(rects).is_file():
                continue
            all = open(rects, 'r')
            data = json.load(all)
            img = parent_folder + r'\mappings\{}\set{}\rects\screen{}_rects.bmp'.format(name, setn, screen)
            if not pathlib.Path(img).is_file():
                continue
            print(setn, screen)
            image = Image.open(img)
            draw = ImageDraw.Draw(image)

            for item in data:
                x0, y0 = float(item[0]), float(item[1])
                x1, y1 = float(item[2]), float(item[3])
                points = []
                points.append((x0, y0))
                points.append((x0, y1))
                draw.line(points, fill='green', width=5)
                points = []
                points.append((x0, y0))
                points.append((x1, y0))
                draw.line(points, fill='green', width=5)
                points = []
                points.append((x1, y1))
                points.append((x1, y0))
                draw.line(points, fill='green', width=5)
                points = []
                points.append((x1, y1))
                points.append((x0, y1))
                draw.line(points, fill='green', width=5)
        
            img_mapped = parent_folder + r'\mappings\{}\set{}\rects\h-screen{}_fix.bmp'.format(name, setn, screen)
            image.save(img_mapped)