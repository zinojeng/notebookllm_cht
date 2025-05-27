# 環境變數設定摘要

## 🚀 快速開始

### 1. 建立 .env 文件
```bash
# 方法一：使用互動式工具（推薦）
./setup_env.sh

# 方法二：使用 Python 工具
python env_manager.py create

# 方法三：手動複製
cp config/env_template.txt .env
```

### 2. 選擇使用方案

#### 🆓 免費方案（推薦新手）
```env
DEFAULT_TTS_PROVIDER=edge
TRANSLATION_PROVIDER=google
WHISPER_MODEL=base
```
- **優點**：完全免費，立即可用
- **缺點**：翻譯品質一般
- **適合**：測試、個人使用

#### 💰 低成本方案
```env
DEFAULT_TTS_PROVIDER=edge
TRANSLATION_PROVIDER=deepl
WHISPER_MODEL=small
DEEPL_API_KEY=your_deepl_key
```
- **優點**：翻譯品質好，成本低
- **缺點**：需要註冊 DeepL
- **適合**：經常使用者

#### ⭐ 高品質方案
```env
DEFAULT_TTS_PROVIDER=elevenlabs
TRANSLATION_PROVIDER=openai
WHISPER_MODEL=medium
OPENAI_API_KEY=sk-your_key
ELEVENLABS_API_KEY=your_key
```
- **優點**：最佳品質
- **缺點**：成本較高
- **適合**：專業用途

### 3. 驗證設定
```bash
python env_manager.py validate
python env_manager.py show
```

## 🔑 必要的 API 金鑰

### 免費開始
- **無需任何 API 金鑰**
- 使用 Edge TTS（免費）+ Google Translate（免費額度）

### 進階使用
根據選擇的服務設定對應金鑰：

| 服務 | 用途 | 免費額度 | 獲取方式 |
|------|------|----------|----------|
| OpenAI | 翻譯、TTS | 無 | [platform.openai.com](https://platform.openai.com/) |
| DeepL | 翻譯 | 500K 字元/月 | [deepl.com/pro-api](https://www.deepl.com/pro-api) |
| ElevenLabs | TTS | 10K 字元/月 | [elevenlabs.io](https://elevenlabs.io/) |
| Google Cloud | 翻譯、TTS | 有免費額度 | [console.cloud.google.com](https://console.cloud.google.com/) |
| Azure | 翻譯、TTS | 有免費層級 | [portal.azure.com](https://portal.azure.com/) |

## 🛠️ 常用命令

```bash
# 建立 .env 文件
python env_manager.py create

# 驗證設定
python env_manager.py validate

# 查看配置
python env_manager.py show

# 互動式設定
./setup_env.sh

# 測試處理（使用預設設定）
python main.py input/samples/test.wav
```

## 🔒 安全提醒

1. **保護 API 金鑰**：
   ```bash
   chmod 600 .env  # 設定安全權限
   ```

2. **不要提交到版本控制**：
   - `.env` 已在 `.gitignore` 中
   - 永遠不要將 API 金鑰推送到 GitHub

3. **定期檢查使用量**：
   - 監控各服務的 API 使用量
   - 設定使用量警告

## ❓ 常見問題

**Q: 我需要設定所有的 API 金鑰嗎？**
A: 不需要。從免費方案開始，只設定您要使用的服務的金鑰。

**Q: 如何知道哪個方案適合我？**
A: 建議從免費方案開始測試，根據需求逐步升級。

**Q: API 金鑰安全嗎？**
A: 只要正確設定文件權限且不提交到版本控制，就是安全的。

**Q: 忘記設定某個 API 金鑰會怎樣？**
A: 系統會自動降級到可用的服務，或顯示警告訊息。

---

📚 **詳細說明**：[API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)  
🚀 **快速開始**：[QUICKSTART.md](QUICKSTART.md)  
📖 **完整文檔**：[README.md](README.md) 