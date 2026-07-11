## **CypherKD rebuttal answers**

### **Reviewer Tb6b: (Soundness: 3 point, Excitement: 3 point, Overall: 3 point)**

**ANSWER:**

We thank the reviewer for the constructive comments. Below, we provide additional baseline implementation details, multi-seed confidence information, and analyses of the proposed supervision signal.

- **The paper lacks some experimental details, especially for baseline implementation. The paper compares with many existing knowledge distillation methods. It does not explain whether these methods use official implementations or the authors' own reimplementations. If the baselines are reimplemented, the paper should provide the implementation details and report whether enough hyperparameter tuning was done.**

    The Baseline Implementation Details table below explicitly states whether each baseline uses the official codebase or our reimplementation, together with the core hyperparameters, tuning ranges, and checkpoint selection strategy.

    | Method    | Source code                           | Key hyperparameters                      | Tuning range                 | Checkpoint |
    |-----------|---------------------------------------|------------------------------------------|------------------------------|------------|
    | FKL / RKL | Code from the paper project on GitHub | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best       |
    | SFKL      | Code from the paper project on GitHub | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best       |
    | DistiLLM  | Code from the paper project on GitHub | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best       |
    | FDD       | Code from the paper project on GitHub | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best       |
    | CSD       | Code from the paper project on GitHub | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best       |
    | AMiD      | Reimplemented from the paper          | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best       |
    | CypherKD  | Ours                                  | kd_ratio ($\beta$), $\lambda_{rel}$      | Both from 0.5 to 1, step 0.1 | Best       |


    For a fair comparison, all methods are trained using the same backbone model, training data, optimizer settings, number of epochs, decoding strategy, and evaluation protocol whenever applicable. We select the best checkpoint for each method using the same validation-based checkpoint-selection protocol, and then evaluate the selected checkpoint on the test set. For all methods, we report the tuned hyperparameters and their search ranges as shown in the table above.

<br>

- **From the experimental results, CypherKD improves a lot over standard supervised fine-tuning. The gains over existing knowledge distillation methods are often small. Some metrics are almost tied. Therefore, I am not sure whether these small gaps come from the proposed method itself or could be closed by hyperparameter tuning. I also suggest that the paper include confidence information or results across multiple runs.**

    Although CypherKD shows clear gains over SFT, some improvements over strong KD baselines are relatively small. To separate method effects from run-to-run variance, we will add results across 5 random seeds and report **mean +/- standard deviation**.

    **CypherBench**

    | Method                 | EX(%)        | PSJS(%)      | Executable(%)|
    |------------------------|-------------:|-------------:|-------------:|
    | **Qwen3 family**       |              |              |              |
    | Qwen3-4B (Teacher)     | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | Qwen3-0.6B (SFT)       | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | RKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | SFKL                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | DistiLLM               | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FDD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | CSD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | AMiD                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | **CypherKD**           | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | **Llama-3.2 family**   |              |              |              |
    | Llama-3.2-8B (Teacher) | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | Llama-3.2-1B (SFT)     | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | RKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | SFKL                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | DistiLLM               | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FDD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | CSD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | AMiD                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | **CypherKD**           | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |

    **Mind-the-Query**

    | Method                 | EX(%)        | PSJS(%)      | Executable(%)|
    |------------------------|-------------:|-------------:|-------------:|
    | **Qwen3 family**       |              |              |              |
    | Qwen3-4B (Teacher)     | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | Qwen3-0.6B (SFT)       | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | RKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | SFKL                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | DistiLLM               | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FDD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | CSD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | AMiD                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | **CypherKD**           | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | **Llama-3.2 family**   |              |              |              |
    | Llama-3.2-8B (Teacher) | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | Llama-3.2-1B (SFT)     | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | RKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | SFKL                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | DistiLLM               | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FDD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | CSD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | AMiD                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | **CypherKD**           | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |

    **Neo4j-Text2Cypher**

    | Method                 | EX(%)        | PSJS(%)      | Executable(%)|
    |------------------------|-------------:|-------------:|-------------:|
    | **Qwen3 family**       |              |              |              |
    | Qwen3-4B (Teacher)     | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | Qwen3-0.6B (SFT)       | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | RKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | SFKL                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | DistiLLM               | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FDD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | CSD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | AMiD                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | **CypherKD**           | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | **Llama-3.2 family**   |              |              |              |
    | Llama-3.2-8B (Teacher) | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | Llama-3.2-1B (SFT)     | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | RKL                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | SFKL                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | DistiLLM               | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | FDD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | CSD                    | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | AMiD                   | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |
    | **CypherKD**           | [MEAN +/- STD] | [MEAN +/- STD] | [MEAN +/- STD] |

