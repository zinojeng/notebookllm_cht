# 目錄結構說明

## 📁 專案目錄結構

```
podcasty-2 notebookllm/
├── 📁 input/                    # 輸入文件目錄
│   ├── 📁 samples/              # 範例音頻文件
│   └── 📁 batch/                # 批次處理音頻文件
├── 📁 output/                   # 輸出結果目錄
│   ├── 📁 processed/            # 處理完成的音頻和逐字稿
│   └── 📁 reports/              # 處理報告和統計
├── 📁 examples/                 # 範例和示範文件
│   ├── 📁 audio/                # 範例音頻文件
│   └── 📁 configs/              # 範例配置文件
├── 📁 temp/                     # 暫存文件目錄
│   ├── 📁 audio/                # 暫存音頻片段
│   └── 📁 transcripts/          # 暫存逐字稿
├── 📁 logs/                     # 日誌文件目錄
│   ├── 📁 processing/           # 處理過程日誌
│   └── 📁 errors/               # 錯誤日誌
├── 📁 config/                   # 配置文件目錄
│   ├── 📁 voices/               # 聲音配置
│   └── 📁 models/               # 模型配置
├── 📄 audio_processor.py        # 核心處理邏輯
├── 📄 main.py                   # 單文件處理入口
├── 📄 batch_processor.py        # 批次處理器
├── 📄 requirements.txt          # 依賴管理
├── 📄 README.md                 # 專案說明
├── 📄 QUICKSTART.md             # 快速開始指南
├── 📄 progress.md               # 專案進度追蹤
└── 📄 install.sh                # 安裝腳本
```

---

## 📂 目錄用途說明

### 🎵 input/ - 輸入文件目錄
存放待處理的音頻文件

#### input/samples/
- **用途**：存放單個測試音頻文件
- **格式**：.wav 文件（推薦 16kHz, 單聲道）
- **使用**：`python main.py input/samples/your_audio.wav`

#### input/batch/
- **用途**：存放批次處理的多個音頻文件
- **格式**：.wav 文件
- **使用**：`python batch_processor.py input/batch/`

### 🎧 output/ - 輸出結果目錄
存放處理完成的結果文件

#### output/processed/
- **內容**：
  - `chinese_podcast_final.wav` - 最終中文 Podcast
  - `transcript.json` - 詳細逐字稿
  - `segment_*.wav` - 個別音頻片段
- **結構**：
  ```
  output/processed/
  ├── 20240131_143022_audio1/
  │   ├── chinese_podcast_final.wav
  │   ├── transcript.json
  │   └── segment_*.wav
  └── 20240131_143155_audio2/
      └── ...
  ```

#### output/reports/
- **內容**：
  - `batch_report.json` - 批次處理報告
  - `summary_report.json` - 摘要統計
  - `processing_stats.json` - 效能統計

### 📚 examples/ - 範例和示範文件
提供使用範例和配置模板

#### examples/audio/
- **內容**：範例音頻文件和預期輸出
- **用途**：測試和學習使用

#### examples/configs/
- **內容**：配置文件範例
- **文件**：
  - `default_config.yaml` - 預設配置
  - `high_quality_config.yaml` - 高品質配置
  - `fast_processing_config.yaml` - 快速處理配置

### 🗂️ temp/ - 暫存文件目錄
存放處理過程中的暫存文件

#### temp/audio/
- **內容**：處理過程中的音頻片段
- **清理**：處理完成後自動清理

#### temp/transcripts/
- **內容**：中間步驟的逐字稿文件
- **清理**：處理完成後自動清理

### 📋 logs/ - 日誌文件目錄
記錄處理過程和錯誤信息

#### logs/processing/
- **內容**：處理過程的詳細日誌
- **格式**：`processing_YYYYMMDD_HHMMSS.log`

#### logs/errors/
- **內容**：錯誤和異常日誌
- **格式**：`error_YYYYMMDD_HHMMSS.log`

### ⚙️ config/ - 配置文件目錄
存放系統配置和設定文件

#### config/voices/
- **內容**：聲音配置文件
- **文件**：
  - `chinese_voices.json` - 中文聲音列表
  - `voice_mapping.json` - 聲音對應關係

#### config/models/
- **內容**：模型配置文件
- **文件**：
  - `whisper_config.json` - Whisper 模型設定
  - `translation_config.json` - 翻譯設定

---

## 🚀 使用方式

### 單文件處理
```bash
# 1. 將音頻文件放入 input/samples/
cp your_audio.wav input/samples/

# 2. 處理文件
python main.py input/samples/your_audio.wav -o output/processed/

# 3. 查看結果
ls output/processed/your_audio/
```

### 批次處理
```bash
# 1. 將多個音頻文件放入 input/batch/
cp *.wav input/batch/

# 2. 批次處理
python batch_processor.py input/batch/ -o output/processed/

# 3. 查看報告
cat output/reports/batch_report.json
```

### 使用範例配置
```bash
# 使用高品質配置
python main.py input/samples/audio.wav --config examples/configs/high_quality_config.yaml

# 使用快速處理配置
python main.py input/samples/audio.wav --config examples/configs/fast_processing_config.yaml
```

---

## 🧹 清理和維護

### 自動清理
系統會自動清理：
- `temp/` 目錄中的暫存文件
- 超過 7 天的日誌文件

### 手動清理
```bash
# 清理暫存文件
rm -rf temp/audio/* temp/transcripts/*

# 清理舊日誌（保留最近 7 天）
find logs/ -name "*.log" -mtime +7 -delete

# 清理輸出文件（謹慎使用）
rm -rf output/processed/*
```

### 備份重要文件
```bash
# 備份配置文件
tar -czf config_backup_$(date +%Y%m%d).tar.gz config/

# 備份處理結果
tar -czf output_backup_$(date +%Y%m%d).tar.gz output/processed/
```

---

## 📊 目錄大小監控

### 檢查目錄大小
```bash
# 檢查各目錄大小
du -sh input/ output/ temp/ logs/

# 檢查總專案大小
du -sh .
```

### 大小限制建議
- `input/`：無限制（根據需求）
- `output/`：建議定期備份和清理
- `temp/`：< 5GB（自動清理）
- `logs/`：< 1GB（自動清理舊日誌）

---

## 🔒 權限設定

### 建議權限
```bash
# 設定目錄權限
chmod 755 input/ output/ examples/ config/
chmod 700 temp/ logs/

# 設定文件權限
chmod 644 *.py *.md *.txt *.json *.yaml
chmod 755 install.sh
```

### 安全注意事項
- `temp/` 和 `logs/` 目錄包含敏感信息，建議限制存取權限
- 定期清理暫存文件避免洩露處理內容
- 備份重要配置文件

---

**建立日期**：2024-01-31  
**最後更新**：2024-01-31  
**維護者**：專案開發團隊 