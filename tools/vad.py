import sys, os, subprocess, json, webrtcvad
adir=sys.argv[1]; vad=webrtcvad.Vad(3); out={}
for f in sorted(os.listdir(adir)):
    pcm=subprocess.run(['ffmpeg','-v','quiet','-i',os.path.join(adir,f),'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
    fr=960; n=len(pcm)//fr; sp=sum(vad.is_speech(pcm[i*fr:(i+1)*fr],16000) for i in range(n))
    first=[vad.is_speech(pcm[i*fr:(i+1)*fr],16000) for i in range(min(n,100))]  # first 3s
    out[f[:-4]]=dict(speech=round(sp/max(n,1),2),speech3s=round(sum(first)/max(len(first),1),2))
json.dump(out,open(sys.argv[2],'w'))
