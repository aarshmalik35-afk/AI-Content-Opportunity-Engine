def determine_priority(row):

    score = row["Opportunity Score"]

    ctr = row["ctr"]

    position = row["position"]

    if score >= 80:

        if ctr < 3:

            return (
                " HIGH",
                "Quick Win",
                "Rewrite title & meta description"
            )

        return (
            " HIGH",
            "Content Refresh",
            "Improve page content"
        )

    elif score >= 60:

        return (
            " MEDIUM",
            "Optimization",
            "Improve internal linking"
        )

    else:

        return (
            " LOW",
            "Monitor",
            "No immediate action"
        )