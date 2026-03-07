import sys
import re
import requests
import os
import argparse

SUPABASE_URL = "https://bcgdqepzakcufaadgnda.supabase.co"
SUPABASE_KEY = "sb_publishable_wHqWLjQwO2lMwkGLeBktng_Mk_xf5xd"

def extract_uuid(url_or_text):
    """从输入字符串中提取标准 UUID"""
    match = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', url_or_text, re.IGNORECASE)
    return match.group(1) if match else None

def download_pdf(target, output_dir="."):
    """执行单个 PDF 的鉴权获取与下载"""
    uuid = extract_uuid(target)
    if not uuid:
        print(f"[-] 无效的输入格式，未找到 UUID: {target}")
        return False

    print(f"\n[*] 解析到目标 UUID: {uuid}")
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    # Step 1: 查询数据库获取对应文章的 pdf_path
    print("[*] 正在从数据库获取文章 PDF 路径...")
    db_url = f"{SUPABASE_URL}/rest/v1/preprints_with_ratings_mat?id=eq.{uuid}&select=pdf_path"
    try:
        response = requests.get(db_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data:
            print("[-] 未找到该 UUID 对应的文章记录。")
            return False
            
        pdf_path = data[0].get("pdf_path")
        if not pdf_path:
            print("[-] 该文章暂无 PDF 路径记录，可能未上传附件。")
            return False
            
        print(f"[+] 定位到存储路径: {pdf_path}")
        
    except Exception as e:
        print(f"[-] 请求文章信息失败: {e}")
        return False

    # Step 2: 向 Supabase Storage 请求一小时内有效的签名下载链接
    print("[*] 正在请求带鉴权签名的防盗链下载地址...")
    sign_url = f"{SUPABASE_URL}/storage/v1/object/sign/manuscripts/{pdf_path}"
    try:
        sign_response = requests.post(
            sign_url, 
            headers=headers,
            json={"expiresIn": 3600}
        )
        sign_response.raise_for_status()
        sign_data = sign_response.json()
        
        signed_path = sign_data.get("signedURL")
        if not signed_path:
            print("[-] 响应异常: 未能获取到签名 URL。")
            return False
            
        final_url = f"{SUPABASE_URL}/storage/v1{signed_path}"
        print(f"[+] 成功生成下载直链！")
        
    except Exception as e:
        print(f"[-] 请求签名链接失败: {e}")
        return False

    # Step 3: 流式下载文件到本地
    print("[*] 正在拉取 PDF 文件...")
    try:
        pdf_response = requests.get(final_url, stream=True)
        pdf_response.raise_for_status()
        
        # 提取真实文件名
        filename = pdf_path.split('/')[-1]
        save_path = os.path.join(output_dir, filename)
        
        # 确保目标目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存文件
        with open(save_path, 'wb') as f:
            for chunk in pdf_response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"[+] 下载完成！已保存至: {os.path.abspath(save_path)}")
        return True
        
    except Exception as e:
        print(f"[-] 下载 PDF 过程出错: {e}")
        return False

def interactive_mode(output_dir):
    """交互模式：方便用户反复手动粘贴链接下载"""
    print("="*55)
    print(" 欢迎使用 S.H.I.T Journal PDF 交互式下载模式")
    print(" 提示: 直接粘贴带 UUID 的链接即可，输入 'q' 退出")
    print("="*55)
    while True:
        try:
            target = input("\n[?] 请输入论文链接或 UUID: ").strip()
            if target.lower() in ['q', 'quit', 'exit']:
                print("[*] 退出交互模式。")
                break
            if target:
                download_pdf(target, output_dir)
        except KeyboardInterrupt:
            print("\n[*] 退出交互模式。")
            break

def batch_mode(file_path, output_dir):
    """批量模式：从文本文件中逐行读取链接下载"""
    if not os.path.exists(file_path):
        print(f"[-] 批处理文件不存在: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            
        print(f"[*] 发现 {len(lines)} 个下载任务，准备开始处理...")
        success_count = 0
        for i, line in enumerate(lines, 1):
            print(f"\n--- 任务进度: {i}/{len(lines)} ---")
            if download_pdf(line, output_dir):
                success_count += 1
                
        print(f"\n[*] 批量下载完毕！成功 {success_count}/{len(lines)} 个文件。")
    except Exception as e:
        print(f"[-] 读取批处理文件时出错: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="S.H.I.T Journal PDF 自动化下载脚本\n"
                    "利用 Supabase 签名机制获取直链下载预印本。",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("url", nargs="?", help="要下载的论文链接或包含 UUID 的字符串 (默认单文件模式)")
    parser.add_argument("-i", "--interactive", action="store_true", help="开启交互模式，可连续粘贴多个链接进行下载")
    parser.add_argument("-f", "--file", help="指定包含多个链接的文本文件，开启批量下载模式")
    parser.add_argument("-o", "--output", default=".", help="指定下载文件保存的目录 (默认保存在当前目录)")
    
    args = parser.parse_args()
    
    # 按照优先级处理运行模式
    if args.interactive:
        interactive_mode(args.output)
    elif args.file:
        batch_mode(args.file, args.output)
    elif args.url:
        download_pdf(args.url, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()