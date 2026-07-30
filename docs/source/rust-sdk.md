# Rust SDK — Serde Data Models

The FAIR Data JSON Schema project provides auto-generated **Rust data structures (`serde`)** for high-performance CLI utilities, data engineering pipelines, and WebAssembly (WASM) tools.

## Overview

The generated Rust models live in `schemas/<version>/rust/src/lib.rs` (and mirrored in the web distribution at `dist/<version>/rust/lib.rs`).

It provides:
- **Serde-annotated Data Structs**: `DatasetSchema`, `SchemaNode`, `TemporalCoverage`, `DatasetRelation`
- **Type Enums**: `I18nString` (text string vs language map), `I18nText`, `JsonType`

## Dependencies (`Cargo.toml`)

To deserialize or serialize FAIR JSON schemas in your Rust project, add `serde` and `serde_json`:

```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
```

## Basic Usage

### Deserializing a FAIR Schema from JSON

```rust
use serde_json::Result;
use fair_data_schema::DatasetSchema;

fn parse_schema(json_data: &str) -> Result<DatasetSchema> {
    let schema: DatasetSchema = serde_json::from_str(json_data)?;

    if let Some(title) = &schema.node.title {
        println!("Dataset Title: {}", title);
    }

    if let Some(license) = &schema.node.fair_license {
        println!("FAIR License: {:?}", license);
    }

    Ok(schema)
}
```

### Building & Serializing a Schema Programmatically

```rust
use std::collections::HashMap;
use fair_data_schema::{DatasetSchema, SchemaNode, I18nString};

fn create_schema() -> DatasetSchema {
    let mut properties = HashMap::new();

    properties.insert(
        "age".to_string(),
        SchemaNode {
            r#type: Some(serde_json::json!("integer")),
            title: Some("Age".to_string()),
            minimum: Some(0.0),
            fair_measurement_unit: Some(I18nString::Text("years".to_string())),
            ..Default::default()
        },
    );

    DatasetSchema {
        schema: Some("https://highvaluedata.net/fair-data-schema/dev".to_string()),
        node: SchemaNode {
            title: Some("Census 2024".to_string()),
            fair_license: Some(I18nString::Text("CC-BY-4.0".to_string())),
            properties: Some(properties),
            ..Default::default()
        },
    }
}
```

## Auto-Generation

The Rust definition file `schemas/<version>/rust/src/lib.rs` is **auto-generated** from the FAIR annotation meta-schemas using Jinja2 templates.

To regenerate Rust models for the development track:

```bash
uv run python scripts/generate_rust.py --version dev
```
