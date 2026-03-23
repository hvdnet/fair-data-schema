# FAIR Data Cookbook

Welcome to the **FAIR Data Cookbook**! This collection of "recipes" provides practical, step-by-step guides for implementing the FAIR Data JSON Schema vocabularies in your own data products.

Each recipe addresses a specific challenge—from basic identification to complex semantic mapping—and includes working examples you can copy and adapt.

::::{grid} 1 2 2 4
:gutter: 3

:::{grid-item-card} 🏷️ Coded Values & Enums
:link: enum-to-fair-coded-values
:link-type: doc

Learn how to evolve from standard JSON Schema `enum` validation to rich, multilingual FAIR coded values.
:::

:::{grid-item-card} 🌊 The Variable Cascade
:link: variable-cascade
:link-type: doc

Understand how to implement the DDI Variable Cascade (Instance -> Represented -> Conceptual) using internal references.
:::

:::{grid-item-card} 📦 Data Products & Relations
:link: data-products
:link-type: doc

How to describe complex data products, including hierarchical files and join relationships between tables.
:::

:::{grid-item-card} 🏗️ Extension Mechanisms
:link: /mechanisms/index
:link-type: doc

A deep dive into the four ways to extend JSON Schema: Annotations, Vocabularies, Dialects, and Refinements.
:::
::::

## All Recipes

```{toctree}
:maxdepth: 1
:hidden:

variable-cascade
enum-to-fair-coded-values
complex-data-product
data-products
```

---

> [!TIP]
> Each recipe includes a "How-to" section with actionable steps. If you're looking for the raw JSON schema examples, check the `examples/` folder in the [source repository](https://github.com/highvaluedata/fair-data-schema).
