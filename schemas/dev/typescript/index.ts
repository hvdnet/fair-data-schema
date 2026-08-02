// AUTO-GENERATED — do not edit manually.
// Source:  https://highvaluedata.net/fair-data-schema/dev/vocab/annotations
// Version: dev
// Run:     uv run python scripts/generate_typescript.py --version dev
//
// This module provides TypeScript types and Zod schemas for the FAIR Data JSON Schema dialect.
// It covers the full JSON Schema Draft 2020-12 vocabulary plus all FAIR extension
// annotations defined in https://highvaluedata.net/fair-data-schema/dev/vocab/annotations.
/**
 * FAIR Data Schema — TypeScript types & Zod schemas (auto-generated).
 */

import { z } from "zod";

// ---------------------------------------------------------------------------
// Type aliases & primitive schemas
// ---------------------------------------------------------------------------

/** A string or a BCP-47 language-mapped dict, e.g. {"en": "Age", "fr": "Âge"}. */
export type I18nString = string | Record<string, string>;
export const I18nStringSchema = z.union([z.string(), z.record(z.string(), z.string())]);

/** A Markdown-formatted string or a language-mapped dict of Markdown strings. */
export type I18nText = string | Record<string, string>;
export const I18nTextSchema = z.union([z.string(), z.record(z.string(), z.string())]);

/** Valid JSON Schema ``type`` values. */
export type JsonType = "string" | "integer" | "number" | "boolean" | "array" | "object" | "null";
export const JsonTypeSchema = z.enum(["string", "integer", "number", "boolean", "array", "object", "null"]);

// ---------------------------------------------------------------------------
// Helper models (generated from inline object definitions in the vocab)
// ---------------------------------------------------------------------------

/** Time period covered by the dataset (fair:temporalCoverage). */
export const TemporalCoverageSchema = z.object({
  description: I18nStringSchema.optional(),
  start: z.string().describe("ISO date string").optional(),
  end: z.string().describe("ISO date string").optional(),
}).passthrough();

export type TemporalCoverage = z.infer<typeof TemporalCoverageSchema>;

/** One relationship entry within fair:datasetRelations. */
export const DatasetRelationSchema = z.object({
  relationType: z.string(),
  targetRef: z.string(),
  sourceVariables: z.array(z.string()).optional(),
  targetVariables: z.array(z.string()).optional(),
  cardinality: z.string().optional(),
  description: I18nStringSchema.optional(),
}).passthrough();

export type DatasetRelation = z.infer<typeof DatasetRelationSchema>;

// ---------------------------------------------------------------------------
// SchemaNode — core recursive interface & Zod schema
// ---------------------------------------------------------------------------

/**
 * A node in a FAIR-extended JSON Schema document.
 * Covers full JSON Schema Draft 2020-12 plus FAIR annotation extensions.
 */
export interface SchemaNode {
  // JSON Schema: core
  $id?: string;
  $ref?: string;
  $anchor?: string;
  $defs?: Record<string, SchemaNode>;
  $vocabulary?: Record<string, boolean>;
  $comment?: string;

  // JSON Schema: metadata
  title?: string;
  description?: string;
  default?: any;
  deprecated?: boolean;
  readOnly?: boolean;
  writeOnly?: boolean;
  examples?: any[];

  // JSON Schema: validation
  type?: JsonType | JsonType[];
  enum?: any[];
  const?: any;
  minimum?: number;
  maximum?: number;
  exclusiveMinimum?: number;
  exclusiveMaximum?: number;
  multipleOf?: number;
  minLength?: number;
  maxLength?: number;
  pattern?: string;
  minItems?: number;
  maxItems?: number;
  uniqueItems?: boolean;
  minContains?: number;
  maxContains?: number;
  required?: string[];
  dependentRequired?: Record<string, string[]>;
  minProperties?: number;
  maxProperties?: number;

