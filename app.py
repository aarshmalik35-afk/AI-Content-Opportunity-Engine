from preprocessing import load_data
from scoring import calculate_opportunity_score
from recommendations import recommend_action
from intent import classify_intent
from priority import determine_priority
from menu import show_menu
from ai.gemini_provider import generate_ai_recommendation

REPORT = None


def analyze_dataset():
    global REPORT

    print("\nLoading SEO dataset...\n")

    df = load_data("seo_data.csv")

    max_impressions = df["impressions"].max()

    scores = []
    reasons = []
    intents = []
    priorities = []
    categories = []
    best_actions = []
    ai_recommendations = []

    print("Analyzing pages...\n")

    for index, (_, row) in enumerate(df.iterrows(), start=1):

        print(f"Analyzing {index}/{len(df)}...")

        score, reason = calculate_opportunity_score(
            row,
            max_impressions
        )

        intent = classify_intent(row["query"])

        temp_row = row.copy()
        temp_row["Opportunity Score"] = score
        temp_row["Intent"] = intent

        priority, category, action = determine_priority(temp_row)

        try:
            ai_response = generate_ai_recommendation(temp_row)

        except Exception as e:
            ai_response = f"Gemini Error: {e}"

        scores.append(score)
        reasons.append(reason)
        intents.append(intent)

        priorities.append(priority)
        categories.append(category)
        best_actions.append(action)

        ai_recommendations.append(ai_response)

    df["Opportunity Score"] = scores
    df["Reasons"] = reasons
    df["Intent"] = intents
    df["Priority"] = priorities
    df["Category"] = categories
    df["Best Action"] = best_actions
    df["AI Recommendation"] = ai_recommendations

    REPORT = df.sort_values(
        by="Opportunity Score",
        ascending=False
    ).reset_index(drop=True)

    REPORT["Priority Rank"] = range(1, len(REPORT) + 1)

    print("\nAnalysis Complete!\n")


def view_report():

    global REPORT

    if REPORT is None:

        print("\nRun analysis first.\n")

        return

    print("\n" + "=" * 80)
    print("TOP SEO OPPORTUNITIES")
    print("=" * 80)

    for _, row in REPORT.iterrows():

        print("\n" + "=" * 80)

        print(f"Priority Rank      : #{row['Priority Rank']}")
        print(f"Page               : {row['page']}")
        print(f"Target Query       : {row['query']}")
        print(f"Intent             : {row['Intent']}")
        print(f"Opportunity Score  : {row['Opportunity Score']:.2f}/100")
        print(f"Priority           : {row['Priority']}")
        print(f"Category           : {row['Category']}")
        print(f"Best Action        : {row['Best Action']}")

        print("\nWhy this page was selected")

        for reason in row["Reasons"]:
            print(f"✓ {reason}")

        print("\nRule-Based Recommendations")

        actions = recommend_action(row)

        for action in actions:
            print(f"• {action}")

        print("\nAI Recommendation")
        print("-" * 60)

        print(row["AI Recommendation"])

        print()


def search_query():

    global REPORT

    if REPORT is None:

        print("\nRun analysis first.\n")

        return

    keyword = input("\nEnter keyword: ").lower()

    results = REPORT[
        REPORT["query"].str.lower().str.contains(
            keyword,
            na=False
        )
    ]

    if results.empty:

        print("\nNo matching results found.\n")

        return

    for _, row in results.iterrows():

        print("\n" + "-" * 80)

        print(f"Priority Rank : #{row['Priority Rank']}")
        print(f"Page          : {row['page']}")
        print(f"Query         : {row['query']}")
        print(f"Intent        : {row['Intent']}")
        print(f"Score         : {row['Opportunity Score']:.2f}")
        print(f"Priority      : {row['Priority']}")
        print(f"Category      : {row['Category']}")
        print(f"Best Action   : {row['Best Action']}")

        print("\nAI Recommendation")

        print(row["AI Recommendation"])

        print()


def export_report():

    global REPORT

    if REPORT is None:

        print("\nRun analysis first.\n")

        return

    REPORT.to_csv(
        "opportunity_report.csv",
        index=False
    )

    print("\nReport exported successfully!")
    print("Saved as opportunity_report.csv\n")


while True:

    choice = show_menu()

    if choice == "1":

        analyze_dataset()

    elif choice == "2":

        view_report()

    elif choice == "3":

        search_query()

    elif choice == "4":

        export_report()

    elif choice == "5":

        print("\nThank you for using FlyRank AI Content Opportunity Engine!")

        break

    else:

        print("\nInvalid option.\n")