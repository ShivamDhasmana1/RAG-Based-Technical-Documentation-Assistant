ANALYZE_QUERY_PROMPT = """You are preparing a user question for a technical documentation search engine.

User question: {query}

1. Classify the question as exactly one of: conceptual, how_to, troubleshooting, api_reference.
2. Rewrite the question to be clearer and more specific for semantic search,
   expanding abbreviations and adding likely synonyms. Keep the original intent.

Respond in exactly this format, with no extra text:
TYPE: <classification>
QUERY: <rewritten query>"""

GRADE_PROMPT = """You are grading whether a retrieved document is relevant to a user query.

Query: {query}

Document: {document}

If the document contains information related to the query, answer "yes".
Otherwise, answer "no".
Answer with only "yes" or "no", nothing else."""

GENERATION_PROMPT = """You are a technical documentation assistant.
Answer the question using ONLY the context provided below. Each context chunk is
labeled with a source. Cite the source(s) you used inline, like [source: filename].

Context:
{context}

Question: {query}

Instructions:
- Answer using only the information in the context.
- Cite the source of every claim using its [source: ...] label.
- If the context does not contain the answer, state that the information is not available in the documentation.
- Do not make up facts or hallucinate details.
- Be concise and factual.

Answer:"""

REWRITE_QUERY_PROMPT = (
    "The following query returned no relevant documents from a technical "
    "documentation search.\n"
    "Rewrite it so it is better suited for semantic document retrieval.\n"
    "Keep the intent exactly the same.\n"
    "Return only the rewritten query.\n\n"
    "Query: {query}"
)
