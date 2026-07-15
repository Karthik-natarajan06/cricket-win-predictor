import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from build_dataset import parse_info_file, process_match

from pathlib import Path

def test_parse_info_file():
    info = parse_info_file(Path("tests/fixtures/test_match_info.csv"))
    assert info["team1"] == "TeamA"
    assert info["team2"] == "TeamB"
    assert info["overs"] == 20
    assert info["match_type"] == "T20"
    assert info["target_runs"] == 100
    assert info["winner"] == "TeamA"

def test_process_match():
    info = parse_info_file(Path("tests/fixtures/test_match_info.csv"))
    result = process_match("9999", Path("tests/fixtures/test_match.csv"), info)
    
    assert len(result) == 6
    
    last_ball = result[-1]
    assert last_ball["balls_remaining"] == 115
    assert last_ball["runs_needed"] == 92
    assert last_ball["wickets_in_hand"] == 9
    assert last_ball["label"] == 1