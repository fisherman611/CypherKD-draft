## **CypherKD rebuttal answers**

### **Reviewer Tb6b: (Soundness: 3 point, Excitement: 3 point, Overall: 3 point)**

**ANSWER:**

We thank the reviewer for the constructive comments. Below, we provide additional baseline implementation details, multi-seed confidence information, and analyses of the proposed supervision signal.

- **The paper lacks some experimental details, especially for baseline implementation. The paper compares with many existing knowledge distillation methods. It does not explain whether these methods use official implementations or the authors' own reimplementations. If the baselines are reimplemented, the paper should provide the implementation details and report whether enough hyperparameter tuning was done.**

    We thank the reviewer for pointing this out. We will add the following table to the revised paper, indicating whether each method uses the official implementation or our reimplementation, together with the tuned hyperparameters and checkpoint selection protocol.

    | Method    | Source code                           | Key hyperparameters                      | Tuning range                 | Checkpoint |
    |-----------|---------------------------------------|------------------------------------------|------------------------------|------------|
    | FKL / RKL | Official implementation | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best validation       |
    | SFKL      | Official implementation | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best validation       |
    | DistiLLM  | Official implementation | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best validation       |
    | FDD       | Reimplemented from the paper | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best validation       |
    | CSD       | Reimplemented from the paper | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best validation       |
    | AMiD      | Official implementation | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Best validation       |
    | CypherKD  | Ours                                  | kd_ratio ($\beta$), $\lambda_{rel}$      | Both from 0.5 to 1, step 0.1 | Best       |


    For a fair comparison, all methods are trained using the same backbone model, training data, optimizer settings, number of epochs, decoding strategy, and evaluation protocol whenever applicable. The best checkpoint was determined using an identical validation protocol before undergoing final evaluation on the test set. For all methods, we report the tuned hyperparameters and their search ranges as shown in the table above.

<br>

- **From the experimental results, CypherKD improves a lot over standard supervised fine-tuning. The gains over existing knowledge distillation methods are often small. Some metrics are almost tied. Therefore, I am not sure whether these small gaps come from the proposed method itself or could be closed by hyperparameter tuning. I also suggest that the paper include confidence information or results across multiple runs.**

    We acknowledge that some gains over strong KD baselines are modest. To ensure a fair comparison, we add the standard deviations over five random seeds, computed under the same training and evaluation protocol. Following the evaluation protocol adopted by AMiD (Shin et al., ICLR 2026), we report statistics over five random seeds on the main benchmarks to assess training stability while keeping the computational cost manageable. 

