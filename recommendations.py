def recommend_action(row):

    recommendations = []

    if row["ctr"] < 3:
        recommendations.append("Rewrite title and meta description")

    if row["position"] > 5:
        recommendations.append("Improve page content")

    if row["impressions"] > 10000:
        recommendations.append("High business priority")

    if len(recommendations) == 0:
        recommendations.append("Monitor performance")

    return recommendations