# 智能旅游规划助手 - 自动更新功能

## 📖 功能介绍

这个自动更新系统能够自动扫描 `destination` 目录中的HTML攻略文件，并自动更新 `index.html` 中的推荐攻略区域。当您添加新的攻略文件到 `destination` 目录时，只需运行一次自动更新脚本，就能让新攻略出现在主页面上。

## 🚀 快速开始

### Windows用户
双击运行 `update.bat` 文件即可

### Linux/Mac用户
在终端中运行：
```bash
chmod +x update.sh
./update.sh
```

### 手动运行Python脚本
```bash
# 安装依赖
pip install -r requirements.txt

# 运行自动更新
python auto_update_index.py
```

## 📁 文件结构

```
项目根目录/
├── index.html                  # 主页面文件
├── destination/                # 攻略文件目录
│   ├── beijing_chengdu_guide.html
│   ├── hefei_nanjing_guide.html
│   ├── hefei_wuhan_guide.html
│   ├── hefei_tongling_guide.html
│   ├── hefei_huangshan_guide.html
│   └── hefei_anqing_guide.html
├── auto_update_index.py        # 自动更新脚本
├── requirements.txt            # Python依赖包
├── update.bat                  # Windows一键运行脚本
├── update.sh                   # Linux/Mac一键运行脚本
└── README_AUTO_UPDATE.md       # 使用说明文档
```

## ⚙️ 工作原理

1. **扫描目录**：自动扫描 `destination` 目录中的所有 `.html` 文件
2. **提取信息**：从每个HTML文件中提取标题信息
3. **生成HTML**：根据预设配置生成推荐攻略的HTML代码
4. **更新文件**：自动替换 `index.html` 中的推荐攻略区域
5. **备份保护**：更新前自动创建 `index.html.backup` 备份文件

## 📝 添加新攻略

### 方式一：使用预设配置（推荐）
如果您的攻略文件符合以下命名规范，系统会自动识别：
- `beijing_chengdu_guide.html` → 北京-成都五一攻略
- `hefei_nanjing_guide.html` → 合肥-南京端午攻略
- `hefei_wuhan_guide.html` → 合肥-武汉端午攻略
- `hefei_tongling_guide.html` → 合肥-铜陵端午攻略
- `hefei_huangshan_guide.html` → 合肥-黄山端午攻略
- `hefei_anqing_guide.html` → 合肥-安庆端午攻略

### 方式二：自定义配置
如果需要添加新的攻略类型，请编辑 `auto_update_index.py` 文件中的 `guide_config` 配置：

```python
self.guide_config = {
    "新文件名.html": ["🎪", "攻略标题", "攻略副标题"],
    # 例如：
    "shanghai_suzhou_guide.html": ["🏮", "上海-苏州攻略", "江南水乡深度游"]
}
```

### 方式三：自动识别
系统会尝试从HTML文件的 `<title>` 标签和 `<h1>` 标签中自动提取信息。

## 🔧 配置说明

### 图标配置
- 🏔️ 山岳类景点（如成都、黄山）
- 🏮 文化类景点（如南京、苏州）
- 🌸 城市风光（如武汉、樱花季）
- 🏭 工业遗产（如铜陵）
- ⛰️ 名山大川（如黄山、泰山）
- 🏛️ 历史古迹（如安庆、西安）

### 标题格式
- **主标题**：简洁明了，格式如"出发地-目的地+节日+攻略"
- **副标题**：突出特色，格式如"体验XX的魅力"、"探索XX风情"

## 🛠️ 高级功能

### 自动备份
每次更新前，系统会自动创建备份文件：
- `index.html.backup` - 原始文件备份
- 如果更新出错，可以手动恢复备份文件

### 错误处理
- 自动检测Python环境
- 自动安装依赖包
- 详细的错误信息提示
- 更新失败时保护原文件

### 批量处理
- 一次性处理所有攻略文件
- 自动排序和布局
- 响应式网格布局适配

## 🐛 故障排除

### 常见问题

**Q: 提示"未找到Python"**
A: 请先安装Python 3.7+，下载地址：https://www.python.org/downloads/

**Q: 依赖包安装失败**
A: 请检查网络连接，或手动运行：`pip install beautifulsoup4 lxml`

**Q: 新添加的攻略没有显示**
A: 请检查文件是否放在 `destination` 目录中，并重新运行更新脚本

**Q: 更新后页面样式异常**
A: 可以使用 `index.html.backup` 备份文件恢复，然后检查HTML文件格式

### 手动恢复
如果自动更新出现问题，可以手动恢复：
```bash
# 恢复备份文件
copy index.html.backup index.html  # Windows
cp index.html.backup index.html    # Linux/Mac
```

## 📞 技术支持

如果您在使用过程中遇到问题，请检查：
1. Python版本是否为3.7+
2. destination目录中的HTML文件格式是否正确
3. 网络连接是否正常（用于安装依赖包）
4. 文件权限是否足够（能否写入index.html）

## 🔄 版本更新

- **v1.0** - 基础自动更新功能
- **v1.1** - 添加预设配置和自动识别
- **v1.2** - 增加备份保护和错误处理
- **v1.3** - 支持一键运行脚本

---

*智能旅游规划助手 - 让旅行规划更简单* ✈️ 