# sites

Static one-off sites built with Claude. Each subfolder is its own site, deployed independently to Vercel.

## Layout

```
sites/
├── interstellar/   → scroll-driven Interstellar tribute (canvas + scroll)
└── afterhours/     → AFTERHOURS / NYC — DJ agency landing (artlist.io style)
```

## Local preview

From this folder:

```sh
python3 -m http.server 8080
```

Then open `http://localhost:8080/interstellar/` or `http://localhost:8080/afterhours/`.

To preview from another device on the same WiFi:

```sh
python3 -m http.server 8080 --bind 0.0.0.0
# then visit http://<your-LAN-ip>:8080/interstellar/
```

## Deploy

Each subfolder is deployed as its own Vercel project. From inside a subfolder:

```sh
cd interstellar
npx vercel --prod
```

First run prompts for project name + scope. Subsequent runs reuse the project.

## Cloning to another machine

```sh
git clone <this-repo-url>
cd sites
# pick a subfolder, edit, push — Vercel redeploys automatically
```
