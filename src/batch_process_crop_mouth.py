from glob import glob
import re
from crop_mouth import crop_mouth_region


for path in glob('data/frame data/*.png'):
    output_filename = re.findall(r'(\w+).png$', path)[0]
    crop_mouth_region(path, f'data/output/{output_filename}_cropped.png')
