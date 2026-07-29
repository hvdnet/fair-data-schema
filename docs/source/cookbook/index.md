# FAIR Data Cookbook

Welcome to the **FAIR Data Cookbook**! This collection of recipes provides practical, step-by-step guides for implementing the FAIR Data JSON Schema vocabularies in your data assets with minimal effort.

Each recipe addresses a specific task—from basic identification to advanced semantic mapping—and includes working code examples you can copy and adapt immediately.

---

## 🟢 Tier 1: Essential Recipes (Start Here)

Get started in minutes using simple, intuitive annotations for everyday datasets:

::::{grid} 1 2 2 4
:gutter: 3

:::{grid-item-card} 📊 Tier 1 Simple Dataset
:link: simple-dataset
:link-type: doc

Annotate a simple, single-table dataset with title, license, unit type, measurement units, and self-documenting codes.
:::

:::{grid-item-card} ✅ Validating Data
:link: validation
:link-type: doc

Validate JSON data against FAIR schemas using common tools (Python `jsonschema`, Node.js `ajv`, CLI, Go, Java).
:::

:::{grid-item-card} 🏷️ Coded Values & Enums
:link: enum-to-fair-coded-values
:link-type: doc

Learn how to evolve standard JSON Schema `enum` fields into self-documenting FAIR coded values mapped to human titles and web concepts.
:::

:::{grid-item-card} 📦 Data Products & Tables
:link: data-products
:link-type: doc

Learn how to annotate basic dataset schemas and describe tables and resources with minimal effort.
:::
::::

---

## 2. Advanced & Extended Recipes (Optional Deep-Dive)

For users who want to dig deeper into formal data stewardship, these advanced recipes explore deep provenance, population bounds, and complex data lineage:

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} 🌊 The Variable Cascade
:link: variable-cascade
:link-type: doc

Implement formal variable lineage (Instance -> Represented -> Conceptual) using internal and external schema references.
:::

:::{grid-item-card} 🏛️ Hierarchical Data Products
:link: complex-data-product
:link-type: doc

Describe complex multi-table data products, hierarchical structures, and cross-dataset join relationships.
:::

:::{grid-item-card} 🏗️ Extension Mechanisms
:link: /mechanisms/index
:link-type: doc

Explore the four core mechanisms used to extend JSON Schema: Annotations, Vocabularies, Dialects, and Refinements.
:::
::::

---

## All Recipes

```{toctree}
:maxdepth: 1
:hidden:

simple-dataset
validation
enum-to-fair-coded-values
data-products
complex-data-product
variable-cascade
```

---

> [!TIP]
> Each recipe includes a "How-to" section with actionable steps. Check out the `examples/` folder in the [source repository](https://github.com/highvaluedata/fair-data-schema) for complete JSON schema files.
