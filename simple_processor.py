#!/usr/bin/env python3
"""
NotebookLM 中文 Podcast 處理器 - 簡化版
專注於翻譯功能，展示 AI 翻譯能力

使用方法:
python simple_processor.py
"""

import os
import asyncio
import edge_tts
from deep_translator import GoogleTranslator
import json
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# API 支援
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class SimpleProcessor:
    def __init__(self):
        """初始化簡化處理器"""
        # 載入環境變數
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        # 設定翻譯提供商
        self.translation_provider = os.getenv('TRANSLATION_PROVIDER', 'google').lower()
        
        # 初始化翻譯器
        self._init_translators()
        
        # 中文語音設定
        self.chinese_voices = {
            'female': os.getenv('EDGE_TTS_VOICE_FEMALE', 'zh-TW-HsiaoChenNeural'),
            'male': os.getenv('EDGE_TTS_VOICE_MALE', 'zh-TW-YunJheNeural')
        }
        
        print(f"🔧 簡化處理器初始化完成")
        print(f"   翻譯提供商: {self.translation_provider}")
        print(f"   女性聲音: {self.chinese_voices['female']}")
        print(f"   男性聲音: {self.chinese_voices['male']}")
    
    def _init_translators(self):
        """初始化翻譯器"""
        self.translator = GoogleTranslator(source='en', target='zh-TW')
        
        # 從環境變數獲取模型名稱
        self.openai_model = os.getenv('OPENAI_MODEL', 'o1-mini')
        self.gemini_model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        
        # 初始化 OpenAI
        if self.openai_api_key and OPENAI_AVAILABLE:
            self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
            print(f"✅ OpenAI 客戶端初始化完成 (模型: {self.openai_model})")
        else:
            self.openai_client = None
            if self.translation_provider == 'openai':
                print("⚠️  OpenAI API 金鑰未設定，將使用 Google 翻譯")
                self.translation_provider = 'google'
        
        # 初始化 Gemini
        if self.gemini_api_key and GEMINI_AVAILABLE:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel(self.gemini_model_name)
            print(f"✅ Gemini 客戶端初始化完成 (模型: {self.gemini_model_name})")
        else:
            self.gemini_model = None
            if self.translation_provider == 'gemini':
                print("⚠️  Gemini API 金鑰未設定，將使用 Google 翻譯")
                self.translation_provider = 'google'
    
    def translate_with_ai(self, text: str, context: Dict = None) -> str:
        """使用 AI 模型進行智能翻譯"""
        if self.translation_provider == 'openai' and self.openai_client:
            return self._translate_with_openai(text, context)
        elif self.translation_provider == 'gemini' and self.gemini_model:
            return self._translate_with_gemini(text, context)
        else:
            # 回退到 Google 翻譯
            return self.translator.translate(text)
    
    def _translate_with_openai(self, text: str, context: Dict = None) -> str:
        """使用 OpenAI o1-mini 進行翻譯"""
        try:
            # 構建提示詞
            system_prompt = """你是一個專業的英文到繁體中文翻譯專家，專門處理 Podcast 對話內容。

翻譯要求：
1. 保持對話的自然性和口語化特色
2. 根據說話者角色調整語氣（主持人 vs 嘉賓）
3. 保留對話中的語氣詞和轉折詞
4. 使用台灣繁體中文的表達習慣
5. 對於專業術語，提供自然的中文表達

請直接返回翻譯結果，不要添加任何解釋。"""

            user_prompt = f"請將以下英文對話翻譯成自然的繁體中文：\n\n{text}"
            
            # 如果有上下文信息，添加到提示中
            if context:
                if context.get('is_question'):
                    user_prompt += "\n\n注意：這是一個問句，請確保翻譯後保持疑問語氣。"
                elif context.get('is_response'):
                    user_prompt += "\n\n注意：這是對前面問題的回應，請使用自然的回答語氣。"
                elif context.get('is_transition'):
                    user_prompt += "\n\n注意：這是話題轉換，請使用適當的轉場表達。"
            
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "user", "content": f"{system_prompt}\n\n{user_prompt}"}
                ],
                max_completion_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"⚠️  OpenAI 翻譯失敗，使用備用翻譯: {e}")
            return self.translator.translate(text)
    
    def _translate_with_gemini(self, text: str, context: Dict = None) -> str:
        """使用 Gemini 2.0 Flash Preview 進行翻譯"""
        try:
            # 構建提示詞
            prompt = f"""你是一個專業的英文到繁體中文翻譯專家，專門處理 Podcast 對話內容。

翻譯要求：
1. 保持對話的自然性和口語化特色
2. 根據說話者角色調整語氣
3. 保留對話中的語氣詞和轉折詞
4. 使用台灣繁體中文的表達習慣
5. 對於專業術語，提供自然的中文表達

請將以下英文對話翻譯成自然的繁體中文：

{text}

請直接返回翻譯結果，不要添加任何解釋。"""

            # 如果有上下文信息，添加到提示中
            if context:
                if context.get('is_question'):
                    prompt += "\n\n注意：這是一個問句，請確保翻譯後保持疑問語氣。"
                elif context.get('is_response'):
                    prompt += "\n\n注意：這是對前面問題的回應，請使用自然的回答語氣。"
                elif context.get('is_transition'):
                    prompt += "\n\n注意：這是話題轉換，請使用適當的轉場表達。"
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"⚠️  Gemini 翻譯失敗，使用備用翻譯: {e}")
            return self.translator.translate(text)
    
    def detect_speakers_and_dialogue(self, segments: List[Dict]) -> List[Dict]:
        """檢測對話模式並標記說話者"""
        dialogue_segments = []
        
        for i, segment in enumerate(segments):
            text = segment['text'].strip()
            
            # 檢測對話特徵
            is_question = text.endswith('?') or any(word in text.lower() for word in ['what', 'how', 'why', 'when', 'where', 'who'])
            is_response = any(word in text.lower() for word in ['well', 'actually', 'so', 'yeah', 'right', 'exactly'])
            is_transition = any(phrase in text.lower() for phrase in ['speaking of', 'by the way', 'another thing', 'also'])
            
            # 簡單的說話者檢測（基於對話模式）
            if i == 0:
                speaker = 'A'
            elif is_question and dialogue_segments and dialogue_segments[-1]['speaker'] == 'A':
                speaker = 'B'
            elif is_response and dialogue_segments and dialogue_segments[-1]['speaker'] == 'B':
                speaker = 'A'
            else:
                # 保持前一個說話者，除非有明顯的轉換
                speaker = dialogue_segments[-1]['speaker'] if dialogue_segments else 'A'
                if len(text) > 100 and i > 0:  # 長句子可能是說話者轉換
                    speaker = 'B' if speaker == 'A' else 'A'
            
            dialogue_segments.append({
                **segment,
                'speaker': speaker,
                'is_question': is_question,
                'is_response': is_response,
                'is_transition': is_transition
            })
        
        print(f"✅ 對話分析完成，檢測到 {len(set(seg['speaker'] for seg in dialogue_segments))} 個說話者")
        return dialogue_segments
    
    def translate_with_context(self, segments: List[Dict]) -> List[Dict]:
        """翻譯文本，保持對話的自然性"""
        translated_segments = []
        
        print("🌐 開始翻譯...")
        print(f"   使用翻譯提供商: {self.translation_provider}")
        
        for i, segment in enumerate(segments):
            try:
                original_text = segment['text']
                
                # 準備上下文信息
                context = {
                    'is_question': segment.get('is_question', False),
                    'is_response': segment.get('is_response', False),
                    'is_transition': segment.get('is_transition', False),
                    'speaker': segment.get('speaker', 'A')
                }
                
                # 使用 AI 翻譯（如果可用）或回退到 Google 翻譯
                translated = self.translate_with_ai(original_text, context)
                
                # 後處理：調整中文表達使其更自然
                translated = self.enhance_chinese_dialogue(translated, segment)
                
                translated_segments.append({
                    **segment,
                    'original_text': original_text,
                    'translated_text': translated
                })
                
                print(f"   {i+1}/{len(segments)} - 翻譯完成")
                
            except Exception as e:
                print(f"❌ 翻譯第 {i+1} 段失敗: {e}")
                translated_segments.append({
                    **segment,
                    'original_text': segment['text'],
                    'translated_text': segment['text']  # 保留原文
                })
        
        print("✅ 翻譯完成")
        return translated_segments
    
    def enhance_chinese_dialogue(self, translated_text: str, segment: Dict) -> str:
        """增強中文對話的自然性"""
        text = translated_text
        
        # 根據對話類型調整表達
        if segment.get('is_question'):
            # 問句調整
            if not text.endswith('？') and not text.endswith('?'):
                text += '？'
            # 添加自然的問句開頭
            question_starters = ['那麼', '所以', '那', '嗯']
            if not any(text.startswith(starter) for starter in question_starters):
                if '什麼' in text or '怎麼' in text:
                    text = '那' + text
        
        elif segment.get('is_response'):
            # 回應調整
            response_starters = ['嗯', '對', '是的', '沒錯', '確實']
            if not any(text.startswith(starter) for starter in response_starters):
                text = '嗯，' + text
        
        elif segment.get('is_transition'):
            # 轉場調整
            transition_words = ['說到這個', '順便說一下', '另外', '還有']
            if not any(phrase in text for phrase in transition_words):
                text = '說到這個，' + text
        
        # 添加自然的語氣詞
        if len(text) > 50 and '，' in text:
            # 在長句中間添加語氣詞
            parts = text.split('，')
            if len(parts) > 1:
                parts[0] += '呢'
                text = '，'.join(parts)
        
        return text
    
    async def generate_chinese_audio_simple(self, segments: List[Dict], output_dir: str) -> str:
        """生成中文語音（簡化版）"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("🎤 開始生成中文語音...")
        
        # 合併所有文本
        full_text = ""
        for segment in segments:
            speaker_voice = self.chinese_voices['female'] if segment['speaker'] == 'A' else self.chinese_voices['male']
            text = segment['translated_text']
            
            # 添加說話者標記和停頓
            if segment['speaker'] == 'A':
                full_text += f"[女聲] {text} [停頓] "
            else:
                full_text += f"[男聲] {text} [停頓] "
        
        # 生成單個音頻文件
        output_file = os.path.join(output_dir, "chinese_podcast_simple.wav")
        
        # 使用女聲作為主要聲音
        communicate = edge_tts.Communicate(full_text, self.chinese_voices['female'])
        await communicate.save(output_file)
        
        print(f"✅ 中文語音生成完成: {output_file}")
        return output_file
    
    def save_transcript(self, segments: List[Dict], output_path: str):
        """保存逐字稿"""
        try:
            transcript_data = {
                'timestamp': datetime.now().isoformat(),
                'total_segments': len(segments),
                'segments': []
            }
            
            for segment in segments:
                transcript_data['segments'].append({
                    'start_time': f"{segment.get('start', 0):.2f}s",
                    'end_time': f"{segment.get('end', 0):.2f}s",
                    'speaker': segment['speaker'],
                    'original_text': segment['original_text'],
                    'translated_text': segment['translated_text'],
                    'dialogue_type': {
                        'is_question': segment.get('is_question', False),
                        'is_response': segment.get('is_response', False),
                        'is_transition': segment.get('is_transition', False)
                    }
                })
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(transcript_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 逐字稿已保存: {output_path}")
            
        except Exception as e:
            print(f"❌ 保存逐字稿失敗: {e}")

def create_sample_transcript():
    """創建示範轉錄文本"""
    sample_segments = [
        {
            'start': 0.0,
            'end': 5.0,
            'text': "Welcome to today's discussion about artificial intelligence and its transformative impact on modern society.",
            'words': []
        },
        {
            'start': 5.5,
            'end': 12.0,
            'text': "What do you think are the most significant challenges we face with AI development in the coming years?",
            'words': []
        },
        {
            'start': 12.5,
            'end': 20.0,
            'text': "Well, I believe the main concerns revolve around ethical considerations, job displacement, and ensuring AI systems remain beneficial to humanity.",
            'words': []
        },
        {
            'start': 20.5,
            'end': 28.0,
            'text': "Speaking of ethics, how do we ensure AI systems are fair, transparent, and free from harmful biases?",
            'words': []
        },
        {
            'start': 28.5,
            'end': 35.0,
            'text': "That's an excellent question. We need robust governance frameworks and diverse teams working on AI development.",
            'words': []
        }
    ]
    
    return {
        'text': ' '.join([seg['text'] for seg in sample_segments]),
        'segments': sample_segments,
        'language': 'en'
    }

async def main():
    """主程式"""
    print("🎙️  NotebookLM 中文 Podcast 處理器 - 簡化版示範")
    print("=" * 60)
    
    # 載入環境變數
    load_dotenv()
    
    # 初始化處理器
    processor = SimpleProcessor()
    
    # 使用示範轉錄文本
    print("\n📝 使用示範轉錄文本...")
    transcription = create_sample_transcript()
    
    # 對話分析
    print("\n🔍 分析對話模式...")
    dialogue_segments = processor.detect_speakers_and_dialogue(transcription['segments'])
    
    # 翻譯
    print("\n🌐 開始翻譯...")
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
    
    # 創建輸出目錄
    output_dir = "output/simple_demo"
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存逐字稿
    transcript_path = os.path.join(output_dir, "transcript.json")
    processor.save_transcript(translated_segments, transcript_path)
    
    # 生成語音（可選）
    try:
        print("\n🎤 生成中文語音...")
        audio_path = await processor.generate_chinese_audio_simple(translated_segments, output_dir)
        print(f"✅ 語音文件已生成: {audio_path}")
    except Exception as e:
        print(f"⚠️  語音生成失敗: {e}")
    
    print("\n🎉 示範完成！")
    print(f"📁 輸出目錄: {output_dir}")
    print("\n💡 提示:")
    print("- 檢查 output/simple_demo/ 目錄中的結果文件")
    print("- 如果翻譯品質不理想，請檢查 API 金鑰設定")
    print("- 可以調整 .env 文件中的模型設定")

if __name__ == "__main__":
    asyncio.run(main()) 