# Rust Package & API Reference

The Rust package (`fair-data-schema` crate or `schemas/<version>/rust/src/lib.rs`) provides auto-generated Rust data structures with `serde` serialization annotations.

## Exported Enums

### `I18nString`
Untagged enum for internationalized string fields (plain string vs BCP-47 language map).

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(untagged)]
pub enum I18nString {
    Text(String),
    Map(HashMap<String, String>),
}
```

### `I18nText`
Untagged enum for internationalized rich-text / Markdown fields.

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(untagged)]
pub enum I18nText {
    Text(String),
    Map(HashMap<String, String>),
}
```

### `JsonType`
Enum representing JSON Schema types.

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "lowercase")]
pub enum JsonType {
    String,
    Integer,
    Number,
    Boolean,
    Array,
    Object,
    Null,
}
```

---

## Exported Structs

### `DatasetSchema`
Root-level FAIR dataset schema struct.

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct DatasetSchema {
    #[serde(rename = "$schema", skip_serializing_if = "Option::is_none")]
    pub schema: Option<String>,

    #[serde(flatten)]
    pub node: SchemaNode,
}
```

### `SchemaNode`
Core schema node struct containing standard Draft 2020-12 keywords and `fair:` annotations mapped to `fair_` field attributes.

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct SchemaNode {
    pub id: Option<String>,
    pub ref_uri: Option<String>,
    pub anchor: Option<String>,
    pub defs: Option<HashMap<String, SchemaNode>>,
    pub vocabulary: Option<HashMap<String, bool>>,
    pub comment: Option<String>,

    pub title: Option<String>,
    pub description: Option<String>,
    pub default: Option<serde_json::Value>,
    pub deprecated: Option<bool>,
    pub read_only: Option<bool>,
    pub write_only: Option<bool>,
    pub examples: Option<Vec<serde_json::Value>>,

    pub properties: Option<HashMap<String, SchemaNode>>,
    pub items: Option<Box<SchemaNode>>,
    pub prefix_items: Option<Vec<SchemaNode>>,
    pub all_of: Option<Vec<SchemaNode>>,
    pub any_of: Option<Vec<SchemaNode>>,
    pub one_of: Option<Vec<SchemaNode>>,

    // FAIR annotation fields
    pub fair_resource_type: Option<String>,
    pub fair_concept_ref: Option<String>,
    pub fair_concept: Option<I18nString>,
    pub fair_label: Option<I18nString>,
    pub fair_description: Option<I18nText>,
    pub fair_dataset_relations: Option<Vec<DatasetRelation>>,
    pub fair_contributors: Option<Vec<serde_json::Value>>,
    pub fair_provider: Option<I18nString>,
    pub fair_provider_ref: Option<String>,
    pub fair_license: Option<I18nString>,
    pub fair_license_ref: Option<String>,
    pub fair_temporal_coverage: Option<TemporalCoverage>,
    pub fair_spatial_coverage: Option<I18nString>,
    pub fair_population: Option<I18nString>,
    pub fair_structure_type: Option<String>,
    pub fair_quality: Option<Vec<serde_json::Value>>,
    pub fair_classification: Option<I18nString>,
    pub fair_measurement_unit: Option<I18nString>,
    pub fair_measurement_technique: Option<I18nString>,
    pub fair_quantity: Option<I18nString>,
    pub fair_unit_type: Option<I18nString>,
    pub fair_universe: Option<I18nString>,
    pub fair_sentinel: Option<bool>,
}
```

### Helper Structs
- **`TemporalCoverage`**: `pub description: Option<I18nString>`, `pub start: Option<String>`, `pub end: Option<String>`.
- **`DatasetRelation`**: `pub relation_type: Option<String>`, `pub target_ref: Option<String>`, `pub source_variables: Option<Vec<String>>`, `pub target_variables: Option<Vec<String>>`, `pub cardinality: Option<String>`, `pub description: Option<I18nString>`.
