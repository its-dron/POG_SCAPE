import requests
import json
import argparse

BASE_URL = "https://api.twitchemotes.com/api/v4/sets?id="

'''
See https://twitchemotes.com/apidocs

Finds channel IDs by searching set ID in ascending order.
Note that this will result in duplicate entries, as multiple set IDs can map to one channel.
Don't ask me why.
'''


def main(output_file, start_id=0):
    with open(output_file, 'a') as f:
        while True:
            print(start_id)
            numbers = ",".join([str(i) for i in range(start_id, start_id + 100)])
            query_url = BASE_URL + numbers

            r = requests.get(query_url)

            if r.status_code != 200:
                print(f"Failed request with status code{r.status_code}")
                print(f"Start id: {start_id}")

            data = json.loads(r.text)

            start_id += 100

            for entry in data:
                channel_id = entry['channel_id']
                name = entry['channel_name']
                f.write(f'{channel_id}\t{name}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_id", type=int, default=0, help="Channel set ID to start at")
    parser.add_argument('--output_file', type=str, default='channels.txt', help='File to write outputs to')

    args = parser.parse_args()
    main(args.output_file, args.start_id)
