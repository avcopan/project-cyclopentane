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


Inserts:

- `A_rh-oh_1e-1`
  - [`C5H8(522) + OH(4) = C5H7(1202) + H2O(5)`](insert/A_rh-oh_1e-1_C5H8-522-OH-4_C5H7-1202-H2O-5) (Y11): failed TS search
  - [`C5H8(522) + OH(4) = C5H7(500) + H2O(5)`](insert/A_rh-oh_1e-1_C5H8-522-OH-4_C5H7-500-H2O-5) (Y12): failed TS search
- `D_r-o2_0a`
  - [`S(722)r0 = S(728)z`](insert/D_r-o2_0a_S-722-r0_S-728-z) (Y61): wrong E/Z product
- `D_r-o2_1e`
  - [`S(1206)r0 = HO2(8) + C5H6(478)`](insert/D_r-o2_1e_S-1206-r0_HO2-8-C5H6-478) (Y14): drop sterically unfeasible TS configuration
  - [`S(1209)r0 = C5O2sidwaoez`](insert/D_r-o2_1e_S-1209-r0_C5O2sidwaoez) (Y56): wrong E/Z product


Unresolved failures:

- `A_rh-oh_1e-2`
  - `C5H8(522) + OH(4) = C5H9O(852)r0` (Y10): submerged TS, requires 2-TS treatment
- `D_r-o2_0a`
  - `S(725)r0 = C5H8O(829)rs + OH(4)` (Y50): failed TS search
- `D_r-o2_1e`
  - `S(1210)r0 = OH(4) + S(1288)rs0` (Y53): failed TS search
  - `S(1210)r0 = C5O2nexammzzz` (Y58): wrong E/Z product
  - `S(1210)r0 = C5Oqidgnvrs + OH(4)` (Y59): failed TS search
  - `S(725)r0 = C5O2qarhfr` (Y63): bug in instability handling
