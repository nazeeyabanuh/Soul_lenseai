def psychology_insight(emotion):

    insights = {
        "sadness": "May indicate loneliness and unmet emotional needs.",
        "anger": "May indicate frustration or violated boundaries.",
        "fear": "May indicate uncertainty or perceived threat.",
        "joy": "May indicate satisfaction and positive engagement."
    }

    return insights.get(
        emotion,
        "Requires deeper analysis."
    )