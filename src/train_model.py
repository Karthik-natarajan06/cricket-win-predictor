import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/processed/deliveries.csv")

match_ids = df["match_id"].unique()

train_match_ids, test_match_ids = train_test_split(match_ids, random_state=42, train_size=0.8)
print(len(train_match_ids), len(test_match_ids))

train_df = df[df["match_id"].isin(train_match_ids)].copy()
test_df = df[df["match_id"].isin(test_match_ids)].copy()

train_df["match_type"] = train_df["match_type"].map({"ODI": 0, "T20": 1})
test_df["match_type"] = test_df["match_type"].map({"ODI": 0, "T20": 1})

feature_columns = ["match_type", "balls_remaining", "runs_needed", "wickets_in_hand", "current_run_rate", "required_run_rate"]

X_train = train_df[feature_columns]
y_train = train_df["label"]

X_test = test_df[feature_columns]
y_test = test_df["label"]

final_model = RandomForestClassifier(random_state=42, max_depth=10, min_samples_leaf=50)
final_model.fit(X_train, y_train)

final_pred = final_model.predict(X_test)
print(classification_report(y_test, final_pred))

joblib.dump(final_model, "app/model.pkl")