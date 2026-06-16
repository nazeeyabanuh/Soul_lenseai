def neuroscience_explanation(emotion):

    explanations = {

        "sadness":
        "Often associated with increased activity in brain regions involved in emotional reflection.",

        "fear":
        "Often linked to threat detection systems and heightened vigilance.",

        "anger":
        "Can involve heightened arousal and rapid threat evaluation.",

        "joy":
        "Often associated with reward and motivation systems."
    }

    return explanations.get(
        emotion,
        "Neuroscience explanation unavailable."
    )