As shown above, CypherKD consistently achieves the highest mean EX and PSJS across both model families. Importantly, all methods are trained and tuned only on CypherBench, while Mind-the-Query and Neo4j-Text2Cypher are evaluated without any additional fine-tuning or dataset-specific hyperparameter tuning. Moreover, on CypherBench and Mind-the-Query, the improvements over the strongest KD baselines generally exceed the observed run-to-run variation. These results suggest that the gains are unlikely to be explained by favorable hyperparameter choices or optimization noise, but instead reflect the effectiveness and generalization of the proposed supervision.


    **CypherBench**

    | Method                 | EX(%)        | PSJS(%)      | Executable(%)|
    |------------------------|-------------:|-------------:|-------------:|
    | **Qwen3 family**       |              |              |              |
    | FKL                    | 58.26 +/- 0.24 | 54.93 +/- 0.46 | 98.25 +/- 0.20 |
    | RKL                    | 61.24 +/- 0.20 | 58.46 +/- 0.33 | 98.47 +/- 0.21 |
    | SFKL                   | 60.26 +/- 0.31 | 56.77 +/- 0.20 | 97.61 +/- 0.16 |
    | DistiLLM               | 62.18 +/- 0.31 | 58.03 +/- 0.09 | 98.51 +/- 0.07 |
    | FDD                    | 56.43 +/- 0.16 | 53.11 +/- 0.05 | 98.68 +/- 0.15 |
    | CSD                    | 61.58 +/- 0.23 | 59.55 +/- 0.35 | 99.06 +/- 0.11 |
    | AMiD                   | 60.39 +/- 0.18 | 57.81 +/- 0.16 | 98.47 +/- 0.19 |
    | **CypherKD**           | 64.61 +/- 0.43 | 61.42 +/- 0.36 | 98.98 +/- 0.17 |
    | **Llama-3.2 family**   |              |              |              |
    | FKL                    | 57.88 +/- 0.09 | 55.23 +/- 0.08 | 96.85 +/- 0.24 |
    | RKL                    | 58.09 +/- 0.12 | 55.33 +/- 0.23 | 97.02 +/- 0.27 |
    | SFKL                   | 58.22 +/- 0.21 | 55.29 +/- 0.30 | 97.87 +/- 0.03 |
    | DistiLLM               | 58.77 +/- 0.36 | 56.96 +/- 0.10 | 98.30 +/- 0.03 |
    | FDD                    | 54.13 +/- 0.33 | 51.69 +/- 0.29 | 95.78 +/- 0.18 |
    | CSD                    | 60.09 +/- 0.45 | 57.98 +/- 0.34 | 98.17 +/- 0.15 |
    | AMiD                   | 57.20 +/- 0.18 | 54.69 +/- 0.22 | 98.25 +/- 0.12 |
    | **CypherKD**           | 62.11 +/- 0.26 | 58.81 +/- 0.02 | 98.54 +/- 0.21 |

    **Mind-the-Query**

    | Method                 | EX(%)        | PSJS(%)      | Executable(%)|
    |------------------------|-------------:|-------------:|-------------:|
    | **Qwen3 family**       |              |              |              |
    | FKL                    | 27.67 +/- 0.86 | 34.39 +/- 0.13 | 86.51 +/- 0.09 |
    | RKL                    | 26.46 +/- 0.83 | 33.28 +/- 0.12 | 87.53 +/- 0.08 |
    | SFKL                   | 27.45 +/- 0.93 | 33.87 +/- 0.17 | 84.57 +/- 0.03 |
    | DistiLLM               | 27.36 +/- 0.45 | 33.24 +/- 0.11 | 86.32 +/- 0.44 |
    | FDD                    | 12.17 +/- 0.91 | 13.02 +/- 0.21 | 88.17 +/- 0.08 |
    | CSD                    | 25.80 +/- 1.02 | 31.72 +/- 0.32 | 88.85 +/- 0.15 |
    | AMiD                   | 26.12 +/- 0.82 | 32.34 +/- 0.12 | 85.86 +/- 0.11 |
    | **CypherKD**           | 29.93 +/- 0.80 | 35.95 +/- 0.08 | 89.39 +/- 0.18 |
    | **Llama-3.2 family**   |              |              |              |
    | FKL                    | 25.66 +/- 0.93 | 28.79 +/- 0.09 | 88.58 +/- 0.09 |
    | RKL                    | 25.33 +/- 0.87 | 28.77 +/- 0.09 | 88.82 +/- 0.08 |
    | SFKL                   | 24.62 +/- 1.00 | 28.67 +/- 0.15 | 91.16 +/- 0.05 |
    | DistiLLM               | 22.62 +/- 0.46 | 26.48 +/- 0.11 | 91.44 +/- 0.44 |
    | FDD                    | 9.56 +/- 0.96  | 10.51 +/- 0.21 | 84.91 +/- 0.05 |
    | CSD                    | 20.61 +/- 1.13 | 24.42 +/- 0.31 | 91.09 +/- 0.14 |
    | AMiD                   | 24.00 +/- 0.88 | 27.59 +/- 0.10 | 89.87 +/- 0.11 |
    | **CypherKD**           | 27.09 +/- 0.86 | 31.13 +/- 0.07 | 92.28 +/- 0.18 |

    **Neo4j-Text2Cypher**

    | Method                 | EX(%)        | PSJS(%)      | Executable(%)|
    |------------------------|-------------:|-------------:|-------------:|
    | **Qwen3 family**       |              |              |              |
    | FKL                    | 7.98 +/- 0.59  | 15.49 +/- 0.81 | 82.71 +/- 0.82  |
    | RKL                    | 9.51 +/- 0.61  | 29.54 +/- 1.51 | 81.70 +/- 1.08  |
    | SFKL                   | 8.22 +/- 0.19  | 28.32 +/- 1.30 | 77.57 +/- 0.57  |
    | FDD                    | 7.29 +/- 0.80  | 20.64 +/- 1.42 | 87.98 +/- 1.09  |
    | DistiLLM               | 8.99 +/- 0.55  | 26.35 +/- 0.46 | 76.23 +/- 0.76  |
    | CSD                    | 9.15 +/- 0.27  | 27.61 +/- 0.57 | 82.06 +/- 0.79  |
    | AMiD                   | 8.79 +/- 0.14  | 26.84 +/- 0.63 | 77.09 +/- 0.93  |
    | **CypherKD**           | 9.84 +/- 0.55  | 30.26 +/- 0.84 | 85.63 +/- 0.89  |
    | **Llama-3.2 family**   |              |              |              |
    | FKL                    | 9.68 +/- 0.92  | 24.49 +/- 1.23 | 83.68 +/- 1.02  |
    | RKL                    | 9.23 +/- 0.70  | 24.23 +/- 1.10 | 83.56 +/- 1.01  |
    | SFKL                   | 8.87 +/- 0.72  | 22.97 +/- 1.20 | 90.28 +/- 0.90  |
    | FDD                    | 7.69 +/- 0.91  | 19.97 +/- 1.48 | 83.08 +/- 0.97  |
    | DistiLLM               | 9.03 +/- 0.45  | 25.74 +/- 0.94 | 87.85 +/- 1.14  |
    | CSD                    | 9.55 +/- 0.78  | 26.07 +/- 1.44 | 91.21 +/- 1.03  |
    | AMiD                   | 9.51 +/- 0.71  | 22.60 +/- 1.07 | 90.04 +/- 0.99  |
    | **CypherKD**           | 9.88 +/- 0.71  | 26.03 +/- 1.00 | 91.17 +/- 1.08  |





