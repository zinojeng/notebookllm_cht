#!/bin/bash

# NotebookLM 中文 Podcast 處理器 - 清理腳本

set -e

echo "🧹 NotebookLM 中文 Podcast 處理器 - 清理工具"
echo "=============================================="

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函數：顯示目錄大小
show_directory_sizes() {
    echo -e "${BLUE}📊 目錄大小統計：${NC}"
    echo "----------------------------------------"
    
    for dir in input output temp logs examples config; do
        if [ -d "$dir" ]; then
            size=$(du -sh "$dir" 2>/dev/null | cut -f1)
            echo -e "  📁 $dir: ${GREEN}$size${NC}"
        fi
    done
    
    echo "----------------------------------------"
    total_size=$(du -sh . 2>/dev/null | cut -f1)
    echo -e "  📦 總大小: ${YELLOW}$total_size${NC}"
    echo ""
}

# 函數：清理暫存文件
cleanup_temp() {
    echo -e "${YELLOW}🗂️  清理暫存文件...${NC}"
    
    if [ -d "temp" ]; then
        temp_size=$(du -sh temp 2>/dev/null | cut -f1)
        echo "  清理前大小: $temp_size"
        
        rm -rf temp/audio/*
        rm -rf temp/transcripts/*
        
        echo -e "  ${GREEN}✅ 暫存文件清理完成${NC}"
    else
        echo -e "  ${YELLOW}⚠️  temp/ 目錄不存在${NC}"
    fi
    echo ""
}

# 函數：清理舊日誌
cleanup_logs() {
    echo -e "${YELLOW}📋 清理舊日誌文件...${NC}"
    
    if [ -d "logs" ]; then
        # 計算清理前的文件數量
        log_count=$(find logs -name "*.log" 2>/dev/null | wc -l)
        echo "  清理前日誌文件數: $log_count"
        
        # 刪除 7 天前的日誌文件
        find logs -name "*.log" -mtime +7 -delete 2>/dev/null || true
        
        # 計算清理後的文件數量
        remaining_count=$(find logs -name "*.log" 2>/dev/null | wc -l)
        deleted_count=$((log_count - remaining_count))
        
        echo -e "  ${GREEN}✅ 已刪除 $deleted_count 個舊日誌文件${NC}"
        echo "  保留 $remaining_count 個最近的日誌文件"
    else
        echo -e "  ${YELLOW}⚠️  logs/ 目錄不存在${NC}"
    fi
    echo ""
}

# 函數：清理輸出文件
cleanup_output() {
    echo -e "${RED}⚠️  清理輸出文件${NC}"
    echo "這將刪除所有處理結果，請確認是否繼續？"
    read -p "輸入 'yes' 確認刪除: " confirm
    
    if [ "$confirm" = "yes" ]; then
        if [ -d "output" ]; then
            output_size=$(du -sh output 2>/dev/null | cut -f1)
            echo "  清理前大小: $output_size"
            
            rm -rf output/processed/*
            rm -rf output/reports/*
            
            echo -e "  ${GREEN}✅ 輸出文件清理完成${NC}"
        else
            echo -e "  ${YELLOW}⚠️  output/ 目錄不存在${NC}"
        fi
    else
        echo -e "  ${BLUE}ℹ️  取消清理輸出文件${NC}"
    fi
    echo ""
}

# 函數：備份重要文件
backup_important() {
    echo -e "${BLUE}💾 備份重要文件...${NC}"
    
    backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # 備份配置文件
    if [ -d "config" ]; then
        cp -r config "$backup_dir/"
        echo "  ✅ 配置文件已備份"
    fi
    
    # 備份範例文件
    if [ -d "examples/configs" ]; then
        mkdir -p "$backup_dir/examples"
        cp -r examples/configs "$backup_dir/examples/"
        echo "  ✅ 範例配置已備份"
    fi
    
    # 壓縮備份
    tar -czf "${backup_dir}.tar.gz" "$backup_dir"
    rm -rf "$backup_dir"
    
    echo -e "  ${GREEN}✅ 備份完成: ${backup_dir}.tar.gz${NC}"
    echo ""
}

# 函數：檢查磁碟空間
check_disk_space() {
    echo -e "${BLUE}💽 磁碟空間檢查：${NC}"
    echo "----------------------------------------"
    
    # 檢查當前目錄所在的磁碟空間
    df -h . | tail -1 | while read filesystem size used avail capacity mounted; do
        echo "  檔案系統: $filesystem"
        echo "  總大小: $size"
        echo "  已使用: $used"
        echo "  可用空間: $avail"
        echo "  使用率: $capacity"
        
        # 檢查是否空間不足（使用率超過 90%）
        usage_percent=$(echo $capacity | sed 's/%//')
        if [ "$usage_percent" -gt 90 ]; then
            echo -e "  ${RED}⚠️  警告：磁碟空間不足！${NC}"
        else
            echo -e "  ${GREEN}✅ 磁碟空間充足${NC}"
        fi
    done
    echo ""
}

# 函數：顯示幫助信息
show_help() {
    echo "使用方式: $0 [選項]"
    echo ""
    echo "選項:"
    echo "  -t, --temp      僅清理暫存文件"
    echo "  -l, --logs      僅清理舊日誌文件"
    echo "  -o, --output    清理輸出文件（需確認）"
    echo "  -b, --backup    備份重要文件"
    echo "  -s, --size      顯示目錄大小"
    echo "  -d, --disk      檢查磁碟空間"
    echo "  -a, --all       執行所有清理操作"
    echo "  -h, --help      顯示此幫助信息"
    echo ""
    echo "範例:"
    echo "  $0 --temp       # 僅清理暫存文件"
    echo "  $0 --all        # 執行所有清理操作"
    echo "  $0 --size       # 顯示目錄大小統計"
}

# 主程式
main() {
    # 檢查是否在正確的目錄
    if [ ! -f "audio_processor.py" ]; then
        echo -e "${RED}❌ 錯誤：請在專案根目錄執行此腳本${NC}"
        exit 1
    fi
    
    # 解析命令行參數
    case "${1:-}" in
        -t|--temp)
            show_directory_sizes
            cleanup_temp
            show_directory_sizes
            ;;
        -l|--logs)
            show_directory_sizes
            cleanup_logs
            show_directory_sizes
            ;;
        -o|--output)
            show_directory_sizes
            cleanup_output
            show_directory_sizes
            ;;
        -b|--backup)
            backup_important
            ;;
        -s|--size)
            show_directory_sizes
            ;;
        -d|--disk)
            check_disk_space
            ;;
        -a|--all)
            echo "執行完整清理流程..."
            echo ""
            show_directory_sizes
            check_disk_space
            backup_important
            cleanup_temp
            cleanup_logs
            cleanup_output
            show_directory_sizes
            echo -e "${GREEN}🎉 清理完成！${NC}"
            ;;
        -h|--help)
            show_help
            ;;
        "")
            # 互動式模式
            echo "請選擇要執行的操作："
            echo "1) 顯示目錄大小"
            echo "2) 清理暫存文件"
            echo "3) 清理舊日誌"
            echo "4) 清理輸出文件"
            echo "5) 備份重要文件"
            echo "6) 檢查磁碟空間"
            echo "7) 執行所有清理"
            echo "0) 退出"
            echo ""
            read -p "請輸入選項 (0-7): " choice
            
            case $choice in
                1) show_directory_sizes ;;
                2) cleanup_temp ;;
                3) cleanup_logs ;;
                4) cleanup_output ;;
                5) backup_important ;;
                6) check_disk_space ;;
                7) 
                    show_directory_sizes
                    check_disk_space
                    backup_important
                    cleanup_temp
                    cleanup_logs
                    cleanup_output
                    show_directory_sizes
                    echo -e "${GREEN}🎉 清理完成！${NC}"
                    ;;
                0) echo "退出清理工具" ;;
                *) echo -e "${RED}❌ 無效選項${NC}" ;;
            esac
            ;;
        *)
            echo -e "${RED}❌ 未知選項: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# 執行主程式
main "$@" 