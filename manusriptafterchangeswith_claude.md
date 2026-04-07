# Are LLM Agents the New RPA? A Comparative Study with RPA Across Standardised RPA Benchmarks
<!-- CHANGE: Subtitle changed from "Across Enterprise Workflows" to "Across Standardised RPA Benchmarks" to accurately reflect scope (R2-C1, R2-C4) -->

Petr Průcha¹, Michaela Matoušková¹, and Jan Strnad²

¹ Technical University of Liberec, Liberec, Czechia
petr.prucha@tul.cz, michaela.matouskova@tul.cz

² Pointee Inc., Delaware, USA

---

## Abstract

<!-- CHANGE: Abstract expanded to include statistical methods and key numerical results (R1-C1) -->
The emergence of large language models (LLMs) has introduced a new paradigm in automation: LLM agents or Agentic Automation with Computer Use (AACU). Unlike traditional Robotic Process Automation (RPA), which relies on rule-based workflows and scripting, AACU enables intelligent agents to perform tasks through natural language instructions and autonomous interaction with user interfaces. This study investigates whether AACU can serve as a viable alternative to RPA in standardised benchmark automation tasks. We conducted controlled experiments across three tasks drawn from the well-known rpachallenge.com benchmark suite — covering data entry, web monitoring, and document extraction — comparing RPA (via UiPath) and AACU (via Anthropic's Computer Use Agent). Execution speed was assessed using Welch's t-test; RPA was significantly faster in both comparable processes (P2: t = −3.38, p = 0.0096; P3: t = −17.30, p < 0.001), with mean execution times of 53.9 s vs. 109.8 s (P2) and 20 s vs. 202.8 s (P3). Large effect sizes (Cohen's d = 1.51 and 7.73 respectively) confirm the practical significance of these differences. Reliability was evaluated using Fisher's Exact Test on P2 and P3; RPA achieved a 100% success rate across all runs, while AACU achieved 90% on P2 and 60% on P3, though these differences did not reach statistical significance at α = 0.05 (p = 1.0 and p = 0.087, respectively). Development effort was assessed descriptively and indicated substantially lower time requirements for AACU (≈10 min vs. ≈38 min for P2; ≈15 min vs. ≈240 min for P3). While RPA outperforms AACU in execution speed and reliability in repetitive, stable environments, AACU demonstrates substantially reduced development effort and greater flexibility with dynamic interfaces. Current AACU implementations are not yet production-ready, but their promise in rapid prototyping and lightweight automation is evident. Future research should explore multi-agent orchestration, hybrid RPA-AACU architectures, and more robust evaluation across task types and platforms.

**Keywords:** Robotic Process Automation, RPA, LLM agent, Computer Use, AI Automation, Agentic Automation, Benchmark Evaluation

---

## 1. Introduction

Currently, large language models (LLMs) and generative AI are rapidly gaining attention in the field of automation. Recent advances in LLMs have enabled a new paradigm known as *AI agentic automation*. In this approach, intelligent agents can perform specific tasks by interacting with digital systems in a way that resembles how a human user would operate a computer. A specific subset of this, referred to here as *AI Agentic Automation with Computer Use* (AACU) or LLM agents with computer use, allows agents to use software tools, interfaces, and APIs autonomously based on high-level natural language instructions.

AACU shares several traits with traditional Robotic Process Automation (RPA). Both technologies aim to automate repetitive digital tasks to reduce human effort, minimize errors, and improve operational efficiency. However, they differ fundamentally in implementation. RPA requires well-defined workflows and low-code or coded instructions to automate specific tasks. In contrast, AACU uses natural language prompts as input. These prompts are dynamically interpreted and translated into executable actions by the agent, reducing the need for explicit programming and enabling faster, more adaptive automation.

The literature suggests that AACU may eventually replace RPA in certain use cases [1–3]. While RPA has demonstrated clear benefits such as cost reduction, improved process quality, and error mitigation across various industries, it still relies heavily on structured rules and manual configuration [4–6]. AACU, by contrast, represents a more flexible and scalable solution. It promises faster deployment and greater adaptability by leveraging the reasoning and language understanding capabilities of LLMs [7]. In this sense, AACU could potentially accelerate process automation by minimising the technical barrier traditionally associated with automation tools.

Despite the growing excitement around LLM-based agents, there is a noticeable gap in empirical, controlled comparisons between AACU and RPA. Current discourse is largely driven by hype rather than evidence. It remains unclear whether agentic automation can reliably perform the same tasks as RPA, or even surpass it in terms of performance and usability. This research aims to investigate the current state of AACU and compare it with the established capabilities of RPA using a **benchmark-based evaluation** on standardised RPA tasks. We explicitly frame this as a benchmark study: the tasks used are drawn from rpachallenge.com, a widely used benchmark suite in the RPA community, covering three archetypal task categories — structured data entry, web monitoring with conditional logic, and document extraction with OCR — that are representative of common automation scenarios, even if they do not constitute live enterprise deployments.

<!-- CHANGE: Added novelty/contribution statement (R1-C8) -->
The primary contribution of this work is one of the first empirical, controlled comparisons between AACU and RPA on standardised benchmark tasks, providing quantitative baselines for execution speed and reliability alongside a descriptive assessment of development effort. A secondary contribution is the adaptation of van der Aalst et al.'s [23] RPA feasibility framework to incorporate agentic automation as a distinct automation modality with a distinct cost and capability profile.

<!-- CHANGE: Added significance and beneficiaries paragraph (R1-C3) -->
The findings of this study are relevant to multiple stakeholder groups. Practitioners and automation engineers can use these results to make informed decisions about when to deploy AACU versus RPA, particularly in contexts where development speed is prioritised over execution reliability. Business analysts and process owners will benefit from a clearer understanding of the current maturity and cost profile of agentic automation. Researchers in AI and business process management will find value in the empirical baseline this study establishes for future comparative work as AACU technologies continue to mature.

---

## 2. Related Work

### 2.1 Robotic Process Automation

<!-- CHANGE: Citations harmonised to numbered style throughout (R1-C2) -->
Recent research suggests a shift from traditional RPA and intelligent automation toward more advanced forms of automation that operate directly from human language inputs [1, 12, 3]. Intelligent agents are increasingly seen as the future of robotic process automation, largely due to advances in artificial intelligence and machine learning [7]. Although the trend is moving toward greater agent autonomy, some systems still rely on RPA to execute specific tasks, due to its high efficiency in interacting with computer environments and its ability to simulate user actions reliably [4–6].

The term *"agentic automation"* does not currently yield substantial literature focused specifically on business process automation in academic databases such as Scopus or Web of Science. This is consistent with the recency of the field: many relevant studies appear in preprint repositories and top-tier AI conference proceedings rather than established journals. We therefore supplemented our search with preprint sources and conference proceedings, using search terms including "LLM-based automation", "tool-using agents", "autonomous UI agents", and "agentic process automation", in addition to "RPA" and "robotic process automation". Emerging research has also begun to explore the integration of AI agents into enterprise processes using newer technologies such as Retrieval-Augmented Generation (RAG) and Model Context Protocols (MCP) [8, 9].

Sapkota et al. provide a taxonomy and clear description of AI agents and agentic AI, illustrating the differences between these two concepts with practical examples [11]. Ye et al. (2023) introduce a new paradigm for agentic process automation through the development of the ProAgent tool, which can automate processes based on user instructions and demonstrates the potential of AI agents to interact with computer systems to carry out complex tasks autonomously [12]. Recent benchmarks such as OSWorld and WebArena have begun to systematically evaluate autonomous UI agents on computer tasks, providing evidence that LLM-based agents can perform a meaningful subset of GUI-based tasks, though with substantially lower success rates than humans [see 7 for a review].

Technology companies are currently racing to offer robust AACU platforms. Many tools remain in closed beta or are not yet publicly accessible worldwide. Anthropic released a publicly available computer-use tool via its open repositories, designed to perform actions through user interfaces, addressing many of the same tasks traditionally handled by RPA solutions [13].

### 2.2 Theoretical Background

<!-- CHANGE: New subsection added to provide theoretical grounding for hypotheses (R1-C4, R2-C3) -->
The comparison between RPA and AACU can be grounded in the fundamental architectural differences between rule-driven and generative decision-making systems. RPA operates through deterministic, pre-compiled workflows: each action is explicitly specified and executed without inference at runtime, resulting in low and predictable latency. AACU, by contrast, relies on iterative perception-action cycles in which the agent captures screenshots, encodes them, submits them to an LLM for reasoning, and translates the model's output into GUI actions. This introduces inference latency at every step — a well-documented bottleneck in deployed LLM systems [7] — which theoretically predicts slower execution for AACU compared to RPA.

On reliability, RPA's deterministic execution theoretically implies high repeatability in stable, structured environments: given identical inputs and interface states, an RPA bot will produce identical outputs. AACU's generative, probabilistic nature implies that outputs may vary across runs even with identical inputs, due to temperature-based sampling and sensitivity to minor visual changes in the interface [18–20]. This theoretically predicts lower reliability for AACU in structured, repetitive tasks.

On development effort, RPA requires explicit specification of every workflow step in low-code or scripted form, demanding familiarity with the RPA platform and the target application's element structure. AACU requires only a natural language prompt, substantially lowering the specification burden. This theoretically predicts lower development effort for AACU.

These theoretical predictions motivate the following hypotheses, framed as empirical tests of claims prominent in industry and popular discourse:

- **H1:** AACU performs automation faster than RPA.
- **H2:** AACU is more reliable than RPA.
- **RQ3:** Does AACU appear to require less development effort than RPA? *(treated descriptively; see Section 4)*

<!-- CHANGE: H3 converted to a research question (RQ3) rather than a formal hypothesis, due to single-measurement limitation (R2-C8) -->

---

## 3. Process Overview

For this study, we selected three processes representative of typical RPA benchmark tasks, sourced from the well-known website https://rpachallenge.com, which features example processes designed to simulate operations commonly automated using RPA. We note that these tasks constitute a **benchmark environment**, not a live enterprise deployment, and results should be interpreted accordingly.

### Process 1 – The RPA Challenge (P1)

Process 1 is widely recognised in the RPA community as "The RPA Challenge." To complete it, an automation must extract data from a spreadsheet and input it into specific fields within a web form whose layout changes with each round. This process is a standard benchmark for evaluating RPA robustness to dynamic form layouts.

### Process 2 – RPA Challenge Stock Market (P2)

Process 2 requires the automation to navigate to a challenge website, select a company from a dropdown menu, monitor a displayed stock price, and notify the user if the price drops below a threshold. It evaluates web scraping, conditional logic, and user notification capabilities.

### Process 3 – RPA Challenge Invoices, Simplified (P3)

Process 3 requires the automation to extract structured data from a table of invoice records and from linked invoice images, writing results to a CSV file. Due to context window limitations of the AACU, the task was limited to the first page of four invoices. **This simplification gives AACU a relative advantage on task scope compared to the full challenge; results for P3 should be interpreted with this in mind.** The rationale and impact of this adaptation are discussed further in Section 5.

---

## 4. Methodology

To test the hypotheses, we conducted experiments using the three processes described in Section 3. For RPA, we used UiPath Studio 2023.4.0 Community Edition. For agentic automation, we used Anthropic's Computer Use Agent running in a controlled Docker environment (Ubuntu 22.04.5 LTS) with Firefox, LibreOffice, and Gedit.

The specific AACU configuration was:
- GitHub commit: 99502f5
- Model: claude-sonnet-4-20250514
- Tool Version: computer_use_20250124
- Max Output Tokens: 16,384
- Image Input: Enabled (3 most recent screenshots per action)

Each process was executed 10 times per technology, with the exception of P1 for AACU (see below). Timing was recorded using UiPath's built-in tools (RPA) and a stopwatch (AACU); manual timing introduces minor imprecision, which we acknowledge as a limitation.

### 4.1 Treatment of Process 1

<!-- CHANGE: P1 AACU treatment restructured — now qualitative/exploratory only, excluded from statistical tests (R2-C5) -->
P1 presented a unique situation: the AACU was unable to complete the task due to technical limitations. After several actions, the application would freeze, fail to accept further input, or attempt to reconnect unsuccessfully. Refreshing the session caused the agent to lose context entirely, requiring re-prompting from the beginning. Only one run was attempted before it became clear that the task could not be completed under current tool constraints.

Given that a single failed run does not constitute a meaningful reliability sample, **P1 AACU data has been excluded from all statistical comparisons.** P1 is instead discussed as a qualitative finding in Section 5.1, documenting the nature of the capability boundary encountered. RPA completed all 10 P1 runs successfully and its performance is reported for completeness.

### 4.2 Statistical Methods

<!-- CHANGE: Added justification for choice of statistical methods with citations (R1-C5) -->
For H1 (execution speed), we used Welch's t-test (two-sample t-test assuming unequal variances), which is appropriate for comparing two independent groups with small and potentially unequal sample sizes and variances [Derrick et al., 2016]. We report the t-statistic, p-value, Cohen's d effect size, and 95% confidence interval for the mean difference.

For H2 (reliability), we applied Fisher's Exact Test, which is the standard method for 2×2 contingency tables with small expected cell counts — a Chi-Square test was not appropriate here as several cells had expected counts below 5 [Fisher, 1922; Agresti, 2002]. **Fisher's Exact Test is applied only to P2 and P3**, where 10 runs were completed for both technologies. We report the odds ratio, p-value, and 95% CI for the odds ratio.

For RQ3 (development effort), no statistical test is applied due to the single-observation-per-process design. Results are presented descriptively and interpreted in light of the magnitude of observed differences.

---

## 5. Results

Results are summarised in Table 1. P1 AACU data is excluded from statistical analysis and discussed separately in Section 5.1.

**Table 1.** Results of duration and success rate per technology.

| Process | RPA time (s) | RPA Successful / Unsuccessful | AACU time (s) | AACU Successful / Unsuccessful |
|---------|-------------|-------------------------------|---------------|-------------------------------|
| P1 | 139.8 | 10 / 0 | — | 0 / 1 (exploratory only) |
| P2 | 53.9 | 10 / 0 | 109.8 | 9 / 1 |
| P3 | 20.0 | 10 / 0 | 202.8 | 6 / 4 |

### 5.1 P1 — Qualitative Finding

<!-- CHANGE: New dedicated section for P1 as qualitative finding (R2-C5) -->
The AACU was unable to complete P1 in the single attempted run. The agent accurately identified and interacted with the correct form fields despite the dynamic layout — demonstrating strong visual grounding capabilities — but the session froze repeatedly before all records could be entered. Refreshing the browser caused complete context loss. This represents a **current capability boundary** of the AACU tool rather than a reliability data point, and is consistent with Anthropic's own advisory that the Computer Use tool is not recommended for production environments. Notably, the layout changes that typically challenge rule-based RPA bots did not impede the LLM agent, suggesting that visual reasoning is a genuine strength of AACU even where execution stability is not.

### 5.2 H1 — Execution Speed

<!-- CHANGE: Added Cohen's d and 95% CIs (R2-C6) -->
**Table 2.** Welch's t-test results for H1.

| Process | t-statistic | p-value | Cohen's d | 95% CI (mean diff, s) |
|---------|-----------|---------|-----------|-----------------------|
| P2 | −3.384 | 0.0096 | 1.51 | [−93.5, −15.3] |
| P3 | −17.30 | <0.001 | 7.73 | [−202.5, −163.1] |

H1 is **not supported**. RPA was significantly faster than AACU for both processes. The large effect sizes (d = 1.51 for P2, d = 7.73 for P3) confirm that these differences are practically meaningful and not artefacts of the small sample size. The speed disadvantage of AACU is consistent with the theoretical prediction outlined in Section 2.2: iterative screenshot-based perception and LLM inference introduce unavoidable latency at each action step, a bottleneck documented in the broader literature on deployed LLM systems [7].

### 5.3 H2 — Reliability

<!-- CHANGE: P1 removed from Fisher's Exact Test; P3 interpretation expanded (R2-C5, R2-C7) -->
**Table 3.** Fisher's Exact Test results for H2 (P2 and P3 only).

| Process | Odds Ratio | p-value | 95% CI (odds ratio) |
|---------|-----------|---------|---------------------|
| P2 | 0 | 1.000 | [0, ∞] |
| P3 | 0 | 0.087 | [0, 2.08] |

H2 is **not supported** at α = 0.05. RPA achieved 100% success on both processes, while AACU achieved 90% (P2) and 60% (P3). The odds ratios of 0 reflect the fact that RPA had zero failures in both cases, making the ratio undefined in the conventional sense (reported as 0 following Fisher's convention for one-sided tables).

For P2, the p-value of 1.0 indicates no statistical basis for distinguishing reliability, which is unsurprising given that AACU failed only once in 10 runs. For P3, the p-value of 0.087 is close to the conventional significance threshold. Rather than simply accepting the null, we note that the observed difference (100% vs. 60% success) is practically meaningful, and the failure to reach α = 0.05 is likely attributable to limited statistical power at n = 10. A larger sample would be needed to resolve this question definitively. We recommend P3 reliability as a priority for replication.

**Failure mode analysis.** Observed AACU failures can be classified into two categories:

1. **Interface-level failures:** Application freezing, UI non-responsiveness, and session timeouts — particularly in P1 and occasionally in P3. These reflect current tool-level limitations rather than cognitive errors.
2. **Cognitive/planning failures:** Unnecessary invocation of LibreOffice in P3 (when only Gedit was needed), context loss leading to task abandonment, and incorrect action sequencing. These reflect the non-deterministic, generative nature of AACU and are consistent with documented LLM hallucination and planning instability [18–20].

<!-- CHANGE: Failure modes classified into two types (R2-C13) -->

### 5.4 RQ3 — Development Effort (Descriptive)

<!-- CHANGE: H3 removed; replaced with descriptive RQ3 section (R2-C8) -->
**Table 4.** Development time to first successful run.

| Process | RPA (min) | AACU (min) |
|---------|-----------|------------|
| P1 | ≈ 40 | — |
| P2 | ≈ 38 | ≈ 10 |
| P3 | ≈ 240 | ≈ 15 |

Observed development times suggest substantially lower effort for AACU, particularly for P3 where the difference is approximately 16-fold. RPA delays included correcting element selectors (P1: ~15 min), fixing dropdown handling (P2: ~10 min), and learning OCR tooling and output formatting (P3: ~2 hrs). AACU development consisted solely of prompt writing.

These observations are consistent with the theoretical prediction that natural language specification substantially lowers the automation development barrier [1, 12], and align with Ye et al.'s (2023) findings on ProAgent [12]. However, given that measurements are based on a single developer, a single development cycle, and manual timing, **no formal statistical claim is made**. The magnitude of the P3 difference is large enough to be suggestive, but formal validation would require multiple developers, cross-over design, and standardised timing. We recommend this as a direction for future research.

---

## 6. Discussion and Limitations

The results clearly favour RPA in terms of execution speed and reliability on structured, stable benchmark tasks. This is consistent with RPA's over a decade of development and optimisation for exactly these conditions [16, 17]. The speed gap is attributable to fundamental architectural differences: RPA executes pre-compiled action sequences at near-native speed, while AACU incurs LLM inference latency at every step [7]. The reliability gap reflects RPA's determinism versus AACU's probabilistic generation [18–20].

However, the AACU demonstrated notable strengths. Its visual grounding was precise: even in P1, where the form layout changed dynamically, the agent consistently located correct fields — a scenario that would break a naive selector-based RPA bot. Invoice processing in P3 was similarly accurate when the agent succeeded. These results suggest that AACU's flexibility with dynamic and visually complex interfaces is a genuine advantage over rule-based RPA.

The unpredictability of AACU remains its most significant practical limitation. Failure mode analysis (Section 5.3) reveals that failures arise from both interface-level instability (application freezing, session loss) and cognitive instability (unnecessary application launches, context drift). Unlike RPA, which produces interpretable code that facilitates error diagnosis, AACU operates as a black box, making error reproduction and diagnosis substantially harder [18–20]. Additional verification layers may be necessary for production use [21, 22].

<!-- CHANGE: Expanded cost discussion (R2-C9) -->
### 6.1 Cost Considerations

A single execution of P3 cost approximately $0.28 in API token charges, comprising approximately 15,000 input tokens (screenshots + prompt) and 1,500 output tokens per run. This per-run cost structure contrasts with RPA, which has negligible per-run cost after development but significant upfront development investment. For P3, the break-even point — the number of runs at which RPA's lower per-run cost offsets its higher development cost — is roughly in the range of 850 runs (assuming a $25/hr developer rate and the observed 240-minute development time). For lower-frequency automations, or where development cost is the binding constraint, AACU may therefore be economically competitive. We acknowledge that a full Total Cost of Ownership (TCO) analysis would require modelling API pricing fluctuations, concurrent execution scaling, maintenance costs, and failure recovery costs, which is beyond the scope of this study and recommended as future work.

### 6.2 Limitations

<!-- CHANGE: Limitations section expanded (R2-C10, R2-C11) -->
**Benchmark scope.** All tasks were drawn from rpachallenge.com, a benchmark environment rather than a live enterprise deployment. Results may not generalise to tasks with greater complexity, longer workflows, or enterprise-specific interface idiosyncrasies.

**P3 simplification.** P3 was limited to four invoices (first page only) to accommodate AACU context window constraints. This constitutes a systematic simplification that reduces task complexity for both technologies but may disproportionately benefit AACU. Full-challenge P3 performance for AACU is expected to be lower.

**Model version sensitivity.** Results are tied to a specific model version (claude-sonnet-4-20250514, commit 99502f5). AACU capabilities are evolving rapidly; results may not generalise to future model versions. Researchers are encouraged to document model versions with equivalent rigour in replications.

**Single technology.** Only one RPA platform (UiPath) and one AACU tool (Anthropic Computer Use) were tested. Results may differ for other platforms.

**Development time measurement.** Single developer, single cycle, manual timing. Reported figures are indicative only.

**Statistical power.** With n = 10 per process, statistical power is limited. Effect sizes are reported to contextualise findings, but replication with larger samples is recommended.

---

## 7. Conclusion

This study provides one of the first empirical, controlled comparisons between AACU and traditional RPA on standardised benchmark tasks. The key findings are:

1. **Speed:** RPA is significantly faster than AACU on both tested processes, with large effect sizes (Cohen's d = 1.51 and 7.73). H1 is not supported.
2. **Reliability:** RPA achieved 100% success; AACU achieved 90% and 60% on the two processes. Differences are not statistically significant at n = 10, but the P3 gap is practically meaningful. H2 is not supported.
3. **P1 (qualitative):** AACU could not complete the basic RPA Challenge, revealing a current capability boundary related to application stability and context management — despite demonstrating accurate visual grounding.
4. **Development effort (descriptive):** AACU required substantially less development time (≈10 min vs. ≈38 min for P2; ≈15 min vs. ≈240 min for P3), consistent with the theoretical advantage of natural language specification. Formal validation is needed.

**Practical implications.** AACU is not yet ready to replace RPA in high-frequency, mission-critical workflows. However, for low-frequency automations, rapid prototyping, or tasks with dynamic interfaces, AACU presents a compelling alternative — particularly where development cost and speed are the binding constraints. Practitioners should consider a hybrid approach: RPA for stable, high-frequency processes; AACU for flexible, infrequent, or rapidly changing tasks.

**Future directions.** We recommend: (1) replication with larger samples (n ≥ 30) and multiple developers; (2) evaluation on real enterprise processes beyond benchmark tasks; (3) comparison of multiple AACU platforms as they become available; (4) development of granular reliability metrics (field-level accuracy, partial success, error recovery); (5) formal TCO modelling; and (6) exploration of hybrid RPA-AACU architectures.

---

## References

[1] Chakraborti, T., et al.: From Natural Language to Workflows. BPM Forum (2022).
[2] Jansen, J.A., et al.: Leveraging LLMs for data analysis automation. PLoS ONE 20 (2025).
[3] Agostinelli, S., et al.: Towards Intelligent RPA for BPMers. arXiv:2001.00804 (2020).
[4] Wewerka, J., Reichert, M.: RPA — systematic mapping study. Enterprise Information Systems 17 (2023).
[5] Enriquez, J.G., et al.: RPA: Scientific and Industrial Mapping Study. IEEE Access 8 (2020).
[6] Syed, R., et al.: RPA: Contemporary themes and challenges. Computers in Industry 115 (2020).
[7] Hughes, L., et al.: AI Agents and Agentic Systems: A Multi-Expert Analysis. J. Computer Information Systems (2025).
[8] Woo, J.J., et al.: Custom LLMs Improve Accuracy. Arthroscopy 41 (2025).
[9] Martins, A., et al.: Automation techniques for personalized healthcare. Int. J. Medical Informatics 185 (2024).
[10] Samdani, G., et al.: Agentic AI in the Age of Hyper-Automation. WJAETS 8 (2023).
[11] Sapkota, R., et al.: AI Agents vs. Agentic AI. arXiv:2505.10468 (2025).
[12] Ye, Y., et al.: ProAgent: From RPA to Agentic Process Automation. arXiv:2311.10751 (2023).
[13] Lamanna, C.: Announcing computer use in Microsoft Copilot Studio. Microsoft Blog (2024).
[14] Xiong: Invoice Extraction with OCR. GitHub (2024).
[15] RPA Challenge Invoice Extraction in UiPath. Video tutorial (2020).
[16] Willcocks, L.P., et al.: The IT function and robotic process automation. LSE Library (2015).
[17] Syed, R., Wynn, M.T.: RPA: a review of the state-of-the-art. Handbook on BPM and Digital Transformation (2024).
[18] Perković, G., et al.: Hallucinations in LLMs. MIPRO (2024).
[19] Chao, P., et al.: Jailbreaking Black Box LLMs. IEEE SaTML (2025).
[20] Martino, A., et al.: Knowledge Injection to Counter LLM Hallucination. ESWC (2023).
[21] Spiess, C., et al.: Calibration and Correctness of LMs for Code. arXiv:2402.02047 (2024).
[22] Schwartz, S., et al.: Enhancing Trust in LLM-Based AI Automation Agents. arXiv:2308.05391 (2023).
[23] van der Aalst, W.M.P., et al.: Robotic Process Automation. BISE 60 (2018).
[24] Czarnecki, C., Fettke, P. (eds.): Robotic process automation. De Gruyter (2021).
[Derrick] Derrick, B., et al.: The Welch t-test. J. Modern Applied Statistical Methods (2016).
[Agresti] Agresti, A.: Categorical Data Analysis. Wiley (2002).

---

## Appendix 1 — P3 Optimised Prompt

INVOICE DATA EXTRACTION TASK

ENVIRONMENT:
- Web browser (Firefox) with invoice management system
- Text editor (gedit) with example.csv file open

OBJECTIVE: Extract and compile invoice information into a structured CSV format.

DATA EXTRACTION PROCESS: For each invoice record:

INPUT DATA (from web interface):
- Invoice ID (unique identifier)
- Due Date (DD-MM-YYYY format)

EXTRACTION STEPS:
1. Click invoice download button for each ID
2. Open the downloaded invoice document
3. Extract: Invoice Number, Invoice Date (DD-MM-YYYY), Company Name, Total Amount Due

OUTPUT FORMAT (CSV):
ID,DueDate,InvoiceNo,InvoiceDate,CompanyName,TotalDue

SAMPLE: 5jef1y8yx4t8yupbpo3fzg,25-02-2019,10021,13-02-2019,Sit Amet Corp.,1234.40

Enter one complete record per line.