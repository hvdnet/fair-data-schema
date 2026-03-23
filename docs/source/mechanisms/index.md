# Extension Mechanisms

The FAIR Data JSON Schema extends the standard JSON Schema (Draft 2020-12) through four primary mechanisms. These allow for rich semantic metadata and data stewardship features while maintaining 100% compatibility with standard validators.

::::{grid} 1 2 2 4
:gutter: 3

:::{grid-item-card} 🏷️ Annotations
:link: annotations
:link-type: doc

The lightest way to add metadata. Custom keywords are used as annotations that validators ignore but specialized tools use.
:::

:::{grid-item-card} 📚 Vocabularies
:link: vocabulary
:link-type: doc

Define new sets of keywords and their associated validation logic using the `$vocabulary` keyword.
:::

:::{grid-item-card} 🗣️ Dialects
:link: dialect
:link-type: doc

A specific "flavor" of JSON Schema that combines multiple vocabularies under a custom `$schema` URI.
:::

:::{grid-item-card} 💎 Refinements
:link: refinements
:link-type: doc

Advanced constraints that go beyond simple data types, such as physical units or semantic classifications.
:::
::::

```{toctree}
:maxdepth: 1
:hidden:

annotations
vocabulary
dialect
refinements
```
