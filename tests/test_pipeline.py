from src.main import run_qualia_entropy_pipeline

def test_basic():
    statements = ["I know nothing about Project 2025.", "Trump's actions align with Project 2025 goals."]
    human_input = "Test input for validation."
    report = run_qualia_entropy_pipeline(statements, human_input)
    assert report is not None
    assert len(report["conflicts"]) > 0
    print("Test passed!")

if __name__ == "__main__":
    test_basic()
