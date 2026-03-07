import requests
import json
import os
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

SUPABASE_URL = "https://bcgdqepzakcufaadgnda.supabase.co"
SUPABASE_KEY = "sb_publishable_wHqWLjQwO2lMwkGLeBktng_Mk_xf5xd"
DATA_FILE = "../data/scraped_articles.json"
ZONES = ["latrine", "septic", "stone", "sediment"]

def load_existing_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"articles": {}, "last_update": None}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_articles(zone):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    url = f"{SUPABASE_URL}/rest/v1/preprints_with_ratings_mat"
    params = {
        "zone": f"eq.{zone}",
        "select": "id,manuscript_title,zone,created_at,author_name,discipline,weighted_score,rating_count,comment_count"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[-] 获取 {zone} 区文章失败: {e}")
        return []

def sanitize_filename(text):
    return re.sub(r'[<>:"/\\|?*]', '_', text)[:30]

def download_and_rename(article, output_dir="downloads"):
    article_id = article["id"]
    title = sanitize_filename(article["manuscript_title"])
    author = sanitize_filename(article["author_name"])
    discipline = article["discipline"]

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    db_url = f"{SUPABASE_URL}/rest/v1/preprints_with_ratings_mat?id=eq.{article_id}&select=pdf_path"
    try:
        response = requests.get(db_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data or not data[0].get("pdf_path"):
            return False

        pdf_path = data[0]["pdf_path"]
        sign_url = f"{SUPABASE_URL}/storage/v1/object/sign/manuscripts/{pdf_path}"
        sign_response = requests.post(sign_url, headers=headers, json={"expiresIn": 3600})
        sign_response.raise_for_status()

        signed_path = sign_response.json().get("signedURL")
        final_url = f"{SUPABASE_URL}/storage/v1{signed_path}"

        pdf_response = requests.get(final_url, stream=True)
        pdf_response.raise_for_status()

        os.makedirs(output_dir, exist_ok=True)
        filename = f"{title}_{author}_{discipline}_{article_id[:8]}.pdf"
        save_path = os.path.join(output_dir, filename)

        with open(save_path, 'wb') as f:
            for chunk in pdf_response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[+] 已下载: {filename}")
        return True
    except Exception as e:
        print(f"[-] 下载失败 {article_id}: {e}")
        return False

def check_missing_downloads(output_dir="downloads"):
    data = load_existing_data()
    if not os.path.exists(output_dir):
        return list(data["articles"].values())

    existing_files = set(os.listdir(output_dir))
    missing = []

    for article in data["articles"].values():
        article_id = article["id"]
        found = any(article_id[:8] in f for f in existing_files)
        if not found:
            missing.append(article)

    return missing

def scrape_all_zones():
    data = load_existing_data()
    existing_ids = set(data["articles"].keys())
    new_articles = []
    updated = 0

    for zone in ZONES:
        print(f"[*] 正在爬取 {zone} 区...")
        articles = fetch_articles(zone)

        for article in articles:
            article_id = article["id"]
            if article_id not in existing_ids:
                data["articles"][article_id] = article
                new_articles.append(article)
                print(f"[+] 新增: {article['manuscript_title']}")
            else:
                data["articles"][article_id] = article
                updated += 1

    data["last_update"] = datetime.now().isoformat()
    save_data(data)
    print(f"\n[*] 爬取完成！新增 {len(new_articles)} 篇，更新 {updated} 篇，总计 {len(data['articles'])} 篇")

    # 检查缺失的下载
    missing = check_missing_downloads()
    if missing:
        print(f"\n[*] 发现 {len(missing)} 篇缺失文件，开始重新下载...")
        success = 0
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(download_and_rename, article): article for article in missing}
            for future in as_completed(futures):
                if future.result():
                    success += 1
        print(f"\n[*] 重新下载完成！成功 {success}/{len(missing)} 篇")
    elif new_articles:
        print(f"\n[*] 开始多线程下载 {len(new_articles)} 篇文章...")
        success = 0
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(download_and_rename, article): article for article in new_articles}
            for future in as_completed(futures):
                if future.result():
                    success += 1
        print(f"\n[*] 下载完成！成功 {success}/{len(new_articles)} 篇")

if __name__ == "__main__":
    scrape_all_zones()