<br>

- **The supervision signal in CypherKD comes entirely from the teacher model, without any additional correction or checking mechanism. If the teacher model makes mistakes in these correspondence relations, the extra supervision may transfer this noise to the student model.**

    This is an important concern, but CypherKD does **not** rely entirely on the teacher signal. The student is still trained with the standard cross-entropy loss on the gold Cypher query. The teacher-derived span-relation signal is only used as an auxiliary objective:

    $$\mathcal{L}_{\text{total}} = (1-\beta)\mathcal{L}_{\text{CE}}+ \beta\left(\mathcal{L}_{\text{logit}} + \lambda_{\text{rel}}\mathcal{L}_{\text{rel}}\right)$$

    Therefore, the gold query remains the primary supervision signal, while the teacher provides additional structural guidance. This design reduces the risk that noisy teacher correspondences dominate training.

    To further address this concern, we will add a teacher-noise analysis. Representative examples where the teacher has incorrect execution accuracy but CypherKD recovers the correct execution result are shown below.

    **Case 1: company #5**

    Question: Identify the individuals who have served as CEOs of companies that, at some point, had Norman Welsh as their CEO, and specify the number of such companies for each individual.

    Gold Cypher: `MATCH (n:Person)<-[r0:hasCEO]-(m0:Company)-[r1:hasCEO]->(m1:Person {name: 'Norman Welsh'}) WITH n, count(DISTINCT m0) AS num RETURN n.name, num`

    | Model | EX | Cypher | Behavior |
    |-------|---:|--------|----------|
    | Teacher | 0 | `MATCH (n:Person)-[r0:hasCEO]->(m0:Company)<-[r1:hasCEO]-(m1:Person {name: 'Norman Welsh'}) WITH n, count(DISTINCT m0) AS num RETURN n.name, num` | Reverses both `hasCEO` directions, incorrectly treating `Person` as the source of `hasCEO`. |
    | CypherKD | 1 | `MATCH (n:Person)<-[r0:hasCEO]-(m0:Company)-[r1:hasCEO]->(m1:Person {name: 'Norman Welsh'}) WITH n, count(DISTINCT m0) AS num RETURN n.name, num` | Recovers the gold `Company -> Person` CEO relation pattern. |

    **Case 2: fictional_character #38**

    Question: What are the names and occupations of characters who have Azazel as their father and are also the father of Nocturne?

    Gold Cypher: `MATCH (n:Character)-[r0:hasFather]->(m0:Character {name: 'Azazel'}),(n:Character)<-[r1:hasFather]-(m1:Character {name: 'Nocturne'}) WITH DISTINCT n RETURN n.name, n.occupation`

    | Model | EX | Cypher | Behavior |
    |-------|---:|--------|----------|
    | Teacher | 0 | `MATCH (n:Character)-[r0:hasFather]->(m0:Character {name: 'Azazel'}),(n:Character)-[r1:hasStudent]->(m1:Character {name: 'Nocturne'}) WITH DISTINCT n RETURN n.name, n.occupation` | Uses the wrong relation `hasStudent` for the Nocturne constraint. |
    | CypherKD | 1 | `MATCH (n:Character)-[r0:hasFather]->(m0:Character {name: 'Azazel'}),(n:Character)<-[r1:hasFather]-(m1:Character {name: 'Nocturne'}) WITH DISTINCT n RETURN n.name, n.occupation` | Recovers the gold father-child relation and direction. |

    **Case 3: movie #14**

    Question: What are the names of the genres associated with Creed III, and how many movies belong to each of those genres?

    Gold Cypher: `MATCH (n:Genre)<-[r1:hasGenre]-(m1:Movie {name: 'Creed III'}) OPTIONAL MATCH (n:Genre)<-[r0:hasGenre]-(m0:Movie) WITH n, count(DISTINCT m0) AS num RETURN n.name, num`

    | Model | EX | Cypher | Behavior |
    |-------|---:|--------|----------|
    | Teacher | 0 | `MATCH (n:Genre)<-[r0:hasGenre]-(m0:Movie {name: 'Creed III'}) WITH n, count(DISTINCT m0) AS num RETURN n.name, num` | Finds the genre of `Creed III` but drops the `OPTIONAL MATCH` needed to count all movies in each genre. |
    | CypherKD | 1 | `MATCH (n:Genre)<-[r1:hasGenre]-(m1:Movie {name: 'Creed III'}) OPTIONAL MATCH (n:Genre)<-[r0:hasGenre]-(m0:Movie) WITH n, count(DISTINCT m0) AS num RETURN n.name, num` | Recovers the full gold query with the optional counting path. |

