# Resume ↔ Job Match

A simple Flask + OpenAI application that scores how well a resume matches a job description.  
It highlights **strengths**, **gaps**, **missing keywords**, and gives **recommendations**.

---

## 🚀 Quick Start (Non‑technical Users)

### 1️⃣ Install Docker
- **Windows / Mac**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux**: Follow the [Docker Engine install guide](https://docs.docker.com/engine/install/)

Make sure Docker is running before continuing.

---

### 2️⃣ Get an OpenAI API Key
1. Go to: [OpenAI API Keys](https://platform.openai.com/api-keys)  
2. Log in (or create an account)  
3. Click **Create new secret key**  
4. Copy your key — it will look like:
```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### 3️⃣ Run the App from Docker Hub
Open a terminal and run:

```bash
docker run --rm -e OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -p 8000:8000 mudabbir1187/resume-matcher:latest
```

Replace `sk-xxxxxxxx...` with **your** OpenAI API key.

**Then open:**  
👉 [http://localhost:8000](http://localhost:8000)

Paste your **Job Description** and **Resume**, click **Analyze match**, and view your results.

---

## 🛠 Local Development

```bash
# Clone the repo
git clone https://github.com/<your-username>/resume-matcher.git
cd resume-matcher

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENAI_API_KEY=sk-XXXX   # Windows PowerShell: $env:OPENAI_API_KEY="sk-XXXX"

# Run the app
python app.py
```

Open: [http://localhost:8000](http://localhost:8000)

---

## 🐳 Build & Run with Docker (Local)

```bash
docker build -t resume-matcher:local .
docker run --rm -e OPENAI_API_KEY=sk-XXXX -p 8000:8000 resume-matcher:local
```

---

## 📦 Publish to Docker Hub

```bash
# Login
docker login

# Tag the local image
docker tag resume-matcher:local mudabbir1187/resume-matcher:latest

# Push to Docker Hub
docker push mudabbir1187/resume-matcher:latest
```

Now anyone can run:
```bash
docker run --rm -e OPENAI_API_KEY=sk-XXXX -p 8000:8000 mudabbir1187/resume-matcher:latest
```

---

## ⚙ Environment Variables

| Variable         | Required | Description                |
|------------------|----------|----------------------------|
| `OPENAI_API_KEY` | ✅       | Your OpenAI API key         |
| `PORT`           | ❌       | Port to run the app (default 8000) |

---

## 📂 Project Structure

```
app.py
resume_scan_script.py
requirements.txt
templates/
  └── index.html
static/
  └── styles.css
Dockerfile
```

---

## 🔍 How It Works

1. **Frontend** (`index.html`) sends Job Description + Resume to `/match`
2. **Backend** (`app.py`) calls `analyze_fit()` in `resume_scan_script.py`
3. `analyze_fit()` sends the data to OpenAI with a strict JSON schema
4. Server **parses and cleans** the response so the client always receives valid JSON
5. Browser updates Score, Summary, Strengths, Gaps, Missing keywords, and Recommendations

---

## 🧾 License

MIT License © 2025
