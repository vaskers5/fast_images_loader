# Fast Images Loader

Fast Images Loader — это асинхронный инструмент для загрузки изображений из интернета и сохранения их в указанной папке. Он использует библиотеку `aiohttp` для асинхронных HTTP-запросов и `tqdm` для отображения прогресса загрузки.

## Установка

Вы можете установить пакет с помощью pip:

```bash
pip install fast_images_loader
```

## Использование

Fast Images Loader можно использовать как команду в командной строке:

```bash
fast_images_loader [photo_urls] [data_folder]
```

- `photo_urls`: Список URL-адресов фотографий для загрузки.
- `data_folder`: Папка, в которую будут сохранены загруженные фотографии.

### Пример

```bash
fast_images_loader https://example.com/photo1.jpg https://example.com/photo2.jpg ./downloads
```

Это загрузит фотографии с указанных URL и сохранит их в папке `./downloads`.

## Зависимости

- `aiohttp`
- `tqdm`
- `loguru`
- `nest_asyncio`

## Разработка

Если вы хотите внести изменения в проект, склонируйте репозиторий и установите зависимости:

```bash
git clone https://github.com/ваш-профиль/fast_images_loader.git
cd fast_images_loader
pip install -r requirements.txt
```

## Тестирование

Тесты находятся в папке `tests`. Используйте `pytest` для запуска тестов:

```bash
pytest
```
