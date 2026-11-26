import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

path = pathlib.Path(sys.argv[1])
start = int(sys.argv[2])
end = int(sys.argv[3])
lines = path.read_text(encoding="utf-8").splitlines()
for i in range(max(0, start - 1), min(len(lines), end)):
    text = lines[i].replace("\u200b", "").replace("\ufffd", "'")
    print(f"{i + 1}: {text}")
