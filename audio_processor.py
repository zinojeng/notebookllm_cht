import asyncio
import edge_tts
from pydub import AudioSegment
from deep_translator import GoogleTranslator
import os
import re
import json
from typing import List, Dict, Tuple
import soundfile as sf
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 新增 API 支援
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

class AudioProcessor:
    def __init__(self):
        """初始化音頻處理器"""
        # 載入環境變數
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        # 設定翻譯提供商
        self.translation_provider = os.getenv('TRANSLATION_PROVIDER', 'google').lower()
        
        # 初始化翻譯器
        self._init_translators()
        
        # 中文語音設定 - 使用更自然的聲音
        self.chinese_voices = {
            'female': os.getenv('EDGE_TTS_VOICE_FEMALE', 'zh-TW-HsiaoChenNeural'),
            'male': os.getenv('EDGE_TTS_VOICE_MALE', 'zh-TW-YunJheNeural')
        }
        
        print(f"🔧 音頻處理器初始化完成")
        print(f"   翻譯提供商: {self.translation_provider}")
        print(f"   女性聲音: {self.chinese_voices['female']}")
        print(f"   男性聲音: {self.chinese_voices['male']}")
    
    def _init_translators(self):
        """初始化翻譯器"""
        self.translator = GoogleTranslator(source='en', target='zh-tw')
        
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
    
    def load_audio(self, file_path: str) -> AudioSegment:
        """載入音頻文件"""
        try:
            audio = AudioSegment.from_wav(file_path)
            print(f"✅ 成功載入音頻: {file_path}")
            print(f"   時長: {len(audio)/1000:.2f} 秒")
            print(f"   採樣率: {audio.frame_rate} Hz")
            return audio
        except Exception as e:
            print(f"❌ 載入音頻失敗: {e}")
            return None
    
    def transcribe_with_timestamps(self, audio_path: str) -> Dict:
        """使用 OpenAI Whisper API 進行語音識別，保留時間戳"""
        try:
            print("🎯 開始語音識別...")
            
            if not self.openai_client:
                print("❌ OpenAI 客戶端未初始化，無法進行語音識別")
                return None
            
            # 使用 OpenAI Whisper API
            with open(audio_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )
            
            # 轉換格式以符合原有的結構
            segments = []
            for segment in transcript.segments:
                segments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip(),
                    'words': []  # OpenAI API 不提供詞級時間戳
                })
            
            print(f"✅ 語音識別完成，共 {len(segments)} 個片段")
            return {
                'text': transcript.text,
                'segments': segments,
                'language': transcript.language or 'en'
            }
            
        except Exception as e:
            print(f"❌ 語音識別失敗: {e}")
            # 如果 OpenAI API 失敗，嘗試使用簡單的分段方法
            return self._fallback_transcription(audio_path)
    
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
                
                # 保留對話的自然表達
                # 預處理：保留語氣詞和對話標記
                text_to_translate = original_text
                
                # 準備上下文信息
                context = {
                    'is_question': segment.get('is_question', False),
                    'is_response': segment.get('is_response', False),
                    'is_transition': segment.get('is_transition', False),
                    'speaker': segment.get('speaker', 'A')
                }
                
                # 使用 AI 翻譯（如果可用）或回退到 Google 翻譯
                translated = self.translate_with_ai(text_to_translate, context)
                
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
    
    async def generate_chinese_audio(self, segments: List[Dict], output_dir: str) -> str:
        """生成中文語音"""
        os.makedirs(output_dir, exist_ok=True)
        audio_files = []
        
        print("🎤 開始生成中文語音...")
        
        for i, segment in enumerate(segments):
            try:
                # 選擇聲音（根據說話者）
                voice = self.chinese_voices['female'] if segment['speaker'] == 'A' else self.chinese_voices['male']
                
                # 調整語音參數以更自然
                text = segment['translated_text']
                
                # 添加適當的停頓標記
                text = self.add_speech_marks(text, segment)
                
                # 生成語音文件
                output_file = os.path.join(output_dir, f"segment_{i:03d}_{segment['speaker']}.wav")
                
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output_file)
                
                audio_files.append({
                    'file': output_file,
                    'start': segment['start'],
                    'end': segment['end'],
                    'speaker': segment['speaker'],
                    'duration': segment['end'] - segment['start']
                })
                
                print(f"   {i+1}/{len(segments)} - 語音生成完成")
                
            except Exception as e:
                print(f"❌ 生成第 {i+1} 段語音失敗: {e}")
        
        # 合併音頻文件
        final_audio_path = await self.merge_audio_segments(audio_files, output_dir)
        print("✅ 中文語音生成完成")
        return final_audio_path
    
    def add_speech_marks(self, text: str, segment: Dict) -> str:
        """添加語音標記以改善自然度"""
        # 添加停頓
        if segment.get('is_question'):
            text = text.replace('？', '<break time="500ms"/>？')
        
        # 在逗號後添加短暫停頓
        text = text.replace('，', '，<break time="300ms"/>')
        
        # 在句號後添加停頓
        text = text.replace('。', '。<break time="500ms"/>')
        
        # 調整語速和音調
        if segment.get('is_question'):
            text = f'<prosody rate="0.9" pitch="+5%">{text}</prosody>'
        elif segment.get('is_response'):
            text = f'<prosody rate="1.0" pitch="-2%">{text}</prosody>'
        
        return text
    
    async def merge_audio_segments(self, audio_files: List[Dict], output_dir: str) -> str:
        """合併音頻片段"""
        try:
            combined = AudioSegment.empty()
            
            for audio_info in audio_files:
                # 載入音頻片段
                segment_audio = AudioSegment.from_wav(audio_info['file'])
                
                # 添加到合併音頻
                combined += segment_audio
                
                # 添加適當的間隔（模擬自然對話）
                if audio_info != audio_files[-1]:  # 不是最後一個片段
                    silence_duration = min(1000, max(300, int(audio_info['duration'] * 100)))
                    combined += AudioSegment.silent(duration=silence_duration)
            
            # 輸出最終文件
            final_path = os.path.join(output_dir, "chinese_podcast_final.wav")
            combined.export(final_path, format="wav")
            
            print(f"✅ 音頻合併完成: {final_path}")
            return final_path
            
        except Exception as e:
            print(f"❌ 音頻合併失敗: {e}")
            return None
    
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
                    'start_time': f"{segment['start']:.2f}s",
                    'end_time': f"{segment['end']:.2f}s",
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
    
    async def process_audio_complete(self, input_wav_path: str, output_dir: str = "output") -> Dict:
        """完整的音頻處理流程"""
        print("🚀 開始完整音頻處理流程...")
        
        # 1. 載入音頻
        audio = self.load_audio(input_wav_path)
        if not audio:
            return None
        
        # 2. 語音識別
        transcription = self.transcribe_with_timestamps(input_wav_path)
        if not transcription:
            return None
        
        # 3. 對話分析
        dialogue_segments = self.detect_speakers_and_dialogue(transcription['segments'])
        
        # 4. 翻譯
        translated_segments = self.translate_with_context(dialogue_segments)
        
        # 5. 生成中文語音
        chinese_audio_path = await self.generate_chinese_audio(translated_segments, output_dir)
        
        # 6. 保存逐字稿
        transcript_path = os.path.join(output_dir, "transcript.json")
        self.save_transcript(translated_segments, transcript_path)
        
        result = {
            'original_audio': input_wav_path,
            'chinese_audio': chinese_audio_path,
            'transcript': transcript_path,
            'segments_count': len(translated_segments),
            'total_duration': sum(seg['end'] - seg['start'] for seg in translated_segments)
        }
        
        print("🎉 音頻處理完成！")
        print(f"   原始音頻: {input_wav_path}")
        print(f"   中文音頻: {chinese_audio_path}")
        print(f"   逐字稿: {transcript_path}")
        print(f"   總時長: {result['total_duration']:.2f} 秒")
        
        return result
    
    def _fallback_transcription(self, audio_path: str) -> Dict:
        """備用轉錄方法，當 OpenAI API 不可用時使用"""
        try:
            print("⚠️  使用備用轉錄方法...")
            
            # 載入音頻並創建簡單的分段
            audio = AudioSegment.from_wav(audio_path)
            duration = len(audio) / 1000.0  # 轉換為秒
            
            # 創建假的分段（每30秒一段）
            segments = []
            segment_duration = 30.0
            num_segments = int(duration / segment_duration) + 1
            
            for i in range(num_segments):
                start_time = i * segment_duration
                end_time = min((i + 1) * segment_duration, duration)
                
                segments.append({
                    'start': start_time,
                    'end': end_time,
                    'text': f"[音頻片段 {i+1}] 請手動添加轉錄內容",
                    'words': []
                })
            
            print(f"✅ 備用轉錄完成，共 {len(segments)} 個片段")
            return {
                'text': "請手動添加完整轉錄內容",
                'segments': segments,
                'language': 'en'
            }
            
        except Exception as e:
            print(f"❌ 備用轉錄也失敗: {e}")
            return None 