# app.py (updated to always return parsed JSON)
import os
import json
import logging
from flask import Flask, render_template, request, jsonify
from resume_scan_script import analyze_fit

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/healthz", methods=["GET"])
def healthz():
    return {"ok": True}

@app.route("/match", methods=["POST"])
def match():
    payload = request.get_json(force=True) or {}
    jd = (payload.get("job_description") or "").strip()
    resume = (payload.get("resume") or "").strip()
    criteria_text = (payload.get("criteria") or "").strip()
    criteria = [c.strip() for c in criteria_text.split(",")] if criteria_text else None

    try:
        raw = analyze_fit(jd, resume, criteria=criteria)  # may return a JSON string
        logger.info("Raw analyze_fit type=%s", type(raw))

        # Always return parsed JSON
        if isinstance(raw, dict):
            parsed = raw
        else:
            # Attempt to extract JSON from a string (tolerates code fences/extra text)
            s = str(raw).strip()
            s = s.replace("```json", "").replace("```", "").strip()
            start, end = s.find("{"), s.rfind("}")
            if start != -1 and end != -1 and end > start:
                s = s[start:end+1]
            try:
                parsed = json.loads(s)
            except Exception:
                # Best-effort safe fallback
                parsed = {"summary": "Unable to parse model response.", "raw": s, "score": 0,
                          "strengths": [], "gaps": [], "missing_keywords": [], "recommendations": []}

        # Ensure required keys exist
        parsed.setdefault("score", 0)
        parsed.setdefault("summary", "")
        parsed.setdefault("strengths", [])
        parsed.setdefault("gaps", [])
        parsed.setdefault("missing_keywords", [])
        parsed.setdefault("recommendations", [])

        return jsonify(parsed)
    except Exception as e:
        logger.exception("Error in /match")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)