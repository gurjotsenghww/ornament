from typing import List, Dict, Optional

class QwenPromptFormatter:
    """
    Formats ChatML templates natively used by the Qwen family (Qwen2.5, Qwen3).
    """

    @staticmethod
    def format_chat(messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> str:
        prompt_parts = []
        if system_prompt:
            prompt_parts.append(f"<|im_start|>system\n{system_prompt}<|im_end|>")
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt_parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")
        prompt_parts.append("<|im_start|>assistant\n")
        return "\n".join(prompt_parts)

    @staticmethod
    def extract_assistant_response(raw_text: str) -> str:
        # Strip stop tokens if present
        clean = raw_text.replace("<|im_end|>", "").replace("<|endoftext|>", "").strip()
        return clean
