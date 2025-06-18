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
            "hefei_anqing_guide.html": ["🏛️", "合肥-安庆端午攻略", "感受历史文化名城"],
            "hefei_chuzhou_guide.html": ["🏛️", "合肥-滁州周末攻略", "探寻醉翁亭文化之旅"],
            "hefei_hefei_guide.html": ["🏛️", "合肥-合肥周末攻略", "体验淝水风投之城"],
            "hefei_huainan_guide.html": ["🏛️", "合肥-淮南周末攻略", "品味豆腐发源之乡"],
            "hefei_liuan_guide.html": ["🏞️", "合肥-六安周末攻略", "皖西风光深度体验"],
            "hefei_wuhu_guide.html": ["🌊", "合肥-芜湖周末攻略", "皖南风光二日游"],
            "hefei_maanshan_guide.html": ["🏔️", "合肥-马鞍山周末攻略", "长江三矶诗韵之旅"],
            "hefei_bozhou_guide.html": ["🏛️", "合肥-亳州周末攻略", "探索千年古城中医药文化"],
            "fuyang_weekend_guide.html": ["🏛️", "合肥-阜阳周末攻略", "探索皖北水乡皖北水乡"],
            "hefei_chizhou_guide.html": ["⛰️", "合肥-池州周末攻略", "佛教圣地九华山之旅"],
            "hefei_xuancheng_guide.html": ["🏞️", "合肥-宣城周末攻略", "诗意皖南山水二日游"],
            "hefei_huaibei_guide.html": ["🏛️", "合肥-淮北周末攻略", "探索淮北煤城文化魅力"],
            "nanjing_nanjing_guide.html": ["🏮", "南京周末游攻略", "探寻六朝古都的魅力"],
            "nanjing_wuxi_guide.html": ["🌸", "南京-无锡周末攻略", "江南水乡风情二日游"],
            "nanjing_zhenjiang_guide.html": ["🏯", "南京-镇江周末攻略", "江南古韵千年文脉之旅"],
            "nanjing_changzhou_guide.html": ["🦕", "南京-常州周末攻略", "体验恐龙王国的刺激与江南古韵"],
            "nanjing_suzhou_guide.html": ["🏮", "南京-苏州周末攻略", "探索江南水乡的诗意之美"],
            "nanjing_suqian_guide.html": ["🏛️", "南京-宿迁周末攻略", "探寻西楚霸王故里，感受千年历史文化"]
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
        elif "hefei" in filename and "chuzhou" in filename:
            icon, main_title, subtitle = "🏛️", "合肥-滁州攻略", "探寻醉翁亭文化之旅"
        elif "hefei" in filename and "liuan" in filename:
            icon, main_title, subtitle = "🏞️", "合肥-六安攻略", "皖西风光深度体验"
        elif "hefei" in filename and "wuhu" in filename:
            icon, main_title, subtitle = "🌊", "合肥-芜湖攻略", "皖南风光二日游"
        elif "hefei" in filename and "maanshan" in filename:
            icon, main_title, subtitle = "🏔️", "合肥-马鞍山攻略", "长江三矶诗韵之旅"
        elif "hefei" in filename and "bozhou" in filename:
            icon, main_title, subtitle = "🏛️", "合肥-亳州攻略", "探索千年古城中医药文化"
        elif "hefei" in filename and "xuancheng" in filename:
            icon, main_title, subtitle = "🏞️", "合肥-宣城攻略", "诗意皖南山水二日游"
        elif "hefei" in filename and "huaibei" in filename:
            icon, main_title, subtitle = "🏛️", "合肥-淮北攻略", "探索淮北煤城文化魅力"
        elif "nanjing" in filename and "nanjing" in filename:
            icon, main_title, subtitle = "🏮", "南京周末游攻略", "探寻六朝古都的魅力"
        elif "nanjing" in filename and "wuxi" in filename:
            icon, main_title, subtitle = "🌸", "南京-无锡攻略", "江南水乡风情二日游"
        elif "nanjing" in filename and "zhenjiang" in filename:
            icon, main_title, subtitle = "🏯", "南京-镇江攻略", "江南古韵千年文脉之旅"
        elif "nanjing" in filename and "changzhou" in filename:
            icon, main_title, subtitle = "🦕", "南京-常州攻略", "体验恐龙王国的刺激与江南古韵"
        elif "nanjing" in filename and "suzhou" in filename:
            icon, main_title, subtitle = "🏮", "南京-苏州攻略", "探索江南水乡的诗意之美"
        elif "nanjing" in filename and "suqian" in filename:
            icon, main_title, subtitle = "🏛️", "南京-宿迁攻略", "探寻西楚霸王故里，感受千年历史文化"
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
    
    def generate_guide_mapping(self, guides_info):
        """
        根据攻略文件生成映射关系
        :param guides_info: 攻略信息列表
        :return: 映射关系字典
        """
        mapping = {}
        
        for guide in guides_info:
            filename = guide['filename']
            
            # 特殊处理fuyang_weekend_guide.html
            if filename == 'fuyang_weekend_guide.html':
                departure_cn = '阜阳'
                destination_cn = '周末游'
                if departure_cn not in mapping:
                    mapping[departure_cn] = {}
                mapping[departure_cn][destination_cn] = filename
                continue
            
            # 特殊处理nanjing_nanjing_guide.html (南京周末游)
            if filename == 'nanjing_nanjing_guide.html':
                departure_cn = '南京'
                destination_cn = '周末游'
                if departure_cn not in mapping:
                    mapping[departure_cn] = {}
                mapping[departure_cn][destination_cn] = filename
                continue
            
            # 解析文件名获取出发地和目的地
            if '_' in filename:
                parts = filename.replace('.html', '').split('_')
                if len(parts) >= 2:
                    departure = parts[0]
                    destination = '_'.join(parts[1:])
                    
                    # 转换为中文城市名
                    departure_cn = self.convert_to_chinese_city(departure)
                    destination_cn = self.convert_to_chinese_city(destination)
                    
                    if departure_cn not in mapping:
                        mapping[departure_cn] = {}
                    
                    mapping[departure_cn][destination_cn] = filename
        
        return mapping
    
    def convert_to_chinese_city(self, english_name):
        """
        将英文城市名转换为中文
        :param english_name: 英文城市名
        :return: 中文城市名
        """
        city_mapping = {
            'hefei': '合肥',
            'beijing': '北京',
            'fuyang': '阜阳',
            'anqing': '安庆',
            'bozhou': '亳州',
            'chizhou': '池州',
            'chuzhou': '滁州',
            'huainan': '淮南',
            'huangshan': '黄山',
            'liuan': '六安',
            'maanshan': '马鞍山',
            'nanjing': '南京',
            'tongling': '铜陵',
            'wuhan': '武汉',
            'wuhu': '芜湖',
            'xuancheng': '宣城',
            'wuxi': '无锡',
            'zhenjiang': '镇江',
            'changzhou': '常州',
            'chengdu': '成都',
            'huaibei': '淮北',
            'weekend_guide': '周末游',
            'guide': ''  # 去掉文件名中的guide后缀
        }
        
        # 特殊处理：去掉guide后缀
        if english_name.endswith('_guide'):
            english_name = english_name.replace('_guide', '')
        
        return city_mapping.get(english_name.lower(), english_name)
    
    def generate_quick_select_html(self, guides_info):
        """
        生成快速选择热门攻略HTML代码
        :param guides_info: 攻略信息列表
        :return: HTML代码字符串
        """
        # 生成映射关系
        mapping = self.generate_guide_mapping(guides_info)
        
        html_parts = []
        
        # 添加快速选择区域开始标签
        html_parts.append('        <!-- 快速攻略选择区域 -->')
        html_parts.append('        <div class="recommendation-container">')
        html_parts.append('            <div class="recommendation-header">')
        html_parts.append('                <span class="icon">🚀</span>')
        html_parts.append('                快速选择热门攻略')
        html_parts.append('            </div>')
        html_parts.append('            <div class="quick-select-container">')
        html_parts.append('                <div class="select-row">')
        html_parts.append('                    <div class="select-group">')
        html_parts.append('                        <label class="select-label">')
        html_parts.append('                            <span class="icon">📍</span>')
        html_parts.append('                            出发地')
        html_parts.append('                        </label>')
        html_parts.append('                        <select class="quick-select" id="quickDeparture">')
        html_parts.append('                            <option value="">请选择出发地</option>')
        
        # 添加出发地选项
        for departure in sorted(mapping.keys()):
            html_parts.append(f'                            <option value="{departure}">{departure}</option>')
        
        html_parts.append('                        </select>')
        html_parts.append('                    </div>')
        html_parts.append('                    ')
        html_parts.append('                    <div class="select-group">')
        html_parts.append('                        <label class="select-label">')
        html_parts.append('                            <span class="icon">🎯</span>')
        html_parts.append('                            目的地')
        html_parts.append('                        </label>')
        html_parts.append('                        <select class="quick-select" id="quickDestination">')
        html_parts.append('                            <option value="">请选择目的地</option>')
        html_parts.append('                        </select>')
        html_parts.append('                    </div>')
        html_parts.append('                    ')
        html_parts.append('                    <div class="select-group">')
        html_parts.append('                        <button class="quick-go-btn" id="quickGoBtn" onclick="goToGuide()">')
        html_parts.append('                            <span class="icon">✨</span>')
        html_parts.append('                            查看攻略')
        html_parts.append('                        </button>')
        html_parts.append('                    </div>')
        html_parts.append('                </div>')
        html_parts.append('                <div class="quick-tip">')
        html_parts.append('                    <span class="icon">💡</span>')
        html_parts.append('                    根据您的出发地选择，为您推荐最适合的目的地攻略')
        html_parts.append('                </div>')
        html_parts.append('            </div>')
        html_parts.append('        </div>')
        html_parts.append('')
        
        return '\n'.join(html_parts), mapping
    
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
        html_parts.append('')
        
        return '\n'.join(html_parts)
    
    def generate_js_mapping(self, mapping):
        """
        生成JavaScript映射关系代码
        :param mapping: 映射关系字典
        :return: JavaScript代码字符串
        """
        js_parts = []
        js_parts.append('        // 攻略文件映射关系（基于destination目录中的实际文件）')
        js_parts.append('        const guideMapping = {')
        
        for departure, destinations in mapping.items():
            js_parts.append(f'            \'{departure}\': {{')
            for destination, filename in destinations.items():
                js_parts.append(f'                \'{destination}\': \'{filename}\',')
            js_parts.append('            },')
        
        js_parts.append('        };')
        
        return '\n'.join(js_parts)
    
    def update_index_html(self, new_quick_select_html, new_recommendation_html, js_mapping):
        """
        更新index.html文件中的快速选择热门攻略区域、推荐攻略区域和JavaScript映射
        :param new_quick_select_html: 新的快速选择热门攻略HTML代码
        :param new_recommendation_html: 新的推荐攻略HTML代码
        :param js_mapping: JavaScript映射关系代码
        :return: 是否更新成功
        """
        try:
            # 读取现有的index.html文件
            with open(self.index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 备份原文件
            backup_file = self.index_file.with_suffix('.html.backup')
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已创建备份文件：{backup_file}")
            
            # 1. 更新快速选择热门攻略区域
            quick_start_pattern = r'        <!-- 快速攻略选择区域 -->'
            quick_end_pattern = r'                                                                                <!-- 推荐攻略按钮区域 -->'
            
            quick_start_match = re.search(quick_start_pattern, content)
            quick_end_match = re.search(quick_end_pattern, content)
            
            if quick_start_match and quick_end_match:
                before_quick = content[:quick_start_match.start()]
                after_quick = content[quick_end_match.start():]
                content = before_quick + new_quick_select_html + after_quick
                print("✓ 快速选择热门攻略区域更新成功")
            else:
                print("⚠ 未找到快速选择热门攻略区域标记，跳过更新")
            
            # 2. 更新推荐攻略区域
            rec_start_pattern = r'        <!-- 推荐攻略按钮区域 -->'
            rec_end_pattern = r'        <!-- 温馨提示区域 -->'
            
            rec_start_match = re.search(rec_start_pattern, content)
            rec_end_match = re.search(rec_end_pattern, content)
            
            if rec_start_match and rec_end_match:
                before_rec = content[:rec_start_match.start()]
                after_rec = content[rec_end_match.start():]
                content = before_rec + new_recommendation_html + after_rec
                print("✓ 推荐攻略区域更新成功")
            else:
                print("⚠ 未找到推荐攻略区域标记，跳过更新")
            
            # 3. 更新JavaScript映射关系
            js_start_pattern = r'        // 攻略文件映射关系（基于destination目录中的实际文件）'
            js_end_pattern = r'        };'
            
            js_start_match = re.search(js_start_pattern, content)
            if js_start_match:
                # 找到映射关系结束位置
                remaining_content = content[js_start_match.start():]
                js_end_match = re.search(js_end_pattern, remaining_content)
                
                if js_end_match:
                    # 计算在原内容中的实际位置
                    js_end_pos = js_start_match.start() + js_end_match.end()
                    
                    before_js = content[:js_start_match.start()]
                    after_js = content[js_end_pos:]
                    content = before_js + js_mapping + after_js
                    print("✓ JavaScript映射关系更新成功")
                else:
                    print("⚠ 未找到JavaScript映射关系结束标记")
            else:
                print("⚠ 未找到JavaScript映射关系开始标记")
            
            # 写入更新后的内容
            with open(self.index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
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
        
        # 3. 生成新的快速选择热门攻略HTML和映射关系
        print("3. 生成快速选择热门攻略HTML...")
        new_quick_select_html, mapping = self.generate_quick_select_html(guides_info)
        print("✓ 快速选择热门攻略HTML代码生成完成")
        print(f"✓ 发现 {len(mapping)} 个出发地，共 {sum(len(dests) for dests in mapping.values())} 个目的地")
        
        # 4. 生成新的推荐攻略HTML
        print("4. 生成推荐攻略HTML...")
        new_recommendation_html = self.generate_recommendation_html(guides_info)
        print("✓ 推荐攻略HTML代码生成完成")
        
        # 5. 生成JavaScript映射关系
        print("5. 生成JavaScript映射关系...")
        js_mapping = self.generate_js_mapping(mapping)
        print("✓ JavaScript映射关系生成完成")
        
        print()
        
        # 6. 更新index.html
        print("6. 更新index.html...")
        if self.update_index_html(new_quick_select_html, new_recommendation_html, js_mapping):
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