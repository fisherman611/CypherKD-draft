## **CypherKD rebuttal answers**

### **Reviewer 1HaF: (Soundness: 4 point, Excitement: 3 point, Overall: 3.5 point)**

**ANSWER:**

Thank you for the thoughtful comments. We appreciate the opportunity to clarify the mechanism of the proposed loss and provide additional evidence on result variability.

- **I honestly find the result a little unbelievable. The extent of extra supervision from the added loss function is a single scalar per query, and I don't understand the mechanism by which is could have such a large effect.**

    The added loss is reduced to a scalar only at the final optimization step; it is not a single query-level label or supervision signal. In our implementation, CypherKD first extracts multiple semantic spans from each Cypher query, including clauses, triplets, node patterns, relationship patterns, and expressions. For each extracted span, it computes the teacher and student span–context relation scores, where the context consists of the question and schema tokens.

    The loss is therefore constructed from many comparisons between individual Cypher spans and their corresponding input context, potentially across multiple spans, context tokens, and selected hidden layers. Although these discrepancies are finally aggregated into a single scalar for optimization, the gradients are propagated through all contributing span and context representations.

    Thus, the supervision is applied over many fine-grained span–context relations before aggregation. This gives the student structured grounding guidance about which parts of the question and schema are relevant to each Cypher component, beyond standard token-level KD, which mainly matches next-token distributions.


<br>

- **Can we get some measure of noise?**

    Thank you for raising this point. We interpret this noise as run-to-run variability. To quantify it, we will add results over 5 random seeds and report **mean ± standard deviation** under the same training and evaluation protocol.

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

    This analysis will make clear whether the observed gains are stable across random seeds or within the expected variance of training.

<br>

- **Is there any reason to think this approach is specific to Cypher, as opposed to any QA finetune? If there's nothing specific, then I'd feel more confident in the intervention with some examples in other domains.**

    We believe CypherKD is particularly suitable for Text-to-Cypher because Cypher queries have explicit graph-structured semantics. A generated query is not only a token sequence, but also a composition of node labels, relationship types, paths, properties, filters, and return expressions. These structures naturally define span-level units whose correctness depends on their grounding to the question and schema context.

    For example, an error in relationship direction or path structure can make a Cypher query executable but semantically incorrect. This makes span-to-context structural grounding especially important. CypherKD transfers this type of teacher behavior by aligning how the teacher and student represent the relations between Cypher spans and the input context.

    At the same time, the general span-relation distillation framework may also be applicable to other structured semantic parsing tasks. To examine whether its effectiveness is limited to Cypher, we conducted an additional experiment on **Text-to-SQL**, where SQL queries similarly contain structured components such as tables, columns, joins, conditions, aggregations, and ordering clauses.

    We use Spider as a representative Text-to-SQL benchmark and report the following results:

    | Method               | EX(%)| EM(%)|
    | -------------------- | ---: | ---: |
    | Qwen3-4B (Teacher)   | 77.4 | 69.0 |
    | Qwen3-0.6B (SFT)     | 62.5 | 57.9 |
    | SRKL                 | 65.2 | 58.7 |
    | SRKL + Proposed loss | 66.6 | 59.9 |

    Adding the proposed span-relation loss to SRKL improves execution accuracy from 65.2 to 66.6 (+1.4%)  and exact match from 58.7 to 59.9 (+1.2%). These results suggest that the proposed supervision is not restricted to Cypher and can also benefit another structured query generation task. Nevertheless, its motivation is especially strong for Text-to-Cypher because graph paths, relationship directions, and node–relationship compositions provide explicit structural units for span-level grounding.
