from functools import lru_cache
from pathlib import Path
import yaml

GLOSSARY_PATH = Path(__file__).with_name("glossary.yaml")


@lru_cache
def load_glossary() -> dict[str, dict[str, str]]:
    return yaml.safe_load(GLOSSARY_PATH.read_text(encoding="utf-8"))


def terms_for(source: str, target: str) -> dict[str, str]:
    # Returns {source_term: target_term} for every concept defined in both languages.
    out = {}
    for concept in load_glossary().values():
        if source in concept and target in concept:
            out[concept[source]] = concept[target]
    return out
