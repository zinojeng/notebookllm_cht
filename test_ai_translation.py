#!/usr/bin/env python3
"""
AI 翻譯功能測試腳本
測試 OpenAI o1-mini 和 Gemini 2.0 Flash Preview 的翻譯品質
"""

import os
import sys
from audio_processor import AudioProcessor
from dotenv import load_dotenv

def test_translation_providers():
    """測試不同的翻譯提供商"""
    
    # 載入環境變數
    load_dotenv()
    
    # 測試文本
    test_texts = [
        {
            "text": "Welcome to today's discussion about artificial intelligence and its impact on society.",
            "context": {"is_question": False, "is_response": False, "is_transition": True, "speaker": "A"}
        },
        {
            "text": "What do you think are the most significant challenges we face with AI development?",
            "context": {"is_question": True, "is_response": False, "is_transition": False, "speaker": "B"}
        },
        {
            "text": "Well, I believe the main concerns revolve around ethical considerations and job displacement.",
            "context": {"is_question": False, "is_response": True, "is_transition": False, "speaker": "A"}
        },
        {
            "text": "Speaking of ethics, how do we ensure AI systems are fair and unbiased?",
            "context": {"is_question": True, "is_response": False, "is_transition": True, "speaker": "B"}
        }
    ]
    
    # 測試不同的翻譯提供商
    providers = ['google', 'openai', 'gemini']
    
    for provider in providers:
        print(f"\n{'='*60}")
        print(f"🧪 測試翻譯提供商: {provider.upper()}")
        print(f"{'='*60}")
        
        # 設定翻譯提供商
        os.environ['TRANSLATION_PROVIDER'] = provider
        
        try:
            # 初始化處理器
            processor = AudioProcessor()
            
            # 測試每個文本
            for i, test_item in enumerate(test_texts, 1):
                print(f"\n📝 測試 {i}:")
                print(f"原文: {test_item['text']}")
                print(f"上下文: {test_item['context']}")
                
                try:
                    # 進行翻譯
                    translated = processor.translate_with_ai(
                        test_item['text'], 
                        test_item['context']
                    )
                    print(f"譯文: {translated}")
                    
                except Exception as e:
                    print(f"❌ 翻譯失敗: {e}")
                
                print("-" * 40)
                
        except Exception as e:
            print(f"❌ 初始化 {provider} 失敗: {e}")

def test_model_availability():
    """測試模型可用性"""
    print("🔍 檢查模型可用性...")
    
    # 檢查 OpenAI
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key and openai_key != 'sk-your_openai_api_key_here':
        print("✅ OpenAI API 金鑰已設定")
    else:
        print("❌ OpenAI API 金鑰未設定或使用範本值")
    
    # 檢查 Gemini
    gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    if gemini_key and gemini_key != 'your_gemini_api_key_here':
        print("✅ Gemini API 金鑰已設定")
    else:
        print("❌ Gemini API 金鑰未設定或使用範本值")
    
    # 檢查模型設定
    openai_model = os.getenv('OPENAI_MODEL', 'o1-mini')
    gemini_model = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
    
    print(f"🤖 OpenAI 模型: {openai_model}")
    print(f"🤖 Gemini 模型: {gemini_model}")

def main():
    """主程式"""
    print("🧪 AI 翻譯功能測試")
    print("=" * 60)
    
    # 載入環境變數
    load_dotenv()
    
    # 檢查模型可用性
    test_model_availability()
    
    # 詢問是否繼續測試
    response = input("\n是否繼續進行翻譯測試？ (y/N): ")
    if response.lower() != 'y':
        print("測試取消")
        return
    
    # 測試翻譯功能
    test_translation_providers()
    
    print("\n🎉 測試完成！")
    print("\n💡 提示：")
    print("- 如果某個提供商失敗，請檢查對應的 API 金鑰設定")
    print("- OpenAI o1-mini 提供最佳的上下文感知翻譯")
    print("- Gemini 2.0 Flash Preview 提供快速且高品質的翻譯")
    print("- Google 翻譯作為可靠的備用選項")

if __name__ == "__main__":
    main() 