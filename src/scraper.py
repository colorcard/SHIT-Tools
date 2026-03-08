import requests
import json
import os
import re
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "https://api.shitjournal.org/api/articles/"
SUPABASE_URL = "https://bcgdqepzakcufaadgnda.supabase.co"
SUPABASE_KEY = "sb_publishable_wHqWLjQwO2lMwkGLeBktng_Mk_xf5xd"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "../data/scraped_articles.json")
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
    all_articles = []
    page = 1
    while True:
        params = {
            "zone": zone,
            "sort": "newest",
            "discipline": "all",
            "page": page,
            "limit": 50
        }
        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            articles = data.get("data", [])

            if not articles:
                break

            for article in articles:
                all_articles.append({
                    "id": article["id"],
                    "manuscript_title": article["title"],
                    "zone": article["zones"],
                    "created_at": article["created_at"],
                    "author_name": article["author"]["display_name"],
                    "discipline": article["discipline"],
                    "weighted_score": article["weighted_score"],
                    "rating_count": article["rating_count"],
                    "comment_count": article["comment_count"]
                })

            page += 1
        except Exception as e:
            print(f"[-] 获取 {zone} 区第 {page} 页失败: {e}")
            break

    return all_articles

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
            return (False, "未找到PDF路径")

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
        return (True, None)
    except Exception as e:
        return (False, str(e))

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

def scrape_all_zones(skip_download=False):
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
                old = data["articles"][article_id]
                changes = []
                if old.get("zone") != article.get("zone"):
                    changes.append(f"zone: {old.get('zone')} → {article.get('zone')}")
                if old.get("weighted_score") != article.get("weighted_score"):
                    changes.append(f"score: {old.get('weighted_score'):.2f} → {article.get('weighted_score'):.2f}")
                if old.get("rating_count") != article.get("rating_count"):
                    changes.append(f"ratings: {old.get('rating_count')} → {article.get('rating_count')}")
                if old.get("comment_count") != article.get("comment_count"):
                    changes.append(f"comments: {old.get('comment_count')} → {article.get('comment_count')}")

                data["articles"][article_id] = article
                updated += 1

                if changes:
                    print(f"[~] 更新: {article['manuscript_title'][:30]} ({', '.join(changes)})")

    data["last_update"] = datetime.now().isoformat()
    save_data(data)
    print(f"\n[*] 爬取完成！新增 {len(new_articles)} 篇，更新 {updated} 篇，总计 {len(data['articles'])} 篇")

    if skip_download:
        print("[*] 跳过PDF下载（--no-download模式）")
        return

    # 检查缺失的下载
    missing = check_missing_downloads()
    if missing:
        print(f"\n[*] 发现 {len(missing)} 篇缺失文件，开始重新下载...")
        success = 0
        failed = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(download_and_rename, article): article for article in missing}
            for future in as_completed(futures):
                article = futures[future]
                ok, error = future.result()
                if ok:
                    success += 1
                else:
                    failed.append((article, error))

        print(f"\n[*] 重新下载完成！成功 {success}/{len(missing)} 篇")
        if failed:
            print(f"\n[!] 以下 {len(failed)} 篇下载失败：")
            for article, error in failed:
                print(f"  - {article['manuscript_title'][:40]} (ID: {article['id'][:8]})")
                print(f"    原因: {error}")
    elif new_articles:
        print(f"\n[*] 开始多线程下载 {len(new_articles)} 篇文章...")
        success = 0
        failed = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(download_and_rename, article): article for article in new_articles}
            for future in as_completed(futures):
                article = futures[future]
                ok, error = future.result()
                if ok:
                    success += 1
                else:
                    failed.append((article, error))

        print(f"\n[*] 下载完成！成功 {success}/{len(new_articles)} 篇")
        if failed:
            print(f"\n[!] 以下 {len(failed)} 篇下载失败：")
            for article, error in failed:
                print(f"  - {article['manuscript_title'][:40]} (ID: {article['id'][:8]})")
                print(f"    原因: {error}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S.H.I.T Journal 文章爬虫")
    parser.add_argument("--no-download", action="store_true", help="只爬取数据，跳过PDF下载")
    args = parser.parse_args()
    scrape_all_zones(skip_download=args.no_download)
