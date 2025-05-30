#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能旅游规划助手 - 自动更新index.html推荐攻略功能
功能：自动扫描destination目录中的HTML文件，提取攻略信息并更新index.html中的推荐攻略区域
作者：智能旅游助手系统
更新时间：自动生成
"""

import os
import re
import datetime
from pathlib import Path
from bs4 import BeautifulSoup


class IndexUpdater:
    """index.html自动更新器类"""
    
    def __init__(self, project_root="."):
        """
        初始化更新器
        :param project_root: 项目根目录路径
        """
        self.project_root = Path(project_root)
        self.destination_dir = self.project_root / "destination"
        self.index_file = self.project_root / "index.html"
        
        # 攻略信息配置：文件名 -> [图标, 主标题, 副标题]
        self.guide_config = {
            "beijing_chengdu_guide.html": ["🏔️", "北京-成都五一攻略", "体验古都到天府的魅力"],
            "hefei_nanjing_guide.html": ["🏮", "合肥-南京端午攻略", "江南文化深度游"],
            "hefei_wuhan_guide.html": ["🌸", "合肥-武汉端午攻略", "探索江城风情"],
            "hefei_tongling_guide.html": ["🏭", "合肥-铜陵端午攻略", "体验铜都历史"],
            "hefei_huangshan_guide.html": ["⛰️", "合肥-黄山端午攻略", "登临天下第一奇山"],
            "hefei_anqing_guide.html": ["🏛️", "合肥-安庆端午攻略", "感受历史文化名城"]
        }
    
    def scan_destination_files(self):
        """
        扫描destination目录中的所有HTML文件
        :return: 文件列表
        """
        if not self.destination_dir.exists():
            print(f"错误：destination目录不存在：{self.destination_dir}")
            return []
        
        html_files = list(self.destination_dir.glob("*.html"))
        print(f"发现 {len(html_files)} 个攻略文件：")
        for file in html_files:
            print(f"  - {file.name}")
        
        return html_files
    
    def extract_guide_info(self, file_path):
        """
        从HTML文件中提取攻略标题信息
        :param file_path: HTML文件路径
        :return: 攻略信息字典
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # 提取页面标题
            title_tag = soup.find('title')
            page_title = title_tag.text.strip() if title_tag else ""
            
            # 提取guide-title内容
            guide_title_tag = soup.find('h1', class_='guide-title')
            if not guide_title_tag:
                guide_title_tag = soup.find('h1')
            
            guide_title = ""
            if guide_title_tag:
                # 移除图标，只保留文字
                guide_title = re.sub(r'[🏔️🏮🌸🏭⛰️🏛️🎭🌅📜🌉🐅⛰️🌺🏔️🏞️🏛️🌊🏔️🎪]', '', guide_title_tag.get_text()).strip()
            
            # 如果配置中有预设信息，使用预设信息
            filename = file_path.name
            if filename in self.guide_config:
                icon, main_title, subtitle = self.guide_config[filename]
                return {
                    'filename': filename,
                    'icon': icon,
                    'main_title': main_title,
                    'subtitle': subtitle,
                    'page_title': page_title,
                    'guide_title': guide_title
                }
            
            # 否则根据文件名和标题自动生成
            return self.auto_generate_guide_info(filename, page_title, guide_title)
            
        except Exception as e:
            print(f"错误：无法解析文件 {file_path}：{e}")
            return None
    
    def auto_generate_guide_info(self, filename, page_title, guide_title):
        """
        根据文件名和标题自动生成攻略信息
        :param filename: 文件名
        :param page_title: 页面标题
        :param guide_title: 攻略标题
        :return: 攻略信息字典
        """
        # 根据文件名推断主标题和副标题
        if "beijing" in filename and "chengdu" in filename:
            icon, main_title, subtitle = "🏔️", "北京-成都攻略", "体验古都到天府的魅力"
        elif "hefei" in filename and "nanjing" in filename:
            icon, main_title, subtitle = "🏮", "合肥-南京攻略", "江南文化深度游"
        elif "hefei" in filename and "wuhan" in filename:
            icon, main_title, subtitle = "🌸", "合肥-武汉攻略", "探索江城风情"
        elif "hefei" in filename and "tongling" in filename:
            icon, main_title, subtitle = "🏭", "合肥-铜陵攻略", "体验铜都历史"
        elif "hefei" in filename and "huangshan" in filename:
            icon, main_title, subtitle = "⛰️", "合肥-黄山攻略", "登临天下第一奇山"
        elif "hefei" in filename and "anqing" in filename:
            icon, main_title, subtitle = "🏛️", "合肥-安庆攻略", "感受历史文化名城"
        else:
            # 通用处理
            icon = "🎪"
            main_title = guide_title or page_title or filename.replace('.html', '').replace('_', '-')
            subtitle = "精彩旅程等您探索"
        
        return {
            'filename': filename,
            'icon': icon,
            'main_title': main_title,
            'subtitle': subtitle,
            'page_title': page_title,
            'guide_title': guide_title
        }
    
    def generate_recommendation_html(self, guides_info):
        """
        生成推荐攻略HTML代码
        :param guides_info: 攻略信息列表
        :return: HTML代码字符串
        """
        html_parts = []
        
        # 添加推荐攻略区域开始标签
        html_parts.append('        <!-- 推荐攻略按钮区域 -->')
        html_parts.append('        <div class="recommendation-container">')
        html_parts.append('            <div class="recommendation-header">')
        html_parts.append('                <span class="icon">🌟</span>')
        html_parts.append('                热门推荐攻略')
        html_parts.append('            </div>')
        html_parts.append('            <div class="recommendation-grid">')
        
        # 为每个攻略生成按钮
        for guide in guides_info:
            html_parts.append(f'                <a href="destination/{guide["filename"]}" class="recommendation-btn">')
            html_parts.append(f'                    <span class="icon">{guide["icon"]}</span>')
            html_parts.append('                    <div class="btn-content">')
            html_parts.append(f'                        <div class="btn-title">{guide["main_title"]}</div>')
            html_parts.append(f'                        <div class="btn-subtitle">{guide["subtitle"]}</div>')
            html_parts.append('                    </div>')
            html_parts.append('                </a>')
            html_parts.append('')
        
        # 添加推荐攻略区域结束标签
        html_parts.append('            </div>')
        html_parts.append('        </div>')
        
        return '\n'.join(html_parts)
    
    def update_index_html(self, new_recommendation_html):
        """
        更新index.html文件中的推荐攻略区域
        :param new_recommendation_html: 新的推荐攻略HTML代码
        :return: 是否更新成功
        """
        try:
            # 读取现有的index.html文件
            with open(self.index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找推荐攻略区域的开始和结束位置
            start_pattern = r'        <!-- 推荐攻略按钮区域 -->'
            end_pattern = r'        </div>\s*\n\s*<!-- 温馨提示区域 -->'
            
            start_match = re.search(start_pattern, content)
            end_match = re.search(end_pattern, content)
            
            if not start_match or not end_match:
                print("错误：无法找到推荐攻略区域的标记")
                return False
            
            # 替换推荐攻略区域内容
            before_section = content[:start_match.start()]
            after_section = content[end_match.start():]
            
            # 重新构建文件内容
            new_content = before_section + new_recommendation_html + '\n\n        ' + after_section
            
            # 备份原文件
            backup_file = self.index_file.with_suffix('.html.backup')
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已创建备份文件：{backup_file}")
            
            # 写入更新后的内容
            with open(self.index_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("index.html更新成功！")
            return True
            
        except Exception as e:
            print(f"错误：更新index.html失败：{e}")
            return False
    
    def run_update(self):
        """
        运行完整的更新流程
        """
        print("=" * 60)
        print("智能旅游规划助手 - 自动更新系统")
        print("=" * 60)
        print(f"项目根目录：{self.project_root.absolute()}")
        print(f"开始时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 1. 扫描destination目录
        print("1. 扫描destination目录...")
        html_files = self.scan_destination_files()
        if not html_files:
            print("没有找到攻略文件，退出更新。")
            return
        
        print()
        
        # 2. 提取攻略信息
        print("2. 提取攻略信息...")
        guides_info = []
        for file_path in html_files:
            print(f"正在处理：{file_path.name}")
            guide_info = self.extract_guide_info(file_path)
            if guide_info:
                guides_info.append(guide_info)
                print(f"  ✓ {guide_info['main_title']} - {guide_info['subtitle']}")
            else:
                print(f"  ✗ 跳过文件：{file_path.name}")
        
        print(f"\n成功提取 {len(guides_info)} 个攻略信息")
        
        if not guides_info:
            print("没有有效的攻略信息，退出更新。")
            return
        
        print()
        
        # 3. 生成新的推荐攻略HTML
        print("3. 生成推荐攻略HTML...")
        new_recommendation_html = self.generate_recommendation_html(guides_info)
        print("✓ HTML代码生成完成")
        
        print()
        
        # 4. 更新index.html
        print("4. 更新index.html...")
        if self.update_index_html(new_recommendation_html):
            print("✓ 更新完成！")
        else:
            print("✗ 更新失败！")
        
        print()
        print("=" * 60)
        print(f"结束时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)


def main():
    """主函数"""
    # 获取脚本所在目录作为项目根目录
    script_dir = Path(__file__).parent
    
    # 创建更新器实例并运行
    updater = IndexUpdater(script_dir)
    updater.run_update()


if __name__ == "__main__":
    main() 