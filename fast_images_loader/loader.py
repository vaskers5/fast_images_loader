import asyncio
import os
import aiohttp
import aiofiles
import cv2
from tqdm.asyncio import tqdm
from loguru import logger
import argparse
from typing import List, Union, Optional
from pathlib import Path

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
                logger.warning(f"Failed to download image from {photo_url}: {e}")
                retry_count -= 1
        return b""


class VideoLoader:
    def __init__(self):
        self.counter = 0

    async def request(self, session, video_url, video_path):
        retry_count = 2
        while retry_count >= 0:
            try:
                async with session.get(video_url, timeout=30) as res:  # Longer timeout for videos
                    if res.status == 200:
                        async with aiofiles.open(video_path, "wb") as f:
                            async for chunk in res.content.iter_chunked(8192):
                                await f.write(chunk)
                        return 1
                    return 0
            except Exception as e:
                logger.warning(f"Failed to download video from {video_url}: {e}")
                retry_count -= 1
        return 0

    def extract_frames(self, video_path: str, output_folder: str, frame_rate: int = 1) -> List[str]:
        """Extract frames from video at specified frame rate"""
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return []

        os.makedirs(output_folder, exist_ok=True)
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error(f"Could not open video: {video_path}")
            return []

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps / frame_rate) if fps > 0 else 1
        
        frame_paths = []
        frame_count = 0
        saved_frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % frame_interval == 0:
                frame_filename = f"frame_{saved_frame_count:06d}.jpg"
                frame_path = os.path.join(output_folder, frame_filename)
                cv2.imwrite(frame_path, frame)
                frame_paths.append(frame_path)
                saved_frame_count += 1
                
            frame_count += 1

        cap.release()
        logger.info(f"Extracted {saved_frame_count} frames from {video_path}")
        return frame_paths


class FastImagesLoader:
    def __init__(self, batch_size=10):
        self.batch_size = batch_size

    async def _load_photos_from_bucket(self, session, photo_urls, photo_paths, data_folder: str) -> None:
        basket = PhotoLoader()
        tasks = [basket.request(session, photo_url, photo_path) for photo_url, photo_path in zip(photo_urls, photo_paths)]
        await asyncio.gather(*tasks)

    async def _load_videos_from_bucket(self, session, video_urls, video_paths, data_folder: str) -> None:
        basket = VideoLoader()
        tasks = [basket.request(session, video_url, video_path) for video_url, video_path in zip(video_urls, video_paths)]
        await asyncio.gather(*tasks)

    async def load_photos_to_folder_async(self, photo_urls: List[str], photo_paths: List[str], data_folder: str) -> None:
        """Async version of load_photos_to_folder"""
        os.makedirs(data_folder, exist_ok=True)
        logger.info(f"Loading {len(photo_paths)} photos in batches of {self.batch_size}")
        async with aiohttp.ClientSession() as session:
            for i in tqdm(range(0, len(photo_urls), self.batch_size), desc="Downloading photos"):
                batch_urls = photo_urls[i:i + self.batch_size]
                batch_paths = photo_paths[i:i + self.batch_size]
                await self._load_photos_from_bucket(session, batch_urls, batch_paths, data_folder)

    def load_photos_to_folder(self, photo_urls: List[str], photo_paths: List[str], data_folder: str) -> None:
        os.makedirs(data_folder, exist_ok=True)
        logger.info(f"Loading {len(photo_paths)} photos in batches of {self.batch_size}")
        async def run_batches():
            async with aiohttp.ClientSession() as session:
                for i in tqdm(range(0, len(photo_urls), self.batch_size), desc="Downloading photos"):
                    batch_urls = photo_urls[i:i + self.batch_size]
                    batch_paths = photo_paths[i:i + self.batch_size]
                    await self._load_photos_from_bucket(session, batch_urls, batch_paths, data_folder)
        
        try:
            # Try to get the current event loop
            loop = asyncio.get_running_loop()
            # If we're in an async context, we need to run this differently
            # For now, just run it synchronously in the current loop
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, run_batches())
                future.result()
        except RuntimeError:
            # No event loop running, safe to use asyncio.run
            asyncio.run(run_batches())

    async def load_videos_to_folder_async(self, video_urls: List[str], video_paths: List[str], data_folder: str) -> None:
        """Async version of load_videos_to_folder"""
        os.makedirs(data_folder, exist_ok=True)
        logger.info(f"Loading {len(video_paths)} videos in batches of {self.batch_size}")
        async with aiohttp.ClientSession() as session:
            for i in tqdm(range(0, len(video_urls), self.batch_size), desc="Downloading videos"):
                batch_urls = video_urls[i:i + self.batch_size]
                batch_paths = video_paths[i:i + self.batch_size]
                await self._load_videos_from_bucket(session, batch_urls, batch_paths, data_folder)

    def load_videos_to_folder(self, video_urls: List[str], video_paths: List[str], data_folder: str) -> None:
        os.makedirs(data_folder, exist_ok=True)
        logger.info(f"Loading {len(video_paths)} videos in batches of {self.batch_size}")
        async def run_batches():
            async with aiohttp.ClientSession() as session:
                for i in tqdm(range(0, len(video_urls), self.batch_size), desc="Downloading videos"):
                    batch_urls = video_urls[i:i + self.batch_size]
                    batch_paths = video_paths[i:i + self.batch_size]
                    await self._load_videos_from_bucket(session, batch_urls, batch_paths, data_folder)
        
        try:
            # Try to get the current event loop
            asyncio.get_running_loop()
            # If we're in an async context, we need to run this differently
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, run_batches())
                future.result()
        except RuntimeError:
            # No event loop running, safe to use asyncio.run
            asyncio.run(run_batches())

    def extract_frames_from_videos(self, video_folder: str, frames_output_folder: str, frame_rate: int = 1) -> List[str]:
        """Extract frames from all videos in a folder"""
        video_loader = VideoLoader()
        all_frame_paths = []
        
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
        video_files = [f for f in os.listdir(video_folder) 
                      if any(f.lower().endswith(ext) for ext in video_extensions)]
        
        for video_file in tqdm(video_files, desc="Extracting frames"):
            video_path = os.path.join(video_folder, video_file)
            video_name = os.path.splitext(video_file)[0]
            video_frames_folder = os.path.join(frames_output_folder, video_name)
            
            frame_paths = video_loader.extract_frames(video_path, video_frames_folder, frame_rate)
            all_frame_paths.extend(frame_paths)
        
        return all_frame_paths


