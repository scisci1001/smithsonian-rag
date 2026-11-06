# Manual review of the v0.5 refinements

**Status:** Reviewed against the available canonical record fields and the selection report's matched-term provenance.

| Record | Evidence class | Evidence | Decision |
|---|---|---|---|
| `nasm_A19480104000` — “Bulb, Temperature Sensing” | B | Structured title/type metadata identifies a temperature-sensing bulb; the artifact is an aircraft engine instrumentation component. | Include under control/instrumentation. The title-specific term avoids matching generic temperature records. |
| `nasm_A19400027000` — controllable-pitch propeller | A | Narrative states that the pilot adjusts the propeller blade pitch. | Include under aircraft control. This is direct evidence of an in-scope control function. |
| `nasm_A19320084000` — “Barograph” | — | Scientific-instrument metadata and a broad indexed `Aviation` usage flag, but no description of a flight or spaceflight function. The current canonical selection fields do not include this generic usage flag. | Exclude under the current field policy. Revisit if generic usage flags are deliberately admitted as evidence. |
| `nmah_850825`, `nmah_850826` — electromechanical clocks | — | Clock records; not identified as electric watches. | Exclude. The accepted scope covers electric watches, not general timekeeping. |

The two additions raise the v0.5 sample result from 41 to 43 accepted records. Both have evidence in the source metadata; no free-text length threshold or model judgment is used. The unchanged exclusions document the current boundary and can be revisited only if the project scope changes or new source evidence is found.

## Validation

The v0.5 report is `build/corpus-selection-report-v05.json`. It contains 200 input records, 43 accepted records (19 A and 24 B), with 34 NASM and 9 NMAH records accepted. Regression tests cover both additions and the barograph exclusion; separate tests preserve the general-clock boundary.
