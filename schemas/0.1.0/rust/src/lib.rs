// AUTO-GENERATED — do not edit manually.
// Source:  https://highvaluedata.net/fair-data-schema/0.1.0/vocab/annotations
// Version: 0.1.0
// Run:     uv run python scripts/generate_rust.py --version 0.1.0
//
// This module provides Rust structs and serde models for the FAIR Data JSON Schema dialect.
// It covers the full JSON Schema Draft 2020-12 vocabulary plus all FAIR extension
// annotations defined in https://highvaluedata.net/fair-data-schema/0.1.0/vocab/annotations.
//! FAIR Data Schema — Rust serde models (auto-generated).

use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use serde_json::Value;

// ---------------------------------------------------------------------------
// Type aliases & primitive enums
// ---------------------------------------------------------------------------

/// A string or a BCP-47 language-mapped map, e.g. {"en": "Age", "fr": "Âge"}.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(untagged)]
pub enum I18nString {
    Text(String),
    Map(HashMap<String, String>),
}

/// A Markdown-formatted string or a language-mapped map of Markdown strings.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(untagged)]
pub enum I18nText {
    Text(String),
    Map(HashMap<String, String>),
}

/// Valid JSON Schema type values.
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

// ---------------------------------------------------------------------------
// Helper models
// ---------------------------------------------------------------------------

/// Time period covered by the dataset (fair:temporalCoverage).
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct TemporalCoverage {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<I18nString>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub start: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub end: Option<String>,
}

/// One relationship entry within fair:datasetRelations.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct DatasetRelation {
    #[serde(rename = "relationType", skip_serializing_if = "Option::is_none")]
    pub relation_type: Option<String>,
    #[serde(rename = "targetRef", skip_serializing_if = "Option::is_none")]
    pub target_ref: Option<String>,
    #[serde(rename = "sourceVariables", skip_serializing_if = "Option::is_none")]
    pub source_variables: Option<Vec<String>>,
    #[serde(rename = "targetVariables", skip_serializing_if = "Option::is_none")]
    pub target_variables: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cardinality: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<I18nString>,
}

// ---------------------------------------------------------------------------
// SchemaNode — core recursive struct
// ---------------------------------------------------------------------------

