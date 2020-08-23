import requests
import urllib.request
import json
import lox
from tqdm import tqdm
import os

BASE_URL = "https://api.twitchemotes.com/api/v4/channels/"
EMOTE_BASE_URL = "https://static-cdn.jtvnw.net/emoticons/v1/"

CHUNK_SIZE = 1000

'''
See https://twitchemotes.com/apidocs

Given a file of [channel_id\tchannel_name] pairs, download all available emotes.
'''


def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()


def download_emotes_for_user(channel_id, channel_name):
    query_url = BASE_URL + channel_id

    output_folder = os.path.join("emotes", channel_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    done_flag = os.path.join(output_folder, "_done")
    if os.path.exists(done_flag):
        return

    r = requests.get(query_url)
    if r.status_code != 200:
        tqdm.write(f"Failed request for {channel_name} with status code {r.status_code}")
        touch(done_flag)
        return

    data = json.loads(r.text)
    for emote in data['emotes']:
        name = emote['code']
        id = emote['id']
        output_path = os.path.join(output_folder, name + ".png")
        if os.path.exists(output_path):
            continue

        image_url = EMOTE_BASE_URL + str(id) + "/4.0"
        try:
            urllib.request.urlretrieve(image_url, output_path)
        except:
            tqdm.write(f"Failed to get {channel_name}'s emote {name} at {image_url}")
    touch(done_flag)
    tqdm.write(f'Downloaded {len(data["emotes"])} emotes for {channel_name}')


@lox.process(40)
def handle_entry(line):
    ch_id, ch_name = line.strip().split('\t')
    download_emotes_for_user(ch_id, ch_name)


def batch_iterator(iterable, batch_size=CHUNK_SIZE):
    length = len(iterable)
    for ndx in range(0, length, batch_size):
        yield iterable[ndx:min(ndx + batch_size, length)]


def main():
    with open('channels.txt', 'r') as f:
        lines = set(f.readlines())  # attempt to dedupe
    pbar = tqdm(total=len(lines))
    for batch in batch_iterator(lines):
        for line in batch:
            handle_entry.scatter(line)
        handle_entry.gather()
        pbar.update(CHUNK_SIZE)


if __name__ == '__main__':
    main()
