from argparse import ArgumentParser
import requests


def download_file_from_www(url, destination):
    session = requests.Session()

    response = session.get(url, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'confirm': token }
        response = session.get(url, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-s', '--src', dest='source_url', type=str, required=True, help='Take URL.')
    parser.add_argument('-d', '--dst', dest='destination_file', type=str, required=True,
                        help='Destination file on your drive.')
    args = parser.parse_args()
    file_id = args.source_url
    destination = args.destination_file
    download_file_from_www(file_id, destination)
