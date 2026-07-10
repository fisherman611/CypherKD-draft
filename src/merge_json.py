import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
# with open(r"results/Cypherbench/ablation_spans/calculated_scores_wo_expression/company_cyphers_result.json", "r", encoding="utf-8") as f:
#     company = json.load(f)

# with open(r"results/Cypherbench/ablation_spans/calculated_scores_wo_expression/fictional_character_cyphers_result.json", "r", encoding="utf-8") as f:
#     fictional_character = json.load(f)
    
# with open(r"results/Cypherbench/ablation_spans/calculated_scores_wo_expression/flight_accident_cyphers_result.json", "r", encoding="utf-8") as f:
#     flight_accident = json.load(f)
    
# with open(r"results/Cypherbench/ablation_spans/calculated_scores_wo_expression/geography_cyphers_result.json", "r", encoding="utf-8") as f:
#     geography = json.load(f)
    
# with open(r"results/Cypherbench/ablation_spans/calculated_scores_wo_expression/movie_cyphers_result.json", "r", encoding="utf-8") as f:
#     movie = json.load(f)
    
# with open(r"results/Cypherbench/ablation_spans/calculated_scores_wo_expression/nba_cyphers_result.json", "r", encoding="utf-8") as f:
#     nba = json.load(f)
    
# with open(r"results/Cypherbench/ablation_spans/calculated_scores_wo_expression/politics_cyphers_result.json", "r", encoding="utf-8") as f:
#     politics = json.load(f)

# test = company + fictional_character + flight_accident + geography + movie + nba + politics

# with open(r"results/Cypherbench/ablation_spans/calculated_scores_wo_expression/test_result.json", "w", encoding="utf-8") as f:
#     json.dump(test, f, ensure_ascii=False, indent=2)

with open(r"results/Mind_the_query/ablation_spans/calculated_scores_wo_expression/bloom50_cyphers_result.json", "r", encoding="utf-8") as f:
    bloom50 = json.load(f)

with open(r"results/Mind_the_query/ablation_spans/calculated_scores_wo_expression/healthcare_cyphers_result.json", "r", encoding="utf-8") as f:
    healthcare = json.load(f)

with open(r"results/Mind_the_query/ablation_spans/calculated_scores_wo_expression/wwc_cyphers_result.json", "r", encoding="utf-8") as f:
    wwc = json.load(f)

test = bloom50 + healthcare + wwc
with open(r"results/Mind_the_query/ablation_spans/calculated_scores_wo_expression/test_result.json", "w", encoding="utf-8") as f:
    json.dump(test, f, ensure_ascii=False, indent=2)