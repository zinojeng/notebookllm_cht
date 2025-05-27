# NotebookLM 英文音頻轉中文 Podcast 處理器

🎙️ 將 NotebookLM 生成的英文音頻概覽轉換為自然的中文對話 Podcast

## 功能特色

✨ **完整的處理流程**
- 🎯 使用 Whisper 進行高精度語音識別
- 👥 智能對話分析與說話者檢測
- 🌐 英文到繁體中文的自然翻譯
- 🎤 使用 Edge TTS 生成自然的中文語音
- 🎵 智能音頻合併與優化

✨ **保留對話自然性**
- 檢測問句、回應和轉場
- 添加適當的語氣詞和停頓
- 不同說話者使用不同聲音
- 調整語速和音調以增強自然度

✨ **批次處理支援**
- 同時處理多個音頻文件
- 可調整並發處理數量
- 詳細的處理報告和統計

## 安裝說明

### 1. 環境要求
- Python 3.8 或更高版本
- macOS / Linux / Windows

### 2. 快速安裝
```bash
# 使用自動安裝腳本（推薦）
chmod +x install.sh
./install.sh

# 或手動安裝
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 3. 環境變數設定

#### 🚀 快速設定（推薦）
```bash
# 使用互動式設定工具
./setup_env.sh

# 或使用 Python 工具
python env_manager.py create
```

#### 📝 手動設定
```bash
# 複製環境變數範本
cp config/env_template.txt .env

# 編輯 .env 文件並填入您的 API 金鑰
nano .env
```

#### 🔑 API 金鑰設定
根據您選擇的服務提供商，設定對應的 API 金鑰：

**免費開始（推薦）**：
```env
DEFAULT_TTS_PROVIDER=edge          # 免費
TRANSLATION_PROVIDER=google        # 有免費額度
WHISPER_MODEL=base                 # 本地處理
```

**高品質選項**：
```env
OPENAI_API_KEY=sk-your_key_here    # OpenAI 服務
ELEVENLABS_API_KEY=your_key_here   # 高品質 TTS
DEEPL_API_KEY=your_key_here        # 高品質翻譯
```

📚 **詳細的 API 金鑰設定指南**：請參考 [API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)

#### 🧪 驗證設定
```bash
# 驗證環境變數配置
python env_manager.py validate

# 查看當前配置
python env_manager.py show
```

### 4. 系統依賴
確保系統已安裝以下工具：
- `ffmpeg` - 音頻格式轉換
- 穩定的網路連接 - 用於翻譯和語音合成

```bash
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg

# Windows:
# 下載 FFmpeg 並添加到 PATH
```

## 使用方法

### 單文件處理

```bash
# 基本使用
python main.py input.wav

# 指定輸出目錄
python main.py input.wav -o my_output/

# 僅生成逐字稿預覽
python main.py input.wav --preview

# 自定義聲音
python main.py input.wav --voice-female zh-TW-HsiaoChenNeural --voice-male zh-TW-YunJheNeural
```

### 批次處理

```bash
# 處理整個目錄
python batch_processor.py input_folder/

