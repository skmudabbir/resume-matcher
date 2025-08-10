# resume_scan_script.py
import logging
from typing import Optional, List
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import OpenAI, RateLimitError, APIError, BadRequestError

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def call_openai(messages, model="gpt-4o-mini", api_key=None):
    try:
        logger.info(f"Attempting OpenAI call with model: {model}")
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2  # ✨ Removed invalid 'response_format'
        )
        return resp.choices[0].message.content
    except RateLimitError as e:
        if model != "gpt-3.5-turbo":
            logger.warning("Quota exceeded on GPT-4o-mini. Falling back to GPT-3.5-turbo.")
            return call_openai(messages, model="gpt-3.5-turbo", api_key=api_key)
        raise RuntimeError("OpenAI quota exceeded. Please check your usage and billing.") from e
    except BadRequestError as e:
        logger.error(f"BadRequest from OpenAI: {e}")
        raise RuntimeError(f"OpenAI request failed: {e}") from e
    except APIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise RuntimeError(f"OpenAI API error: {e}") from e
    except Exception as e:
        logger.exception("Unhandled exception during OpenAI call")
        raise RuntimeError(f"Unexpected error: {e}") from e

def analyze_fit(job_description: str, resume: str, criteria: Optional[List[str]] = None, model: str = "gpt-4o-mini"):
    if not job_description or not resume:
        raise ValueError("Both job_description and resume must be provided")

    criteria_text = ", ".join(criteria) if criteria else "Auto-extract from job description"

    system_prompt = (
        "You are a precise recruiting assistant.\n"
        "Return STRICT JSON only, matching this schema:\n"
        "{\n"
        '  "score": 0-100,\n'
        '  "summary": "string",\n'
        '  "strengths": ["string", ...],\n'
        '  "gaps": ["string", ...],\n'
        '  "missing_keywords": ["string", ...],\n'
        '  "recommendations": ["string", ...]\n'
        "}\n"
        "Guidelines:\n"
        "- Score reflects the resume's fit to the job description and criteria.\n"
        "- Be concise and specific. No prose outside JSON. No markdown.\n"
    )

    user_content = f"[Job Description]\n{job_description}\n\n[Resume]\n{resume}\n\n[Criteria]\n{criteria_text}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]

    return call_openai(messages, model=model)