class FastVideosLoader(FastImagesLoader):
    """Specialized loader for videos with frame extraction capabilities"""
    
    def __init__(self, batch_size=5):  # Smaller batch size for videos
        super().__init__(batch_size)

    def load_videos_and_extract_frames(self, video_urls: List[str], data_folder: str, 
                                     frame_rate: int = 1, extract_frames: bool = True) -> Optional[List[str]]:
        """Load videos and optionally extract frames"""
        video_paths = [os.path.join(data_folder, f"video_{i}.mp4") for i in range(len(video_urls))]
        
        # Download videos
        self.load_videos_to_folder(video_urls, video_paths, data_folder)
        
        if extract_frames:
            frames_folder = os.path.join(data_folder, "frames")
            return self.extract_frames_from_videos(data_folder, frames_folder, frame_rate)
        
        return None


def main():
    parser = argparse.ArgumentParser(description="Load photos and videos from URLs to a specified folder.")
    parser.add_argument("urls", type=str, nargs='+', help="List of URLs to download.")
    parser.add_argument("data_folder", type=str, help="Folder to save downloaded files.")
    parser.add_argument("--batch_size", type=int, default=10, help="Number of files to download in each batch. Default is 10.")
    parser.add_argument("--media_type", type=str, choices=['photo', 'video', 'auto'], default='auto', 
                       help="Type of media to download. 'auto' detects based on URL extension.")
    parser.add_argument("--extract_frames", action='store_true', 
                       help="Extract frames from videos (only applicable for video downloads).")
    parser.add_argument("--frame_rate", type=int, default=1, 
                       help="Frame extraction rate (frames per second). Default is 1.")
    
    args = parser.parse_args()

    urls = args.urls
    data_folder = args.data_folder
    batch_size = args.batch_size
    media_type = args.media_type
    extract_frames = args.extract_frames
    frame_rate = args.frame_rate

    # Detect media type if auto
    if media_type == 'auto':
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        
        # Check first URL to determine type
        first_url_lower = urls[0].lower()
        if any(first_url_lower.endswith(ext) for ext in video_extensions):
            media_type = 'video'
        elif any(first_url_lower.endswith(ext) for ext in image_extensions):
            media_type = 'photo'
        else:
            logger.warning("Could not auto-detect media type, defaulting to photo")
            media_type = 'photo'

    if media_type == 'video':
        if extract_frames:
            client_basket = FastVideosLoader(batch_size=batch_size)
            client_basket.load_videos_and_extract_frames(urls, data_folder, frame_rate, extract_frames)
        else:
            video_paths = [os.path.join(data_folder, f"video_{i}.mp4") for i in range(len(urls))]
            client_basket = FastImagesLoader(batch_size=batch_size)
            client_basket.load_videos_to_folder(urls, video_paths, data_folder)
    else:
        photo_paths = [os.path.join(data_folder, f"photo_{i}.jpg") for i in range(len(urls))]
        client_basket = FastImagesLoader(batch_size=batch_size)
        client_basket.load_photos_to_folder(urls, photo_paths, data_folder)


if __name__ == "__main__":
    main()
