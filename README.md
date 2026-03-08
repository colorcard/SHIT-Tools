<div align="center">

# 💩 S.H.I.T Journal 工具集

**[S.H.I.T Journal](https://shitjournal.org) 数据采集、下载与可视化分析的完整工具套件**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/v/release/colorcard/SHIT-PDF-Downloader)](https://github.com/colorcard/SHIT-Tools/releases)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fcolorcard.github.io%2FSHIT-PDF-Downloader%2F)](https://shit.colorcard.cc/)

[🌐 在线下载器](https://shit.colorcard.cc/) • [📊 数据观测站](https://shit.colorcard.cc/analysis.html) • [📦 批量下载](https://github.com/colorcard/SHIT-Tools/releases/tag/latest)

</div>

---

## ✨ 核心特性

- 🚀 **Web PDF 下载器** - 简洁优雅的界面，支持 UUID/URL 直接下载
- 📊 **数据观测站** - 16 个交互式图表，实时数据可视化分析
- 🕷️ **多线程爬虫** - 自动化采集所有分区数据
- 💻 **命令行工具** - 支持批量下载的强大 CLI
- 📱 **移动端适配** - 完美支持各种屏幕尺寸
- 🎨 **学术风格设计** - 优雅的期刊风格界面
- ⚡ **极致压缩** - 数据文件压缩 60%，加载速度显著提升

---

## 🎯 快速开始

### 在线工具（无需安装）

**单文件下载：**
```
https://shit.colorcard.cc/
```

**数据分析：**
```
https://shit.colorcard.cc/analysis.html
```

**批量下载（所有 PDF）：**
```
https://github.com/colorcard/SHIT-Tools/releases/tag/latest
```

### 命令行工具

```bash
# 安装依赖
pip install requests

# 单文件下载
python src/shitjournal_downloader.py https://shitjournal.org/preprints/UUID

# 交互模式
python src/shitjournal_downloader.py -i

# 批量下载
python src/shitjournal_downloader.py -f urls.txt -o ./pdfs/
```

---

## 📁 项目结构

```
SHIT-Tools/
├── src/
│   ├── scraper.py                    # 多线程数据爬虫
│   ├── shitjournal_downloader.py     # 命令行 PDF 下载器
│   └── compress_articles.py          # 数据压缩脚本
├── docs/
│   ├── shitjournal_downloader.html   # Web 下载器
│   └── analysis.html                 # 数据分析仪表板
├── data/
│   └── scraped_articles.json         # 爬取的文章元数据
├── dev/
│   └── serve-local.sh                # 本地部署脚本
└── downloads/                         # PDF 下载目录
```

---

## 🛠️ 功能模块

### 1. Web PDF 下载器

优雅的学术风格单页应用，零依赖免安装。

**功能特性：**
- 直接下载：输入 UUID 或完整 URL 即可下载
- 检索下载：按标题、作者、发酵区、学科搜索文章
- 智能排序：支持按日期或浏览量排序
- 自动解析：智能识别 URL 并提取 UUID
- 响应式设计：完美适配手机、平板、桌面

**使用方法：**
1. 访问 [在线下载器](https://shit.colorcard.cc/)
2. 选择"直接下载"或"检索下载"标签页
3. 输入 UUID/URL 或搜索文章
4. 点击下载按钮

---

### 2. 数据观测站

💩 粪坑数据观测站 - 学术蝗虫排泄行为可视化分析

**统计指标：**
- 💩 总排泄量、🦗 学术蝗虫数、⏱️ 发酵天数
- 📊 日均排泄率、🎯 人均产量、💬 总评论数、⭐ 平均粘度

**16 个可视化图表：**
- 🔥 旷古烁今构思热词榜（词云）
- 🚽 发酵区分布态势（饼图）
- 📚 学科蝗灾分布图（饼图）
- 📈 每日排泄活跃度（折线图）
- 🌊 各发酵区时间演化（多线图）
- 🎨 发酵区-学科交叉污染（柱状图）
- ⏰ 排泄者作息规律（柱状图）
- 🏆 Top 15 高产排泄者（柱状图）
- 📅 周排泄习惯分析（柱状图）
- 📊 月度发酵统计（柱状图）
- 🏅 Top 20 高粘度构思（柱状图）
- 📊 粘度分布直方图（柱状图）
- 🔥 评论数 Top 15（柱状图）
- 💎 粘度 vs 评论数散点图（散点图）
- 👃 嗅探者活跃度分布（柱状图）
- 🎯 各分区平均粘度对比（柱状图）

**技术栈：**
- Chart.js - 交互式图表库
- WordCloud2.js - 词云生成
- 纯 JavaScript - 无框架依赖

---

### 3. 数据爬虫

多线程自动化数据采集工具。

**功能特性：**
- 爬取四个发酵区（旱厕/化粪池/构石/沉淀区）所有文章
- 提取元数据：标题、作者、学科、粘度评分、评论数
- 8 线程并发下载 PDF 文件
- 自动重试失败的下载
- 智能文件名处理（避免过长路径）

**使用方法：**
```bash
pip install requests
python src/scraper.py
```

**输出：**
- `data/scraped_articles.json` - 文章元数据
- `downloads/` - 下载的 PDF 文件

---

### 4. 命令行下载器

轻量级批量下载工具。

**命令选项：**
```bash
python src/shitjournal_downloader.py [选项]

选项:
  URL                  直接从 URL 下载
  -i, --interactive    交互模式
  -f, --file FILE      从文件批量下载
  -o, --output DIR     输出目录（默认: ./downloads）
```

**使用示例：**
```bash
# 单文件下载
python src/shitjournal_downloader.py https://shitjournal.org/preprints/abc123

# 批量下载
echo "uuid1\nuuid2\nuuid3" > urls.txt
python src/shitjournal_downloader.py -f urls.txt -o ./pdfs/
```

---

### 5. 数据压缩优化

智能数据压缩系统，显著提升页面加载性能。

**压缩效果：**
- 原始 JSON：831 KB
- 压缩后 JS：333 KB
- 压缩率：60%

**优化技术：**
- 移除 UUID 冗余（数组替代对象键）
- ISO 时间戳转 Unix 时间戳
- 浮点数精度优化（保留 2 位小数）
- 单字母键名压缩
- JS 格式替代 JSON（移除键名引号）

**使用方法：**
```bash
# 手动压缩
python src/compress_articles.py

# 本地测试部署
./dev/serve-local.sh
```

**自动化：**
- GitHub Actions 自动在部署时压缩
- 本地开发脚本集成压缩流程

---

## 🔬 技术原理

### 架构说明

S.H.I.T Journal 使用 **Supabase Storage** 托管 PDF 文件。下载流程：

1. 通过 UUID 查询数据库获取 `pdf_path`
2. 使用 Anon Key 请求签名 URL（有效期 1 小时）
3. 从签名 URL 下载文件

本工具自动化了整个流程。

### API 端点

```javascript
// Supabase 配置
const SUPABASE_URL = 'https://ybgjzxdswzrcfzbtpnmf.supabase.co'
const BUCKET_NAME = 'shit-journal-pdfs'

// 生成下载 URL
const { data } = supabase.storage
  .from(BUCKET_NAME)
  .getPublicUrl(`${uuid}.pdf`)
```

### 数据结构

```json
{
  "id": "uuid",
  "manuscript_title": "string",
  "zone": "latrine|septic|stone|sediment",
  "discipline": "string",
  "author_name": "string",
  "created_at": "ISO8601",
  "weighted_score": "float",
  "rating_count": "int",
  "comment_count": "int"
}
```

---

## 📊 数据统计

基于最新爬取数据：

- **文章总数：** 1000+
- **活跃作者：** 200+
- **覆盖分区：** 4 个（旱厕、化粪池、构石、沉淀区）
- **学科领域：** 10+ 个
- **数据更新：** 每日通过 GitHub Actions 自动更新

---

## 🚀 部署说明

### GitHub Pages

Web 工具通过 GitHub Actions 自动部署：

```yaml
# .github/workflows/deploy.yml
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 20 * * *'  # 每日 04:00 CST
```

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/colorcard/SHIT-PDF-Downloader.git
cd SHIT-PDF-Downloader

# 打开 Web 工具
open docs/shitjournal_downloader.html
open docs/analysis.html

# 运行爬虫
python src/scraper.py
```

---

## 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## ⚠️ 免责声明

本项目仅供**学习和研究目的**使用。

- 尊重版权和知识产权
- 请勿用于商业用途
- 遵守 [S.H.I.T Journal](https://shitjournal.org) 使用条款
- 负责任和道德地使用

---

## 📄 开源协议

本项目采用 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [S.H.I.T Journal](https://shitjournal.org) 提供平台
- [Supabase](https://supabase.com) 提供存储基础设施
- [Chart.js](https://www.chartjs.org) 提供可视化库
- [WordCloud2.js](https://github.com/timdream/wordcloud2.js) 提供词云生成
- 所有贡献者和用户

---

<div align="center">

**用数学的严谨，守护思想的粪坑 💩**

[报告问题](https://github.com/colorcard/SHIT-Tools/issues) • [功能建议](https://github.com/colorcard/SHIT-Tools/issues)

</div>
