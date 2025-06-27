#!/usr/bin/env python3
"""
Example script demonstrating video loading functionality
"""
import os
from fast_images_loader import FastImagesLoader, FastVideosLoader

def example_video_download():
    """Example of downloading videos"""
    # Example video URLs (replace with actual video URLs)
    video_urls = [
        "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
        "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4"
    ]
    
    # Download folder
    download_folder = "./downloaded_videos"
    
    # Create loader
    loader = FastImagesLoader(batch_size=2)
    
    # Generate video paths
    video_paths = [os.path.join(download_folder, f"video_{i}.mp4") for i in range(len(video_urls))]
    
    print("Downloading videos...")
    loader.load_videos_to_folder(video_urls, video_paths, download_folder)
    print(f"Videos downloaded to: {download_folder}")

def example_video_with_frame_extraction():
    """Example of downloading videos and extracting frames"""
    # Example video URLs
    video_urls = [
        "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"
    ]
    
    # Download folder
    download_folder = "./downloaded_videos_with_frames"
    
    # Create specialized video loader
    loader = FastVideosLoader(batch_size=1)
    
    print("Downloading videos and extracting frames...")
    frame_paths = loader.load_videos_and_extract_frames(
        video_urls, 
        download_folder, 
        frame_rate=2,  # Extract 2 frames per second
        extract_frames=True
    )
    
    if frame_paths:
        print(f"Extracted {len(frame_paths)} frames")
        print(f"Frames saved to: {os.path.join(download_folder, 'frames')}")
    else:
        print("No frames were extracted")

def example_frame_extraction_from_existing_videos():
    """Example of extracting frames from already downloaded videos"""
    video_folder = "./existing_videos"
    frames_output_folder = "./extracted_frames"
    
    # Create loader
    loader = FastImagesLoader()
    
    print("Extracting frames from existing videos...")
    frame_paths = loader.extract_frames_from_videos(
        video_folder, 
        frames_output_folder, 
        frame_rate=1  # Extract 1 frame per second
    )
    
    print(f"Extracted {len(frame_paths)} frames")
    print(f"Frames saved to: {frames_output_folder}")

if __name__ == "__main__":
    print("Fast Images Loader - Video Support Examples")
    print("=" * 50)
    
    print("\n1. Basic video download:")
    try:
        example_video_download()
    except Exception as e:
        print(f"Error in video download: {e}")
    
    print("\n2. Video download with frame extraction:")
    try:
        example_video_with_frame_extraction()
    except Exception as e:
        print(f"Error in video download with frames: {e}")
    
    print("\n3. Frame extraction from existing videos:")
    try:
        example_frame_extraction_from_existing_videos()
    except Exception as e:
        print(f"Error in frame extraction: {e}")
    
    print("\nAll examples completed!")
