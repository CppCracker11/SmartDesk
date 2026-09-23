import json as js


def enc(msg):
    return (js.dumps(msg, separators=(",", ":")) + "\n").encode("utf-8")
# Glossary:
# enc = encode


def dec(dat):
    val = js.loads(dat.decode("utf-8"))
    if not isinstance(val, dict):
        raise ValueError("message must be an object")
    return val
# Glossary:
# dec = decode


def ok(i, dat=None):
    res = {"id": i, "status": "ok"}
    if dat is not None:
        res["data"] = dat
    return res
# Glossary:
# ok = success response


def err(i, cod, txt):
    return {"id": i, "status": "error", "error": {"code": cod, "message": txt}}
# Glossary:
# err = error response