  // JSON Schema: applicator
  properties?: Record<string, SchemaNode>;
  patternProperties?: Record<string, SchemaNode>;
  additionalProperties?: SchemaNode | boolean;
  items?: SchemaNode;
  prefixItems?: SchemaNode[];
  contains?: SchemaNode;
  allOf?: SchemaNode[];
  anyOf?: SchemaNode[];
  oneOf?: SchemaNode[];
  not?: SchemaNode;
  if?: SchemaNode;
  then?: SchemaNode;
  else?: SchemaNode;

  // JSON Schema: unevaluated
  unevaluatedProperties?: SchemaNode | boolean;
  unevaluatedItems?: SchemaNode | boolean;

  // JSON Schema: format & content
  format?: string;
  contentEncoding?: string;
  contentMediaType?: string;
  contentSchema?: SchemaNode;

  // FAIR extension annotations
  "fair:resourceType"?: string;
  "fair:conceptRef"?: string;
  "fair:concept"?: I18nString;
  "fair:label"?: I18nString;
  "fair:description"?: I18nText;
  "fair:version"?: I18nString;
  "fair:datasetRelations"?: DatasetRelation[];
  "fair:contributors"?: any[];
  "fair:provider"?: I18nString;
  "fair:providerRef"?: string;
  "fair:license"?: I18nString;
  "fair:licenseRef"?: string;
  "fair:temporalCoverage"?: TemporalCoverage;
  "fair:temporalCoverageRef"?: string;
  "fair:spatialCoverage"?: I18nString;
  "fair:spatialCoverageRef"?: string;
  "fair:population"?: I18nString;
  "fair:populationRef"?: string;
  "fair:structureType"?: string;
  "fair:quality"?: any[];
  "fair:classification"?: I18nString;
  "fair:classificationRef"?: any[];
  "fair:measurementUnit"?: I18nString;
  "fair:measurementUnitRef"?: string;
  "fair:measurementTechnique"?: I18nString;
  "fair:measurementTechniqueRef"?: string;
  "fair:quantity"?: I18nString;
  "fair:quantityRef"?: string;
  "fair:measurementScale"?: I18nString;
  "fair:measurementScaleRef"?: string;
  "fair:unitType"?: I18nString;
  "fair:unitTypeRef"?: string;
  "fair:universe"?: I18nString;
  "fair:universeRef"?: string;
  "fair:variableRef"?: string;
  "fair:instanceVariableRef"?: string;
  "fair:representedVariableRef"?: string;
  "fair:conceptualVariableRef"?: string;
  "fair:sentinel"?: boolean;
}

