from textwrap import dedent


def get_system_prompt(path: str) -> str:
    """
    Retrieve the system prompt from the specified file path.
    """
    with open(path, "r", encoding="utf-8") as file:
        prompt = file.read().strip()

    return {
        "role": "system",
        "content": dedent(prompt).strip(),
    }
