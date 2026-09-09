"""Reply generation using templates with optional LLM enhancement."""

import os
from typing import Optional


class ReplyGenerator:
    """Generate replies using templates or LLM (when API key available)."""

    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm and self._has_llm_key()
        self.client = None

        if self.use_llm:
            try:
                import openai
                api_key = os.getenv("OPENAI_API_KEY") or os.getenv("HIVER_LLM_API_KEY")
                self.client = openai.OpenAI(api_key=api_key)
            except Exception:
                self.use_llm = False

    def generate(
        self,
        query: str,
        intent: str,
        retrieved_docs: list[dict],
        context: Optional[dict] = None,
    ) -> str:
        """Generate a reply based on query, intent, and retrieved knowledge."""
        if self.use_llm and self.client:
            return self._generate_llm(query, intent, retrieved_docs, context)

        return self._generate_template(query, intent, retrieved_docs)

    def _generate_template(
        self, query: str, intent: str, retrieved_docs: list[dict]
    ) -> str:
        """Template-based reply generation (works without API key)."""
        if not retrieved_docs:
            return "Thank you for contacting Uber support. I'll look into your issue and get back to you shortly."

        template = retrieved_docs[0].get("template", retrieved_docs[0]["text"])
        return template

    def _generate_llm(
        self,
        query: str,
        intent: str,
        retrieved_docs: list[dict],
        context: Optional[dict],
    ) -> str:
        """LLM-enhanced reply generation (requires API key)."""
        try:
            kb_context = "\n".join([doc["text"] for doc in retrieved_docs[:2]])

            system_prompt = f"""You are an Uber customer support agent. Generate a helpful, empathetic, and professional response.

Intent: {intent}
Knowledge Base:
{kb_context}

Guidelines:
- Be concise (2-3 sentences)
- Show empathy
- Provide actionable next steps
- Do not invent information not in the knowledge base"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ],
                max_tokens=150,
                temperature=0.7,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return self._generate_template(query, intent, retrieved_docs)

    @staticmethod
    def _has_llm_key() -> bool:
        """Check if LLM API key is available."""
        return bool(os.getenv("OPENAI_API_KEY") or os.getenv("HIVER_LLM_API_KEY"))
