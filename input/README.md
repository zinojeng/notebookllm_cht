# 輸入文件目錄

## 📁 目錄說明

這個目錄用於存放待處理的音頻文件。

### 🎵 samples/ 目錄
存放單個測試音頻文件，適合：
- 測試新功能
- 學習使用方式
- 處理單個重要文件

**使用方式：**
```bash
# 將音頻文件放入此目錄
cp your_audio.wav input/samples/

# 處理單個文件
python main.py input/samples/your_audio.wav
```

### 📦 batch/ 目錄
存放批次處理的多個音頻文件，適合：
- 大量文件處理
- 自動化工作流程
- 生產環境使用

**使用方式：**
```bash
# 將多個音頻文件放入此目錄
cp *.wav input/batch/

# 批次處理
python batch_processor.py input/batch/
```

## 📋 文件格式要求

### 支援格式
- **主要格式**：`.wav`（推薦）
- **其他格式**：`.mp3`, `.m4a`（需要 FFmpeg 轉換）

### 建議規格
- **採樣率**：16kHz 或 22kHz
- **聲道**：單聲道（mono）
- **位元深度**：16-bit
- **時長**：建議 1-30 分鐘

### 格式轉換
如果您的文件不是 .wav 格式，可以使用 FFmpeg 轉換：

```bash
# MP3 轉 WAV
ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav

# M4A 轉 WAV
ffmpeg -i input.m4a -ar 16000 -ac 1 output.wav

# 批次轉換
for file in *.mp3; do
    ffmpeg -i "$file" -ar 16000 -ac 1 "${file%.mp3}.wav"
done
```

## 🎯 最佳實踐

### 文件命名
建議使用有意義的文件名：
```
✅ 好的命名：
- notebooklm_ai_discussion_20240131.wav
- podcast_episode_001.wav
- interview_john_doe.wav

❌ 避免的命名：
- audio.wav
- 錄音檔案.wav
- untitled.wav
```

### 文件組織
```
input/
├── samples/
│   ├── test_audio.wav          # 測試文件
│   └── demo_conversation.wav   # 示範文件
└── batch/
    ├── episode_001.wav         # 批次處理文件
    ├── episode_002.wav
    └── episode_003.wav
```

### 品質檢查
處理前建議檢查：
- 音頻是否清晰
- 是否包含對話內容
- 文件是否完整（未損壞）

```bash
# 檢查音頻信息
ffprobe input/samples/your_audio.wav

# 播放測試（macOS）
afplay input/samples/your_audio.wav
```

## ⚠️ 注意事項

1. **文件大小**：建議單個文件不超過 500MB
2. **存儲空間**：確保有足夠的磁碟空間
3. **備份**：重要文件請先備份
4. **隱私**：注意音頻內容的隱私保護

## 🔧 故障排除

### 常見問題

**問題：文件無法識別**
```bash
# 檢查文件格式
file input/samples/your_audio.wav

# 轉換格式
ffmpeg -i input/samples/your_audio.mp3 input/samples/your_audio.wav
```

**問題：音頻品質差**
```bash
# 檢查音頻參數
ffprobe -v quiet -show_format -show_streams input/samples/your_audio.wav

# 提升音頻品質
ffmpeg -i input.wav -ar 22050 -ac 1 -b:a 128k output.wav
```

**問題：文件太大**
```bash
# 壓縮音頻
ffmpeg -i input.wav -ar 16000 -ac 1 -b:a 64k compressed.wav
```

---

**建立日期**：2024-01-31  
**維護者**：專案開發團隊 