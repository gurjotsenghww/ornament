import re

class TokenEstimator:
    """
    Fast, model-aware token estimator for Qwen family models.
    Approximates BPE token count without requiring heavy external binaries.
    """

    @staticmethod
    def estimate_tokens(text: str) -> int:
        if not text:
            return 0
        # For code and structured text, token density is typically ~3.2 characters per token in BPE.
        # Splits on whitespace and code punctuation.
        tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
        # BPE heuristic: word tokens count + subword factor for long tokens
        count = 0
        for t in tokens:
            count += 1 + (len(t) // 6)
        return max(1, count)
