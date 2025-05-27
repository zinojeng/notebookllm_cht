#!/usr/bin/env python3
"""
NotebookLM 中文 Podcast 處理器 - 環境變數管理工具
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional, List
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnvManager:
    """環境變數管理器"""
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.required_vars = {
            # 基本設定
            'LOG_LEVEL': 'INFO',
            'DEFAULT_LANGUAGE': 'zh-tw',
            'DEFAULT_TTS_PROVIDER': 'edge',
            'WHISPER_MODEL': 'base',
            
            # 目錄設定
            'TEMP_DIR': './temp',
            'OUTPUT_DIR': './output',
            
            # 效能設定
            'MAX_CONCURRENT_JOBS': '2',
            'MAX_FILE_SIZE': '500MB',
            
            # Edge TTS 設定（免費選項）
            'EDGE_TTS_VOICE_FEMALE': 'zh-TW-HsiaoChenNeural',
            'EDGE_TTS_VOICE_MALE': 'zh-TW-YunJheNeural',
            
            # 翻譯設定
            'TRANSLATION_PROVIDER': 'google',
            'PRESERVE_DIALOGUE_STYLE': 'true',
            'ENHANCE_NATURALNESS': 'true',
        }
        
        self.optional_vars = {
            # API 金鑰（可選，根據使用的服務）
            'OPENAI_API_KEY': None,
            'OPENAI_ORG_ID': None,
            'GEMINI_API_KEY': None,
            'GOOGLE_API_KEY': None,
            'GOOGLE_APPLICATION_CREDENTIALS': None,
            'GOOGLE_CLOUD_PROJECT_ID': None,
            'GOOGLE_TRANSLATE_API_KEY': None,
            'AZURE_SPEECH_KEY': None,
            'AZURE_SPEECH_REGION': None,
            'DEEPL_API_KEY': None,
            'ELEVENLABS_API_KEY': None,
            'HUGGINGFACE_API_TOKEN': None,
            
            # 進階設定
            'DATABASE_URL': None,
            'SECRET_KEY': None,
            'WEBHOOK_URL': None,
            'SLACK_WEBHOOK_URL': None,
            'REDIS_URL': None,
            'SENTRY_DSN': None,
        }
    
    def load_env(self) -> bool:
        """載入環境變數"""
        try:
            # 嘗試載入 .env 文件
            if os.path.exists(self.env_file):
                self._load_env_file()
                logger.info(f"✅ 已載入環境變數文件: {self.env_file}")
            else:
                logger.warning(f"⚠️  環境變數文件不存在: {self.env_file}")
                logger.info("將使用預設值和系統環境變數")
            
            # 設定預設值
            self._set_defaults()
            
            # 驗證設定
            return self._validate_config()
            
        except Exception as e:
            logger.error(f"❌ 載入環境變數失敗: {e}")
            return False
    
    def _load_env_file(self):
        """載入 .env 文件"""
        with open(self.env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    os.environ[key] = value
    
    def _set_defaults(self):
        """設定預設值"""
        for key, default_value in self.required_vars.items():
            if key not in os.environ:
                os.environ[key] = default_value
                logger.debug(f"設定預設值: {key}={default_value}")
    
    def _validate_config(self) -> bool:
        """驗證配置"""
        errors = []
        warnings = []
        
        # 檢查必要變數
        for key in self.required_vars:
            if not os.environ.get(key):
                errors.append(f"缺少必要環境變數: {key}")
        
        # 檢查 TTS 提供商相關設定
        tts_provider = os.environ.get('DEFAULT_TTS_PROVIDER', 'edge')
        if tts_provider == 'openai' and not os.environ.get('OPENAI_API_KEY'):
            warnings.append("使用 OpenAI TTS 但未設定 OPENAI_API_KEY")
        elif tts_provider == 'elevenlabs' and not os.environ.get('ELEVENLABS_API_KEY'):
            warnings.append("使用 ElevenLabs TTS 但未設定 ELEVENLABS_API_KEY")
        
        # 檢查翻譯提供商相關設定
        translation_provider = os.environ.get('TRANSLATION_PROVIDER', 'google')
        if translation_provider == 'openai' and not os.environ.get('OPENAI_API_KEY'):
            warnings.append("使用 OpenAI 翻譯但未設定 OPENAI_API_KEY")
        elif translation_provider == 'deepl' and not os.environ.get('DEEPL_API_KEY'):
            warnings.append("使用 DeepL 翻譯但未設定 DEEPL_API_KEY")
        
        # 檢查目錄
        temp_dir = os.environ.get('TEMP_DIR', './temp')
        output_dir = os.environ.get('OUTPUT_DIR', './output')
        
        for directory in [temp_dir, output_dir]:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                    logger.info(f"✅ 建立目錄: {directory}")
                except Exception as e:
                    errors.append(f"無法建立目錄 {directory}: {e}")
        
        # 顯示結果
        if errors:
            logger.error("❌ 配置驗證失敗:")
            for error in errors:
                logger.error(f"  - {error}")
            return False
        
        if warnings:
            logger.warning("⚠️  配置警告:")
            for warning in warnings:
                logger.warning(f"  - {warning}")
        
        logger.info("✅ 環境變數配置驗證通過")
        return True
    
    def create_env_file(self) -> bool:
        """建立 .env 文件"""
        try:
            if os.path.exists(self.env_file):
                response = input(f"⚠️  {self.env_file} 已存在，是否覆蓋？ (y/N): ")
                if response.lower() != 'y':
                    logger.info("取消建立 .env 文件")
                    return False
            
            # 讀取範本
            template_path = "config/env_template.txt"
            if not os.path.exists(template_path):
                logger.error(f"❌ 找不到範本文件: {template_path}")
                return False
            
            # 複製範本到 .env
            with open(template_path, 'r', encoding='utf-8') as src:
                content = src.read()
            
            with open(self.env_file, 'w', encoding='utf-8') as dst:
                dst.write(content)
            
            logger.info(f"✅ 已建立 {self.env_file} 文件")
            logger.info("請編輯此文件並填入您的 API 金鑰")
            return True
            
        except Exception as e:
            logger.error(f"❌ 建立 .env 文件失敗: {e}")
            return False
    
    def show_config(self):
        """顯示當前配置"""
        print("\n📋 當前環境變數配置:")
        print("=" * 50)
        
        print("\n🔧 基本設定:")
        for key in ['LOG_LEVEL', 'DEFAULT_LANGUAGE', 'DEFAULT_TTS_PROVIDER', 'WHISPER_MODEL']:
            value = os.environ.get(key, 'Not Set')
            print(f"  {key}: {value}")
        
        print("\n📁 目錄設定:")
        for key in ['TEMP_DIR', 'OUTPUT_DIR']:
            value = os.environ.get(key, 'Not Set')
            exists = "✅" if os.path.exists(value) else "❌"
            print(f"  {key}: {value} {exists}")
        
        print("\n🔑 API 金鑰狀態:")
        api_keys = [
            'OPENAI_API_KEY', 'GEMINI_API_KEY', 'GOOGLE_TRANSLATE_API_KEY', 
            'AZURE_SPEECH_KEY', 'DEEPL_API_KEY', 'ELEVENLABS_API_KEY'
        ]
        for key in api_keys:
            value = os.environ.get(key)
            status = "✅ 已設定" if value else "❌ 未設定"
            print(f"  {key}: {status}")
        
        print("\n🎵 語音設定:")
        for key in ['EDGE_TTS_VOICE_FEMALE', 'EDGE_TTS_VOICE_MALE']:
            value = os.environ.get(key, 'Not Set')
            print(f"  {key}: {value}")

def main():
    """主程式"""
    env_manager = EnvManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "create":
            env_manager.create_env_file()
        elif command == "validate":
            env_manager.load_env()
        elif command == "show":
            env_manager.load_env()
            env_manager.show_config()
        else:
            print("使用方式:")
            print("  python env_manager.py create    # 建立 .env 文件")
            print("  python env_manager.py validate  # 驗證環境變數")
            print("  python env_manager.py show      # 顯示當前配置")
    else:
        # 互動式模式
        print("🔧 環境變數管理工具")
        print("1. 建立 .env 文件")
        print("2. 驗證環境變數")
        print("3. 顯示當前配置")
        print("0. 退出")
        
        choice = input("\n請選擇操作 (0-3): ")
        
        if choice == "1":
            env_manager.create_env_file()
        elif choice == "2":
            env_manager.load_env()
        elif choice == "3":
            env_manager.load_env()
            env_manager.show_config()
        elif choice == "0":
            print("退出")
        else:
            print("❌ 無效選項")

if __name__ == "__main__":
    main() 