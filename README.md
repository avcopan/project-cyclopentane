# project-cyclopentane

Submechanisms:

| PES                       | R | Starting Step         | Name            | Version 0 |
|---------------------------|---|-----------------------|-----------------|-----------|
| $\text{RH} + \text{OH}$   | e | abstraction           | `A_rh-oh_1e-1`  | 6S, 3R    |
| $\text{RH} + \text{OH}$   | e | $\pi$-addition        | `A_rh-oh_1e-2`  | 4S, 2R    |
| $\text{RH} + \text{OH}$   | x | abstraction           | `A_rh-oh_2x`    | 8S, 5R    |
| $\text{RH} + \text{HO}_2$ | e | abstraction           | `B_rh-ho2_1e-1` | 6S, 3R    |
| $\text{RH} + \text{HO}_2$ | e | $\pi$-addition        | `B_rh-ho2_1e-2` | 6S, 4R    |
| $\text{RH} + \text{HO}_2$ | x | abstraction           | `B_rh-ho2_2x`   | 8S, 3R    |
| $\text{R}$                | e | ring-opening          | `C_r_1e`        | 7S, 2R    |
| $\text{R}$                | x | ring-opening          | `C_r_2x`        | 12S, 8R   |
| $\text{R}$                | o | ring-opening          | `C_r_3o`        | 6S, 6R    |
| $\text{R} + \text{O}_2$   | e | $\text{O}_2$-addition | `D_r-o2_1e`     | 9S, 6R    |
| $\text{R} + \text{O}_2$   | x | $\text{O}_2$-addition | `D_r-o2_2x`     | 15S, 14R  |
| $\text{R} + \text{O}_2$   | o | $\text{O}_2$-addition | `D_r-o2_3o`     | 11S, 10R  |

