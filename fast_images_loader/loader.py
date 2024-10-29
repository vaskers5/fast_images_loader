import asyncio
import os
import aiohttp
from tqdm.asyncio import tqdm
from loguru import logger
import argparse

try:
    get_ipython
    import nest_asyncio
    nest_asyncio.apply()
except NameError:
    pass

class PhotoLoader:
    def __init__(self):
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
    def __init__(self, batch_size=10):
        self.batch_size = batch_size

    async def _load_photos_from_bucket(self, session, photo_urls, photo_paths, data_folder: str) -> None:
        basket = PhotoLoader()
        tasks = [basket.request(session, photo_url, photo_path) for photo_url, photo_path in zip(photo_urls, photo_paths)]
        await asyncio.gather(*tasks)

    def load_photos_to_folder(self, photo_urls: list[str], photo_paths: list[str], data_folder: str) -> list[object]:
        os.makedirs(data_folder, exist_ok=True)
        logger.info(f"Loading {len(photo_paths)} photos in batches of {self.batch_size}")
        async def run_batches():
            async with aiohttp.ClientSession() as session:
                for i in tqdm(range(0, len(photo_urls), self.batch_size), desc="Downloading photos"):
                    batch_urls = photo_urls[i:i + self.batch_size]
                    batch_paths = photo_paths[i:i + self.batch_size]
                    await self._load_photos_from_bucket(session, batch_urls, batch_paths, data_folder)
        asyncio.run(run_batches())


def main():
    parser = argparse.ArgumentParser(description="Load photos from URLs to a specified folder.")
    parser.add_argument("photo_urls", type=str, nargs='+', help="List of photo URLs to download.")
    parser.add_argument("data_folder", type=str, help="Folder to save downloaded photos.")
    parser.add_argument("--batch_size", type=int, default=10, help="Number of photos to download in each batch. Default is 10.")
    args = parser.parse_args()

    photo_urls = args.photo_urls
    data_folder = args.data_folder
    batch_size = args.batch_size
    photo_paths = [os.path.join(data_folder, f"photo_{i}.jpg") for i in range(len(photo_urls))]

    client_basket = FastImagesLoader(batch_size=batch_size)
    client_basket.load_photos_to_folder(photo_urls, photo_paths, data_folder)


if __name__ == "__main__":
    main()