export const SchemaNodeSchema: z.ZodType<SchemaNode> = z.lazy(() =>
  z.object({
    $id: z.string().optional(),
    $ref: z.string().optional(),
    $anchor: z.string().optional(),
    $defs: z.record(z.string(), SchemaNodeSchema).optional(),
    $vocabulary: z.record(z.string(), z.boolean()).optional(),
    $comment: z.string().optional(),

    title: z.string().optional(),
    description: z.string().optional(),
    default: z.any().optional(),
    deprecated: z.boolean().optional(),
    readOnly: z.boolean().optional(),
    writeOnly: z.boolean().optional(),
    examples: z.array(z.any()).optional(),

    type: z.union([JsonTypeSchema, z.array(JsonTypeSchema)]).optional(),
    enum: z.array(z.any()).optional(),
    const: z.any().optional(),
    minimum: z.number().optional(),
    maximum: z.number().optional(),
    exclusiveMinimum: z.number().optional(),
    exclusiveMaximum: z.number().optional(),
    multipleOf: z.number().optional(),
    minLength: z.number().optional(),
    maxLength: z.number().optional(),
    pattern: z.string().optional(),
    minItems: z.number().optional(),
    maxItems: z.number().optional(),
    uniqueItems: z.boolean().optional(),
    minContains: z.number().optional(),
    maxContains: z.number().optional(),
    required: z.array(z.string()).optional(),
    dependentRequired: z.record(z.string(), z.array(z.string())).optional(),
    minProperties: z.number().optional(),
    maxProperties: z.number().optional(),

    properties: z.record(z.string(), SchemaNodeSchema).optional(),
    patternProperties: z.record(z.string(), SchemaNodeSchema).optional(),
    additionalProperties: z.union([SchemaNodeSchema, z.boolean()]).optional(),
    items: SchemaNodeSchema.optional(),
    prefixItems: z.array(SchemaNodeSchema).optional(),
    contains: SchemaNodeSchema.optional(),
    allOf: z.array(SchemaNodeSchema).optional(),
    anyOf: z.array(SchemaNodeSchema).optional(),
    oneOf: z.array(SchemaNodeSchema).optional(),
    not: SchemaNodeSchema.optional(),
    if: SchemaNodeSchema.optional(),
    then: SchemaNodeSchema.optional(),
    else: SchemaNodeSchema.optional(),

    unevaluatedProperties: z.union([SchemaNodeSchema, z.boolean()]).optional(),
    unevaluatedItems: z.union([SchemaNodeSchema, z.boolean()]).optional(),

    format: z.string().optional(),
    contentEncoding: z.string().optional(),
    contentMediaType: z.string().optional(),
    contentSchema: SchemaNodeSchema.optional(),

    "fair:resourceType": z.string().optional(),
    "fair:conceptRef": z.string().optional(),
    "fair:concept": I18nStringSchema.optional(),
    "fair:label": I18nStringSchema.optional(),
    "fair:description": I18nTextSchema.optional(),
    "fair:version": I18nStringSchema.optional(),
    "fair:datasetRelations": z.array(DatasetRelationSchema).optional(),
    "fair:contributors": z.array(z.any()).optional(),
    "fair:provider": I18nStringSchema.optional(),
    "fair:providerRef": z.string().optional(),
    "fair:license": I18nStringSchema.optional(),
    "fair:licenseRef": z.string().optional(),
    "fair:temporalCoverage": TemporalCoverageSchema.optional(),
    "fair:temporalCoverageRef": z.string().optional(),
    "fair:spatialCoverage": I18nStringSchema.optional(),
    "fair:spatialCoverageRef": z.string().optional(),
    "fair:population": I18nStringSchema.optional(),
    "fair:populationRef": z.string().optional(),
    "fair:structureType": z.string().optional(),
    "fair:quality": z.array(z.any()).optional(),
    "fair:classification": I18nStringSchema.optional(),
    "fair:classificationRef": z.array(z.any()).optional(),
    "fair:measurementUnit": I18nStringSchema.optional(),
    "fair:measurementUnitRef": z.string().optional(),
    "fair:measurementTechnique": I18nStringSchema.optional(),
    "fair:measurementTechniqueRef": z.string().optional(),
    "fair:quantity": I18nStringSchema.optional(),
    "fair:quantityRef": z.string().optional(),
    "fair:measurementScale": I18nStringSchema.optional(),
    "fair:measurementScaleRef": z.string().optional(),
    "fair:unitType": I18nStringSchema.optional(),
    "fair:unitTypeRef": z.string().optional(),
    "fair:universe": I18nStringSchema.optional(),
    "fair:universeRef": z.string().optional(),
    "fair:variableRef": z.string().optional(),
    "fair:instanceVariableRef": z.string().optional(),
    "fair:representedVariableRef": z.string().optional(),
    "fair:conceptualVariableRef": z.string().optional(),
    "fair:sentinel": z.boolean().optional(),
  }).passthrough()
);

// ---------------------------------------------------------------------------
// DatasetSchema — root-level dataset schema
// ---------------------------------------------------------------------------

/** Root-level FAIR dataset schema interface. */
export interface DatasetSchema extends SchemaNode {
  $schema?: string;
}

/** Root-level FAIR dataset schema Zod validation schema. */
export const DatasetSchemaSchema: z.ZodType<DatasetSchema> = SchemaNodeSchema.and(
  z.object({
    $schema: z.string().default("https://highvaluedata.net/fair-data-schema/dev").optional(),
  })
);
