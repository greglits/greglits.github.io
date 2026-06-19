import os
src = "C:/Users/glits/Documents/GitHub/greglits.github.io/content/fr"   # puis recommence avec content/en
seen = {}
for name in sorted(os.listdir(src)):
    if not name.endswith(".md"):
        continue
    with open(os.path.join(src, name), encoding="utf-8") as f:
        lines = f.read().split("---", 2)[1].splitlines()
    slug = next((l.split(":",1)[1].strip() for l in lines if l.strip().startswith("slug:")), name[:-3])
    seen.setdefault(slug, []).append(name)

for slug, files in seen.items():
    if len(files) > 1:
        print(f"⚠️  slug '{slug}' produit par : {', '.join(files)}")