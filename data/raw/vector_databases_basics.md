# Vector Databases Basics

A vector database stores data as high-dimensional numeric vectors —
embeddings — and is optimized for finding vectors that are close to a
given query vector, rather than for exact keyword matching.

## Embeddings

An embedding model converts a piece of text into a fixed-length vector of
numbers, positioned so that texts with similar meaning end up close
together in the vector space. The same embedding model must be used
consistently for both indexing documents and embedding queries, since
different models produce vectors in incompatible spaces.

## Similarity search

Given a query vector, a vector database finds the stored vectors nearest
to it, typically using a distance metric such as cosine similarity or
Euclidean distance. The result is a ranked list of the most similar
stored items, usually returned along with a similarity score.

## Chunking before indexing

Full documents are usually too large and topically mixed to embed as a
single vector, so they are split into smaller chunks first. Chunk size
and overlap affect retrieval quality: chunks that are too large dilute
the embedding with unrelated content, while chunks that are too small
lose surrounding context. Overlapping consecutive chunks by a small
amount helps avoid cutting a relevant sentence in half at a chunk
boundary.

## Metadata filtering

Most vector databases allow each stored vector to carry metadata, such as
the source filename or page number. Metadata can be used to filter search
results — for example, restricting a search to documents from a specific
source — in addition to the similarity ranking.

## Persistence

Some vector databases run entirely in memory, while others, like
ChromaDB, support persisting the index to disk so it does not need to be
rebuilt every time the application restarts.

## Troubleshooting: irrelevant results

If similarity search consistently returns irrelevant chunks, common
causes include: using a different embedding model at query time than was
used at indexing time, chunks that are too large and topically diluted,
or a corpus that simply does not contain information related to the
query.
