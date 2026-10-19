from app.glossary import terms_for
from app.translate import build_prompt


def test_es_to_en_drywall():
    assert terms_for("es", "en")["tablaroca"] == "drywall"


def test_prompt_pins_terms():
    prompt = build_prompt("Falta tablaroca", "es", "en")
    assert "tablaroca => drywall" in prompt
