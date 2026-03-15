# Background & Motivation

## The Challenge
JSON Schema is the industry-standard language for describing and validating JSON data structures. It is widely adopted across the information technology ecosystem, powering everything from web APIs (OpenAPI) to data integration tools and AI agents.

However, standard JSON Schema was primarily designed for structural validation (e.g., "is this a string?", "is this integer between 1 and 100?"). It lacks the semantic richness necessary for the effective discovery, exchange, and stewardship of high-quality data. In the world of **FAIR Data** (Findable, Accessible, Interoperable, and Reusable), we need to capture much more:
- Semantic concepts (what does this variable *mean*?)
- Controlled vocabularies and classifications.
- Units of measure and quantity kinds.
- Temporal and spatial coverage.
- Data provenance, lineage, and licensing.

## Bridging the Gap
Existing metadata standards like **DDI**, **DCAT**, and **Croissant** provide these features but often face adoption barriers among web developers and IT professionals more accustomed to the JSON Schema ecosystem. While traditional metadata standards remain vital, they often rely on niche technologies like RDF and triple stores.

The **FAIR Data JSON Schema** project aims to bridge this gap. Instead of creating a new language, we extend JSON Schema using its native extension mechanisms (Dialects and Vocabularies). This creates a "lingua franca" for high-value data that integrates seamlessly with modern APIs and AI toolchains.

## Why JSON Schema?
JSON and JSON Schema serve as a universal language across the modern technology stack. This approach brings:
1. **IT Power to Data Stewards**: Leverage the massive ecosystem of JSON Schema validators, UI generators, and documentation tools.
2. **AI-Readiness**: JSON Schema is a first-class citizen in the AI world—inherently understood by Large Language Models (LLMs) and widely adopted for tool-calling and the Model Context Protocol (MCP).
3. **Developer Accessibility**: Introduce data documentation best practices to information technologists in the formats and tools they already use every day.

## What is a JSON Meta-Schema?
A JSON Schema defines the structure and validation rules for a JSON document (an "instance"). A **JSON Meta-Schema** is a schema that defines the structure and validation rules for *other schemas*. Essentially, it is a **"schema for schemas."**

In this project, the meta-schema defines the **FAIR Dialect** of JSON Schema. It:
- **Declares Standards**: Specifies which version of the JSON Schema standard is being used (Draft 2020-12).
- **Defines Keywords**: Introduces custom FAIR keywords (e.g., `fair:concept`, `fair:unit`) and specifies where they can be used and what values they should hold.
- **Enables Interoperability**: Bundles various specialized vocabularies into a single cohesive dialect, allowing FAIR-aware tools and AI agents to recognize and act upon the metadata.

## Vision
This project provides a "FAIR Dialect" for JSON Schema. A data steward can write a schema that is 100% valid JSON Schema while also containing rich, machine-actionable FAIR metadata.

> [!NOTE]
> This project is in an **early development and prototyping stage**. The vocabularies described here are subject to change as we refine the core features.
