## **CypherKD rebuttal answers**

### **Reviewer 1HaF: (Soundness: 4 point, Excitement: 3 point, Overall: 3.5 point)**

**ANSWER:**

Thank you for the thoughtful comments. We appreciate the opportunity to clarify the mechanism of the proposed loss and provide additional evidence on result variability.

- **I honestly find the result a little unbelievable. The extent of extra supervision from the added loss function is a single scalar per query, and I don't understand the mechanism by which is could have such a large effect.**

    We thank the reviewer for raising this concern. We believe there is a misunderstanding regarding the amount of supervision introduced by our objective. Although the final loss is, as with virtually all training objectives, reduced to a single scalar for optimization, the supervision itself is not a single scalar signal.

    Specifically, CypherKD decomposes each target query into multiple semantic spans (e.g., clauses, triplets, node/relationship patterns, and expressions). For every span, we compute relevance scores with the corresponding question and schema representations, producing a large number of span–context alignment terms across the sequence. The final loss aggregates these fine-grained alignment terms rather than introducing only one additional supervision value per query.
    
    Consequently, the resulting gradients are distributed over all participating span and context representations, explicitly encouraging the student to associate each Cypher component with the relevant parts of the input. This structured grounding signal is complementary to next-token distribution matching, which mainly supervises output prediction without explicitly modeling these intermediate semantic correspondences. We therefore attribute the observed improvements to the richer and more structured supervision provided by these numerous alignment constraints, rather than to a single additional scalar.


- **Can we get some measure of noise?**

    Thank you for raising this point. We interpret this noise as run-to-run variability. To quantify it, we add the standard deviations over five random seeds, computed under the same training and evaluation protocol. Following the evaluation protocol adopted by AMiD (Shin et al., ICLR 2026), we report statistics over five random seeds on the main benchmarks to assess training stability while keeping the computational cost manageable.

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

    This analysis will make clear whether the observed gains are stable across random seeds or within the expected variance of training.

<br>

- **Is there any reason to think this approach is specific to Cypher, as opposed to any QA finetune? If there's nothing specific, then I'd feel more confident in the intervention with some examples in other domains.**

    We thank the reviewer for this question. We do not believe the proposed span-relation distillation objective is inherently specific to Cypher. The core idea is to distill structured semantic correspondences between spans in the target representation and the input context, which is applicable whenever the target language contains meaningful structural units.
Text-to-Cypher is a particularly suitable setting because Cypher queries explicitly encode graph semantics through node labels, relationship types, paths, properties, filters, and return expressions. Errors such as an incorrect relationship direction or path composition may still produce executable queries while changing the intended semantics, making structural grounding especially important.
To evaluate whether the proposed objective generalizes beyond Cypher, we conducted an additional experiment on **Text-to-SQL**. The distillation objective remains unchanged; only the span extractor is adapted to SQL by identifying tables, columns, JOIN conditions, WHERE clauses, and aggregation expressions. Using Spider as the benchmark, we obtained the following results:

    | Method               | EX(%)| EM(%)|
    | -------------------- | ---: | ---: |
    | Qwen3-4B (Teacher)   | 77.4 | 69.0 |
    | Qwen3-0.6B (SFT)     | 62.5 | 57.9 |
    | SRKL                 | 65.2 | 58.7 |
    | SRKL + Proposed loss | 66.6 | 59.9 |

    Adding the proposed span-relation loss to SRKL improves execution accuracy from 65.2 to 66.6 (**+1.4%**)  and exact match from 58.7 to 59.9 (**+1.2%**). These results suggest that the proposed supervision is not restricted to Cypher and can also benefit another structured query generation task. Nevertheless, its motivation is especially strong for Text-to-Cypher because graph paths, relationship directions, and node–relationship compositions provide explicit structural units for span-level grounding.



