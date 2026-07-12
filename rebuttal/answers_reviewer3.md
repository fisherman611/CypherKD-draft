## **CypherKD rebuttal answers**

### **Reviewer mATV: (Soundness: 4 point, Excitement: 3.5 point, Overall: 3 point)**

**ANSWER:**

- **In the Related Work section (Section 2.1), the paper points out that existing Text-to-Cypher generation remains difficult mainly due to the lack of modeling span-to-context grounding in Cypher queries. However, Text-to-SQL and Text-to-Cypher share high structural similarity—both require aligning natural language questions with structured schemas (relational schema vs. property graph schema) and generating structured query languages. This paper lacks discussion of relevant advances in Text-to-SQL and the extent to which Text-to-SQL methods can be transferred to Text-to-Cypher. If they cannot be transferred, what are the Cypher-specific challenges?**

    We thank the reviewer for this valuable suggestion. We agree that the connection between Text-to-SQL and Text-to-Cypher should be discussed more explicitly, and we will expand the Related Work accordingly.

Text-to-SQL and Text-to-Cypher share the core challenge of grounding natural-language questions in a structured schema before generating an executable query. Recent Text-to-SQL methods can be broadly categorized into black-box approaches, which leverage synthetic data, rationales, query plans, or execution feedback, and white-box approaches, which perform knowledge distillation through token-level teacher supervision or learning from imperfect SQL data [1–7].

Many of these ideas are transferable to Text-to-Cypher, including synthetic-data distillation, rationale distillation, query-plan supervision, execution-feedback learning, and token-level knowledge distillation. However, Cypher introduces graph-specific challenges such as relationship directions, variable bindings, multi-hop graph patterns, and path semantics, which require modeling structural correspondences beyond token-level supervision. To address these challenges, CypherKD extends conventional knowledge distillation with a span-relation objective that explicitly aligns semantic Cypher spans with the question-schema context.

To further demonstrate that the proposed span-relation objective is not limited to Cypher, we additionally evaluate it on Spider by replacing the Cypher-specific span extractor with a SQL-specific one while keeping the distillation objective unchanged. The proposed objective consistently improves SRKL by +1.4 EX and +1.2 EM, suggesting that the framework generalizes beyond Text-to-Cypher, although its motivation is particularly compelling for graph query generation.


    | Method               | EX           | EM           |
    |----------------------|-------------:|-------------:|
    | Qwen3-4B (Teacher)   | 77.4         | 69.0         |
    | Qwen3-0.6B (SFT)     | 62.5         | 57.9         |
    | SRKL                 | 65.2         | 58.7         |
    | SRKL + Proposed loss | 66.6         | 59.9         |

[1] Hoang et al. 2025. Distill-C: Enhanced NL2SQL via Distilled Customization with LLMs. NAACL Industry Track

[2] Rossiello et al. 2025. Rationalization Models for Text-to-SQL. ICLR Workshop on Reasoning and Planning for LLMs

[3] He et al. 2025. STaR-SQL: Self-Taught Reasoner for Text-to-SQL. ACL

[4] Zhu et al. 2025. Text2Sql: Pure Fine-Tuning and Pure Knowledge Distillation. NAACL Industry Track

[5] Zhong et al. 2024. Learning from Imperfect Data: Towards Efficient Knowledge Distillation of Autoregressive Language Models for Text-to-SQL. Findings of EMNLP

[6] Thaker and Bresler. 2025. Knowledge Distillation with Structured Chain-of-Thought for Text-to-SQL. arXiv

[7] Hoang et al. 2026. FINER-SQL: Boosting Small Language Models for Text-to-SQL. arXiv

 


<br>

