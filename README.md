# project-cyclopentane

Submechanisms:

| PES                       | R | Starting Step         | Name            |
|---------------------------|---|-----------------------|-----------------|
| $\text{RH} + \text{OH}$   | e | abstraction           | `A_rh-oh_1e-1`  |
| $\text{RH} + \text{OH}$   | e | $\pi$-addition        | `A_rh-oh_1e-2`  |
| $\text{RH} + \text{OH}$   | x | abstraction           | `A_rh-oh_2x`    |
| $\text{RH} + \text{HO}_2$ | e | abstraction           | `B_rh-hO2_1e-1` |
| $\text{RH} + \text{HO}_2$ | e | $\pi$-addition        | `B_rh-hO2_1e-2` |
| $\text{RH} + \text{HO}_2$ | x | abstraction           | `B_rh-hO2_2x`   |
| $\text{R}$                | e | ring-opening          | `C_r_1e`        |
| $\text{R}$                | x | ring-opening          | `C_r_2x`        |
| $\text{R}$                | o | ring-opening          | `C_r_3o`        |
| $\text{R} + \text{O}_2$   | e | $\text{O}_2$-addition | `D_r-o2_1e`     |
| $\text{R} + \text{O}_2$   | x | $\text{O}_2$-addition | `D_r-o2_2x`     |
| $\text{R} + \text{O}_2$   | o | $\text{O}_2$-addition | `D_r-o2_3o`     |

