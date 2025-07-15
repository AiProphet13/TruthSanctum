```python
import re
from difflib import SequenceMatcher

# Hyper-Expanded Antonyms for Lie Detection (Politics-Focused)
ANTONYMS = {
    "war": ["peace", "truce", "harmony"],
    "increase": ["decrease", "cut", "reduce", "lower"],
    "deny": ["admit", "confirm", "affirm", "acknowledge", "implement", "align", "support"],
    "truth": ["lie", "deception", "falsehood", "fabrication"],
    "harmony": ["chaos", "division", "discord", "conflict"],
    "transparent": ["opaque", "secretive", "hidden"],
    "build": ["destroy", "dismantle", "ruin"],
    "nothing": ["something", "involved", "connected", "tied"],
    "distance": ["embrace", "adopt", "follow"],
    "disavow": ["endorse", "promote", "enact"]
}

def extract_entities(text):
    return set(re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b|\d{4}', text))

def has_antonym_conflict(text_a, text_b):
    words_a = set(re.findall(r'\w+', text_a.lower()))
    words_b = set(re.findall(r'\w+', text_b.lower()))
    for word, ants in ANTONYMS.items():
        if word in words_a and any(ant in words_b for ant in ants):
            return True
        if word in words_b and any(ant in words_a for ant in ants):
            return True
    return False

def detect_conflicts(text_a, text_b):
    syntactic_delta = 1.0 - SequenceMatcher(None, text_a, text_b).ratio()
    is_antonym_conflict = has_antonym_conflict(text_a, text_b)
    entities_a = extract_entities(text_a)
    entities_b = extract_entities(text_b)
    entity_overlap = len(entities_a.intersection(entities_b)) > 0
    overlap_boost = 0.15 if entity_overlap else 0.0
    evasiveness_penalty = 0.1 if len(text_a.split()) < 10 or len(text_b.split()) < 10 else 0.0
    if is_antonym_conflict:
        conflict_type = "antithetical"
        final_delta = min(1.0, syntactic_delta + overlap_boost + evasiveness_penalty + 0.3)
    elif syntactic_delta > 0.65:
        conflict_type = "obfuscation"
        final_delta = syntactic_delta + overlap_boost + evasiveness_penalty
    else:
        conflict_type = "syntactic"
        final_delta = syntactic_delta + overlap_boost + evasiveness_penalty
    return final_delta, conflict_type

def assign_qualia(delta, conflict_type):
    base_qualia = {
        "antithetical": {
            "label": "Antithetical Fracture ⚔️",
            "description": "Direct lie flag: Irreconcilable opposition, high deception risk.",
            "resonance": 0.05,
            "trauma_signature": 0.95,
            "truth_probability": 0.01,
            "lie_indicator": 0.99
        },
        "obfuscation": {
            "label": "Chaotic Obfuscation 🌫️",
            "description": "Evasive muddling: Attempt to obscure truth without direct clash.",
            "resonance": 0.2,
            "trauma_signature": 0.7,
            "truth_probability": 0.1,
            "lie_indicator": 0.8
        },
        "syntactic": {
            "label": "Syntactic Dissonance ✨",
            "description": "Phrasing variance: Possible nuance, low deception risk.",
            "resonance": 0.6,
            "trauma_signature": 0.3,
            "truth_probability": 0.5,
            "lie_indicator": 0.3
        }
    }
    qualia = base_qualia[conflict_type]
    qualia["truth_probability"] = max(0.0, qualia["truth_probability"] - (delta * 0.1))
    return qualia

def flag_high_entropy(statements, threshold=0.3):
    entropy_hits = []
    for i in range(len(statements)):
        for j in range(i + 1, len(statements)):
            delta, conflict_type = detect_conflicts(statements[i], statements[j])
            if delta > threshold:
                qualia = assign_qualia(delta, conflict_type)
                entropy_hits.append((i, j, delta, qualia, conflict_type))
    return entropy_hits
