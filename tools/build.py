import json, sys, re, datetime
def v(s):
    s=s.strip().upper()
    m={'K':1e3,'M':1e6}
    return int(float(s[:-1])*m[s[-1]]) if s and s[-1] in m else int(s or 0)
tiles={x['id']:v(x['tile']) for x in json.load(open('fcc/reels.json'))}
rows=[]
for l in open('fcc/meta.jsonl'):
    d=json.loads(l); desc=d.get('description') or ''
    rows.append(dict(id=d['id'],date=datetime.datetime.fromtimestamp(d['timestamp'],datetime.UTC).strftime('%Y-%m-%d %a %H:%M'),
        dur=round(d.get('duration') or 0),views=tiles.get(d['id'],0),
        likes=d.get('like_count'),comments=d.get('comment_count'),
        caption=re.sub(r'\s+',' ',desc)))
rows.sort(key=lambda r:r['date'])
json.dump(rows,open('fcc/data.json','w'),ensure_ascii=False,indent=0)
for r in rows: print(r['date'],r['dur'],r['views'],r['likes'],r['comments'],'|',r['caption'][:110])
