import asyncio
import os

import aiohttp
from tqdm.asyncio import tqdm

from loguru import logger
import nest_asyncio
import argparse

nest_asyncio.apply()

class PhotoLoader:
    def __init__(self, folder):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)
        self.counter = 0

    async def request(self, session, photo_url, photo_path):
        retry_count = 2
        while retry_count >= 0:
            try:
                async with session.get(photo_url, timeout=5) as res:
                    if res.status == 200:
                        with open(photo_path, "wb") as f:
                            f.write(await res.read())
                        return 1
                    return b""
            except Exception as e:
                retry_count -= 1
        return b""


class FastImagesLoader:

    @staticmethod
    async def load_photos_from_bucket(photo_urls, photo_paths, data_folder: str) -> None:
        basket = PhotoLoader(data_folder)
        async with aiohttp.ClientSession() as session:
            tasks = [basket.request(session, photo_url, photo_path) for photo_url, photo_path in zip(photo_urls, photo_paths)]
            for f in tqdm.as_completed(tasks):
                await f

    def get_photos(self, photo_paths: list[tuple[str, str]], data_folder: str) -> list[object]:
        logger.info(f"Loading {len(photo_paths)} photos")
        asyncio.run(self.load_photos_from_bucket(photo_paths, data_folder))


def main():
    parser = argparse.ArgumentParser(description="Load photos from URLs to a specified folder.")
    parser.add_argument("photo_urls", type=str, nargs='+', help="List of photo URLs to download.")
    parser.add_argument("data_folder", type=str, help="Folder to save downloaded photos.")
    args = parser.parse_args()

    photo_urls = args.photo_urls
    data_folder = args.data_folder
    photo_paths = [os.path.join(data_folder, f"photo_{i}.jpg") for i in range(len(photo_urls))]

    client_basket = ClientBasket()
    client_basket.get_photos(photo_paths, photo_urls, data_folder)


if __name__ == "__main__":
    main()
