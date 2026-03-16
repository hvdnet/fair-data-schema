# Coded Values: From Enums to FAIR Domains

This explains by example how to handle categorical data (code lists, classifications, or response domains) using JSON Schema, evolving from simple technical validation to rich FAIR metadata.

See the companion schema file: [`examples/enum-to-fair-coded-values.json`](examples/enum-to-fair-coded-values.json)

---

## 1. The Standard `enum` (Validation only)

The most basic way to restrict a value in JSON Schema is the [`enum`](https://json-schema.org/draft/2020-12/json-schema-validation#name-enum) keyword.

```json
{
  "type": "string",
  "enum": ["red", "green", "blue"]
}
```

**Pros**: extremely simple; natively supported by all tools.
**Cons**: No way to associate a human-readable label or description with each code. The codes must be self-explanatory.

---

## 2. The Labeled Enum Pattern (Standard JSON Schema)

To associate a label like "Yes" with a code like `1`, we use the [**`oneOf`**](https://json-schema.org/draft/2020-12/json-schema-core#name-oneof) + [**`const`**](https://json-schema.org/draft/2020-12/json-schema-validation#name-const) pattern. This is **100% standard JSON Schema**, requires no extensions, and is natively supported by all standard-compliant JSON Schema validators.

```json
{
  "type": "integer",
  "oneOf": [
    { "const": 1, "title": "Yes" },
    { "const": 2, "title": "No" }
  ]
}
```

By using the standard [`title`](https://json-schema.org/draft/2020-12/json-schema-validation#name-title) keyword inside each `oneOf` branch, you create an unambiguous mapping between the stored value and its human-readable representation.

---

## 3. The Shared Response Domain (DRY Principle)

In data stewardship, many variables often share the same "Response Domain" (e.g., several "Yes/No" questions in a survey). Instead of repeating the `oneOf` logic, you define it once in `$defs` and reference it using `$ref`.

```json
{
  "$defs": {
    "YesNo": {
      "type": "integer",
      "oneOf": [
        { "const": 1, "title": "Yes" },
        { "const": 2, "title": "No" }
      ]
    }
  },
  "properties": {
    "satisfied": { "$ref": "#/$defs/YesNo" },
    "completed": { "$ref": "#/$defs/YesNo" }
  }
}
```

This ensures consistency: if you decide to change the label "Yes" to "Agree", you only change it in one place, and it updates across all variables.

---

## 4. The FAIR Data Domain (Rich Metadata)

While `title` is great for simple labels, FAIR data requires more depth: multilingual support, semantic pointers, and persistence. The **FAIR Data JSON Schema** dialect extends the `oneOf` pattern with custom keywords.

```json
{
  "const": 1,
  "title": "Yes",
  "fair:label": {
    "en": "Yes",
    "fr": "Oui",
    "de": "Ja"
  },
  "fair:conceptRef": "https://www.wikidata.org/wiki/Q231043"
}
```

### Why use FAIR extensions instead of just `title`?

1.  **Multilingualism**: Standard `title` is a single string. `fair:label` supports localized objects.
2.  **Semantic Context**: `fair:conceptRef` links the code to a global ontology (like Wikidata or SKOS), making the data machine-understandable across different languages and systems.
3.  **Variable Cascade**: This pattern implements a light version of the DDI "Variable Cascade." The shared definition in `$defs` acts as the *Represented Variable*, while the local property in `properties` acts as the *Instance Variable*, allowing you to have a local label (e.g., "User's Satisfaction") while inheriting a global domain definition.

---

## 5. External Semantic Mapping (SKOS)

For high-value datasets, the code list is often defined in an external authority or registry using [SKOS](https://www.w3.org/2004/02/skos/) (Simple Knowledge Organization System).

### The "Hybrid" Approach

Crucially, this is a **hybrid approach**. We do not replace the technical validation logic with semantic URIs; we anchor them together.

In each entry, we keep:
- **`const`**: Ensures that data files still validate against the correct codes (e.g., "FR").
- **`title`**: Provides a baseline human label for standard tools.
- **`fair:conceptRef`**: Provides the "semantic bridge" to the official authority URI.

Note that at this stage, we **no longer need `fair:label`** inside the schema. Since each code is mapped to a formal URI, a FAIR-aware application can dynamically retrieve the multilingual labels directly from the authoritative source (the SKOS Concept).

```json
{
  "fair:classification": ["http://data.europa.eu/nuts"],
  "oneOf": [
    {
      "const": "FR",
      "title": "France",
      "fair:conceptRef": "http://data.europa.eu/nuts/code/FR"
    }
  ]
}
```

This mapping allows a FAIR data harvester to:
1.  Discover that the variable follows the **NUTS** classification.
2.  Automatically translate "FR" to "France" in any language supported by the Eurostat registry.
3.  Perform automated data integration with other datasets that also use the NUTS level 0 URIs.

---

## Summary Comparison

| Feature | Standard `enum` | Standard `oneOf` | FAIR Dialect | SKOS Mapping |
| :--- | :---: | :---: | :---: | :---: |
| Value Validation | ✅ | ✅ | ✅ | ✅ |
| Human Labels | ❌ | ✅ (`title`) | ✅ (`fair:label`) | ✅ (External) |
| Shared Definitions | ❌ | ✅ (`$ref`) | ✅ (`$ref`) | ✅ (`$ref`) |
| Multilingual (i18n) | ❌ | ❌ | ✅ | ✅ (External) |
| Semantic Mapping | ❌ | ❌ | ✅ | ✅ (`skos:Concept`) |
| Authority Link | ❌ | ❌ | ❌ | ✅ (`skos:ConceptScheme`) |
| Standard Compatibility| ✅ | ✅ | ✅ (ignored by defaults) | ✅ |
