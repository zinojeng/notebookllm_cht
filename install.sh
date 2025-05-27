#!/bin/bash

# NotebookLM 英文音頻轉中文 Podcast 處理器 - 自動安裝腳本

set -e  # 遇到錯誤時停止執行

echo "🎙️  NotebookLM 英文音頻轉中文 Podcast 處理器"
echo "================================================"
echo "開始自動安裝..."

# 檢查 Python 版本
check_python() {
    echo "🔍 檢查 Python 版本..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "❌ 錯誤：未找到 Python。請先安裝 Python 3.8 或更高版本。"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo "✅ 找到 Python $PYTHON_VERSION"
    
    # 檢查版本是否符合要求（3.8+）
    if ! $PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        echo "❌ 錯誤：需要 Python 3.8 或更高版本，當前版本：$PYTHON_VERSION"
        exit 1
    fi
}

# 檢查並安裝 FFmpeg
install_ffmpeg() {
    echo "🔍 檢查 FFmpeg..."
    
    if command -v ffmpeg &> /dev/null; then
        echo "✅ FFmpeg 已安裝"
        return
    fi
    
    echo "📦 安裝 FFmpeg..."
    
    # 檢測作業系統
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "❌ 錯誤：需要 Homebrew 來安裝 FFmpeg。請先安裝 Homebrew："
            echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y ffmpeg
        elif command -v yum &> /dev/null; then
            sudo yum install -y ffmpeg
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y ffmpeg
        else
            echo "❌ 錯誤：無法自動安裝 FFmpeg。請手動安裝 FFmpeg。"
            exit 1
        fi
    else
        echo "❌ 錯誤：不支援的作業系統。請手動安裝 FFmpeg。"
        exit 1
    fi
    
    echo "✅ FFmpeg 安裝完成"
}

# 建立虛擬環境
setup_venv() {
    echo "🏗️  建立虛擬環境..."
    
    if [ -d "venv" ]; then
        echo "⚠️  虛擬環境已存在，跳過建立"
    else
        $PYTHON_CMD -m venv venv
        echo "✅ 虛擬環境建立完成"
    fi
    
    # 啟動虛擬環境
    echo "🔄 啟動虛擬環境..."
    source venv/bin/activate
    
    # 升級 pip
    echo "⬆️  升級 pip..."
    pip install --upgrade pip
}

# 安裝 Python 依賴
install_dependencies() {
    echo "📦 安裝 Python 依賴套件..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        echo "✅ 依賴套件安裝完成"
    else
        echo "❌ 錯誤：找不到 requirements.txt 文件"
        exit 1
    fi
}

# 測試安裝
test_installation() {
    echo "🧪 測試安裝..."
    
    # 測試主要模組是否可以導入
    $PYTHON_CMD -c "
import whisper
import edge_tts
import pydub
from deep_translator import GoogleTranslator
print('✅ 所有模組導入成功')
"
    
    if [ $? -eq 0 ]; then
        echo "✅ 安裝測試通過"
    else
        echo "❌ 安裝測試失敗"
        exit 1
    fi
}

# 建立範例文件
create_examples() {
    echo "📝 建立範例文件..."
    
    mkdir -p examples
    
    # 建立範例使用腳本
    cat > examples/example_usage.sh << 'EOF'
#!/bin/bash

# 範例使用腳本

echo "NotebookLM 中文 Podcast 處理器 - 使用範例"
echo "=========================================="

# 啟動虛擬環境
source ../venv/bin/activate

echo "1. 單文件處理範例："
echo "   python ../main.py your_audio.wav"
echo ""

echo "2. 指定輸出目錄："
echo "   python ../main.py your_audio.wav -o my_output/"
echo ""

echo "3. 僅生成逐字稿預覽："
echo "   python ../main.py your_audio.wav --preview"
echo ""

echo "4. 批次處理範例："
echo "   python ../batch_processor.py audio_folder/ -o batch_output/"
echo ""

echo "5. 自定義聲音："
echo "   python ../main.py your_audio.wav --voice-female zh-TW-HsiaoYuNeural"
echo ""

echo "請將您的 .wav 文件放在此目錄中，然後運行相應的命令。"
EOF

    chmod +x examples/example_usage.sh
    
    # 建立測試用的空文件夾
    mkdir -p examples/input_audio
    mkdir -p examples/output
    
    echo "✅ 範例文件建立完成"
}

# 顯示使用說明
show_usage() {
    echo ""
    echo "🎉 安裝完成！"
    echo "=============="
    echo ""
    echo "📁 專案結構："
    echo "   ├── main.py              # 單文件處理"
    echo "   ├── batch_processor.py   # 批次處理"
    echo "   ├── audio_processor.py   # 核心處理邏輯"
    echo "   ├── requirements.txt     # 依賴列表"
    echo "   ├── README.md           # 詳細說明"
    echo "   ├── venv/               # 虛擬環境"
    echo "   └── examples/           # 使用範例"
    echo ""
    echo "🚀 快速開始："
    echo "   1. 啟動虛擬環境："
    echo "      source venv/bin/activate"
    echo ""
    echo "   2. 處理單個音頻文件："
    echo "      python main.py your_audio.wav"
    echo ""
    echo "   3. 批次處理多個文件："
    echo "      python batch_processor.py audio_folder/"
    echo ""
    echo "   4. 查看詳細說明："
    echo "      python main.py --help"
    echo ""
    echo "📖 更多資訊請參閱 README.md"
    echo ""
    echo "🎧 享受您的中文 Podcast 體驗！"
}

# 主安裝流程
main() {
    echo "開始安裝流程..."
    
    check_python
    install_ffmpeg
    setup_venv
    install_dependencies
    test_installation
    create_examples
    show_usage
    
    echo ""
    echo "✅ 安裝完成！您現在可以開始使用 NotebookLM 中文 Podcast 處理器了。"
}

# 錯誤處理
trap 'echo "❌ 安裝過程中發生錯誤。請檢查上面的錯誤訊息。"; exit 1' ERR

# 執行主函數
main "$@" 