<br>

- **The supervision signal in CypherKD comes entirely from the teacher model, without any additional correction or checking mechanism. If the teacher model makes mistakes in these correspondence relations, the extra supervision may transfer this noise to the student model.**

    We thank the reviewer for this concern. We respectfully clarify that CypherKD does not blindly copy the teacher's internal representations, and its training design inherently mitigates the transfer of teacher noise. The student is still trained with the standard cross-entropy loss on the gold Cypher query. The teacher-derived span-relation signal is only used as an auxiliary objective:

    $$\mathcal{L}_{\text{total}} = (1-\beta)\mathcal{L}_{\text{CE}}+ \beta\left(\mathcal{L}_{\text{logit}} + \lambda_{\text{rel}}\mathcal{L}_{\text{rel}}\right)$$

    Thus, the optimization remains anchored to the gold target, while the teacher provides complementary structural guidance. To further examine this issue, we analyze representative cases where the teacher produces an incorrect query but CypherKD recovers the correct execution result. As shown below, CypherKD can recover from teacher errors such as incorrect relationship directions, wrong relation types, or missing query clauses, suggesting that the proposed span-relation supervision does not simply propagate teacher prediction errors.

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

    CypherKD achieves the lowest error rates among all student and distillation methods in both categories. Compared with SFT, the schema-grounding error rate decreases from **43.44%** to **24.23%**, while the graph-pattern construction error rate decreases from **40.84%** to **29.22%**. It also consistently outperforms strong KD baselines such as CSD and DistiLLM.
These results are consistent with the intended effect of the proposed span-relation objective, suggesting that it improves the student's ability to preserve structural correspondences between Cypher spans and the question-schema context. Since this analysis is based on rule matching, we regard it as supporting evidence rather than a comprehensive characterization of all structural errors. Overall, the reduced schema-grounding and graph-pattern errors provide direct evidence that CypherKD alleviates the learning difficulty motivating our method.


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



