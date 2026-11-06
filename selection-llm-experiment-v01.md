# Exploratory AI screen of v0.3 exclusions

**Status:** Qualitative screening completed in this ChatGPT review; the user-approved scope expansion was implemented in policy v0.4. No external model API call was made.

## Purpose and method

The deterministic v0.3 policy accepted 28 of the 200 NASM/NMAH sample records. The 172 exclusions were screened semantically against the current D-019 domains: computing, electronics, guidance, control, and human-machine interaction. Titles, object types, narrative summaries, and physical descriptions were used. Candidate records were then inspected in their full canonical fields.

This is an exploratory model-assisted screen, not a blinded benchmark or a gold-standard annotation. It does not support a formal precision or recall score. No API tokens were consumed and no provider cost was incurred.

## Likely missed records

The screen identified 11 strong candidates for inclusion if electronic timekeeping and aircraft instrumentation fall within the current electronics/control scope.

| Candidate family | Records | Evidence and likely domain |
|---|---|---|
| Hamilton electric watches | `nmah_1203283`–`nmah_1203287` | Titles and object types identify electric wristwatches, prototypes, and the Ventura model. Likely electronics / consumer technology. |
| Aircraft engine and flight instruments | `nasm_A19480100000`, `nasm_A19480101000`, `nasm_A19480102000`, `nasm_A19480143000`, `nasm_A19480151000`, `nasm_A19480154000` | Combined oil/temperature/fuel indicators, an electric panel tachometer, a fuel quantity indicator, and a panel voltmeter/ammeter. Likely control / flight instrumentation or electronics. |

These candidates show a vocabulary and category gap, not merely a handful of spelling variants. The current policy has no general representation for electric watches, voltmeters, ammeters, tachometers, or engine-monitoring gauges.

## Scope-dependent candidates

These records require a scope decision before they should be counted as false negatives:

- `nmah_1301195` — Marine Clock; likely navigation/timekeeping, but the available canonical record has little descriptive evidence.
- `nmah_1303304` — John Bliss transit; a surveying instrument that may belong if guidance includes terrestrial navigation.
- `nmah_850825` and `nmah_850826` — electromechanical clocks; relevant only if electromechanical timekeeping belongs in the electronics domain.
- `nasm_A19480104000` — temperature-sensing bulb; potentially an aircraft instrumentation component.
- `nasm_A19400027000` — controllable-pitch propeller; its pitch is adjusted by the pilot, but the artifact is also propulsion equipment.
- `nasm_A19320084000` — barograph; a pressure-recording instrument with limited contextual evidence in this sample.
- Whole-aircraft records whose narratives mention control mechanisms or other in-scope systems; inclusion depends on the V1 policy for platform records.

Most other exclusions in this convenience sample are aircraft propulsion engines and propellers, whole-aircraft records without sufficiently direct in-scope system evidence, mechanical clocks and watches, locks, and unrelated artifacts. They remain outside the current D-019 scope unless the project domains are broadened.

## Rough API cost estimate

The 200 records contain about 456,000 characters across the canonical fields considered by selection. A rough estimate of 4 characters per input token gives about 114,000 content tokens. Allowing approximately 300 prompt tokens and 60 output tokens per record gives about 174,000 input tokens and 12,000 output tokens.

At the current displayed Batch rates, this is roughly **$0.01 with gpt-6-luna** or **$0.23 with gpt-6.1-sol** for this 200-record pass. For 10,000 similarly sized records, the same assumptions give roughly **$0.59** and **$11.71**, respectively. These estimates are approximate: no model tokenizer was run, prompt and output sizes are assumptions, and retries or larger records would increase usage. Batch pricing is listed at half the corresponding standard rates and is designed for asynchronous classification work. See the [Batch API guide](https://developers.openai.com/api/docs/guides/batch) and [current API pricing](https://developers.openai.com/api/docs/pricing).

## Conclusion and follow-up

The user's concern is valid: semantic screening can reveal whole missing categories that keyword iteration may not anticipate. For this sample, however, the likely API cost is small; the main remaining question is whether the project scope includes electric timepieces and engine/flight instrumentation.

The user confirmed that electric watches and aircraft instruments belong in the project. Policy v0.4 implements those categories with field-specific terms and reclassifies the G-meter as control instrumentation. Reprocessing the 200-record sample produced 41 accepted records; 13 records were added compared with v0.3. See `build/corpus-selection-report-v04.json` and the D-019 v0.4 section in `PROJECT.md`.

The exploratory ChatGPT screen helped locate candidate categories, but it is not a substitute for an API run or a human-verified evaluation set. A structured-output API comparison remains optional and has not been executed.
