from __future__ import annotations

import re
from typing import Any

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "can", "do", "does",
    "for", "from", "get", "how", "i", "if", "in", "is", "it", "me", "my", "need",
    "of", "on", "or", "our", "should", "so", "the", "their", "to", "use", "what",
    "when", "where", "who", "why", "with", "you", "your",
}


def tokenize(text: str) -> set[str]:
    """Convert text into a set of searchable lowercase tokens.

    TODO:
    - Lowercase the text.
    - Extract word-like values.
    - Remove leading/trailing apostrophes.
    - Remove tokens with length <= 1.
    - Remove tokens in STOPWORDS.
    - Return a set of searchable terms.
    """
    # TODO: Replace this placeholder with your implementation.
    raw_tokens = re.findall(r"[a-zA-Z0-9']+", text.lower())

    return {
        token.strip("'")
        for token in raw_tokens
        if len(token.strip("'")) > 1 and token.strip("'") not in STOPWORDS
    }

def document_search_text(document: dict[str, Any]) -> str:
    """Combine searchable document fields into one text value.

    TODO:
    Include title, category, tags, and text.
    """
    # TODO: Replace this placeholder with your implementation.
    tags = " ".join(document.get("tags", []))

    return (
        f"{document.get('title', '')} "
        f"{document.get('category', '')} "
        f"{tags} "
        f"{document.get('text', '')}"
    )


def score_document(query: str, document: dict[str, Any]) -> dict[str, Any]:
    """Score a document using keyword overlap.

    TODO:
    - Tokenize the query.
    - Tokenize the combined searchable document text.
    - Tokenize the document title.
    - Find matched terms between query tokens and document tokens.
    - Add a small title boost: 0.5 for each query token found in the title.
    - Return a dictionary with keys: document, score, matched_terms.
    """
    # TODO: Replace this placeholder with your implementation.
    query_tokens = tokenize(query)
    document_tokens = tokenize(document_search_text(document))
    title_tokens = tokenize(document.get("title", ""))

    matched_terms = query_tokens.intersection(document_tokens)
    title_matches = query_tokens.intersection(title_tokens)

    score = len(matched_terms) + (0.5 * len(title_matches))

    return {
        "document": document,
        "score": score,
        "matched_terms": sorted(matched_terms),
    }


def retrieve_context(
    query: str,
    documents: list[dict[str, Any]],
    limit: int = 2,
    minimum_score: float = 1.0,
) -> list[dict[str, Any]]:
    """Select the most relevant documents for the query.

    TODO:
    - Score all documents.
    - Keep only matches with score >= minimum_score.
    - Sort by score from highest to lowest.
    - Return only the top `limit` matches.

    The selected context must depend on the user's query. Do not return the same
    hardcoded document for every request.
    """
    # TODO: Replace this placeholder with your implementation.
    scored_matches = [score_document(query, document) for document in documents]

    relevant_matches = [
        match for match in scored_matches if match["score"] >= minimum_score
    ]

    return sorted(
        relevant_matches,
        key=lambda match: match["score"],
        reverse=True,
    )[:limit]


def format_context(context_matches: list[dict[str, Any]]) -> str:
    """Format retrieved documents into a context block for the prompt.

    TODO:
    - If no matches exist, return a short no-context message.
    - For each match, include Source ID, Title, Category, and Content.
    - Separate document blocks clearly.
    """
    # TODO: Replace this placeholder with your implementation.
    if not context_matches:
        return "No relevant context was found in the approved support documents."

    context_blocks = []

    for match in context_matches:
        document = match["document"]

        context_blocks.append(
            "\n".join(
                [
                    f"Source ID: {document['id']}",
                    f"Title: {document['title']}",
                    f"Category: {document['category']}",
                    f"Content: {document['text']}",
                ]
            )
        )

    return "\n\n---\n\n".join(context_blocks)


def build_prompt(query: str, context_matches: list[dict[str, Any]]) -> str:
    """Build a structured prompt with instructions, context, question, and requirements.

    TODO:
    The prompt should include these sections:
    - Instructions
    - Context
    - Question
    - Response requirements

    The prompt should tell the model to use only the provided context and avoid
    inventing unsupported details.
    """
    # TODO: Replace this placeholder with your implementation.
    context_block = format_context(context_matches)

    return f"""You are an internal IT support assistant.

    Instructions:
    Use only the provided context to answer the user's question.
    If the context does not contain enough information, say that the approved support documents do not contain enough information.
    Do not invent policies, URLs, phone numbers, timelines, or escalation paths.

    Context:
    {context_block}

    Question:
    {query.strip()}

    Response requirements:
    - Answer in 2-4 concise sentences.
    - Use a helpful internal-support tone.
    - Mention the source ID or source IDs used.
    """



def source_metadata(match: dict[str, Any]) -> dict[str, str]:
    """Return source information that is safe to expose in the API response.

    TODO:
    Return only the document id and title.
    """
    # TODO: Replace this placeholder with your implementation.
    document = match["document"]

    return {
        "id": document["id"],
        "title": document["title"],
    }

