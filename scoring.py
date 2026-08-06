def normalize_impressions(impressions, max_impressions):
    """
    Convert impressions into a score between 0 and 100.
    """
    return (impressions / max_impressions) * 100


def ctr_opportunity_score(ctr):
    """
    Lower CTR = Bigger opportunity.
    """
    return max(0, (10 - ctr) * 10)


def ranking_score(position):
    """
    Position 3–15 is considered 'striking distance'.
    """
    if position < 3:
        return 20      # already ranking well
    elif position <= 15:
        return 100 - ((position - 3) * 6)
    else:
        return 20


def calculate_opportunity_score(row, max_impressions):

    IMPRESSION_WEIGHT = 0.4
    CTR_WEIGHT = 0.3
    POSITION_WEIGHT = 0.3

    impression = normalize_impressions(
        row["impressions"],
        max_impressions
    )

    ctr = ctr_opportunity_score(row["ctr"])

    position = ranking_score(row["position"])

    score = (
        impression * IMPRESSION_WEIGHT
        + ctr * CTR_WEIGHT
        + position * POSITION_WEIGHT
    )

    reasons = []

    if impression > 70:
        reasons.append("High search visibility")

    if ctr > 60:
        reasons.append("CTR optimization opportunity")

    if position > 60:
        reasons.append("Ranking in striking distance")

    return round(score, 2), reasons