# -*- coding: utf-8 -*-
import shutil, zipfile, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SRC = r"C:\Users\Mahboobian\Desktop\article 6\Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE11_REEXEC.docx"
DST = r"C:\Users\Mahboobian\Desktop\article 6\Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE11_REEXEC_SINGLECOLUMN.docx"
shutil.copy(SRC, DST)
zin = zipfile.ZipFile(SRC)
items = {n: zin.read(n) for n in zin.namelist()}; zin.close()
xml = items["word/document.xml"].decode("utf-8")
assert '<w:cols w:num="2"' in xml, "two-col marker not found"
x2 = xml.replace('<w:cols w:num="2" w:space="360"/>', '<w:cols w:num="1" w:space="360"/>')
items["word/document.xml"] = x2.encode("utf-8")
with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as z:
    for n, data in items.items():
        z.writestr(n, data)
print("single-col saved:", DST, os.path.getsize(DST), "bytes")
# verify
z = zipfile.ZipFile(DST)
x = z.read("word/document.xml").decode("utf-8")
print("cols marker now:", [s for s in ['<w:cols w:num="1"', '<w:cols w:num="2"'] if s in x])
z.close()
