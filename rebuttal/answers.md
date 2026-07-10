## **CypherKD rebuttal answers**

### **Reviewer Tb6b: (3 point)**

**ANSWER:**

Thank you for the constructive comments. We agree that the paper should provide clearer baseline implementation details and stronger analysis of the proposed supervision signal.

- **The paper lacks some experimental details, especially for baseline implementation. The paper compares with many existing knowledge distillation methods. It does not explain whether these methods use official implementations or the authors' own reimplementations. If the baselines are reimplemented, the paper should provide the implementation details and report whether enough hyperparameter tuning was done.**

    Thank you for pointing this out. We agree that the current version does not provide sufficient details about baseline implementation. In the revised version, we will include a detailed Baseline Implementation Details table. This table will explicitly clarify whether each baseline relies on the official codebase or our own reimplementation, alongside the core hyperparameters, tuning ranges, and checkpoint selection strategies.

    | Method    | Source code                           | Key hyperparameters                      | Tuning range                 | Checkpoint |
    |-----------|---------------------------------------|------------------------------------------|------------------------------|------------|
    | FKL / RKL | Code from the paper project on GitHub | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Last       |
    | SFKL      | Code from the paper project on GitHub | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Last       |
    | DistiLLM  | Code from the paper project on GitHub | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Last       |
    | FDD       | Code from the paper project on GitHub | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Last       |
    | CSD       | Code from the paper project on GitHub | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Last       |
    | AMiD      | Reimplemented from the paper          | kd_ratio ($\beta$)                       | 0.5 to 1, step 0.1           | Last       |
    | CypherKD  | Ours                                  | kd_ratio ($\beta$), $\lambda_{rel}$      | Both from 0.5 to 1, step 0.1 | Last       |


    For a fair comparison, all methods are trained using the same backbone model, training data, optimizer settings, number of epochs, decoding strategy, and evaluation protocol whenever applicable. We use the last checkpoint for every method instead of selecting the best checkpoint based on evaluation results, to avoid overfitting to the evaluation set. For all methods, we report the tuned hyperparameters and their search ranges as shown in the table above.

<br>

- **From the experimental results, CypherKD improves a lot over standard supervised fine-tuning. The gains over existing knowledge distillation methods are often small. Some metrics are almost tied. Therefore, I am not sure whether these small gaps come from the proposed method itself or could be closed by hyperparameter tuning. I also suggest that the paper include confidence information or results across multiple runs.**

    We agree with this concern. Although CypherKD shows clear gains over SFT, some improvements over strong KD baselines are relatively small. To make the comparison more reliable, we will add results across multiple random seeds and report **mean ± standard deviation**.

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

<br>

- **The supervision signal in CypherKD comes entirely from the teacher model, without any additional correction or checking mechanism. If the teacher model makes mistakes in these correspondence relations, the extra supervision may transfer this noise to the student model.**

    Thank you for raising this important point. We would like to clarify that CypherKD does **not** rely entirely on the teacher signal. The student is still trained with the standard cross-entropy loss on the gold Cypher query. The teacher-derived span-relation signal is only used as an auxiliary objective:

    $$\mathcal{L}_{\text{total}} = (1-\beta)\mathcal{L}_{\text{CE}}+ \beta\left(\mathcal{L}_{\text{logit}} + \lambda_{\text{rel}}\mathcal{L}_{\text{rel}}\right)$$

    Therefore, the gold query remains the primary supervision signal, while the teacher provides additional structural guidance. This design reduces the risk that noisy teacher correspondences dominate training.

    To further address this concern, we will add an analysis of teacher-induced noise. Specifically, we will examine cases where the teacher produces incorrect or questionable span-context correspondences and analyze whether the student inherits these errors or whether they are mitigated by the gold cross-entropy objective.

    | Teacher error type           |       # Cases | Student copies teacher error | Student recovers / follows gold |
    | ---------------------------- | ------------: | ---------------------------: | ------------------------------: |
    | Wrong schema element         | [PLACEHOLDER] |                [PLACEHOLDER] |                   [PLACEHOLDER] |
    | Wrong relationship direction | [PLACEHOLDER] |                [PLACEHOLDER] |                   [PLACEHOLDER] |
    | Missing filter condition     | [PLACEHOLDER] |                [PLACEHOLDER] |                   [PLACEHOLDER] |
    | Wrong aggregation / ordering | [PLACEHOLDER] |                [PLACEHOLDER] |                   [PLACEHOLDER] |