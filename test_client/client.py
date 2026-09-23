import json as js
import socket as soc
import time as tim

PRT = 8765
DPT = 8766
VER = "1.0"

class Cli:
    def __init__(self):
        self.soc = None
        self.tok = None
        self.fil = None
        self.nxt = 1

    def msg(self, typ, act, dat=None):
        msg={"version":VER,"id":str(self.nxt),"type":typ,"action":act,"data":dat or {}}
        self.nxt += 1
        if self.tok: msg["token"] = self.tok
        return msg
    # Glossary:
    # msg = message
    # typ = type
    # act = action
    # dat = data

    def snd(self, msg):
        self.soc.sendall((js.dumps(msg,separators=(",",":"))+"\n").encode())
        return js.loads(self.fil.readline().decode())
    # Glossary:
    # snd = send message

    def con(self, hst, prt):
        self.soc=soc.create_connection((hst,prt),5)
        self.soc.settimeout(5)
        self.fil = self.soc.makefile("rb")
        self.fil.readline()
        print(f"Connected to {hst}:{prt}")
    # Glossary:
    # con = connect
    # hst = host
    # prt = port

    def pai(self, cod):
        res=self.snd(self.msg("auth","pair",{"code":cod}))
        print(js.dumps(res,indent=2))
        if res.get("status")=="ok": self.tok=res.get("data",{}).get("token")
    # Glossary:
    # pai = pair
    # cod = code
    # res = response

    def run(self):
        hst=input("Host [127.0.0.1]: ").strip() or "127.0.0.1"
        try: prt=int(input(f"Port [{PRT}]: ").strip() or PRT)
        except ValueError: prt=PRT
        self.con(hst,prt)
        cod=input("Pair code: ").strip(); self.pai(cod)
        if not self.tok: return
        while True:
            cmd=input("Command [ping/info/move/key/quit]: ").strip().lower()
            if cmd=="quit": break
            if cmd=="ping": res=self.snd(self.msg("system","ping"))
            elif cmd=="info": res=self.snd(self.msg("system","get_host_info"))
            elif cmd=="move":
                dx=int(input("dx: ")); dy=int(input("dy: ")); res=self.snd(self.msg("mouse","move",{"dx":dx,"dy":dy}))
            elif cmd=="key":
                key=input("key: "); res=self.snd(self.msg("keyboard","press",{"key":key})); print(js.dumps(res,indent=2)); res=self.snd(self.msg("keyboard","release",{"key":key}))
            else: print("Unknown command"); continue
            print(js.dumps(res,indent=2))
        if self.fil: self.fil.close()
        self.soc.close()
    # Glossary:
    # run = client loop

if __name__ == "__main__": Cli().run()
