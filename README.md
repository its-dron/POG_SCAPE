# POG SCAPE
Tools for collecting pogs

Works thanks to the generousity of https://twitchemotes.com/. See https://twitchemotes.com/apidocs for more details.

## Requirements
[lox](https://lox.readthedocs.io/) for multithreading the downloader.

[tqdm](https://github.com/tqdm/tqdm) for progress bars

## Usage

### Downloading
`python scrape_channel_ids.py` to generate a file containing all channels documented by https://twitchemotes.com/.

`python emote_downloader.py` to start downloading the emotes. 

### Prep for network usage
`python im_prep` will clean up the data to be RGB and 128x128, ready for use in your AI of choice.
