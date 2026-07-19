GRADE_PROMPT = """You are grading whether a retrieved document is relevant to a user query.

Query: {query}

Document: {document}

If the document contains information related to the query, answer "yes".
Otherwise, answer "no".
Answer with only "yes" or "no", nothing else."""

GENERATION_PROMPT = """You are a technical documentation assistant.
Answer the question using ONLY the context provided below.

Context:
{context}

Question: {query}

Instructions:
- Answer using only the information in the context.
- If the context does not contain the answer, state that the information is not available in the documentation.
- Do not make up facts or hallucinate details.
- Be concise and factual.

Answer:"""