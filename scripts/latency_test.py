import argparse as arg
import json as js
import socket as soc
import statistics as sta
import time as tim

def msg(i):
    return {"version":"1.0","id":str(i),"type":"system","action":"ping","data":{}}
# Glossary:
# msg = message
# i = request id

def run():
    par=arg.ArgumentParser(description="Measure SmartDesk TCP ping latency")
    par.add_argument("host",dest="hst")
    par.add_argument("--port",dest="prt",type=int,default=8765)
    par.add_argument("--token",dest="tok",required=True)
    par.add_argument("--count",dest="cnt",type=int,default=20)
    cfg=par.parse_args()
    sam=[]; fail=0
    sk=soc.create_connection((cfg.hst,cfg.prt),timeout=5); sk.settimeout(3); fil=sk.makefile("rwb")
    try:
        fil.readline()
        req={"version":"1.0","id":"0","type":"auth","action":"resume","data":{"token":cfg.tok}}
        fil.write((js.dumps(req)+"\n").encode()); fil.flush(); res=js.loads(fil.readline().decode())
        if res.get("status")!="ok": raise RuntimeError("session resume failed")
        for i in range(1,cfg.cnt+1):
            req=msg(i); req["token"]=cfg.tok; ts=tim.perf_counter(); fil.write((js.dumps(req)+"\n").encode()); fil.flush(); lin=fil.readline()
            if not lin: fail+=1; continue
            res=js.loads(lin.decode())
            if res.get("status")=="ok": sam.append((tim.perf_counter()-ts)*1000)
            else: fail+=1
    finally:
        fil.close(); sk.close()
    rat=len(sam)/cfg.cnt*100 if cfg.cnt else 0
    print(f"Samples: {cfg.cnt}"); print(f"Successful: {len(sam)}"); print(f"Failed: {fail}"); print(f"Success rate: {rat:.2f}%")
    if sam:
        print(f"Average RTT: {sta.mean(sam):.2f} ms"); print(f"Minimum RTT: {min(sam):.2f} ms"); print(f"Maximum RTT: {max(sam):.2f} ms")
# Glossary:
# run = latency test
# par = parser
# cfg = configuration
# sam = samples
# fail = failures
# sk = socket
# fil = file
# req = request
# res = response
# lin = line
# ts = start time
# rat = success rate

if __name__ == "__main__": run()
