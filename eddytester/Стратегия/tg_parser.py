#!/usr/bin/env python3
"""
Парсинг публичных Telegram-каналов через tg.i-c-a.su (без API ID/Token)
Использование: python3 tg_parser.py <username_канала> [--limit 200]
Пример: python3 tg_parser.py qachanell --limit 100
Результат: /root/.openclaw/workspace/eddy_tg/competitors_<username>.json
"""

import requests, re, html, json, datetime, time, sys, os

def fetch_all_posts(channel, max_posts=200):
    all_posts = []
    offset_id = 0
    no_progress = 0
    
    while len(all_posts) < max_posts:
        url = f'https://tg.i-c-a.su/json/{channel}'
        params = {}
        if offset_id:
            params['offset_id'] = offset_id
        
        try:
            r = requests.get(url, params=params, timeout=15)
            data = r.json()
        except Exception as e:
            print(f'  Ошибка запроса: {e}')
            break
        
        msgs = data.get('messages', [])
        if not msgs:
            print('  Больше сообщений нет')
            break
        
        for m in msgs:
            txt = m.get('message', '')
            clean = re.sub(r'<[^>]+>', '', txt)
            clean = html.unescape(clean).strip()
            
            date_ts = m.get('date', 0)
            if isinstance(date_ts, (int, float)):
                date_str = datetime.datetime.fromtimestamp(date_ts).strftime('%Y-%m-%d %H:%M')
            else:
                date_str = str(date_ts)
            
            all_posts.append({
                'id': m.get('id'),
                'date': date_str,
                'text': clean,
                'views': m.get('views', 0),
                'forwards': m.get('forwards', 0)
            })
        
        ids = [m.get('id', 0) for m in msgs]
        new_offset = min(ids)
        
        if new_offset == offset_id:
            no_progress += 1
            if no_progress >= 3:
                break
        else:
            no_progress = 0
        
        offset_id = new_offset
        print(f'  загружено {len(all_posts)} | id={offset_id} | дата={all_posts[-1]["date"][:10]}', end='\r')
        time.sleep(0.3)
    
    print()
    return all_posts

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Использование: python3 tg_parser.py <username_канала> [--limit N]')
        sys.exit(1)
    
    channel = sys.argv[1].strip('@')
    limit = 200
    if '--limit' in sys.argv:
        idx = sys.argv.index('--limit')
        if idx + 1 < len(sys.argv):
            limit = int(sys.argv[idx + 1])
    
    print(f'Парсинг @{channel} (max {limit} постов)...')
    posts = fetch_all_posts(channel, limit)
    
    out_path = f'/root/.openclaw/workspace/eddy_tg/competitors_{channel}.json'
    with open(out_path, 'w') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    
    print(f'\nГотово: {len(posts)} постов')
    if posts:
        print(f'  Диапазон: {posts[-1]["date"]} -> {posts[0]["date"]}')
    print(f'  Файл: {out_path}')
