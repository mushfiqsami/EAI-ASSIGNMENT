# TechConnect EAI Demo

Light-weight working prototype that accompanies my CIT6324 project report
(**Enterprise Application Integration**).  
The repository contains:

| Folder   | Contents                                |
|----------|-----------------------------------------|
| `backend`| Python 3.10 + Flask REST API (JSON & XML) |
| `web`    | Static HTML / JS single-page demo       |
| `desktop`| Tkinter desktop client                  |
| `tests`  | Minimal pytest suite (ping, order flow) |
| `samples`| Example XML/JSON payloads               |

---

## 1. Clone & set-up

```bash
cd techconnect-eai-demo
python -m venv venv                # optional but recommended
# Windows
venv\Scripts\activate
# Linux / macOS
# source venv/bin/activate

pip install -r backend/requirements.txt
