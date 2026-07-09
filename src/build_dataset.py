import pandas as pd
from pathlib import Path

RAW_DATA_DIRS = [
    Path("data/raw/odis"),
    Path("data/raw/t20s"),
]
OUTPUT_PATH = Path("data/processed/deliveries.csv")
BALLS_PER_OVER = 6


def parse_info_file(info_path):
    matches={}
    count=0
    with open(info_path) as f:
        team=[]
        overs=0
        winner=""
        target_runs=-1
        match_type=""
        for line in f:
            fields = line.strip().split(",")
            if (fields[1]== "team"):
                team.append(fields[2])
            elif (fields[1]== "overs"):
                overs = int(fields[2])
            elif (fields[1]== "winner"):
                winner = fields[2]
            elif (fields[1]== "target_runs"):
                target_runs = int(fields[3])
            elif (fields[1]== "match_type"):
                match_type = fields[2]
            
        if winner=="" or target_runs==-1:
            print(f"Skipping match {info_path.stem} due to missing winner or target_runs")
            return None
        
        matches={"team1": team[0], "team2": team[1], "match_type": match_type, "overs": overs, "winner": winner,  "target_runs": target_runs}
    return matches


def process_match(match_id, ball_by_ball_path, info):
    df = pd.read_csv(ball_by_ball_path)
    match=[]
    innings2 = df[df["innings"] == 2]
    ball=0
    balls_remaining=info["overs"] * BALLS_PER_OVER
    runs_needed=info["target_runs"]
    wickets_remaining=10
    runs_scored_so_far=0
    current_run_rate=0
    required_run_rate=0
    label=0

    label = 1 if innings2.iloc[0]["batting_team"] == info["winner"] else 0

    for index, row in innings2.iterrows():
        is_legal = pd.isna(row["wides"]) and pd.isna(row["noballs"])
        if(is_legal):
            ball += 1
            balls_remaining =  balls_remaining - 1
        if not pd.isna(row["wicket_type"]):
            wickets_remaining = wickets_remaining - 1
        runs_scored_so_far += row["runs_off_bat"] + row["extras"]
        runs_needed = runs_needed - (row["runs_off_bat"] + row["extras"])
        if ball>0:
            current_run_rate = current_run_rate = (runs_scored_so_far) / ball * BALLS_PER_OVER
        else:
            current_run_rate=0
        
        if balls_remaining>0:
            required_run_rate = (runs_needed) / balls_remaining * BALLS_PER_OVER
        else:
            required_run_rate=0

        temp={
            "match_id": match_id,
            "batting_team": row["batting_team"],
            "bowling_team": row["bowling_team"],
            "match_type": info["match_type"],
            "ball": row["ball"],
            "balls_remaining": balls_remaining,
            "runs_needed": runs_needed,
            "wickets_in_hand": wickets_remaining,
            "current_run_rate": current_run_rate,
            "required_run_rate": required_run_rate,
            "label": label
        }
        match.append(temp)

    return match


def build_dataset():
    """
    Loop through all match files in RAW_DATA_DIRS, call parse_info_file
    and process_match for each, collect all rows, and save to OUTPUT_PATH.
    """
    all_rows = []

    for raw_dir in RAW_DATA_DIRS:
        info_files = sorted(raw_dir.glob("*_info.csv"))
        for info_path in info_files:
            match_id = info_path.stem.replace("_info", "")
            ball_by_ball_path = raw_dir / f"{match_id}.csv"

            info = parse_info_file(info_path)
            if info is None:
                continue

            rows = process_match(match_id, ball_by_ball_path, info)
            all_rows.extend(rows)

    df = pd.DataFrame(all_rows)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(df)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    build_dataset()

