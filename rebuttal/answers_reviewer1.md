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

    Although CypherKD shows clear gains over SFT, some improvements over strong KD baselines are relatively small. To separate method effects from run-to-run variance, we will add results across multiple random seeds and report **mean +/- standard deviation**.

    **CypherBench**

    | Method                 | EX           | PSJS         | Executable   |
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

    | Method                 | EX           | PSJS         | Executable   |
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

    | Method                 | EX           | PSJS         | Executable   |
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

    We thank the reviewer for this important suggestion. To directly examine structural correspondence errors, we add an error analysis using two grouped categories from the CypherBench taxonomy that are most closely related to span-context grounding:

    - **Schema grounding:** wrong entity, relationship, or property type; entity-linking errors; and schema violations.
    - **Graph-pattern construction:** reversed relationship directions and graph patterns that do not align with the question.

    We compare the gold and predicted Cypher queries on the test set and report the frequency of these two structural error groups.

    | Method | Schema grounding | Graph-pattern construction |
    |---|---:|---:|
    | Qwen3-4B (Teacher) | 16.31% | 21.76% |
    | Qwen3-0.6B (SFT) | 43.70% | 24.19% |
    | CSD | 28.58% | 24.74% |
    | DistiLLM | 29.43% | 23.94% |
    | **CypherKD** | **26.83%** | **23.59%** |

    The clearest improvement is in schema grounding. Compared with SFT, CypherKD reduces the full-test schema-grounding error rate from 43.70% to 26.83%, a reduction of 16.87 percentage points. It also produces fewer schema-grounding errors than CSD and DistiLLM. This indicates that the additional span-relation objective helps the student associate question and schema spans with the correct Cypher entity types, relationship types, properties, and linked entities.

    The graph-pattern improvements are smaller: CypherKD obtains the lowest error rate among the student/KD methods (23.59%), compared with 24.19% for SFT, 24.74% for CSD, and 23.94% for DistiLLM. We therefore interpret the evidence as strongest for improved schema grounding, with a more modest benefit for graph-pattern construction, rather than claiming a uniformly large reduction across every structural error type.

<br>

- **I suggest that the authors add a robustness analysis for the rule-based span extraction method. For example, they could discuss when this method may fail under different Cypher structures and how to test its robustness more carefully**

     We sincerely thank the reviewer for this suggestion. Our span extraction is implemented using deterministic rules derived from the Cypher syntax:

    - Clause spans are identified by matching predefined Cypher clause keywords.
    - Node spans are extracted from parenthesized structures that satisfy Cypher node syntax (e.g., labels, properties, or variables adjacent to relationships).
    - Triplet spans are extracted using structural patterns that capture relationship chains.
    - Expression spans are obtained from the expressions following clauses such as WHERE, WITH, RETURN, and ORDER BY.

    These rules are not intended to cover every possible Cypher construct. Failure cases may arise for highly complex queries, such as nested subqueries (EXISTS { ... }), variable-length paths (-[*1..3]-), or other uncommon language constructs, where the extracted span boundaries may be incomplete, missing, or slightly inaccurate.

    Nevertheless, our rule extractor is designed to provide weak structural supervision rather than a complete Cypher parser. Therefore, perfect span extraction is not required for the proposed span-level distillation objective to be effective. While a small number of extracted spans may be noisy or missing, the majority of spans in standard Cypher queries are correctly identified and continue to provide informative structural alignment between the teacher and student. Consequently, occasional extraction errors behave as annotation noise rather than systematic supervision errors, and do not substantially reduce the effectiveness of the proposed span-level distillation.



