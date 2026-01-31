"""
NLP utilities for categorization and rewriting of OCR-extracted articles.

- categorize_text: Assigns a news category to a given text using keyword/topic matching.
- rewrite_text: Rewrites or summarizes a given article for clarity and comprehension.

This module is designed to be lightweight and extensible. For production, consider integrating spaCy, transformers, or external LLM APIs.
"""

from typing import Optional
import re

CATEGORIES = {
    "technology": ["technology", "tech", "software", "hardware", "AI", "robotics", "computer", "internet", "startup", "gadget", "app", "IT", "cyber"],
    "world": ["world", "international", "global", "UN", "diplomacy", "country", "nation", "conflict", "war", "peace", "embassy", "foreign"],
    "business": ["business", "finance", "market", "stock", "trade", "economy", "company", "corporate", "IPO", "merger", "acquisition", "startup", "investment"],
    "science": ["science", "research", "study", "experiment", "discovery", "biology", "physics", "chemistry", "space", "astronomy", "lab", "scientist"],
    "general": ["news", "update", "report", "event", "breaking", "headline", "media", "public", "society", "community", "general"]
}


def categorize_text(text: str) -> str:
    """
    Assign a category to the given text using keyword/topic matching.
    Returns one of: technology, world, business, science, general
    """
    text_lower = text.lower()
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if re.search(rf"\\b{re.escape(kw)}\\b", text_lower):
                return category
    return "general"


def rewrite_text(text: str) -> str:
    """
    Rewrite or summarize the article for clarity.
    This is a placeholder using simple heuristics. For production, use an LLM or summarization model.
    """
    # Simple: return first 2 sentences as a 'summary'
    sentences = re.split(r"(?<=[.!?]) +", text.strip())
    summary = " ".join(sentences[:2])
    if len(summary) < 40 and len(sentences) > 2:
        summary += " " + sentences[2]
    return summary.strip()
