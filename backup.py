import shutil, os
from datetime import datetime

def auto_backup():
    if not os.path.exists("backup"):
        os.mkdir("backup")

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    shutil.copy("pol.db", f"backup/pol_{ts}.db")
