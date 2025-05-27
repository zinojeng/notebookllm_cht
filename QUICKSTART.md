# 快速開始指南

🚀 **5 分鐘內開始使用 NotebookLM 中文 Podcast 處理器**

## 一鍵安裝

```bash
# 下載並執行自動安裝腳本
curl -fsSL https://raw.githubusercontent.com/yourusername/notebooklm-chinese-podcast/main/install.sh | bash

# 或者手動下載後執行
chmod +x install.sh
./install.sh
```

## 手動安裝（如果自動安裝失敗）

```bash
# 1. 建立虛擬環境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 安裝 FFmpeg
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg
```

## 立即開始

### 1. 準備您的音頻文件
- 確保文件是 `.wav` 格式
- 如果是其他格式，使用 FFmpeg 轉換：
```bash
ffmpeg -i your_audio.mp3 your_audio.wav
```

### 2. 處理單個文件

```bash
# 啟動虛擬環境
source venv/bin/activate

# 基本處理
python main.py your_audio.wav

# 指定輸出目錄
python main.py your_audio.wav -o my_output/

# 僅預覽逐字稿（不生成音頻）
python main.py your_audio.wav --preview
```

### 3. 批次處理多個文件

```bash
# 處理整個目錄中的所有 .wav 文件
python batch_processor.py audio_folder/

# 指定輸出目錄和並發數
python batch_processor.py audio_folder/ -o batch_output/ --concurrent 4
```

## 輸出結果

處理完成後，您將獲得：

```
output/
├── chinese_podcast_final.wav    # 🎧 最終的中文 Podcast
├── transcript.json              # 📄 詳細逐字稿
└── segment_*.wav               # 🎵 個別音頻片段
```

## 常用命令

```bash
# 查看幫助
python main.py --help

# 自定義聲音
python main.py audio.wav --voice-female zh-TW-HsiaoYuNeural --voice-male zh-TW-YunJheNeural

# 批次處理幫助
python batch_processor.py --help
```

## 故障排除

### 問題：FFmpeg 未找到
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### 問題：記憶體不足
```bash
# 減少並發數
python batch_processor.py folder/ --concurrent 1
```

### 問題：網路連接
- 確保網路連接正常（翻譯和語音合成需要網路）
- 如果在中國大陸，可能需要 VPN

## 進階使用

### 可用的中文聲音
- **女性**：`zh-TW-HsiaoChenNeural`（預設）、`zh-TW-HsiaoYuNeural`、`zh-TW-HanHanNeural`
- **男性**：`zh-TW-YunJheNeural`（預設）、`zh-TW-HsiaoYuNeural`

### 自定義聲音範例
```bash
python main.py audio.wav \
  --voice-female zh-TW-HsiaoYuNeural \
  --voice-male zh-TW-HsiaoYuNeural
```

## 需要幫助？

- 📖 查看完整文檔：[README.md](README.md)
- 🐛 回報問題：[GitHub Issues](https://github.com/yourusername/notebooklm-chinese-podcast/issues)
- 💬 討論交流：[GitHub Discussions](https://github.com/yourusername/notebooklm-chinese-podcast/discussions)

---

🎉 **開始享受您的中文 Podcast 體驗！** 