/// A node in a FAIR-extended JSON Schema document.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct SchemaNode {
    // Core JSON Schema keywords
    #[serde(rename = "$id", skip_serializing_if = "Option::is_none")]
    pub id: Option<String>,
    #[serde(rename = "$ref", skip_serializing_if = "Option::is_none")]
    pub ref_uri: Option<String>,
    #[serde(rename = "$anchor", skip_serializing_if = "Option::is_none")]
    pub anchor: Option<String>,
    #[serde(rename = "$defs", skip_serializing_if = "Option::is_none")]
    pub defs: Option<HashMap<String, SchemaNode>>,
    #[serde(rename = "$vocabulary", skip_serializing_if = "Option::is_none")]
    pub vocabulary: Option<HashMap<String, bool>>,
    #[serde(rename = "$comment", skip_serializing_if = "Option::is_none")]
    pub comment: Option<String>,

    // Metadata
    #[serde(skip_serializing_if = "Option::is_none")]
    pub title: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub default: Option<Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub deprecated: Option<bool>,
    #[serde(rename = "readOnly", skip_serializing_if = "Option::is_none")]
    pub read_only: Option<bool>,
    #[serde(rename = "writeOnly", skip_serializing_if = "Option::is_none")]
    pub write_only: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub examples: Option<Vec<Value>>,

    // Validation
    #[serde(skip_serializing_if = "Option::is_none")]
    pub r#type: Option<Value>,
    #[serde(rename = "enum", skip_serializing_if = "Option::is_none")]
    pub enum_values: Option<Vec<Value>>,
    #[serde(rename = "const", skip_serializing_if = "Option::is_none")]
    pub const_value: Option<Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub minimum: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub maximum: Option<f64>,
    #[serde(rename = "exclusiveMinimum", skip_serializing_if = "Option::is_none")]
    pub exclusive_minimum: Option<f64>,
    #[serde(rename = "exclusiveMaximum", skip_serializing_if = "Option::is_none")]
    pub exclusive_maximum: Option<f64>,
    #[serde(rename = "multipleOf", skip_serializing_if = "Option::is_none")]
    pub multiple_of: Option<f64>,
    #[serde(rename = "minLength", skip_serializing_if = "Option::is_none")]
    pub min_length: Option<u64>,
    #[serde(rename = "maxLength", skip_serializing_if = "Option::is_none")]
    pub max_length: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub pattern: Option<String>,
    #[serde(rename = "minItems", skip_serializing_if = "Option::is_none")]
    pub min_items: Option<u64>,
    #[serde(rename = "maxItems", skip_serializing_if = "Option::is_none")]
    pub max_items: Option<u64>,
    #[serde(rename = "uniqueItems", skip_serializing_if = "Option::is_none")]
    pub unique_items: Option<bool>,

    // Applicators
    #[serde(skip_serializing_if = "Option::is_none")]
    pub properties: Option<HashMap<String, SchemaNode>>,
    #[serde(rename = "patternProperties", skip_serializing_if = "Option::is_none")]
    pub pattern_properties: Option<HashMap<String, SchemaNode>>,
    #[serde(rename = "additionalProperties", skip_serializing_if = "Option::is_none")]
    pub additional_properties: Option<Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub items: Option<Box<SchemaNode>>,
    #[serde(rename = "prefixItems", skip_serializing_if = "Option::is_none")]
    pub prefix_items: Option<Vec<SchemaNode>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub contains: Option<Box<SchemaNode>>,
    #[serde(rename = "allOf", skip_serializing_if = "Option::is_none")]
    pub all_of: Option<Vec<SchemaNode>>,
    #[serde(rename = "anyOf", skip_serializing_if = "Option::is_none")]
    pub any_of: Option<Vec<SchemaNode>>,
    #[serde(rename = "oneOf", skip_serializing_if = "Option::is_none")]
    pub one_of: Option<Vec<SchemaNode>>,

    // FAIR annotation fields
    #[serde(rename = "fair:conceptRef", skip_serializing_if = "Option::is_none")]
    pub fair_concept_ref: Option<String>,
    #[serde(rename = "fair:concept", skip_serializing_if = "Option::is_none")]
    pub fair_concept: Option<I18nString>,
    #[serde(rename = "fair:description", skip_serializing_if = "Option::is_none")]
    pub fair_description: Option<I18nText>,
    #[serde(rename = "fair:label", skip_serializing_if = "Option::is_none")]
    pub fair_label: Option<I18nString>,
    #[serde(rename = "fair:instanceVariableRef", skip_serializing_if = "Option::is_none")]
    pub fair_instance_variable_ref: Option<String>,
    #[serde(rename = "fair:representedVariableRef", skip_serializing_if = "Option::is_none")]
    pub fair_represented_variable_ref: Option<String>,
    #[serde(rename = "fair:conceptualVariableRef", skip_serializing_if = "Option::is_none")]
    pub fair_conceptual_variable_ref: Option<String>,
    #[serde(rename = "fair:unitType", skip_serializing_if = "Option::is_none")]
    pub fair_unit_type: Option<I18nString>,
    #[serde(rename = "fair:unitTypeRef", skip_serializing_if = "Option::is_none")]
    pub fair_unit_type_ref: Option<String>,
    #[serde(rename = "fair:universe", skip_serializing_if = "Option::is_none")]
    pub fair_universe: Option<I18nString>,
    #[serde(rename = "fair:universeRef", skip_serializing_if = "Option::is_none")]
    pub fair_universe_ref: Option<String>,
    #[serde(rename = "fair:population", skip_serializing_if = "Option::is_none")]
    pub fair_population: Option<I18nString>,
    #[serde(rename = "fair:populationRef", skip_serializing_if = "Option::is_none")]
    pub fair_population_ref: Option<String>,
    #[serde(rename = "fair:provider", skip_serializing_if = "Option::is_none")]
    pub fair_provider: Option<I18nString>,
    #[serde(rename = "fair:providerRef", skip_serializing_if = "Option::is_none")]
    pub fair_provider_ref: Option<String>,
    #[serde(rename = "fair:license", skip_serializing_if = "Option::is_none")]
    pub fair_license: Option<I18nString>,
    #[serde(rename = "fair:licenseRef", skip_serializing_if = "Option::is_none")]
    pub fair_license_ref: Option<String>,
    #[serde(rename = "fair:unit", skip_serializing_if = "Option::is_none")]
    pub fair_unit: Option<I18nString>,
    #[serde(rename = "fair:unitRef", skip_serializing_if = "Option::is_none")]
    pub fair_unit_ref: Option<String>,
    #[serde(rename = "fair:quantity", skip_serializing_if = "Option::is_none")]
    pub fair_quantity: Option<I18nString>,
    #[serde(rename = "fair:quantityRef", skip_serializing_if = "Option::is_none")]
    pub fair_quantity_ref: Option<String>,
    #[serde(rename = "fair:temporalCoverage", skip_serializing_if = "Option::is_none")]
    pub fair_temporal_coverage: Option<TemporalCoverage>,
    #[serde(rename = "fair:temporalCoverageRef", skip_serializing_if = "Option::is_none")]
    pub fair_temporal_coverage_ref: Option<String>,
    #[serde(rename = "fair:spatialCoverage", skip_serializing_if = "Option::is_none")]
    pub fair_spatial_coverage: Option<I18nString>,
    #[serde(rename = "fair:spatialCoverageRef", skip_serializing_if = "Option::is_none")]
    pub fair_spatial_coverage_ref: Option<String>,
    #[serde(rename = "fair:classification", skip_serializing_if = "Option::is_none")]
    pub fair_classification: Option<Vec<Value>>,
}

// ---------------------------------------------------------------------------
// DatasetSchema — root-level dataset schema
// ---------------------------------------------------------------------------

/// Root-level FAIR dataset schema struct.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct DatasetSchema {
    #[serde(rename = "$schema", skip_serializing_if = "Option::is_none")]
    pub schema: Option<String>,

    #[serde(flatten)]
    pub node: SchemaNode,
}
