import os


api_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
fixtures_path = os.path.join(api_path, "tests", "fixtures")
prompts_path = os.path.join(api_path, "utils", "prompts")

prompts_verbs_path = os.path.join(prompts_path, "verbs")

CONSTANTS = {
    "ENV_FILE": ".env.local",
    "AI_DEFAULT_MODEL": "gpt-4o-mini",
    "FIXTURES_PATH": fixtures_path,
    "PROMPTS_VERBS_PATH": prompts_verbs_path,
}