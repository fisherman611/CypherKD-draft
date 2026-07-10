## **CypherKD rebuttal answers**

### **Reviewer 1HaF: (Soundness: 4 point, Excitement: 3 point, Overall: 3.5 point)**

**ANSWER:**

Thank you for the thoughtful comments. We appreciate the opportunity to clarify the mechanism of the proposed loss and provide additional evidence on result variability.

- **I honestly find the result a little unbelievable. The extent of extra supervision from the added loss function is a single scalar per query, and I don't understand the mechanism by which is could have such a large effect.**

    Thank you for raising this concern. The added loss is reduced to a scalar only at the final optimization step; it is not a single query-level label. In our implementation, CypherKD extracts multiple Cypher spans, including clauses, triplets, node patterns, and expressions. For each span, it compares the teacher and student span-context relation scores, where the context comes from the question and schema tokens.

    Thus, the supervision is applied over many fine-grained span-context relations before aggregation. This gives the student structured grounding guidance beyond standard token-level KD, which mainly matches next-token distributions.

<br>

- **Can we get some measure of noise?**

    Thank you for raising this point. We interpret this noise as run-to-run variability. To quantify it, we will add results over multiple random seeds and report **mean ± standard deviation** under the same training and evaluation protocol.

    **CypherBench**

    | Method                 | EX           | PSJS         | Executable   |
    |------------------------|-------------:|-------------:|-------------:|
    | **Qwen3 family**       |              |              |              |
    | Qwen3-4B (Teacher)     | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | Qwen3-0.6B (SFT)       | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | RKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | SFKL                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | DistiLLM               | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FDD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | CSD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | AMiD                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | **CypherKD**           | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | **Llama-3.2 family**   |              |              |              |
    | Llama-3.2-8B (Teacher) | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | Llama-3.2-1B (SFT)     | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | RKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | SFKL                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | DistiLLM               | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FDD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | CSD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | AMiD                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | **CypherKD**           | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |

    **Mind-the-Query**

    | Method                 | EX           | PSJS         | Executable   |
    |------------------------|-------------:|-------------:|-------------:|
    | **Qwen3 family**       |              |              |              |
    | Qwen3-4B (Teacher)     | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | Qwen3-0.6B (SFT)       | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | RKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | SFKL                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | DistiLLM               | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FDD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | CSD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | AMiD                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | **CypherKD**           | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | **Llama-3.2 family**   |              |              |              |
    | Llama-3.2-8B (Teacher) | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | Llama-3.2-1B (SFT)     | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | RKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | SFKL                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | DistiLLM               | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FDD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | CSD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | AMiD                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | **CypherKD**           | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |

    **Neo4j-Text2Cypher**

    | Method                 | EX           | PSJS         | Executable   |
    |------------------------|-------------:|-------------:|-------------:|
    | **Qwen3 family**       |              |              |              |
    | Qwen3-4B (Teacher)     | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | Qwen3-0.6B (SFT)       | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | RKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | SFKL                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | DistiLLM               | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FDD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | CSD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | AMiD                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | **CypherKD**           | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | **Llama-3.2 family**   |              |              |              |
    | Llama-3.2-8B (Teacher) | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | Llama-3.2-1B (SFT)     | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | RKL                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | SFKL                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | DistiLLM               | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | FDD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | CSD                    | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | AMiD                   | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |
    | **CypherKD**           | [MEAN ± STD] | [MEAN ± STD] | [MEAN ± STD] |

    This analysis will make clear whether the observed gains are stable across random seeds or within the expected variance of training.

<br>

- **Is there any reason to think this approach is specific to Cypher, as opposed to any QA finetune? If there's nothing specific, then I'd feel more confident in the intervention with some examples in other domains.**

    Thank you for this important question. We believe CypherKD is particularly suitable for Text-to-Cypher because Cypher queries have explicit graph-structured semantics. A generated query is not only a token sequence, but also a composition of node labels, relationship types, paths, properties, filters, and return expressions. These structures naturally define span-level units whose correctness depends on grounding to the question and schema context.

    For example, in Text-to-Cypher, an error in relationship direction or path structure can make the query executable but semantically wrong. This makes span-to-context structural grounding especially important. CypherKD is designed to transfer this kind of teacher behavior by aligning how teacher and student represent the relations between Cypher spans and the input context.

    That said, we agree that the general idea may also be useful in other structured semantic parsing tasks. To test whether the method is not limited to Cypher, we will add an additional experiment on **Text-to-SQL**, where SQL queries also contain structured components such as tables, columns, joins, conditions, aggregations, and ordering clauses.

    We plan to use Spider as a representative Text-to-SQL benchmark and compare the following settings:

    | Method                 | EX           | EM           |
    |------------------------|-------------:|-------------:|
    | Qwen3-4B (Teacher)     | [MEAN ± STD] | [MEAN ± STD] |
    | Qwen3-0.6B (SFT)       | [MEAN ± STD] | [MEAN ± STD] |
    | SRKL                   | [MEAN ± STD] | [MEAN ± STD] |
    | SRKL + Proposed loss   | [MEAN ± STD] | [MEAN ± STD] |