- **Comparison of total training time: Although it is reported that CypherKD's step time increases by approximately 8%, are the total training steps or number of convergence steps the same as other methods? If the convergence speed differs, step time cannot fully reflect the total overhead. Has the additional overhead of generating student queries in the mixed data been accounted for?**

    We thank the reviewer for this suggestion. We agree that step time alone does not fully characterize the training overhead. Since all methods use the same batch size, training schedule, and checkpoint-selection protocol, we will additionally report time per epoch to capture the end-to-end training cost. We will also clarify that the additional overhead from generating student queries for the mixed data is included in the reported training cost when the mixed data are generated during training.

    | Method                          | Time/epoch (s) |
    |---------------------------------|---------------:|
    | RKL                             | 638.55         |
    | RKL w/ $\mathcal{L}_{rel}$      | 668.92         |
    | SFKL                            | 624.10         |
    | SFKL w/ $\mathcal{L}_{rel}$     | 653.19         |
    | CSD                             | 593.44         |
    | CSD w/ $\mathcal{L}_{rel}$      | 642.13         |
    | DistiLLM                        | 675.82         |
    | DistiLLM w/ $\mathcal{L}_{rel}$ | 724.49         |


    Importantly, the reported time per epoch includes the cost of generating student queries for constructing the mixed data during training. Compared with the corresponding baselines, adding $\mathcal{L}_{rel}$ increases the end-to-end training time by only 4.7–8.2% per epoch, consistent with the previously reported per-step overhead.

We also analyze the training dynamics by reporting the development loss and Exact Match after each epoch. Both the baselines and their relation-grounding variants exhibit nearly identical convergence patterns, with rapid improvement during the first three epochs followed by clear performance saturation in epochs 4–5. Therefore, the proposed objective does not require additional optimization steps or training epochs to reach convergence, indicating that the modest increase in wall-clock time per epoch closely reflects the overall end-to-end training overhead.


    **Training loss**

    | Method | E1 | E2 | E3 | E4 | E5 |
    |---|---:|---:|---:|---:|---:|
    | RKL | 0.0195 | 0.0090 | 0.0070 | 0.0059 | 0.0058 |
    | RKL + $\mathcal{L}_{rel}$ | 0.0167 | 0.0086 | 0.0065 | 0.0058 | 0.0057 |
    | SFKL | 0.0097 | 0.0057 | 0.0049 | 0.0046 | 0.0045 |
    | SFKL + $\mathcal{L}_{rel}$ | 0.0109 | 0.0061 | 0.0052 | 0.0048 | 0.0048 |
    | CSD | 0.0187 | 0.0093 | 0.0062 | 0.0058 | 0.0057 |
    | CSD + $\mathcal{L}_{rel}$ | 0.0164 | 0.0085 | 0.0059 | 0.0054 | 0.0054 |
    | DistiLLM | 0.0101 | 0.0057 | 0.0047 | 0.0045 | 0.0045 |
    | DistiLLM + $\mathcal{L}_{rel}$ | 0.0099 | 0.0059 | 0.0052 | 0.0047 | 0.0046 |

**Development Exact Match (%)**

    | Method | E1 | E2 | E3 | E4 | E5 |
    |---|---:|---:|---:|---:|---:|
    | RKL | 83.30 | 90.51 | 92.56 | 93.03 | 93.44 |
    | RKL + $\mathcal{L}_{rel}$ | 84.18 | 91.56 | 92.38 | 92.79 | 92.97 |
    | SFKL | 89.63 | 92.62 | 93.44 | 94.08 | 94.08 |
    | SFKL + $\mathcal{L}_{rel}$ | 88.28 | 92.85 | 92.91 | 93.97 | 94.02 |
    | CSD | 83.42 | 90.57 | 92.50 | 93.09 | 93.50 |
    | CSD + $\mathcal{L}_{rel}$ | 84.48 | 90.92 | 92.62 | 92.97 | 93.38 |
    | DistiLLM | 89.10 | 92.21 | 93.61 | 94.43 | 94.49 |
    | DistiLLM + $\mathcal{L}_{rel}$ | 90.10 | 92.74 | 93.32 | 93.97 | 94.14 |


<br>

