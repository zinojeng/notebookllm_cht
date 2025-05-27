#!/usr/bin/env python3
"""
批次處理器 - 處理多個 NotebookLM 音頻文件
"""

import asyncio
import os
import glob
from pathlib import Path
from typing import List, Dict
from audio_processor import AudioProcessor
import json
from datetime import datetime

class BatchProcessor:
    def __init__(self):
        self.processor = AudioProcessor()
        self.results = []
    
    def find_wav_files(self, input_dir: str) -> List[str]:
        """尋找目錄中的所有 .wav 文件"""
        wav_files = []
        
        # 支援多種模式
        patterns = [
            os.path.join(input_dir, "*.wav"),
            os.path.join(input_dir, "**/*.wav")
        ]
        
        for pattern in patterns:
            wav_files.extend(glob.glob(pattern, recursive=True))
        
        # 去重並排序
        wav_files = sorted(list(set(wav_files)))
        
        print(f"🔍 在 {input_dir} 中找到 {len(wav_files)} 個 .wav 文件")
        for i, file in enumerate(wav_files, 1):
            print(f"   {i}. {os.path.basename(file)}")
        
        return wav_files
    
    async def process_single_file(self, input_file: str, output_base_dir: str) -> Dict:
        """處理單個文件"""
        file_name = Path(input_file).stem
        output_dir = os.path.join(output_base_dir, file_name)
        
        print(f"\n🎯 處理文件: {os.path.basename(input_file)}")
        print(f"📁 輸出目錄: {output_dir}")
        
        try:
            result = await self.processor.process_audio_complete(input_file, output_dir)
            
            if result:
                result['input_file'] = input_file
                result['output_dir'] = output_dir
                result['status'] = 'success'
                result['processed_at'] = datetime.now().isoformat()
                
                print(f"✅ {file_name} 處理完成")
                return result
            else:
                error_result = {
                    'input_file': input_file,
                    'output_dir': output_dir,
                    'status': 'failed',
                    'error': 'Processing failed',
                    'processed_at': datetime.now().isoformat()
                }
                print(f"❌ {file_name} 處理失敗")
                return error_result
                
        except Exception as e:
            error_result = {
                'input_file': input_file,
                'output_dir': output_dir,
                'status': 'error',
                'error': str(e),
                'processed_at': datetime.now().isoformat()
            }
            print(f"❌ {file_name} 處理錯誤: {e}")
            return error_result
    
    async def process_batch(self, input_dir: str, output_dir: str, max_concurrent: int = 2) -> Dict:
        """批次處理多個文件"""
        print("🚀 開始批次處理...")
        print("=" * 60)
        
        # 尋找所有 .wav 文件
        wav_files = self.find_wav_files(input_dir)
        
        if not wav_files:
            print("❌ 沒有找到 .wav 文件")
            return {'status': 'no_files', 'results': []}
        
        # 建立輸出目錄
        os.makedirs(output_dir, exist_ok=True)
        
        # 使用信號量限制並發數量
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(file_path):
            async with semaphore:
                return await self.process_single_file(file_path, output_dir)
        
        # 並發處理所有文件
        print(f"\n🔄 開始並發處理 {len(wav_files)} 個文件 (最大並發數: {max_concurrent})")
        
        tasks = [process_with_semaphore(file_path) for file_path in wav_files]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 處理結果
        successful = 0
        failed = 0
        
        for result in results:
            if isinstance(result, Exception):
                failed += 1
                self.results.append({
                    'status': 'exception',
                    'error': str(result),
                    'processed_at': datetime.now().isoformat()
                })
            elif result['status'] == 'success':
                successful += 1
                self.results.append(result)
            else:
                failed += 1
                self.results.append(result)
        
        # 生成批次報告
        batch_result = {
            'batch_id': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'input_directory': input_dir,
            'output_directory': output_dir,
            'total_files': len(wav_files),
            'successful': successful,
            'failed': failed,
            'max_concurrent': max_concurrent,
            'started_at': datetime.now().isoformat(),
            'results': self.results
        }
        
        # 保存批次報告
        report_path = os.path.join(output_dir, "batch_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(batch_result, f, ensure_ascii=False, indent=2)
        
        print("\n🎉 批次處理完成！")
        print("=" * 60)
        print(f"📊 總文件數: {len(wav_files)}")
        print(f"✅ 成功: {successful}")
        print(f"❌ 失敗: {failed}")
        print(f"📄 批次報告: {report_path}")
        
        return batch_result
    
    def generate_summary_report(self, output_dir: str):
        """生成摘要報告"""
        if not self.results:
            return
        
        successful_results = [r for r in self.results if r['status'] == 'success']
        
        if not successful_results:
            return
        
        # 計算統計信息
        total_duration = sum(r.get('total_duration', 0) for r in successful_results)
        total_segments = sum(r.get('segments_count', 0) for r in successful_results)
        
        summary = {
            'summary': {
                'total_processed_files': len(successful_results),
                'total_audio_duration': f"{total_duration:.2f} seconds",
                'total_segments': total_segments,
                'average_duration_per_file': f"{total_duration/len(successful_results):.2f} seconds",
                'average_segments_per_file': f"{total_segments/len(successful_results):.1f}"
            },
            'files': []
        }
        
        for result in successful_results:
            file_info = {
                'filename': os.path.basename(result['input_file']),
                'duration': f"{result.get('total_duration', 0):.2f}s",
                'segments': result.get('segments_count', 0),
                'chinese_audio': result.get('chinese_audio', ''),
                'transcript': result.get('transcript', '')
            }
            summary['files'].append(file_info)
        
        # 保存摘要
        summary_path = os.path.join(output_dir, "summary_report.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"📋 摘要報告已保存: {summary_path}")

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="批次處理 NotebookLM 音頻文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  python batch_processor.py input_folder/                    # 處理 input_folder/ 中的所有 .wav 文件
  python batch_processor.py input_folder/ -o output_batch/  # 指定輸出目錄
  python batch_processor.py input_folder/ --concurrent 4    # 設定並發數量
        """
    )
    
    parser.add_argument(
        'input_dir',
        help='包含 .wav 文件的輸入目錄'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='batch_output',
        help='輸出目錄 (預設: batch_output/)'
    )
    
    parser.add_argument(
        '--concurrent',
        type=int,
        default=2,
        help='最大並發處理數量 (預設: 2)'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_dir):
        print(f"❌ 輸入目錄不存在: {args.input_dir}")
        return
    
    batch_processor = BatchProcessor()
    
    try:
        result = await batch_processor.process_batch(
            args.input_dir,
            args.output,
            args.concurrent
        )
        
        # 生成摘要報告
        batch_processor.generate_summary_report(args.output)
        
        if result['successful'] > 0:
            print(f"\n🎧 您可以在 {args.output} 目錄中找到所有生成的中文 Podcast！")
        
    except KeyboardInterrupt:
        print("\n⚠️  批次處理被用戶中斷")
    except Exception as e:
        print(f"❌ 批次處理錯誤: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 