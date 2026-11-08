# -*- coding: utf-8 -*-
"""Apply E1 and E5 with exact unicode to the already-saved PHASE11 docx."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import docx
DST = r"C:\Users\Mahboobian\Desktop\article 6\Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE11_REEXEC.docx"
d = docx.Document(DST)

# E1: para 113 - insert re-exec NR finding
p = d.paragraphs[113]
old = "This margin is empirical rather than a guarantee:"
new = ("Re-executed on all seven Study-B days, the F-P1 LinDistFlow minimum of 0.930 pu corresponds to an NR minimum of 0.9261-0.9277 pu "
       "(maximum LD-NR deviation 0.0082 pu on 10 April), so the 'zero voltage violations' statement is a LinDistFlow result and the empirical AC margin "
       "is about 0.004 pu. " + old)
assert old in p.text, "E1 anchor not found"
p.text = p.text.replace(old, new, 1)
print("E1 applied (para 113)")

# E5: para 123 - append (alpha,K) robustness before final sentence
p = d.paragraphs[123]
old = "Xu is retained as a convex approximation, not as evidence of a superior aging law."
new = ("Re-executed over alpha in {0.8, 0.9, 0.95} x K in {12, 100}, mean profit varies by at most 6.1 EUR (0.2%), so the operating choice "
       "(alpha = 0.95, K = 12) is not load-bearing. " + old)
assert old in p.text, "E5 anchor not found"
p.text = p.text.replace(old, new, 1)
print("E5 applied (para 123)")

d.save(DST)
print("SAVED", DST)
# verify
d2 = docx.Document(DST)
print("para113 has '0.9261':", "0.9261" in d2.paragraphs[113].text)
print("para123 has '6.1 EUR':", "6.1 EUR" in d2.paragraphs[123].text)
