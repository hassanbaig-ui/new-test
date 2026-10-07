import sys, os, json, time
from faster_whisper import WhisperModel
adir, out, size = sys.argv[1], sys.argv[2], sys.argv[3]
m = WhisperModel(size, device='cpu', compute_type='int8', cpu_threads=4)
done = set()
if os.path.exists(out):
    done = {json.loads(l)['id'] for l in open(out)}
files = sorted(f for f in os.listdir(adir) if f.endswith('.mp3'))
with open(out, 'a') as fo:
    for f in files:
        vid = f[:-4]
        if vid in done: continue
        t = time.time()
        segs, info = m.transcribe(os.path.join(adir, f), language='ur', vad_filter=True, beam_size=1,
                                  initial_prompt='کار اے سی، کمپریسر، گیس، کولنگ کوائل، وارنٹی، ملتان، FineCool')
        segs = [{'s': round(s.start,1), 'e': round(s.end,1), 't': s.text.strip()} for s in segs]
        fo.write(json.dumps({'id': vid, 'dur': info.duration, 'speech': sum(s['e']-s['s'] for s in segs), 'segs': segs}, ensure_ascii=False) + '\n'); fo.flush()
        print(vid, round(time.time()-t), 's', len(segs), 'segs', flush=True)
