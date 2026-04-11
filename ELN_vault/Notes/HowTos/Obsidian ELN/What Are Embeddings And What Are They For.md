---
ELN version: 0.5.0
cssclasses:
  - normal-page
date created: 2026-04-11
author: StarDustX
note type: how-to
tags:
  - "#note/how-to"
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

# What Are Embeddings And What Are They For?

Embeddings are numeric vector representations of text. In the `Lab Log Writer` resource workflow, they are created from PDF text chunks so the vault can retain a machine-readable representation of semantic meaning, not just the raw extracted text.

## What They Mean Here

When you ingest a PDF from [[Resources/APT-FIM/Library|APT/FIM Resources]], the writer can:

1. Extract the PDF text into chunked JSON records in `Resources/APT-FIM/.index`.
2. Optionally call an embedding model for each chunk.
3. Save the embedding vectors alongside the extracted chunk data.

That means the vault keeps a richer index of each paper than plain text alone.

## What Embeddings Are Used For Right Now

At the moment, embeddings mainly serve as future-ready indexing data:

- They let the intake pipeline mark which papers were processed with embeddings and which were not.
- They preserve semantic vectors beside the extracted chunks so you do not need to regenerate them later if you decide to build search or retrieval features.
- They give you a cleaner handoff point for later tooling that may want to compare papers, paragraphs, or topics by meaning instead of exact keywords.

In the current writer, embeddings are optional and are controlled by the `Generate embeddings during ingest` checkbox in the [[Lab Log Writer]] resource workflow.

## What They Are Not Doing Yet

Embeddings are not currently used by the existing:

- PDF summary generation
- Topic synthesis
- Basic PDF scanning
- Note creation forms

Those current features still rely on the extracted chunk text and the selected LLM model, not on vector search.

## What They Could Enable Later

Keeping embeddings now makes it much easier to add higher-value retrieval features later, such as:

- Semantic search across the `Resources/APT-FIM` literature collection
- "Find papers similar to this one" workflows
- Retrieval-augmented generation (RAG) for question answering over the indexed PDFs
- Better clustering of related topics, methods, or specimen systems
- Re-ranking literature chunks before sending them to a summary or synthesis model

## Practical Takeaway

If you do not need semantic retrieval yet, embeddings are safe to leave off. If you expect to grow the literature library and later want meaning-based search or context retrieval, generating them during ingest saves rework.

## Related Guides

- [[Help & Guides Index]]
- [[Lab Log Writer]]
- [[Resources/APT-FIM/Library|APT/FIM Resources]]
- [[Obsidian ELN - Getting started]]

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
