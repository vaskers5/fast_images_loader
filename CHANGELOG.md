# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-06-27

### Added
- **Video loading support**: Download videos from URLs with asynchronous processing
- **Frame extraction**: Extract frames from videos at configurable frame rates
- **FastVideosLoader class**: Specialized loader for videos with frame extraction capabilities
- **VideoLoader class**: Core video downloading functionality with streaming support
- **Enhanced CLI**: Extended command-line interface with video support and auto-detection
- **Async methods**: Added async versions of loading methods for better integration

### New Features
- `load_videos_to_folder()` - Download videos asynchronously
- `load_videos_to_folder_async()` - Async version of video loading
- `extract_frames_from_videos()` - Extract frames from downloaded videos
- `load_videos_and_extract_frames()` - Combined video download and frame extraction
- Auto media type detection based on file extensions
- Support for multiple video formats (mp4, avi, mov, mkv, wmv, flv, webm)
- Configurable frame extraction rates

### Enhanced
- Updated CLI with new options: `--media_type`, `--extract_frames`, `--frame_rate`
- Better error handling and logging for video operations
- Improved progress bars for video downloads
- Extended test coverage for video functionality

### Dependencies
- Added `opencv-python` for video processing
- Added `aiofiles` for async file operations

### Breaking Changes
- CLI argument `photo_urls` renamed to `urls` to support both images and videos
- Minimum Python version remains 3.6+ but recommended 3.8+ for better async support

## [0.1.2] - Previous Release
- Basic image loading functionality
- Asynchronous image downloads
- Progress bars with tqdm
- Command-line interface for images
