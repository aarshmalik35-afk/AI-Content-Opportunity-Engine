from scoring import calculate_opportunity_score
from intent import classify_intent
from priority import determine_priority
from ai.gemini_provider import generate_ai_recommendation


def analyze_dataframe(df):

    print("=" * 60)
    print("Starting FlyRank Analysis")
    print("=" * 60)

    max_impressions = df["impressions"].max()

    scores = []
    reasons = []
    intents = []
    priorities = []
    categories = []
    best_actions = []
    ai_recommendations = []

    total_rows = len(df)

    for index, (_, row) in enumerate(df.iterrows(), start=1):

        print(f"\nProcessing {index}/{total_rows}")
        print(f"Query: {row['query']}")

        score, reason = calculate_opportunity_score(
            row,
            max_impressions
        )

        intent = classify_intent(row["query"])

        temp_row = row.copy()
        temp_row["Opportunity Score"] = score
        temp_row["Intent"] = intent

        priority, category, action = determine_priority(temp_row)

        print("Calling Gemini...")

        try:
            ai = generate_ai_recommendation(temp_row)
            print("Gemini response received.")

        except Exception as e:
            print(f"Gemini Error: {e}")
            ai = f"Gemini Error: {e}"

        scores.append(score)
        reasons.append(reason)
        intents.append(intent)
        priorities.append(priority)
        categories.append(category)
        best_actions.append(action)
        ai_recommendations.append(ai)

    df["Opportunity Score"] = scores
    df["Reasons"] = reasons
    df["Intent"] = intents
    df["Priority"] = priorities
    df["Category"] = categories
    df["Best Action"] = best_actions
    df["AI Recommendation"] = ai_recommendations

    df = df.sort_values(
        by="Opportunity Score",
        ascending=False
    ).reset_index(drop=True)

    df["Priority Rank"] = range(1, len(df) + 1)

    print("\nAnalysis Finished!")

    return df