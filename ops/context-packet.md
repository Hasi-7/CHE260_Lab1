# CHE260 Lab 1 context packet

- Goal: read measured time, temperature, pressure, and mass-flow data; make three separate graphs; integrate mass flow versus time only.
- Inputs in this repository: `lab-part1a`, `lab-part1b`, and `lab-part2` are tab-separated, have two ambient-condition metadata lines, and have a blank line after the header. The requested input may also be an ordinary comma-separated CSV.
- Columns: `Time(s)`, `T1(Deg C)`, `T2(Deg C)`, `P1(PSI)`, `P2(PSI)`, `Mass Flowrate(g/min)`.
- Units: integrating g/min against seconds requires dividing each time interval by 60 to obtain mass in grams.
- Existing code: none; `README.md` is nearly empty. The three lab files are untracked source data and must be preserved.
- Implementation entry point: `analyze_lab.py`; start with input parsing and validation so the plotting/integration steps can use the same clean measurements.

## Part 1 report figures (October 8, 2026)

- Goal: insert the existing Part 1a and Part 1b pressure, temperature, and mass-flow PNGs beneath `Processed Results: Rapid and Slow Expansion` in `lab_report.tex`.
- Sources: `lab-part1a_plots/` and `lab-part1b_plots/` each contain three tracked PNGs; the report already loads `graphicx` and requests numbered, captioned figures.
- Preserve the current uncommitted blank-line edits in `lab_report.tex` and leave the Part 2 placeholder intact.
- Verify that pdfLaTeX resolves all six image paths and that figures stay with Part 1 before the following subsection.

## Report body formatting (October 8, 2026)

- Goal: make the user's existing body paragraph wrap within the page and leave room for future body paragraphs without changing their wording.
- Entry point: `lab_report.tex`; its `\text{...}` wrapper is in ordinary prose and produces an overfull line in the compiled PDF.
- Preserve figures, user-written content, minimum 12 pt double spacing, and the report's existing outline. Remove unnecessary manual pagination and use normal LaTeX paragraphs.
- Verify with two pdfLaTeX passes and inspect page count and overfull-box messages.

## Part 1 state windows (October 8, 2026)

- Goal: print mean gauge pressures and temperatures for each tank in chosen initial/final recorded windows and show those windows with dotted boundaries on the pressure/temperature plots.
- Input: `lab-part1a`, `lab-part1b`; existing `analyze_lab.py` already supports explicit mass-flow integration windows. Keep those windows independent of state averaging.
- Candidate windows from plotted traces: Part 1a initial 108–115 s, final 175–185 s; Part 1b initial 125–145 s, final 760–779 s. The slow run still has unequal tank pressures at the end, so label its final range as recorded, not fully equilibrated.
- Expose windows as explicit CLI parameters to allow revision; regenerate both summaries and graphics, verify representative counts and output.
