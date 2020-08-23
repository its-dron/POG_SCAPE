import glob
import os
from PIL import Image
from tqdm import tqdm
import argparse

'''
Clean up output of emote_downloader and resize to 128x128 for stylegan.
'''


def main(input_root_dir, output_folder, output_size):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    im_list = glob.glob(os.path.join(input_root_dir, '**/*.png'), recursive=True)
    for im_path in tqdm(im_list, total=len(im_list)):
        emote_name = os.path.basename(im_path)
        output_path = os.path.join(output_folder, emote_name)

        im = Image.open(im_path)
        if im.mode == 'P' and 'transparency' in im.info:
            # Handle palette images that have transparency
            im = im.convert("RGBA")
        im = im.convert("RGB")
        im = im.resize((output_size, output_size), Image.LANCZOS)
        im.save(output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_root_dir', type=str, default='emotes', help='Root folder of emote_downloader output.')
    parser.add_argument('--output_dir', type=str, default='emotes_128_rgb', help='Folder to save outputs to')
    parser.add_argument('--output_size', type=int, default=128, help='Resize images to this')

    args = parser.parse_args()
    main(args.input_root_dir, args.output_dir, args.output_size)
