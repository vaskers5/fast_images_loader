import asyncio
import os
import pytest
from unittest.mock import patch, MagicMock
from fast_images_loader.loader import FastImagesLoader, FastVideosLoader, VideoLoader

@pytest.mark.asyncio
async def test_load_photos(monkeypatch, tmp_path):
    # Патчим request метод для симуляции загрузки
    async def mock_request(self, session, photo_url, photo_path):
        with open(photo_path, "wb") as f:
            f.write(b"fake image data")
        return 1

    monkeypatch.setattr("fast_images_loader.loader.PhotoLoader.request", mock_request)

    # Создаем тестовые данные
    photo_urls = ["https://github.com/vaskers5/fast_images_loader/blob/main/test_images/photo_2024-09-11_13-47-44.jpg?raw=true",
                   "https://github.com/vaskers5/fast_images_loader/blob/main/test_images/photo_2024-10-01_20-55-34.jpg?raw=true",
                   "https://github.com/vaskers5/fast_images_loader/blob/main/test_images/photo_2024-10-01_20-55-35.jpg?raw=true"]
    
    photo_paths = [os.path.join(tmp_path, f"photo_{i}.jpg") for i in range(len(photo_urls))]

    # Выполняем тестируемую функцию
    loader = FastImagesLoader()
    await loader.load_photos_to_folder_async(photo_urls, photo_paths, str(tmp_path))

    # Проверяем, что файлы созданы
    for photo_path in photo_paths:
        assert os.path.exists(photo_path)
        assert os.path.getsize(photo_path) > 0


@pytest.mark.asyncio
async def test_load_videos(monkeypatch, tmp_path):
    # Mock the video request method
    async def mock_video_request(self, session, video_url, video_path):
        with open(video_path, "wb") as f:
            f.write(b"fake video data")
        return 1

    monkeypatch.setattr("fast_images_loader.loader.VideoLoader.request", mock_video_request)

    # Test data
    video_urls = ["https://example.com/video1.mp4", "https://example.com/video2.mp4"]
    video_paths = [os.path.join(tmp_path, f"video_{i}.mp4") for i in range(len(video_urls))]

    # Execute the function
    loader = FastImagesLoader()
    await loader.load_videos_to_folder_async(video_urls, video_paths, str(tmp_path))

    # Check that files were created
    for video_path in video_paths:
        assert os.path.exists(video_path)
        assert os.path.getsize(video_path) > 0


def test_extract_frames(tmp_path):
    # Create a mock video file
    video_path = os.path.join(tmp_path, "test_video.mp4")
    frames_output_folder = os.path.join(tmp_path, "frames")
    
    # Mock cv2.VideoCapture and related methods
    with patch('cv2.VideoCapture') as mock_cap_class:
        mock_cap = MagicMock()
        mock_cap_class.return_value = mock_cap
        
        # Mock successful video opening
        mock_cap.isOpened.return_value = True
        mock_cap.get.return_value = 30.0  # 30 FPS
        
        # Mock frame reading - return 3 frames then False
        mock_cap.read.side_effect = [
            (True, MagicMock()),  # Frame 1
            (True, MagicMock()),  # Frame 2
            (True, MagicMock()),  # Frame 3
            (False, None)         # End of video
        ]
        
        # Mock cv2.imwrite
        with patch('cv2.imwrite') as mock_imwrite:
            # Create fake video file
            with open(video_path, 'wb') as f:
                f.write(b'fake video content')
            
            video_loader = VideoLoader()
            frame_paths = video_loader.extract_frames(video_path, frames_output_folder, frame_rate=1)
            
            # Verify that frames were "extracted"
            assert len(frame_paths) == 1  # At 30fps with frame_rate=1, only every 30th frame
            mock_cap.release.assert_called_once()


def test_fast_videos_loader(monkeypatch, tmp_path):
    # Mock video loading
    def mock_load_videos(self, urls, paths, folder):
        for path in paths:
            with open(path, 'wb') as f:
                f.write(b'fake video data')
    
    # Mock frame extraction
    def mock_extract_frames(self, video_folder, frames_folder, frame_rate):
        os.makedirs(frames_folder, exist_ok=True)
        frame_paths = []
        for i in range(3):  # Mock 3 extracted frames
            frame_path = os.path.join(frames_folder, f"frame_{i:06d}.jpg")
            with open(frame_path, 'wb') as f:
                f.write(b'fake frame data')
            frame_paths.append(frame_path)
        return frame_paths
    
    monkeypatch.setattr("fast_images_loader.loader.FastImagesLoader.load_videos_to_folder", mock_load_videos)
    monkeypatch.setattr("fast_images_loader.loader.FastImagesLoader.extract_frames_from_videos", mock_extract_frames)
    
    video_urls = ["https://example.com/video1.mp4", "https://example.com/video2.mp4"]
    
    loader = FastVideosLoader()
    frame_paths = loader.load_videos_and_extract_frames(video_urls, str(tmp_path))
    
    # Check that frames were extracted
    assert frame_paths is not None
    assert len(frame_paths) == 3