- **The authors specifically ablate triplet spans rather than the other three span types, possibly based on the assumption that triplets (source node-relationship-target node) are the most essential syntactic structure that distinguishes graph queries from relational SQL. The experiments also confirm their critical role (EX drops by 4.43 percentage points after removal). However, for completeness, suggest providing separate ablation results for the other three span types (clause, node pattern, expression) in the appendix or supplementary material, so that readers can understand the contribution of each span type.**

    We thank the reviewer for this suggestion. Ablating only triplet spans does not fully reveal the contribution of each span type. We therefore conduct separate ablations for clause, node-pattern, triplet, and expression spans and will include the complete results in the appendix.

    **CypherBench**

    | Method                        | EX (%)    | PSJS (%)  |
    |-------------------------------|----------:|----------:|
    | CypherKD                      | **64.61** | **61.42** |
    | CypherKD w/o triplet spans    |     60.18 |     56.44 |
    | CypherKD w/o node spans       |     61.97 |     58.39 |
    | CypherKD w/o clause spans     |     61.58 |     58.56 |
    | CypherKD w/o expression spans |     61.29 |     57.72 |

    **Mind-the-Query**

    | Method                        | EX (%)    | PSJS (%)  |
    |-------------------------------|----------:|----------:|
    | CypherKD                      | **29.93** | **35.95** |
    | CypherKD w/o triplet spans    |     26.92 |     32.10 |
    | CypherKD w/o node spans       |     26.28 |     33.55 |
    | CypherKD w/o clause spans     |     27.17 |     34.43 |
    | CypherKD w/o expression spans |     27.79 |     34.91 |

    These results show that all four span types contribute to performance, as removing any span type consistently degrades both EX and PSJS across the two benchmarks. On CypherBench, triplet spans have the largest impact, supporting our motivation that graph triplets capture essential graph-specific relational structure. On Mind-the-Query, however, the most influential span type depends on the evaluation metric: removing node-pattern spans causes the largest EX drop, whereas removing triplet spans causes the largest PSJS drop. These findings indicate that the four span types provide complementary structural information, and that their relative importance varies across benchmarks.

<br>

