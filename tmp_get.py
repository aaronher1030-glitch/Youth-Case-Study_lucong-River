import requests, pypdf, io
u="https://citycouncilofmanila.com.ph/wp-content/uploads/2023/02/ORDINANCE-NO.-8491.pdf"
r=requests.get(u, headers={"User-Agent":"Mozilla/5.0"}, timeout=60)
print(r.status_code, len(r.content))
p=pypdf.PdfReader(io.BytesIO(r.content))
t="\n".join((pg.extract_text() or "") for pg in p.pages)
open("ord8491.txt","w",encoding="utf-8").write(t)
print(len(t))
