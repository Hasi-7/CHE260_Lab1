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

## LaTeX formatting check and build (October 8, 2026)

- Goal: check `lab_report.tex` formatting and build the report PDF.
- Normalize paragraph breaks, sentence spacing, inline variables, and display equations using the existing `amsmath` package; preserve the author's scientific claims and numerical expressions for separate review.
- Keep 12 pt type, double spacing, one-inch margins, and the existing figure captions and labels.
- Build with two pdfLaTeX passes into `out/`, the existing editor build directory, and check page count, references, and box warnings.

## Two-column report body (October 8, 2026)

- Goal: format the main report in two columns while retaining a full-width title page.
- Entry point: [[lab_report.tex]]; switch to two columns after the title page. Figures already size themselves relative to `\linewidth`.
- Preserve report wording, equations, 12 pt type, double spacing, and one-inch margins.
- Verify with two pdfLaTeX passes into `out/` and check for unresolved references and overfull boxes.

## Compact slow-expansion figures (October 8, 2026)

- Goal: reduce the gap between Figures 3 and 4 and allow following content onto their page.
- Keep both numbered captions and labels, grouping the slow-expansion plots in one float with a fixed 12 pt gap.
- Use ragged-bottom columns to avoid stretching vertical whitespace; preserve current report content and user edits.
- Build twice into `out/` and check references and layout warnings.

## Part 2 graphs placed by content (October 8, 2026)

- Goal: add the existing graphs from `lab-part2_plots/` to [[lab_report.tex]] near the relevant Part 2 discussion.
- Put pressure and temperature together under processed results; put mass flow under initial mass and tank volume before its integration discussion.
- Preserve numerical claims and existing prose, adding captions, unique labels, and figure references.
- Build twice into `out/` to verify images and references.

## Part 2 reading order and equation spacing (October 8, 2026)

- Goal: keep the complete mass-and-volume explanation before Part 2 graphs, tighten its two formulas, and place heading 2.2.3 in the left column.
- Move Part 2 figure blocks after the calculation and use fixed source-order placement to prevent graphs from interrupting paragraphs.
- Combine the two formulas into one compact gathered display; preserve prose and values.
- Verify the compiled PDF's text order and heading position, adjusting placement as needed.
