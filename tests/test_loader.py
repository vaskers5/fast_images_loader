import asyncio
import os
import pytest
from fast_images_loader.loader import FastImagesLoader

@pytest.mark.asyncio
async def test_load_photos(monkeypatch, tmp_path):
    # Патчим request метод для симуляции загрузки
    async def mock_request(self, session, photo_url, photo_path):
        with open(photo_path, "wb") as f:
            f.write(b"fake image data")
        return 1

    monkeypatch.setattr("fast_images_loader.loader.PhotoLoader.request", mock_request)

    # Создаем тестовые данные
    photo_urls = ["http://example.com/photo1.jpg", "http://example.com/photo2.jpg"]
    photo_paths = [os.path.join(tmp_path, f"photo_{i}.jpg") for i in range(len(photo_urls))]

    # Выполняем тестируемую функцию
    loader = FastImagesLoader()
    await loader.load_photos_from_bucket(photo_urls, photo_paths, tmp_path)

    # Проверяем, что файлы созданы
    for photo_path in photo_paths:
        assert os.path.exists(photo_path)
        assert os.path.getsize(photo_path) > 0