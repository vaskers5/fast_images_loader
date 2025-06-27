from setuptools import setup, find_packages

setup(
    name="fast_images_loader",
    version="0.2.0",
    author="kazanplova",
    author_email="danil.krokodil@mail.ru",
    description="A fast and asynchronous image and video loader with frame extraction capabilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vaskers5/fast_images_loader",
    project_urls={
        "Bug Tracker": "https://github.com/vaskers5/fast_images_loader/issues",
        "Documentation": "https://github.com/vaskers5/fast_images_loader#readme",
        "Source Code": "https://github.com/vaskers5/fast_images_loader",
    },
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "tqdm",
        "loguru",
        "nest_asyncio",
        "opencv-python",
        "aiofiles",
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