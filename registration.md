# Silicon Sample Benchmark — method registration form

Fill in every item before the prediction lock; this file ships inside your repo's Zenodo release
(see the README's *Deposit* step). This form covers **one entry** (one repo / one Zenodo release,
`primary` or `secondary-k` — see the README's *What counts as a submission*); if you submit several
entries, fill one form per entry. Items marked **★**
must be disclosed **fully publicly** (never escrowed or withheld). Items marked **†** must be at
minimum escrowed — they may be sealed from the public, but never withheld from the core team. Items
not applicable to your approach: write `N/A`. When several models serve different pipeline stages, complete the model
sections (B) once per model. See the call's *Disclosure policy* for escrow rules.

---

## 0 · Approach identity and output
- **0.1 Team ★** — GESISCSS; Leon Fröhling and Claudia Wagner, both GESIS CSS. Corresponding contact: leon.froehling@gesis.org
- **0.2 Plain-language summary ★** — We use survey data (WVS US) to construct persona descriptions for a sample of the US population. We expose these personas to the conditions as well as to the survey questions in the context of zero-shot prompts, prompting an LLM to generate survey responses from the perspectives of these personas.
- **0.3 Submission tier & approach family ★** — tier (1); per-respondent simulation; single model; zero-shot
- **0.4 Pipeline diagram** — 1. identification of relevant US general population survey; 2. selection of relevant survey variables to use for persona constructions via LLM-based approach; 3. creation of persona descriptions; 4. preparation of prompts for zero-shot persona-prompting setup (using shared materials, i.e., condition texts, survey questions, etc.); 5. generation of survey responses (1 prompt := 1 survey response); 6. processing of generated survey responses to match required formats
- **0.5 Coverage ★** — **all 16 interventions and all 13 outcomes** - we have full coverage, with 500 participants per condition and 1,500 for control; each participant-row features all 13 outcomes

## A · Scope of LLM use
- **A.1 Purpose** — 1. we used an LLM (Qwen3-32B-AWQ 4bit) for the selection of relevant persona attributes from the set of all variables available in our base survey (WVS US 2017 wave) and 2. we used an LLM (Gemma3-12B-it) for the zero-shot persona-prompting setup used for response generation
- **A.2 Degree of automation ★** — The LLM used for response generation was given a prompt featuring the condition, the description of the participant, the survey question text, the available response options / outcome range, and some instructions on how to reply to the prompt. Each prompt thus led to the simulation of an individual participant's response to a single survey question for a specific condition as featured in the survey materials. 

## B · Model / system details (once per model)
- **B.1 Model name(s)** — https://huggingface.co/google/gemma-3-12b-it (Google, 12B, instruction-tuned)
- **B.2 Access & context mode** — local
- **B.3 Configuration** — model's default parameters; explicitly set were temperature=1, max_tokens=16, n=1, seed=42; no reasoning
- **B.4 Customization** — None
- **B.5 Persistent memory** — None
- **B.6 Inference stack** — vLLM; no quantization; single 40GB partition of NVIDIA A100 80GB GPU
- **B.7 Ensembles** — None

## C · Prompts
- **C.1 Exact prompts** — pre-specified; prompts were generated using a simple template featuring placeholders for the condition-texts, the persona description, the survey question, as well as the available response options / the response range; prompt template for outcomes: "Your task is to predict the survey response of a given participant. This is a brief description of the survey: A between-subjects field experiment testing 16 text-based interventions to increase trust in climate scientists against a control condition. The sample is N=18,000 U.S. adults (1,000 per intervention plus 2,000 control), recruited from an opt-in panel under census-based cross quotas on gender x age and gender x race/ethnicity. The primary outcome is a 12-item multidimensional trust composite; secondary and tertiary outcomes span funding perceptions, policy attitudes, institutional trust, climate beliefs and behaviors, and two behavioral measures: a real-money donation decision and a newsletter sign-up. This is the condition that the participant is being exposed to: {condition_text} This is the profile of the participant: {persona} This is the survey question for which you will predict the participant's response: {outcome_text} The response is on a scale from 0 to 100, with {outcome_scale} Your response may only contain the integer response between 0 and 100, no additional text or formating. Return just the plain integer response value."
- **C.2 System-wide instructions**: — None
- **C.3 Prompt-design rationale** — None

## D · Persona / profile construction (Tiers 1–2)
- **D.1 Profile source** — WVS US Wave 7; random sample of 500 survey respondents; relevant attributes for persona construction identified via LLM-based approach, selecting the 10 most frequently selected attributes across 1,000 independent model runs
- **D.2 Profile verbalization** — simple key-value format for persona descriptions, with (paraphrases of) survey questions as keys and (self-contained) survey responses as values; selected attributes (WVS US Wave 7 Question IDs: ['Q275', 'Q261', 'Q240', 'Q288', 'Q290', 'Q199', 'Q75', 'Q158', 'Q164', 'Q266'] / Paraphrases: [What is the highest level of education you have completed?; In what year were you born?; Where do you place your political views on a left–right scale from left (1) to right (10)?; On a 1–10 income scale for your country, where 1 is the lowest and 10 the highest income group, which step best represents your household’s total income?; Do you belong to any racial or ethnic group, and if so, which one?; How interested are you in politics?; How much confidence do you have in universities: a great deal, quite a lot, not very much, or none at all?; To what extent do you agree or disagree that science and technology are making our lives healthier, easier, and more comfortable?; How important is God in your life?; In which country were you born?])
- **D.3 Assignment & weighting** — 500 personas; reused across all conditions (each response generated completely independently of all other responses)

## E · Stimulus and survey administration
- **E.1 Stimulus presentation** — Single zero-shot prompt per survey question, featuring the relevant context (instructions, persona, condition, question, response options) 
- **E.2 Survey walk-through** — Not applicable; each response generated independently
- **E.3 Response elicitation** — Free text; relying on instruct-model's ability to select from presented response options / range of valid responses 

## F · Stochasticity and aggregation
- **F.1 Runs & seeds** — single run per respondent; seed and prompts stored 
- **F.2 Aggregation rule** — Not applicable

## G · Validation & post-processing
- **G.1 Human validation** — Not applicable
- **G.2 Post-processing** — Check if generated responses complied with available response options; in very few cases the response option value would be generated in place of the requested key, in which case the expected response could be retrieved via the available mapping between keys and values; valid n=500 due to strong adherence of LLM to required response format
- **G.3 Calibration corrections** — Not applicable

## H · Learning and conditioning components
- **H.1 Fine-tuning data** — Not applicable
- **H.2 Context & retrieval corpora** — Not applicable

## I · Data inputs, blinding, and competing interests
- **I.1 Competing interests ★** — None
- **I.2 External human data †** — WVS Wave 7 - USA 2017 (https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp) used for persona construction
- **I.3 Blinding attestation ★** — **mandatory.** No team member accessed, solicited, or was shown any human outcome data from this study, including pilots, before the prediction lock.
- **I.4 Contamination note †** — Google Gemma 3 family released 2025/03, thus training cutoff likely months before that date

## J · Internal selection procedure
- **J.1 Design-space search †** — Not applicable; no optimization across alternative approaches or parameter constellations due to time and resource constraints

## K · Reproducibility & frozen artifacts
- **K.1 Code & materials** — https://github.com/frohleon/silicon_sample_bench; documentation of unprocessed model responses and code for preparation of predictions-file available in raw_data_deposit
- **K.2 Raw output logs †** — complete unprocessed model responses - as they have been produced and stored during response generation - are provided in raw_data_deposit, together with all code and materials necessary to generate our predictions (predictions/team_4_T1_primary_v1.csv) from them
- **K.3 Computational resources** — 57,000 prompts (19 conditions, 500 personas, 6 variables) with on average 573 tokens for generation of demographics/control variables and 418,000 prompts (19 conditions, 500 personas, 44 variables) with on average 1,150 tokens for generation of outcome responses, totalling approx. 57,000 * 573 + 418,000 * 1,150 = 32,661,000 + 480,700,000 = 513,361,000 tokens (>>99% input tokens); approximately 5 minutes compute time per condition for demographics/control variables and approximately 30 minutes compute time per condition for outcome responses, totalling approx. 5 * 19 + 30 * 19 = 95 + 570 = 665 minutes compute time

## L · Disclosure class
Each item above is deposited as **public**, **escrowed** (sealed from the public but available to the
core team and auditors under confidentiality, with a public SHA-256 hash + timestamp so the lock is
still verifiable — an embargo with a sunset date is encouraged), or **withheld** (permitted only for
items marked neither ★ nor †). Your entry's class is set by its **most restricted item** and recorded
in `metadata.json` → `disclosure_class` (and `escrow_doi` if anything is escrowed):
- **A · Open** — all items public. Full results-table standing; all features enter the design-choice analysis.
- **B · Escrowed** — some items sealed but every item is available to the core team/auditors under confidentiality. Full standing with an *escrowed* badge; only publicly disclosed features enter the design-choice analysis.
- **C · Sealed** — one or more permitted items withheld even from escrow. Scored and reported with a *not independently verifiable* flag; excluded from the approach catalogue and design-choice analysis.

★ items must always be public (never escrowed or withheld); † items must be at minimum escrowed. Full
policy: <https://janpfander.github.io/llm_predictions_megastudy/#disclosure>
