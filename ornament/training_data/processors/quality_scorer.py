"""Quality scorer."""
class QualityScorer:
    def score(self, content: str, lang: str) -> float:
        if not content: return 0.0
        return 0.8
