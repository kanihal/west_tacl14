''''
Creates html files from JSON files

usage: j2h.py [--input_dir INPUT_DIR] [--output_dir OUTPUT_DIR]
        OR
       j2h.py [--input_file INPUT_FILE] [--output_file OUTPUT_FILE]

    Note - Second parameter is optional, By default html files are created @ the input file directory

'''

import os, sys
import json
from glob import glob
from json2html import json2html
import argparse
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s : %(levelname)s ' ': %(module)s : %(message)s',
                    level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input_dir",
                    default=None,
                    help="/path/to/json_files/folder")
parser.add_argument("-id","--output_dir",
                    default=None,
                    help="/path/to/html_files/output/folder")

parser.add_argument("-o","--input_file",
                    default=None,
                    help="/path/to/json_file")

parser.add_argument("-od","--output_file",
                    default=None,
                    help="/path/to/out_html_file")

args = parser.parse_args()

if args.input_dir and os.path.isdir(args.input_dir):
    in_dir = args.input_dir
    if args.output_dir and os.path.isdir(args.output_dir):
        out_dir = args.output_dir
    else:
        out_dir = in_dir

    pattern = os.path.join(in_dir, '*.json')  # json
    for file in glob(pattern):
        with open(file) as data_file:
            in_data = json.load(data_file)
        h = json2html.convert(in_data)
        name = os.path.splitext(os.path.basename(file))[0]
        htmlfile = os.path.join(out_dir, name + '.html')
        with open(htmlfile, 'w') as hfile:
            hfile.write(h)
        logger.info("Success : html file saved @ " + htmlfile)

if args.input_file and os.path.isfile(args.input_file):
    in_file = args.input_file
    if args.output_file:
        out_file = args.output_file
    else:
        name = os.path.splitext(os.path.basename(in_file))[0]
        in_dir = os.path.splitext(os.path.dirname(in_file))[0]
        out_file = os.path.join(in_dir, name + '.html')
    with open(in_file) as data_file:
        in_data = json.load(data_file)
    h = json2html.convert(in_data)
    with open(out_file, 'w') as hfile:
        hfile.write(h)
    logger.info("Success : html file saved @ " + out_file)
