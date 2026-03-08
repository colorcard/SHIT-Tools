#!/usr/bin/env python3
import json
import os
import shutil

def organize_pdfs():
    with open('data/scraped_articles.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create zone directories
    for zone in ['latrine', 'septic', 'stone', 'sediment']:
        os.makedirs(f'downloads_{zone}', exist_ok=True)

    # Map each PDF to its current zone
    organized = 0
    missing = 0

    for article_id, article in data['articles'].items():
        zone = article['zone']
        article_prefix = article_id[:8]

        # Find PDF file by article ID prefix (ID is at the end of filename)
        found = False
        if os.path.exists('downloads'):
            for pdf in os.listdir('downloads'):
                if f'_{article_prefix}.pdf' in pdf:
                    src = os.path.join('downloads', pdf)
                    dst = os.path.join(f'downloads_{zone}', pdf)
                    shutil.copy2(src, dst)
                    organized += 1
                    found = True
                    break

        if not found:
            missing += 1

    print(f"[*] 组织完成: {organized} 个PDF已分配到分区")
    if missing > 0:
        print(f"[!] {missing} 个文章缺少PDF文件")

    # Print zone statistics
    for zone in ['latrine', 'septic', 'stone', 'sediment']:
        zone_dir = f'downloads_{zone}'
        if os.path.exists(zone_dir):
            count = len([f for f in os.listdir(zone_dir) if f.endswith('.pdf')])
            print(f"  - {zone}: {count} 篇")

if __name__ == '__main__':
    organize_pdfs()
