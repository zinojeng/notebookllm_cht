#!/usr/bin/env python3
"""
安裝腳本 - NotebookLM 英文音頻轉中文 Podcast 處理器
"""

from setuptools import setup, find_packages
import os

# 讀取 README 文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 讀取依賴文件
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="notebooklm-chinese-podcast",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="將 NotebookLM 英文音頻概覽轉換為自然的中文對話 Podcast",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/notebooklm-chinese-podcast",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "notebooklm-podcast=main:main",
            "notebooklm-batch=batch_processor:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
    keywords=[
        "notebooklm",
        "podcast",
        "audio",
        "translation",
        "chinese",
        "tts",
        "whisper",
        "speech-to-text",
        "text-to-speech",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/notebooklm-chinese-podcast/issues",
        "Source": "https://github.com/yourusername/notebooklm-chinese-podcast",
        "Documentation": "https://github.com/yourusername/notebooklm-chinese-podcast#readme",
    },
) 