- **There is a lack of error analysis. Suggest supplementing with statistical comparisons of error query types generated by CypherKD versus baselines before and after distillation, qualitatively demonstrating the reduction of "syntactically correct but grounding-incorrect" errors. This would help support the core argument that "span-context grounding improves semantic correctness."**

    We thank the reviewer for this suggestion. We add both quantitative and qualitative error analyses on CypherBench [8]. Following the CypherBench taxonomy, we focus on two error groups directly related to span-context grounding: (1) **schema grounding**, which includes incorrect entity labels, relationship types, properties, entity linking, and other schema violations; and (2) **graph-pattern construction**, which includes incorrect relationship directions and graph patterns that do not align with the question. We implement a rule-based analyzer that compares each predicted query against the corresponding gold query and reports the percentage of test examples exhibiting each error type.

    | Method             | Schema grounding (%) | Graph-pattern construction (%) |
    |--------------------|---------------------:|--------------------------------:|
    | Qwen3-4B (Teacher) |                10.99 |                           20.40 |
    | Qwen3-0.6B (SFT)   |                43.44 |                           40.84 |
    | CSD                |                26.62 |                           32.45 |
    | DistiLLM           |                27.13 |                           31.60 |
    | **CypherKD**       |            **24.23** |                       **29.22** |

    Compared with the SFT student, CypherKD reduces schema-grounding errors from **43.44% to 24.23%** (19.21 percentage points) and graph-pattern construction errors from **40.84% to 29.22%** (11.62 percentage points). It also yields lower error rates than CSD and DistiLLM in both categories. The following examples illustrate cases in which all student predictions are syntactically valid and executable, but only CypherKD recovers the correct grounding exhibited by the teacher.

    **Case 1: Schema-grounding error (flight_accident)**

    Question: Which aircraft model is longer, the Dash 7 or the Bell 206?

    Gold Cypher: `MATCH (n:AircraftModel {name: 'Dash 7'}), (m0:AircraftModel {name: 'Bell 206'}) RETURN CASE WHEN n.length_metre > m0.length_metre THEN n.name ELSE m0.name END AS answer`

    | Model | EX | Executable | Cypher | Behavior |
    |-------|---:|-----------:|--------|----------|
    | Teacher | 1 | 1 | `MATCH (n:AircraftModel {name: 'Dash 7'}), (m0:AircraftModel {name: 'Bell 206'}) RETURN CASE WHEN n.length_metre > m0.length_metre THEN n.name ELSE m0.name END AS answer` | Correctly grounds "longer" to the `length_metre` property. |
    | SFT | 0 | 1 | `MATCH (n:AircraftModel {name: 'Dash 7'}), (m0:AircraftModel {name: 'Bell 206'}) RETURN CASE WHEN n.long_metre > m0.long_metre THEN n.name ELSE m0.name END AS answer` | Invents the property `long_metre`. |
    | CSD | 0 | 1 | `MATCH (n:AircraftModel {name: 'Dash 7'}), (m0:AircraftModel {name: 'Bell 206'}) RETURN CASE WHEN n.range_km > m0.range_km THEN n.name ELSE m0.name END AS answer` | Grounds "longer" to the wrong property, `range_km`. |
    | DistiLLM | 0 | 1 | `MATCH (n:AircraftModel {name: 'Dash 7'}), (m0:AircraftModel {name: 'Bell 206'}) RETURN CASE WHEN n.range_km > m0.range_km THEN n.name ELSE m0.name END AS answer` | Grounds "longer" to the wrong property, `range_km`. |
    | **CypherKD** | **1** | **1** | `MATCH (n:AircraftModel {name: 'Dash 7'}), (m0:AircraftModel {name: 'Bell 206'}) RETURN CASE WHEN n.length_metre > m0.length_metre THEN n.name ELSE m0.name END AS answer` | Recovers the correct question-to-property alignment. |

    **Case 2: Graph-pattern construction error (company)**

    Question: What are the names of companies that have had a board member at any time, sorted by their launch year from the most recent to the oldest?

    Gold Cypher: `MATCH (n:Company)-[r0:hasBoardMember]->(m0:Person) WITH DISTINCT n RETURN n.name ORDER BY n.launch_year DESC`

    | Model | EX | Executable | Cypher | Behavior |
    |-------|---:|-----------:|--------|----------|
    | Teacher | 1 | 1 | `MATCH (n:Company)-[r0:hasBoardMember]->(m0:Person) WITH DISTINCT n RETURN n.name ORDER BY n.launch_year DESC` | Correctly represents the `Company -> Person` direction of `hasBoardMember`. |
    | SFT | 0 | 1 | `MATCH (n:Company)<-[r0:hasBoardMember]-(m0:Person) WITH DISTINCT n RETURN n.name ORDER BY n.launch_year DESC` | Reverses the relationship direction. |
    | CSD | 0 | 1 | `MATCH (n:Company)<-[r0:hasBoardMember]-(m0:Person) WITH DISTINCT n RETURN n.name ORDER BY n.launch_year DESC` | Reverses the relationship direction. |
    | DistiLLM | 0 | 1 | `MATCH (n:Company)<-[r0:hasBoardMember]-(m0:Person) WITH DISTINCT n RETURN n.name ORDER BY n.launch_year DESC` | Reverses the relationship direction. |
    | **CypherKD** | **1** | **1** | `MATCH (n:Company)-[r0:hasBoardMember]->(m0:Person) WITH DISTINCT n RETURN n.name ORDER BY n.launch_year DESC` | Recovers the correct graph direction and matches the gold query. |

    These cases separate syntactic validity from semantic correctness: SFT, CSD, and DistiLLM all produce executable Cypher, yet their queries are grounded to the wrong property or relationship direction. CypherKD preserves the teacher's correct span-to-context correspondences and produces execution-correct queries. Together with the full-test error-rate reductions, this provides direct evidence that span-context grounding improves semantic correctness rather than merely increasing query executability. Because the aggregate analysis relies on rule-based matching, we treat it as supporting evidence rather than a complete measure of all semantically equivalent Cypher formulations.

[8] Feng et al. 2025. CypherBench: Towards Precise Retrieval over Full-Scale Modern Knowledge Graphs in the LLM Era. ACL



