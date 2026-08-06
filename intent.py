def classify_intent(query):

    query = query.lower()

    if " vs " in query:
        return "Comparison"

    elif "alternative" in query:
        return "Replacement"

    elif "side effects" in query or "safe" in query:
        return "Risk / Safety"

    elif "for" in query:
        return "Use Case"

    else:
        return "Discovery"