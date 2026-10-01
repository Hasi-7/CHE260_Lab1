# CHE260 Lab 1 context packet

- Goal: read measured time, temperature, pressure, and mass-flow data; make three separate graphs; integrate mass flow versus time only.
- Inputs in this repository: `lab-part1a`, `lab-part1b`, and `lab-part2` are tab-separated, have two ambient-condition metadata lines, and have a blank line after the header. The requested input may also be an ordinary comma-separated CSV.
- Columns: `Time(s)`, `T1(Deg C)`, `T2(Deg C)`, `P1(PSI)`, `P2(PSI)`, `Mass Flowrate(g/min)`.
- Units: integrating g/min against seconds requires dividing each time interval by 60 to obtain mass in grams.
- Existing code: none; `README.md` is nearly empty. The three lab files are untracked source data and must be preserved.
- Implementation entry point: `analyze_lab.py`; start with input parsing and validation so the plotting/integration steps can use the same clean measurements.
