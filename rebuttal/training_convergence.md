# Training convergence

We report development-set performance after every epoch under the same five-epoch training schedule.

## Development loss

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

## Development Exact Match (%)

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

For all methods, development loss decreases and Exact Match increases substantially over the first three epochs, followed by only small changes in epochs 4 and 5. These trajectories show that both the baseline and relation-grounding variants approach convergence within the shared five-epoch training schedule.
