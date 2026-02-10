from decision_tool.io import load_input

def test_load_input_returns_path():
    assert load_input("file.csv") == "file.csv"