# 指定輸出目錄和並發數
python batch_processor.py input_folder/ -o batch_output/ --concurrent 4
```

### 命令行參數

#### main.py 參數
- `input_file` - 輸入的 .wav 音頻文件路徑
- `-o, --output` - 輸出目錄（預設：output/）
- `--preview` - 僅生成逐字稿預覽，不生成音頻
- `--voice-female` - 女性聲音（預設：zh-TW-HsiaoChenNeural）
- `--voice-male` - 男性聲音（預設：zh-TW-YunJheNeural）

#### batch_processor.py 參數
- `input_dir` - 包含 .wav 文件的輸入目錄
- `-o, --output` - 輸出目錄（預設：batch_output/）
- `--concurrent` - 最大並發處理數量（預設：2）

## 處理流程

### 1. 🎯 語音識別
- 使用 OpenAI Whisper 模型進行語音轉文字
- 保留時間戳信息
- 支援詞級別的時間對齊

### 2. 👥 對話分析
- 檢測對話模式（問句、回應、轉場）
- 智能說話者分離
- 標記對話特徵

### 3. 🌐 翻譯處理
- 英文到繁體中文翻譯
- 保留對話的自然表達
- 根據對話類型調整翻譯風格

### 4. 🎤 語音合成
- 使用 Microsoft Edge TTS
- 不同說話者使用不同聲音
- 添加適當的停頓和語調調整

### 5. 🎵 音頻合併
- 智能合併音頻片段
- 添加自然的對話間隔
- 輸出高品質的最終音頻

## 輸出文件

處理完成後，您將獲得：

```
output/
├── chinese_podcast_final.wav    # 最終的中文 Podcast 音頻
├── transcript.json              # 詳細的逐字稿（包含原文和譯文）
├── segment_000_A.wav           # 個別音頻片段
├── segment_001_B.wav
└── ...
```

### 逐字稿格式
```json
{
  "timestamp": "2024-01-01T12:00:00",
  "total_segments": 50,
  "segments": [
    {
      "start_time": "0.00s",
      "end_time": "3.50s",
      "speaker": "A",
      "original_text": "Welcome to today's discussion...",
      "translated_text": "歡迎來到今天的討論...",
      "dialogue_type": {
        "is_question": false,
        "is_response": false,
        "is_transition": true
      }
    }
  ]
}
```

## 可用的中文聲音

### 台灣繁體中文聲音
- **女性聲音**：
  - `zh-TW-HsiaoChenNeural` - 曉晨（預設女聲）
  - `zh-TW-HsiaoYuNeural` - 曉雨
  - `zh-TW-HanHanNeural` - 涵涵

- **男性聲音**：
  - `zh-TW-YunJheNeural` - 雲哲（預設男聲）
  - `zh-TW-HsiaoYuNeural` - 曉宇

### 使用自定義聲音
```bash
python main.py input.wav --voice-female zh-TW-HsiaoYuNeural --voice-male zh-TW-HsiaoYuNeural
```

## 效能優化建議

### 硬體建議
- **CPU**：多核心處理器（推薦 8 核心以上）
- **記憶體**：至少 8GB RAM（推薦 16GB）
- **儲存空間**：SSD 硬碟（提升 I/O 效能）

### 軟體優化
- 使用虛擬環境避免套件衝突
- 調整批次處理的並發數量
- 定期清理暫存文件

### 批次處理最佳實踐
```bash
# 根據系統效能調整並發數
# 4 核心系統
python batch_processor.py input/ --concurrent 2

# 8 核心系統
python batch_processor.py input/ --concurrent 4

# 16 核心系統
python batch_processor.py input/ --concurrent 6
```

## 故障排除

### 常見問題

#### 1. FFmpeg 未安裝
```
錯誤：FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
解決：安裝 FFmpeg 並確保在 PATH 中
```

#### 2. 記憶體不足
```
錯誤：CUDA out of memory 或 MemoryError
解決：
- 減少批次處理並發數
- 使用較小的 Whisper 模型
- 增加系統記憶體
```

#### 3. 網路連接問題
```
錯誤：翻譯或語音合成失敗
解決：
- 檢查網路連接
- 使用 VPN（如果需要）
- 重試處理
```

#### 4. 音頻格式不支援
```
錯誤：無法載入音頻文件
解決：
- 確保文件是 .wav 格式
- 使用 FFmpeg 轉換格式：
  ffmpeg -i input.mp3 output.wav
```

### 除錯模式
如果遇到問題，可以查看詳細的處理日誌：

```bash
# 啟用詳細日誌
python main.py input.wav --verbose

# 僅測試前幾個片段
python main.py input.wav --preview
```

## 進階使用

### 自定義翻譯風格
您可以修改 `audio_processor.py` 中的 `enhance_chinese_dialogue` 方法來調整翻譯風格：

```python
def enhance_chinese_dialogue(self, translated_text: str, segment: Dict) -> str:
    # 添加您的自定義邏輯
    # 例如：特定術語的翻譯規則
    # 或：特定語氣的調整
    pass
```

### 添加新的語音
在 `audio_processor.py` 中修改聲音設定：

```python
self.chinese_voices = {
    'female': 'zh-TW-HsiaoChenNeural',
    'male': 'zh-TW-YunJheNeural',
    'narrator': 'zh-TW-HanHanNeural'  # 添加旁白聲音
}
```

## 授權條款

本專案使用 MIT 授權條款。請參閱 LICENSE 文件了解詳細信息。

## 貢獻指南

歡迎提交 Issue 和 Pull Request！

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

## 更新日誌

### v1.0.0 (2024-01-01)
- ✨ 初始版本發布
- 🎯 支援 Whisper 語音識別
- 🌐 支援英文到中文翻譯
- 🎤 支援 Edge TTS 語音合成
- 📦 支援批次處理

## 聯絡方式

如有問題或建議，請：
- 提交 GitHub Issue
- 發送電子郵件至：[您的郵箱]

---

🎉 **享受您的中文 Podcast 體驗！** 