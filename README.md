# Fast Images Loader

Fast Images Loader is an asynchronous tool for downloading images and videos from the internet and saving them to a specified folder. It uses the `aiohttp` library for asynchronous HTTP requests, `tqdm` for displaying download progress, and `opencv-python` for video frame extraction.

## Features

- ✅ Asynchronous image downloading
- ✅ Asynchronous video downloading
- ✅ Video frame extraction
- ✅ Batch processing
- ✅ Progress bars
- ✅ Auto media type detection
- ✅ Command line interface

## Installation

### From PyPI (Recommended)

You can install the latest stable version using pip:

```bash
pip install fast_images_loader
```

### From GitHub Repository

You can install the latest development version directly from GitHub:

```bash
# Install latest from main branch
pip install git+https://github.com/vaskers5/fast_images_loader.git

# Install specific version/tag
pip install git+https://github.com/vaskers5/fast_images_loader.git@v0.2.0

# Install from specific branch
pip install git+https://github.com/vaskers5/fast_images_loader.git@development
```

### Development Installation

For development purposes, clone and install in editable mode:

```bash
git clone https://github.com/vaskers5/fast_images_loader.git
cd fast_images_loader
pip install -e .
```

## Usage

### Image Loading

Loading via import is supported:

```python
from fast_images_loader import FastImagesLoader

photo_urls = [
    "list of urls",
]
photo_dir = "test_dir"
photo_paths = [os.path.join(photo_dir, f"{idx}.jpeg") for idx in range(len(photo_urls))]
FastImagesLoader().load_photos_to_folder(photo_urls, photo_paths, photo_dir)
```

### Video Loading

```python
from fast_images_loader import FastImagesLoader

video_urls = [
    "https://example.com/video1.mp4",
    "https://example.com/video2.mp4"
]
video_dir = "videos"
video_paths = [os.path.join(video_dir, f"video_{idx}.mp4") for idx in range(len(video_urls))]
FastImagesLoader().load_videos_to_folder(video_urls, video_paths, video_dir)
```

### Video Loading with Frame Extraction

```python
from fast_images_loader import FastVideosLoader

video_urls = ["https://example.com/video.mp4"]
download_folder = "./videos"

loader = FastVideosLoader(batch_size=2)
frame_paths = loader.load_videos_and_extract_frames(
    video_urls, 
    download_folder, 
    frame_rate=1,  # Extract 1 frame per second
    extract_frames=True
)
print(f"Extracted {len(frame_paths)} frames")
```

### Frame Extraction from Existing Videos

```python
from fast_images_loader import FastImagesLoader

loader = FastImagesLoader()
frame_paths = loader.extract_frames_from_videos(
    video_folder="./existing_videos", 
    frames_output_folder="./frames",
    frame_rate=2  # Extract 2 frames per second
)
```

### Command Line Interface

Fast Images Loader can be used as a command in the command line:

```bash
fast_images_loader [urls] [data_folder] [options]
```

- `urls`: List of URLs to download.
- `data_folder`: Folder where the downloaded files will be saved.

#### Options

- `--media_type`: Type of media ('photo', 'video', 'auto'). Default: 'auto'
- `--batch_size`: Number of files to download in each batch. Default: 10
- `--extract_frames`: Extract frames from videos (video mode only)
- `--frame_rate`: Frame extraction rate in fps. Default: 1

### Examples

Download images:
```bash
fast_images_loader https://example.com/photo1.jpg https://example.com/photo2.jpg ./downloads --media_type photo
```

Download videos:
```bash
fast_images_loader https://example.com/video1.mp4 https://example.com/video2.mp4 ./downloads --media_type video
```

Download videos and extract frames:
```bash
fast_images_loader https://example.com/video1.mp4 ./downloads --media_type video --extract_frames --frame_rate 2
```

Auto-detect media type:
```bash
fast_images_loader https://example.com/photo1.jpg https://example.com/video1.mp4 ./downloads --media_type auto
```

## Dependencies

- `aiohttp` - Async HTTP client
- `tqdm` - Progress bars
- `loguru` - Logging
- `nest_asyncio` - Nested event loop support
- `opencv-python` - Video processing and frame extraction
- `aiofiles` - Async file operations

## Development

If you want to make changes to the project, clone the repository and install the dependencies:

```bash
git clone https://github.com/your-profile/fast_images_loader.git
cd fast_images_loader
pip install -r requirements.txt
```

## Testing

Tests are located in the `tests` folder. Use `pytest` to run the tests:

```bash
pytest
```

