from setuptools import setup, find_packages

setup(
    name="fast_images_loader",
    version="0.1.0",
    author="kazanplova",
    author_email="danil.krokodil@mail.ru",
    description="A fast and asynchronous image loader",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ваш-профиль/fast_images_loader",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "tqdm",
        "loguru",
        "nest_asyncio",
    ],
    entry_points={
        "console_scripts": [
            "fast_images_loader=fast_images_loader.loader:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)