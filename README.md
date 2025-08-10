# Resume ↔ Job Match

A tiny Flask app + OpenAI that scores how well a resume matches a job description and highlights strengths, gaps, missing keywords, and recommendations.

## Quick Start (Non‑technical)

1. **Install Docker** (Windows/Mac: Docker Desktop).
2. **Get an OpenAI API key** and keep it handy.
3. Open a terminal and run:
   ```bash
   docker run -e OPENAI_API_KEY=sk-XXXX -p 8000:8000 syedmudabbir/resume-matcher:latest
   ```
4. Visit **http://localhost:8000** in your browser.
5. Paste your **Job Description** and **Resume**, then click **Analyze match**.

> No personal data is stored by the app; your text is only sent to OpenAI to compute the result.

---

## Local Development

```bash
git clone https://github.com/<your-username>/resume-matcher.git
cd resume-matcher
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-XXXX  # Windows PowerShell: $env:OPENAI_API_KEY="sk-XXXX"
python app.py
# open http://localhost:8000
```

## Docker (build & run)

```bash
docker build -t resume-matcher:local .
docker run --rm -e OPENAI_API_KEY=sk-XXXX -p 8000:8000 resume-matcher:local
# open http://localhost:8000
```

## Publish to Docker Hub

```bash
docker login
docker tag resume-matcher:local <your-dockerhub-username>/resume-matcher:latest
docker push <your-dockerhub-username>/resume-matcher:latest
```

Other users can then run:
```bash
docker run -e OPENAI_API_KEY=sk-XXXX -p 8000:8000 <your-dockerhub-username>/resume-matcher:latest
```

## GitHub Setup

1. Create a new repo on GitHub (e.g., `resume-matcher`).
2. Push this project to your repo:
   ```bash
   git init
   git remote add origin https://github.com/<your-username>/resume-matcher.git
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git push -u origin main
   ```
3. **Optional:** Enable CI to build & publish the Docker image on every push.
   - Add repository secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.
   - Commit the workflow in `.github/workflows/docker-publish.yml` (included).

## Environment Variables

- `OPENAI_API_KEY` – your OpenAI API key (required).
- `PORT` (default: 8000).

## Project Structure

```
app.py
resume_scan_script.py
templates/
  └─ index.html
static/
  └─ styles.css
Dockerfile
requirements.txt
```

## How it works

- Frontend posts JD + resume to `/match`.
- Backend calls OpenAI with a strict JSON schema.
- The API response is parsed and **the server always returns valid JSON** to the browser.
- The page updates the **Score**, **Summary**, **Strengths**, **Gaps**, **Missing keywords**, and **Recommendations**.

## Troubleshooting

- If you see “Unable to parse model response,” your API key might be invalid or rate-limited. Check your key and try again.
- Ensure port `8000` is free on your machine or set `PORT`.