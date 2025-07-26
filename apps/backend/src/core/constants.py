import os
from pathlib import Path


src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
fixtures_path = os.path.join(src_path, "tests", "fixtures")
prompts_path = os.path.join(src_path, "utils", "prompts")

prompts_verbs_path = os.path.join(prompts_path, "verbs")

CONSTANTS = {
    "ENV_FILE": Path(__file__).parent.parent.parent / ".env.local",
    "AI_DEFAULT_MODEL": "gpt-4o-mini",
    "FIXTURES_PATH": fixtures_path,
    "PROMPTS_VERBS_PATH": prompts_verbs_path,
}