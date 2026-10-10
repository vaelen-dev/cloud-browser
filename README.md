# Cloud Browser on GitHub Codespaces

> AI-controlled persistent browser — logins/sessions cloud mein save rehte hain

## 🚀 Quick Start

### Step 1: Codespaces open karo
1. Is repo pe jao GitHub pe
2. Green **"Code"** button → **"Codespaces"** tab → **"Create codespace"**
3. Wait karo ~2-3 minutes (auto setup hoga)

### Step 2: Browser start karo
Terminal mein:
```bash
bash browser/start.sh
```

### Step 3: Browser dekho
- **Ports** tab mein `6080` pe click karo
- noVNC web interface mein browser dikhega

### Step 4: AI control
```bash
python browser/controller.py
```

## 📁 Structure
```
cloud-browser/
├── .devcontainer/
│   ├── devcontainer.json   # Codespaces config
│   └── setup.sh            # Auto install
├── browser/
│   ├── start.sh            # VNC + Browser start
│   └── controller.py       # AI browser control
└── browser-data/           # ← Persistent logins (auto-created)
└── screenshots/            # ← Screenshots (auto-created)
```

## 💾 Persistent Data
Browser data `/workspaces/cloud-browser/browser-data/` mein save hota hai.
- Codespaces mein yeh folder persist karta hai
- Login karo ek baar → hamesha logged in raho

## 🔐 Security Note
`browser-data/` folder mein sensitive data hota hai. Isko `.gitignore` mein add karo!
