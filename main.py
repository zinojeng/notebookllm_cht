#!/usr/bin/env python3
"""
NotebookLM 英文音頻轉中文 Podcast 處理器
將英文對話音頻轉換為自然的中文對話音頻
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path
from audio_processor import AudioProcessor

def validate_input_file(file_path: str) -> bool:
    """驗證輸入文件"""
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    if not file_path.lower().endswith('.wav'):
        print(f"❌ 僅支援 .wav 格式文件")
        return False
    
    return True

async def main():
    parser = argparse.ArgumentParser(
        description="將 NotebookLM 英文音頻概覽轉換為中文 Podcast",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  python main.py input.wav                    # 處理 input.wav，輸出到 output/ 目錄
  python main.py input.wav -o my_output/     # 指定輸出目錄
  python main.py input.wav --preview         # 僅生成逐字稿預覽
  
處理流程:
  1. 🎯 語音識別 (Whisper)
  2. 👥 對話分析與說話者檢測
  3. 🌐 英文轉中文翻譯
  4. 🎤 中文語音合成 (Edge TTS)
  5. 🎵 音頻合併與優化
        """
    )
    
    parser.add_argument(
        'input_file',
        help='輸入的 .wav 音頻文件路徑'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='輸出目錄 (預設: output/)'
    )
    
    parser.add_argument(
        '--preview',
        action='store_true',
        help='僅生成逐字稿預覽，不生成音頻'
    )
    
    parser.add_argument(
        '--voice-female',
        default='zh-TW-HsiaoChenNeural',
        help='女性聲音 (預設: zh-TW-HsiaoChenNeural)'
    )
    
    parser.add_argument(
        '--voice-male',
        default='zh-TW-YunJheNeural',
        help='男性聲音 (預設: zh-TW-YunJheNeural)'
    )
    
    args = parser.parse_args()
    
    # 驗證輸入文件
    if not validate_input_file(args.input_file):
        sys.exit(1)
    
    # 建立輸出目錄
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎙️  NotebookLM 英文音頻轉中文 Podcast 處理器")
    print("=" * 50)
    print(f"📁 輸入文件: {args.input_file}")
    print(f"📁 輸出目錄: {output_dir}")
    print(f"🎤 女性聲音: {args.voice_female}")
    print(f"🎤 男性聲音: {args.voice_male}")
    print("=" * 50)
    
    try:
        # 初始化處理器
        processor = AudioProcessor()
        
        # 自定義聲音設定
        processor.chinese_voices['female'] = args.voice_female
        processor.chinese_voices['male'] = args.voice_male
        
        if args.preview:
            # 僅預覽模式
            print("📋 預覽模式：僅生成逐字稿...")
            
            # 語音識別
            transcription = processor.transcribe_with_timestamps(args.input_file)
            if not transcription:
                print("❌ 語音識別失敗")
                sys.exit(1)
            
            # 對話分析
            dialogue_segments = processor.detect_speakers_and_dialogue(transcription['segments'])
            
            # 翻譯
            translated_segments = processor.translate_with_context(dialogue_segments)
            
            # 保存逐字稿
            transcript_path = output_dir / "transcript_preview.json"
            processor.save_transcript(translated_segments, str(transcript_path))
            
            # 顯示預覽
            print("\n📋 逐字稿預覽:")
            print("-" * 40)
            for i, segment in enumerate(translated_segments[:5]):  # 顯示前5段
                print(f"[{segment['start']:.1f}s-{segment['end']:.1f}s] 說話者{segment['speaker']}:")
                print(f"  英文: {segment['original_text']}")
                print(f"  中文: {segment['translated_text']}")
                print()
            
            if len(translated_segments) > 5:
                print(f"... 還有 {len(translated_segments) - 5} 段內容")
            
            print(f"✅ 完整逐字稿已保存至: {transcript_path}")
            
        else:
            # 完整處理模式
            result = await processor.process_audio_complete(
                args.input_file,
                str(output_dir)
            )
            
            if result:
                print("\n🎉 處理完成！")
                print("=" * 50)
                print(f"📄 逐字稿: {result['transcript']}")
                print(f"🎵 中文音頻: {result['chinese_audio']}")
                print(f"📊 片段數量: {result['segments_count']}")
                print(f"⏱️  總時長: {result['total_duration']:.2f} 秒")
                print("\n🎧 您現在可以播放生成的中文 Podcast 了！")
            else:
                print("❌ 處理失敗")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⚠️  處理被用戶中斷")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 處理過程中發生錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 