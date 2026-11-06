# Manual review of the 13 v0.4 additions

**Status:** Reviewed against canonical source fields and matching-term provenance.

| Record | Evidence class | Match evidence | Review |
|---|---|---|---|
| `nmah_1203283` | B | “wristwatch model electric”; “electric wristwatch” in object types | In scope as a model representing an electric wristwatch. Confirm model-object retention in the final corpus rules. |
| `nmah_1203284` | B | “wristwatch electric”; “electric wristwatch prototype” | Electric wristwatch prototype; in scope. |
| `nmah_1203285` | B | “wristwatch electric”; “electric wristwatch prototype” | Electric wristwatch prototype; in scope. |
| `nmah_1203286` | B | “wristwatch electric”; “Hamilton electric wristwatch” | Electric wristwatch; in scope. |
| `nmah_1203287` | B | “electric watch”; “Watch, Electric, Large Model Of” | Large model of an electric watch; in scope if object models are retained. |
| `nasm_A19480100000` | B | Title names oil temperature, oil pressure, and fuel pressure indicators | Engine monitoring instrument; in scope as aircraft instrumentation. |
| `nasm_A19480101000` | B | Title names oil temperature, oil pressure, and fuel pressure indicators | Engine monitoring instrument; in scope as aircraft instrumentation. |
| `nasm_A19480102000` | B | “indicator temperature” in title | Dual temperature indicator; in scope as aircraft instrumentation. |
| `nasm_A19480143000` | B | “tachometer” in title | Electric, panel-mounted tachometer; in scope as aircraft instrumentation. |
| `nasm_A19480151000` | B | “fuel quantity” in title | Fuel quantity indicator; in scope as aircraft instrumentation. |
| `nasm_A19480154000` | B | “voltmeter” and “ammeter” in title | Electrical panel meters; in scope as electronics. |
| `nasm_A19280002000` | A | Long description lists oil temperature, oil pressure, fuel quantity, tachometer, and airspeed indicator | Whole-aircraft record with direct evidence for its installed instruments; in scope under the platform rule below. |
| `nasm_A19490051000` | A | Long description names oil temperature, oil pressure, altimeter, and tachometer | Whole-aircraft record with direct evidence for its installed instruments; in scope under the platform rule below. |

The review found no off-domain addition among these records. Evidence classes and matching terms agree with the source data. Two NMAH records represent models rather than functional watches; they remain included in the current report because they explicitly represent electric-watch designs, with final model-object retention still to be stated in the V1 corpus rules.

## Platform-record rule

An aircraft record is eligible when its source description explicitly identifies an in-scope onboard instrument or system. The aircraft's historical importance or its `Aircraft` object type alone is not sufficient. The two platform records added by v0.4 meet this rule because their descriptions enumerate flight instruments. A regression test ensures that a generic aircraft record without such evidence remains excluded.

## Validation

Both narrative-evidence platform records and all structured-evidence instrument/watch records remain represented in `build/corpus-selection-report-v04.json`. The rule does not use an arbitrary text-length threshold or LLM classification.
