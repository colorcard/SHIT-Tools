# S.H.I.T Journal Downloader

S.H.I.T Journal Downloader 是一套用于从 [S.H.I.T Journal](https://shitjournal.org) 安全、快速地下载预印本 PDF 文件的工具集。包含一个功能全面的 **Python 自动化脚本** 以及一个仿官方极简设计的 **Web 网页工具**。

## 🔬 原理说明

> [!WARNING]
> 仅供交流学习使用，请勿用于非法攻击用途。

由于该期刊网站的附件并没有直接暴露公网的静态 URL，而是使用了 **Supabase Storage** 的鉴权防盗链机制，普通下载工具无法直接抓取 PDF 文件。其背后的运作逻辑如下：

1. 网站将 PDF 文件存放于权限受限的 `manuscripts` 存储桶中。
2. 页面在加载时，通过内置的公开匿名密钥（Anon Key）向数据库（`preprints_with_ratings_mat`）请求检索该文章对应的内部文件路径（`pdf_path`）。
3. 利用获取到的 `pdf_path` 向 Supabase Storage API 请求一个带 JWT Token 的**签名访问链接（Signed URL）**，该链接的有效期通常为 1 小时。
4. 拼接基础路由 `/storage/v1` 后，最终得到可安全下载文件的直链。

本工具通过自动化模拟上述前端交互流程，通过提取原文链接中的 `UUID` 标识，自动完成 **查询路径 -> 签发 Token -> 获取防盗链直链** 的全过程。

---

## 🛠️ 工具一：Python 命令行下载器

`shitjournal_downloader.py` 是一个轻量级、无需浏览器环境的自动化脚本。支持丰富的运行模式，非常适合需要批量处理或在服务器环境运行的用户。

### 依赖安装

首先，你需要确保 Python 环境中安装了 `requests` 库：
```bash
pip install requests
```

### 使用方法

该脚本支持四种主要模式，可以通过命令行参数灵活调用：

**1. 默认模式（单文件下载）**  
直接在命令行后追加预印本的链接或纯 UUID 即可下载，文件会默认保存在当前目录：
```bash
python shitjournal_downloader.py https://shitjournal.org/preprints/b9cff339-52e2-4c44-bf5c-db7626c251ab
```

**2. 交互模式（`-i` / `--interactive`）**  
适用于需要手动连续下载多篇文献的情况，程序将保持运行并提示你不断输入新的链接：
```bash
python shitjournal_downloader.py -i
```

**3. 批量模式（`-f` / `--file`）**  
将所有想要下载的链接或 UUID 按行保存在一个文本文件中（如 `urls.txt`），脚本会自动逐行读取并批量下载：
```bash
python shitjournal_downloader.py -f urls.txt
```

**4. 自定义保存目录（`-o` / `--output`）**  
结合以上任何模式，使用 `-o` 参数指定下载目标文件夹（如不存在会自动创建）：
```bash
python shitjournal_downloader.py https://... -o ./pdfs/
```

查看所有支持的命令说明：
```bash
python shitjournal_downloader.py -h
```

---

## 🌐 工具二：Web UI 网页下载器

`shitjournal_downloader.html` 是一个纯粹的 HTML/JS 静态单页面应用。它的 UI 经过深度优化，模仿了期刊官网优雅的学术风格（使用了衬线字体、深灰色调与亮金色点缀）。

### 核心特性
- **免安装、零依赖**：只要有浏览器就能运行，无需任何服务端支持或环境配置。
- **美观还原**：完美复现了源站所采用的 Playfair Display 和 Noto Serif SC 学术字体风格。
- **规避 CORS 限制**：因为 Supabase 的默认跨域配置较为宽泛，双击本地 HTML 文件即可直接发起 API 请求并成功回传结果。

### 使用方法
1. 使用电脑中任意现代浏览器（Chrome、Edge、Safari 等）直接双击打开 `shitjournal_downloader.html`。
2. 在输入框内粘贴带 UUID 的论文网址。
3. 按下回车或点击“Generate Direct Link”，等待处理完成后点击生成的醒目按钮即可保存 PDF。
