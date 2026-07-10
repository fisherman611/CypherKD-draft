## **CypherKD rebuttal answers**

### **Reviewer mATV: (Soundness: 4 point, Excitement: 3.5 point, Overall: 3 point)**

**ANSWER:**

- **In the Related Work section (Section 2.1), the paper points out that existing Text-to-Cypher generation remains difficult mainly due to the lack of modeling span-to-context grounding in Cypher queries. However, Text-to-SQL and Text-to-Cypher share high structural similarity—both require aligning natural language questions with structured schemas (relational schema vs. property graph schema) and generating structured query languages. This paper lacks discussion of relevant advances in Text-to-SQL and the extent to which Text-to-SQL methods can be transferred to Text-to-Cypher. If they cannot be transferred, what are the Cypher-specific challenges?**

    Thank you for the comment. We agree that Text-to-SQL is closely related to Text-to-Cypher, and we will expand the Related Work section accordingly. Recent Text-to-SQL methods can be broadly grouped into black-box and white-box directions. In the black-box setting, methods such as Distill-C use LLM-generated and filtered customization data for NL2SQL, while Rationalization Models and STaR-SQL use rationale- or reasoning-based supervision. Struct-SQL distills structured chain-of-thought query plans, and FINER-SQL uses fine-grained execution feedback and reward optimization. In the white-box setting, Text2Sql: Pure Fine-Tuning and Pure Knowledge Distillation studies prompt-purity-based fine-tuning and distillation, while KID improves distillation by learning from imperfect SQL data.

    These methods are relevant because their core ideas can be adapted to Text-to-Cypher: synthetic-data distillation, rationale distillation, query-plan supervision, execution feedback, and token-level teacher distribution matching can all provide useful supervision signals. However, adapting them to Cypher requires handling graph-specific structures such as relationship directions, graph patterns, variable bindings, and multi-hop topology. Most existing Text-to-SQL distillation methods are black-box approaches, while the white-box methods mainly operate at the token-distribution level. CypherKD extends this direction by adding span-relation distillation, which explicitly aligns Cypher spans with the question/schema context.

    To further demonstrate that the proposed idea can generalize beyond Cypher, we will add an additional Text-to-SQL experiment on Spider:

    | Method               | EX           | EM           |
    |----------------------|-------------:|-------------:|
    | Qwen3-4B (Teacher)   | [MEAN ± STD] | [MEAN ± STD] |
    | Qwen3-0.6B (SFT)     | [MEAN ± STD] | [MEAN ± STD] |
    | SRKL                 | [MEAN ± STD] | [MEAN ± STD] |
    | SRKL + Proposed loss | [MEAN ± STD] | [MEAN ± STD] |


<br>

- **Comparison of total training time: Although it is reported that CypherKD's step time increases by approximately 8%, are the total training steps or number of convergence steps the same as other methods? If the convergence speed differs, step time cannot fully reflect the total overhead. Has the additional overhead of generating student queries in the mixed data been accounted for?**

<br>

- **The authors specifically ablate triplet spans rather than the other three span types, possibly based on the assumption that triplets (source node-relationship-target node) are the most essential syntactic structure that distinguishes graph queries from relational SQL. The experiments also confirm their critical role (EX drops by 4.43 percentage points after removal). However, for completeness, suggest providing separate ablation results for the other three span types (clause, node pattern, expression) in the appendix or supplementary material, so that readers can understand the contribution of each span type.**

    Thank you for the helpful suggestion. We agree that ablating only triplet spans does not fully show the contribution of each span type. In the revision, we will include separate ablations for clause, node-pattern, triplet, and expression spans in the appendix. We already have the triplet-span ablation and are currently running the other three ablations.

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
    | CypherKD w/o node spans       | [RUNNING] | [RUNNING] |
    | CypherKD w/o clause spans     | [RUNNING] | [RUNNING] |
    | CypherKD w/o expression spans | [RUNNING] | [RUNNING] |

    This additional ablation will make the role of each span inventory explicit and help verify whether triplets are uniquely important or whether other Cypher span types also provide complementary grounding signals.

<br>

- **There is a lack of error analysis. Suggest supplementing with statistical comparisons of error query types generated by CypherKD versus baselines before and after distillation, qualitatively demonstrating the reduction of "syntactically correct but grounding-incorrect" errors. This would help support the core argument that "span-context grounding improves semantic correctness."**
