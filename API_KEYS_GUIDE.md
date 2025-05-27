# API 金鑰設定指南

## 📋 概述

本指南將協助您設定 NotebookLM 中文 Podcast 處理器所需的 API 金鑰。根據您選擇的服務提供商，您可能需要設定不同的 API 金鑰。

## 🚀 快速開始

### 1. 建立 .env 文件
```bash
# 使用環境變數管理工具
python env_manager.py create

# 或手動複製範本
cp config/env_template.txt .env
```

### 2. 編輯 .env 文件
```bash
# 使用您喜歡的編輯器
nano .env
# 或
code .env
```

### 3. 驗證設定
```bash
python env_manager.py validate
```

---

## 🔑 API 金鑰設定

### 🎯 推薦配置（免費開始）

**最小設定**：使用免費服務
```env
# 基本設定（使用免費的 Edge TTS）
DEFAULT_TTS_PROVIDER=edge
TRANSLATION_PROVIDER=google
WHISPER_MODEL=base

# Edge TTS 聲音（免費）
EDGE_TTS_VOICE_FEMALE=zh-TW-HsiaoChenNeural
EDGE_TTS_VOICE_MALE=zh-TW-YunJheNeural
```

### 🌟 OpenAI API

**用途**：高品質翻譯、TTS、GPT 增強
**費用**：按使用量計費

#### 獲取方式：
1. 前往 [OpenAI Platform](https://platform.openai.com/)
2. 註冊並登入帳戶
3. 前往 [API Keys](https://platform.openai.com/api-keys)
4. 點擊 "Create new secret key"
5. 複製金鑰並保存

#### 設定：
```env
OPENAI_API_KEY=sk-your_actual_api_key_here
OPENAI_ORG_ID=org-your_organization_id_here  # 可選
```

#### 使用：
```env
# 使用 OpenAI 進行翻譯
TRANSLATION_PROVIDER=openai

# 使用 OpenAI TTS
DEFAULT_TTS_PROVIDER=openai
```

### 🌍 Google Cloud API

**用途**：Google 翻譯、語音服務
**費用**：有免費額度，超出後按使用量計費

#### 獲取方式：
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 Cloud Translation API 和 Text-to-Speech API
4. 建立服務帳戶金鑰：
   - 前往 IAM & Admin > Service Accounts
   - 建立服務帳戶
   - 下載 JSON 金鑰文件

#### 設定：
```env
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_TRANSLATE_API_KEY=your_api_key  # 或使用服務帳戶
```

### 🔷 Azure Cognitive Services

**用途**：Azure 翻譯、語音服務
**費用**：有免費層級

#### 獲取方式：
1. 前往 [Azure Portal](https://portal.azure.com/)
2. 建立 Cognitive Services 資源
3. 選擇 Speech Services 或 Translator
4. 在資源的 "Keys and Endpoint" 頁面取得金鑰

#### 設定：
```env
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=eastus  # 您的資源區域
```

### 🔵 DeepL API

**用途**：高品質翻譯
**費用**：有免費額度（每月 500,000 字元）

#### 獲取方式：
1. 前往 [DeepL API](https://www.deepl.com/pro-api)
2. 註冊 DeepL Pro 帳戶
3. 在帳戶設定中取得 API 金鑰

#### 設定：
```env
DEEPL_API_KEY=your_deepl_api_key
TRANSLATION_PROVIDER=deepl
```

### 🎵 ElevenLabs API

**用途**：高品質 AI 語音合成
**費用**：有免費額度

#### 獲取方式：
1. 前往 [ElevenLabs](https://elevenlabs.io/)
2. 註冊帳戶
3. 在 Profile Settings 中取得 API 金鑰

#### 設定：
```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key
DEFAULT_TTS_PROVIDER=elevenlabs
```

### 🤗 Hugging Face

**用途**：開源模型、額外功能
**費用**：基本使用免費

#### 獲取方式：
1. 前往 [Hugging Face](https://huggingface.co/)
2. 註冊並登入
3. 前往 Settings > Access Tokens
4. 建立新的 token

#### 設定：
```env
HUGGINGFACE_API_TOKEN=hf_your_token_here
```

---

## 🛠️ 服務提供商選擇建議

### 💰 預算考量

**免費開始**：
```env
DEFAULT_TTS_PROVIDER=edge          # 免費
TRANSLATION_PROVIDER=google        # 有免費額度
WHISPER_MODEL=base                 # 本地處理
```

**低成本**：
```env
DEFAULT_TTS_PROVIDER=edge          # 免費
TRANSLATION_PROVIDER=deepl         # 免費額度大
WHISPER_MODEL=small                # 更好品質
```

**高品質**：
```env
DEFAULT_TTS_PROVIDER=elevenlabs    # 最佳語音品質
TRANSLATION_PROVIDER=openai        # 上下文感知翻譯
WHISPER_MODEL=medium               # 更高準確度
```

### 🌏 地區考量

**台灣用戶**：
- Google Translate：支援繁體中文
- Edge TTS：優秀的台灣中文聲音
- DeepL：翻譯品質佳

**中國大陸用戶**：
- Azure：在中國有服務
- 本地 Whisper：避免網路限制

### 🎯 使用場景

**個人使用**：
- Edge TTS + Google Translate
- 成本低，品質可接受

**商業使用**：
- ElevenLabs + OpenAI
- 最佳品質，適合專業用途

**大量處理**：
- Azure + DeepL
- 穩定性好，成本可控

---

## 🔒 安全最佳實踐

### 1. 保護 API 金鑰
```bash
# 設定文件權限
chmod 600 .env

# 確保 .env 在 .gitignore 中
echo ".env" >> .gitignore
```

### 2. 使用環境變數
```bash
# 在生產環境中直接設定環境變數
export OPENAI_API_KEY="your_key_here"
```

### 3. 定期輪換金鑰
- 定期更新 API 金鑰
- 監控使用量和異常活動
- 使用最小權限原則

### 4. 備份重要設定
```bash
# 備份配置（不包含敏感信息）
cp .env .env.backup
# 移除敏感信息後再備份
```

---

## 🧪 測試設定

### 驗證 API 金鑰
```bash
# 使用環境變數管理工具
python env_manager.py validate

# 顯示當前配置
python env_manager.py show
```

### 測試各項服務
```bash
# 測試語音識別
python -c "import whisper; print('Whisper OK')"

# 測試 Edge TTS
python -c "import edge_tts; print('Edge TTS OK')"

# 測試翻譯（需要 API 金鑰）
python -c "from googletrans import Translator; print('Google Translate OK')"
```

---

## ❓ 常見問題

### Q: 我需要設定所有的 API 金鑰嗎？
A: 不需要。您只需要設定您選擇使用的服務的 API 金鑰。推薦從免費的 Edge TTS 開始。

### Q: API 金鑰會被上傳到 GitHub 嗎？
A: 不會。`.env` 文件已經在 `.gitignore` 中，不會被版本控制追蹤。

### Q: 如何知道我的 API 用量？
A: 大部分服務提供商都有使用量儀表板：
- OpenAI: [Usage Dashboard](https://platform.openai.com/usage)
- Google Cloud: [Billing](https://console.cloud.google.com/billing)
- Azure: [Cost Management](https://portal.azure.com/#blade/Microsoft_Azure_CostManagement)

### Q: API 金鑰過期了怎麼辦？
A: 重新生成新的金鑰並更新 `.env` 文件中的對應值。

---

**建立日期**：2024-01-31  
**最後更新**：2024-01-31  
**維護者**：專案開發團隊 