import platform as plt
from .base import Nul
from .linux import Lin
from .macos import Mac
from .windows import Win

def new():
    sys = plt.system()
    try:
        if sys == "Windows": return Win()
        if sys == "Linux": return Lin()
        if sys == "Darwin": return Mac()
    except Exception:
        return Nul()
    return Nul()
# Glossary:
# new = create platform adapter
# sys = operating system
