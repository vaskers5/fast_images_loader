# Fast Images Loader

Fast Images Loader is an asynchronous tool for downloading images from the internet and saving them to a specified folder. It uses the `aiohttp` library for asynchronous HTTP requests and `tqdm` for displaying download progress.

## Installation

You can install the package using pip:

```bash
pip install fast_images_loader
```

## Usage

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

Fast Images Loader can be used as a command in the command line:

```bash
fast_images_loader [photo_urls] [data_folder]
```

- `photo_urls`: List of photo URLs to download.
- `data_folder`: Folder where the downloaded photos will be saved.

### Example

```bash
fast_images_loader https://example.com/photo1.jpg https://example.com/photo2.jpg ./downloads
```

This will download the photos from the specified URLs and save them in the `./downloads` folder.

## Dependencies

- `aiohttp`
- `tqdm`
- `loguru`
- `nest_asyncio`

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

