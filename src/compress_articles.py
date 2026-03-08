#!/usr/bin/env python3
import json
from datetime import datetime

def compress():
    with open('data/scraped_articles.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    articles = []
    for article in data['articles'].values():
        ts = int(datetime.fromisoformat(article['created_at'].replace('+00:00', '')).timestamp())
        articles.append({
            't': article['manuscript_title'],
            'z': article['zone'],
            'c': ts,
            'a': article['author_name'],
            'd': article['discipline'],
            's': round(article['weighted_score'], 2),
            'r': article['rating_count'],
            'm': article['comment_count']
        })

    with open('site/articles.js', 'w', encoding='utf-8') as f:
        f.write('const articles=')
        json.dump(articles, f, ensure_ascii=False, separators=(',', ':'))
        f.write(';')

if __name__ == '__main__':
    compress()
