# CHE260_Lab1

Install the plotting dependency:

```sh
python -m pip install -r requirements.txt
```

Run the analysis:

```sh
python analyze_lab.py lab-part1a
python analyze_lab.py measurements.csv --output-dir results
python analyze_lab.py lab-part1a --section 8.3:45.7 --section 71.2:90.9
python analyze_lab.py lab-part1b --section 16.1:53.4 --section 77.6:104.2
```

The input must have columns `Time(s)`, `T1(Deg C)`, `T2(Deg C)`, `P1(PSI)`,
`P2(PSI)`, and `Mass Flowrate(g/min)`. CSV and tab-separated files both work;
the existing `lab-part1a`, `lab-part1b`, and `lab-part2` files contain two
ambient-condition lines before the header, which are skipped.

The program writes **three separate PNG graphs** (pressure, temperature, and
mass flow rate) plus `summary.txt` in `<input name>_plots/` by default.
`summary.txt` contains the same results printed in the terminal, including the
mass-flow area in grams. The area uses the trapezoidal rule across the full measurement
period, converting each time difference from seconds to minutes. Negative
flow measurements are included as recorded (the result is a signed integral).

Use `--section START:END` (seconds) once per interval to calculate the mass
in each flow period separately. The examples for `lab-part1a` and `lab-part1b`
use the approximate starts and returns to zero visible in the recorded flow;
adjust those boundaries if your lab specifies different ones. The section
results appear in both the terminal and `summary.txt`, and the selected time
ranges are shaded on the mass-flow graph. When a boundary falls between two
measurements, the flow there is linearly interpolated. The full-recording
integral is always reported as well.
