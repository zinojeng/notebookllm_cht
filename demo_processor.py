#!/usr/bin/env python3
"""
NotebookLM 中文 Podcast 處理器 - 示範腳本
將英文 NotebookLM 音頻轉換為自然的中文對話 Podcast

使用方法:
python demo_processor.py [input_audio.wav]
"""

import os
import sys
import asyncio
from pathlib import Path
from audio_processor import AudioProcessor
from dotenv import load_dotenv

def create_sample_audio():
    """創建示範音頻文件（如果沒有輸入文件）"""
    print("🎵 創建示範音頻文件...")
    
    # 創建一個簡單的示範音頻（靜音）
    from pydub import AudioSegment
    from pydub.generators import Sine
    
    # 創建 30 秒的示範音頻
    sample_audio = AudioSegment.silent(duration=30000)  # 30秒靜音
    
    # 添加一些音調來模擬對話
    tone1 = Sine(440).to_audio_segment(duration=2000)  # A4 音調 2秒
    tone2 = Sine(523).to_audio_segment(duration=2000)  # C5 音調 2秒
    
    # 組合音頻
    sample_audio = sample_audio[:5000] + tone1 + sample_audio[7000:15000] + tone2 + sample_audio[17000:]
    
    # 保存示範文件
    sample_path = "input/sample_notebookllm.wav"
    os.makedirs("input", exist_ok=True)
    sample_audio.export(sample_path, format="wav")
    
    print(f"✅ 示範音頻已創建: {sample_path}")
    return sample_path

def create_sample_transcript():
    """創建示範轉錄文本（用於測試翻譯功能）"""
    sample_segments = [
        {
            'start': 0.0,
            'end': 5.0,
            'text': "Welcome to today's discussion about artificial intelligence and its transformative impact on modern society.",
            'words': [],
            'speaker': 'A',
            'is_question': False,
            'is_response': False,
            'is_transition': True
        },
        {
            'start': 5.5,
            'end': 12.0,
            'text': "What do you think are the most significant challenges we face with AI development in the coming years?",
            'words': [],
            'speaker': 'B',
            'is_question': True,
            'is_response': False,
            'is_transition': False
        },
        {
            'start': 12.5,
            'end': 20.0,
            'text': "Well, I believe the main concerns revolve around ethical considerations, job displacement, and ensuring AI systems remain beneficial to humanity.",
            'words': [],
            'speaker': 'A',
            'is_question': False,
            'is_response': True,
            'is_transition': False
        },
        {
            'start': 20.5,
            'end': 28.0,
            'text': "Speaking of ethics, how do we ensure AI systems are fair, transparent, and free from harmful biases?",
            'words': [],
            'speaker': 'B',
            'is_question': True,
            'is_response': False,
            'is_transition': True
        }
    ]
    
    return {
        'text': ' '.join([seg['text'] for seg in sample_segments]),
        'segments': sample_segments,
        'language': 'en'
    }

async def demo_translation_only():
    """示範純翻譯功能（不需要音頻文件）"""
    print("\n🧪 示範翻譯功能...")
    
    processor = AudioProcessor()
    
    # 使用示範轉錄文本
    transcription = create_sample_transcript()
    
    # 對話分析
    dialogue_segments = processor.detect_speakers_and_dialogue(transcription['segments'])
    
    # 翻譯
    translated_segments = processor.translate_with_context(dialogue_segments)
    
    # 顯示結果
    print("\n📝 翻譯結果:")
    print("=" * 60)
    
    for i, segment in enumerate(translated_segments, 1):
        print(f"\n片段 {i} ({segment['speaker']}):")
        print(f"原文: {segment['original_text']}")
        print(f"譯文: {segment['translated_text']}")
        
        # 顯示對話特徵
        features = []
        if segment.get('is_question'):
            features.append("問句")
        if segment.get('is_response'):
            features.append("回應")
        if segment.get('is_transition'):
            features.append("轉場")
        
        if features:
            print(f"特徵: {', '.join(features)}")
    
    return translated_segments

async def demo_full_process(input_path: str):
    """示範完整處理流程"""
    print(f"\n🚀 開始完整處理流程: {input_path}")
    
    processor = AudioProcessor()
    
    # 創建輸出目錄
    output_dir = "output/demo_result"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 完整處理
        result = await processor.process_audio_complete(input_path, output_dir)
        
        if result:
            print("\n🎉 處理完成！")
            print("=" * 50)
            print(f"原始音頻: {result['original_audio']}")
            print(f"中文音頻: {result['chinese_audio']}")
            print(f"逐字稿: {result['transcript']}")
            print(f"片段數量: {result['segments_count']}")
            print(f"總時長: {result['total_duration']:.2f} 秒")
            
            return result
        else:
            print("❌ 處理失敗")
            return None
            
    except Exception as e:
        print(f"❌ 處理過程中發生錯誤: {e}")
        return None

def check_environment():
    """檢查環境設定"""
    print("🔍 檢查環境設定...")
    
    # 檢查 API 金鑰
    openai_key = os.getenv('OPENAI_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    
    print(f"OpenAI API: {'✅ 已設定' if openai_key and openai_key != 'sk-your_openai_api_key_here' else '❌ 未設定'}")
    print(f"Gemini API: {'✅ 已設定' if gemini_key and gemini_key != 'your_gemini_api_key_here' else '❌ 未設定'}")
    
    # 檢查目錄
    required_dirs = ['input', 'output', 'temp']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            print(f"📁 已創建目錄: {dir_name}")
        else:
            print(f"📁 目錄存在: {dir_name}")

async def main():
    """主程式"""
    print("🎙️  NotebookLM 中文 Podcast 處理器 - 示範")
    print("=" * 60)
    
    # 載入環境變數
    load_dotenv()
    
    # 檢查環境
    check_environment()
    
    # 檢查命令行參數
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        if not os.path.exists(input_path):
            print(f"❌ 找不到輸入文件: {input_path}")
            return
    else:
        print("\n💡 未提供輸入文件，將使用示範模式")
        
        # 詢問用戶選擇
        print("\n請選擇示範模式:")
        print("1. 純翻譯示範（不需要音頻文件）")
        print("2. 完整流程示範（使用示範音頻）")
        print("3. 退出")
        
        choice = input("\n請輸入選擇 (1-3): ").strip()
        
        if choice == "1":
            await demo_translation_only()
            return
        elif choice == "2":
            input_path = create_sample_audio()
        elif choice == "3":
            print("退出示範")
            return
        else:
            print("❌ 無效選擇")
            return
    
    # 執行完整處理流程
    result = await demo_full_process(input_path)
    
    if result:
        print("\n💡 提示:")
        print("- 檢查輸出目錄中的結果文件")
        print("- 如果翻譯品質不理想，請檢查 API 金鑰設定")
        print("- 可以調整 .env 文件中的模型和聲音設定")

if __name__ == "__main__":
    asyncio.run(main()) 