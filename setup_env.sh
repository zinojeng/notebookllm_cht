#!/bin/bash

# NotebookLM 中文 Podcast 處理器 - 環境變數快速設定腳本

set -e

echo "🔧 NotebookLM 中文 Podcast 處理器 - 環境變數設定"
echo "=================================================="

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查是否在正確的目錄
if [ ! -f "audio_processor.py" ]; then
    echo -e "${RED}❌ 錯誤：請在專案根目錄執行此腳本${NC}"
    exit 1
fi

# 函數：檢查 .env 文件
check_env_file() {
    if [ -f ".env" ]; then
        echo -e "${YELLOW}⚠️  .env 文件已存在${NC}"
        read -p "是否要覆蓋現有的 .env 文件？ (y/N): " overwrite
        if [ "$overwrite" != "y" ] && [ "$overwrite" != "Y" ]; then
            echo -e "${BLUE}ℹ️  保留現有的 .env 文件${NC}"
            return 1
        fi
    fi
    return 0
}

# 函數：建立 .env 文件
create_env_file() {
    echo -e "${BLUE}📝 建立 .env 文件...${NC}"
    
    if [ ! -f "config/env_template.txt" ]; then
        echo -e "${RED}❌ 找不到範本文件: config/env_template.txt${NC}"
        exit 1
    fi
    
    cp config/env_template.txt .env
    echo -e "${GREEN}✅ .env 文件建立完成${NC}"
}

# 函數：互動式設定基本配置
interactive_setup() {
    echo -e "${BLUE}🎯 互動式基本設定${NC}"
    echo "請選擇您的使用場景："
    echo "1) 免費開始（Edge TTS + Google 翻譯）"
    echo "2) 低成本（Edge TTS + DeepL 翻譯）"
    echo "3) 高品質（ElevenLabs + OpenAI）"
    echo "4) 自定義設定"
    echo "5) 跳過，稍後手動設定"
    
    read -p "請選擇 (1-5): " scenario
    
    case $scenario in
        1)
            setup_free_tier
            ;;
        2)
            setup_low_cost
            ;;
        3)
            setup_high_quality
            ;;
        4)
            setup_custom
            ;;
        5)
            echo -e "${BLUE}ℹ️  跳過自動設定，請手動編輯 .env 文件${NC}"
            ;;
        *)
            echo -e "${YELLOW}⚠️  無效選項，使用預設設定${NC}"
            setup_free_tier
            ;;
    esac
}

# 函數：免費方案設定
setup_free_tier() {
    echo -e "${GREEN}🆓 設定免費方案...${NC}"
    
    # 更新 .env 文件
    sed -i.bak 's/DEFAULT_TTS_PROVIDER=.*/DEFAULT_TTS_PROVIDER=edge/' .env
    sed -i.bak 's/TRANSLATION_PROVIDER=.*/TRANSLATION_PROVIDER=google/' .env
    sed -i.bak 's/WHISPER_MODEL=.*/WHISPER_MODEL=base/' .env
    
    echo "✅ 免費方案設定完成"
    echo "   - TTS: Edge TTS (免費)"
    echo "   - 翻譯: Google Translate (有免費額度)"
    echo "   - 語音識別: Whisper Base (本地)"
}

# 函數：低成本方案設定
setup_low_cost() {
    echo -e "${YELLOW}💰 設定低成本方案...${NC}"
    
    # 更新 .env 文件
    sed -i.bak 's/DEFAULT_TTS_PROVIDER=.*/DEFAULT_TTS_PROVIDER=edge/' .env
    sed -i.bak 's/TRANSLATION_PROVIDER=.*/TRANSLATION_PROVIDER=deepl/' .env
    sed -i.bak 's/WHISPER_MODEL=.*/WHISPER_MODEL=small/' .env
    
    echo "✅ 低成本方案設定完成"
    echo "   - TTS: Edge TTS (免費)"
    echo "   - 翻譯: DeepL (免費額度大)"
    echo "   - 語音識別: Whisper Small (更好品質)"
    
    echo ""
    echo -e "${BLUE}📝 請設定 DeepL API 金鑰：${NC}"
    read -p "DeepL API Key (可稍後設定): " deepl_key
    if [ ! -z "$deepl_key" ]; then
        sed -i.bak "s/DEEPL_API_KEY=.*/DEEPL_API_KEY=$deepl_key/" .env
        echo "✅ DeepL API 金鑰已設定"
    fi
}