<br>

- **The main problem addressed by this method is that student models may fail to learn detailed structural correspondences between the input and output in Text-to-Cypher. The paper does not provide detailed analysis of this specific problem. It is still unclear whether the extra loss term and the corresponding supervision signal actually alleviate this learning difficulty.**

    To examine this issue more directly, we add a rule-based error analysis based on two grouped categories from the CypherBench [1] taxonomy that are closely related to span–context grounding:

    * **Schema grounding:** incorrect entity labels, relationship types, properties, entity linking, or other schema violations.
    * **Graph-pattern construction:** incorrect relationship directions or graph patterns that do not align with the question.

    Specifically, we implement a rule-based analysis script that compares each predicted Cypher query with the corresponding gold query. The script extracts schema elements and graph patterns from both queries and detects mismatches associated with the two error groups above. We then report the percentage of test examples containing each type of error.

    | Method             | Schema grounding (%) | Graph-pattern construction (%) |
    | ------------------ | -------------------: | -----------------------------: |
    | Qwen3-4B (Teacher) |                10.99 |                          20.40 |
    | Qwen3-0.6B (SFT)   |                43.44 |                          40.84 |
    | CSD                |                26.62 |                          32.45 |
    | DistiLLM           |                27.13 |                          31.60 |
    | **CypherKD**       |            **24.23** |                      **29.22** |

    CypherKD has the lowest error rates among the student and distillation methods in both categories. Compared with SFT, its schema-grounding error rate decreases from **43.44% to 24.23%**, while its graph-pattern construction error rate decreases from **40.84% to 29.22%**. CypherKD also shows moderately lower error rates than CSD and DistiLLM.

    These results are consistent with the intended effect of the proposed span-relation objective: encouraging the student to better preserve the teacher’s correspondence between Cypher spans and the question-schema context. In particular, the larger difference in schema-grounding errors suggests that the objective may help the student identify the entity labels, relationship types, and properties associated with each output span.

    However, because this analysis relies on rule-based matching, it may not capture all semantic equivalences or structurally different but execution-equivalent queries. We therefore treat these results as supporting evidence that CypherKD alleviates structural correspondence errors, rather than as a definitive measurement of every grounding or graph-construction error.

[1] Yanlin Feng, Simone Papicchio, and Sajjadur Rahman. 2025. Cypherbench: Towards precise retrieval over full-scale modern knowledge graphs in the LLM era. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2025, Vienna, Austria, July 27 - August 1, 2025, pages 8934–8958. Association for Computational Linguistics. 

<br>

- **I suggest that the authors add a robustness analysis for the rule-based span extraction method. For example, they could discuss when this method may fail under different Cypher structures and how to test its robustness more carefully**

     We sincerely thank the reviewer for this suggestion. Our span extraction is implemented using deterministic rules derived from the Cypher syntax:

    - Clause spans are identified by matching predefined Cypher clause keywords.
    - Node spans are extracted from parenthesized structures that satisfy Cypher node syntax (e.g., labels, properties, or variables adjacent to relationships).
    - Triplet spans are extracted using structural patterns that capture relationship chains.
    - Expression spans are obtained from the expressions following clauses such as WHERE, WITH, RETURN, and ORDER BY.

    These rules are not intended to cover every possible Cypher construct. Failure cases may arise for highly complex queries, such as nested subqueries (EXISTS { ... }), variable-length paths (-[*1..3]-), or other uncommon language constructs, where the extracted span boundaries may be incomplete, missing, or slightly inaccurate.

    Nevertheless, our rule extractor is designed to provide weak structural supervision rather than a complete Cypher parser. Therefore, perfect span extraction is not required for the proposed span-level distillation objective to be effective. While a small number of extracted spans may be noisy or missing, the majority of spans in standard Cypher queries are correctly identified and continue to provide informative structural alignment between the teacher and student. Consequently, occasional extraction errors behave as annotation noise rather than systematic supervision errors, and do not substantially reduce the effectiveness of the proposed span-level distillation.



