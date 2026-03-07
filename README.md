# 💩 S.H.I.T Journal 工具集

一套用于 [S.H.I.T Journal](https://shitjournal.org) 的数据采集、下载和可视化分析工具。
>[!TIP]
> **在线单文件下载**: https://colorcard.github.io/SHIT-PDF-Downloader/
>
> **下载全部PDF**: https://github.com/colorcard/SHIT-PDF-Downloader/releases/tag/latest

---

## 📁 项目结构

```
.
├── src/                          # 源代码
│   ├── scraper.py               # 数据爬虫（多线程）
│   └── shitjournal_downloader.py # PDF下载器（命令行）
├── docs/                         # 网页工具
│   ├── shitjournal_downloader.html # PDF下载器（Web UI）
│   └── analysis.html            # 数据分析仪表板
├── data/                         # 数据文件
│   └── scraped_articles.json    # 爬取的文章数据
└── downloads/                    # PDF下载目录
```

---

## 🛠️ 功能模块

### 1. 数据爬虫 (`src/scraper.py`)

自动爬取所有分区的文章元数据，支持多线程下载PDF。

**功能特性：**
- 爬取四个发酵区（旱厕/化粪池/构石/沉淀区）的所有文章
- 获取标题、作者、学科、粘度评分、评论数等字段
- 8线程并发下载PDF文件
- 自动检测并重新下载缺失文件
- 智能文件名处理（避免过长）

**使用方法：**
```bash
pip install requests
python src/scraper.py
```

---

### 2. PDF下载器 - 命令行版 (`src/shitjournal_downloader.py`)

轻量级命令行工具，支持单个/批量下载。

**使用方法：**
```bash
# 单文件下载
python src/shitjournal_downloader.py https://shitjournal.org/preprints/UUID

# 交互模式
python src/shitjournal_downloader.py -i

# 批量下载
python src/shitjournal_downloader.py -f urls.txt -o ./pdfs/
```

---

### 3. PDF下载器 - Web版 (`docs/shitjournal_downloader.html`)

仿官网设计的单页面应用，免安装零依赖。

**特性：**
- 优雅的学术风格UI
- 输入UUID或完整URL即可下载
- 自动生成带签名的直链
- 内置跳转到数据分析页面

---

### 4. 数据分析仪表板 (`docs/analysis.html`)

全面的可视化分析页面，展示学术蝗虫的排泄行为。

**分析维度：**
- 📊 总体统计：总排泄量、学术蝗虫数、发酵天数、平均粘度
- 🔥 旷古烁今构思热词榜（词云）
- 🚽 发酵区分布态势
- 📈 每日排泄活跃度趋势
- 🏅 Top 20 高粘度构思排行
- 📊 粘度分布直方图
- 💎 粘度 vs 评论数散点图
- 👃 嗅探者活跃度分布
- 🎯 各分区平均粘度对比
- 🏆 Top 15 高产排泄者
- ⏰ 排泄者作息规律
- 📅 周排泄习惯分析

---

## 🔬 技术原理

S.H.I.T Journal 使用 Supabase Storage 存储PDF，需要通过以下流程获取文件：

1. 通过UUID查询数据库获取 `pdf_path`
2. 使用Anon Key请求签名URL（有效期1小时）
3. 拼接完整路径下载文件

本工具自动化了这一流程。

---

## ⚠️ 使用说明

- 仅供学习交流使用
- 请勿用于非法用途
- 尊重原作者版权

---

## 📄 开源协议

本项目采用 [MIT](LICENSE) 许可证开源，欢迎任何形式的使用、修改和分发。请保留原作者信息，并在适当位置注明本项目的来源。