# 函數：高品質方案設定
setup_high_quality() {
    echo -e "${GREEN}⭐ 設定高品質方案...${NC}"
    
    # 更新 .env 文件
    sed -i.bak 's/DEFAULT_TTS_PROVIDER=.*/DEFAULT_TTS_PROVIDER=elevenlabs/' .env
    sed -i.bak 's/TRANSLATION_PROVIDER=.*/TRANSLATION_PROVIDER=openai/' .env
    sed -i.bak 's/WHISPER_MODEL=.*/WHISPER_MODEL=medium/' .env
    
    echo "✅ 高品質方案設定完成"
    echo "   - TTS: ElevenLabs (最佳語音品質)"
    echo "   - 翻譯: OpenAI (上下文感知)"
    echo "   - 語音識別: Whisper Medium (高準確度)"
    
    echo ""
    echo -e "${BLUE}📝 請設定 API 金鑰：${NC}"
    
    read -p "OpenAI API Key: " openai_key
    if [ ! -z "$openai_key" ]; then
        sed -i.bak "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$openai_key/" .env
        echo "✅ OpenAI API 金鑰已設定"
    fi
    
    read -p "ElevenLabs API Key: " elevenlabs_key
    if [ ! -z "$elevenlabs_key" ]; then
        sed -i.bak "s/ELEVENLABS_API_KEY=.*/ELEVENLABS_API_KEY=$elevenlabs_key/" .env
        echo "✅ ElevenLabs API 金鑰已設定"
    fi
}

# 函數：自定義設定
setup_custom() {
    echo -e "${BLUE}🛠️  自定義設定${NC}"
    
    echo "選擇 TTS 提供商："
    echo "1) Edge TTS (免費)"
    echo "2) OpenAI TTS"
    echo "3) ElevenLabs"
    read -p "選擇 (1-3): " tts_choice
    
    case $tts_choice in
        1) sed -i.bak 's/DEFAULT_TTS_PROVIDER=.*/DEFAULT_TTS_PROVIDER=edge/' .env ;;
        2) sed -i.bak 's/DEFAULT_TTS_PROVIDER=.*/DEFAULT_TTS_PROVIDER=openai/' .env ;;
        3) sed -i.bak 's/DEFAULT_TTS_PROVIDER=.*/DEFAULT_TTS_PROVIDER=elevenlabs/' .env ;;
    esac
    
    echo "選擇翻譯提供商："
    echo "1) Google Translate"
    echo "2) DeepL"
    echo "3) OpenAI"
    read -p "選擇 (1-3): " trans_choice
    
    case $trans_choice in
        1) sed -i.bak 's/TRANSLATION_PROVIDER=.*/TRANSLATION_PROVIDER=google/' .env ;;
        2) sed -i.bak 's/TRANSLATION_PROVIDER=.*/TRANSLATION_PROVIDER=deepl/' .env ;;
        3) sed -i.bak 's/TRANSLATION_PROVIDER=.*/TRANSLATION_PROVIDER=openai/' .env ;;
    esac
    
    echo "選擇 Whisper 模型："
    echo "1) tiny (最快)"
    echo "2) base (平衡)"
    echo "3) small (更好)"
    echo "4) medium (高品質)"
    read -p "選擇 (1-4): " whisper_choice
    
    case $whisper_choice in
        1) sed -i.bak 's/WHISPER_MODEL=.*/WHISPER_MODEL=tiny/' .env ;;
        2) sed -i.bak 's/WHISPER_MODEL=.*/WHISPER_MODEL=base/' .env ;;
        3) sed -i.bak 's/WHISPER_MODEL=.*/WHISPER_MODEL=small/' .env ;;
        4) sed -i.bak 's/WHISPER_MODEL=.*/WHISPER_MODEL=medium/' .env ;;
    esac
    
    echo "✅ 自定義設定完成"
}

# 函數：設定文件權限
set_permissions() {
    echo -e "${BLUE}🔒 設定文件權限...${NC}"
    chmod 600 .env
    echo "✅ .env 文件權限設定為 600 (僅擁有者可讀寫)"
}

# 函數：驗證設定
validate_setup() {
    echo -e "${BLUE}🧪 驗證設定...${NC}"
    
    if command -v python3 &> /dev/null; then
        python3 env_manager.py validate
    elif command -v python &> /dev/null; then
        python env_manager.py validate
    else
        echo -e "${YELLOW}⚠️  找不到 Python，請手動驗證設定${NC}"
    fi
}

# 函數：顯示後續步驟
show_next_steps() {
    echo ""
    echo -e "${GREEN}🎉 環境變數設定完成！${NC}"
    echo "=================================================="
    echo ""
    echo "📋 後續步驟："
    echo "1. 編輯 .env 文件並填入您的 API 金鑰："
    echo "   nano .env"
    echo ""
    echo "2. 驗證設定："
    echo "   python env_manager.py validate"
    echo ""
    echo "3. 查看當前配置："
    echo "   python env_manager.py show"
    echo ""
    echo "4. 開始處理音頻："
    echo "   python main.py input/samples/your_audio.wav"
    echo ""
    echo "📚 更多資訊請參考："
    echo "   - API_KEYS_GUIDE.md - API 金鑰設定指南"
    echo "   - QUICKSTART.md - 快速開始指南"
    echo "   - README.md - 完整說明文檔"
}

# 主程式
main() {
    echo "開始環境變數設定流程..."
    echo ""
    
    # 檢查並建立 .env 文件
    if check_env_file; then
        create_env_file
        interactive_setup
        set_permissions
        validate_setup
        show_next_steps
    else
        echo -e "${BLUE}ℹ️  使用現有的 .env 文件${NC}"
        validate_setup
    fi
}

# 執行主程式
main "$@" 