# CHE260_Lab1

## Data analysis

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
python analyze_lab.py lab-part1a --section 8.3:45.7 --section 71.2:90.9 --initial-window 108:115 --final-window 175:185
python analyze_lab.py lab-part1b --section 16.1:53.4 --section 77.6:104.2 --initial-window 125:145 --final-window 760:779
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

Use `--initial-window START:END` and `--final-window START:END` to average both
tanks' recorded gauge pressures (psig) and temperatures (°C) over selected
time ranges. The summary lists each range, its sample count, and four means;
green and red dotted boundary lines mark the ranges on the pressure and
temperature graphs. These options do not change the mass-flow integration.
The example final window for Part 1b is the last recorded range: its two
pressures have not quite converged, so it should not be treated as a confirmed
fully equilibrated state.

## LaTeX lab report: first-time setup

[`lab_report.tex`](lab_report.tex) is the blank report template. LaTeX turns this
text file into a formatted PDF. It already sets up the cover page, 12-point type,
double spacing, and the outline for both parts of Lab 1.

### Quick compile commands

Once MiKTeX is installed, open PowerShell in the repository folder and run:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error lab_report.tex
```

This creates `lab_report.pdf` in the repository folder. To compile with updated
citations and cross-references, run two passes, then open the PDF:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error lab_report.tex
pdflatex -interaction=nonstopmode -halt-on-error lab_report.tex
Start-Process .\lab_report.pdf
```

Save `lab_report.tex` before running these commands. If you have not installed
LaTeX yet, follow one of the setup options below.

### Option 1: Overleaf (no installation required)

1. Create a free account at [Overleaf](https://www.overleaf.com/).
2. Choose **New Project > Blank Project** and give the project a name.
3. Upload `lab_report.tex` from this repository using the upload button in the
   project's file panel.
4. In the project settings/menu, select `lab_report.tex` as the **Main document**
   and **pdfLaTeX** as the compiler.
5. Open `lab_report.tex`, fill in the cover-page fields, and write your report
   under the appropriate headings.
6. Click **Recompile** to update the PDF preview, then use **Download PDF** to
   save the report.

If you add graphs, upload their image files too. Keep the image paths in your
LaTeX code consistent with their locations in the Overleaf project.

### Option 2: Compile locally on Windows with MiKTeX

1. Download and install [MiKTeX](https://miktex.org/download). MiKTeX provides
   the LaTeX compiler; Python is not required to compile the report.
2. Open **MiKTeX Console**, check for updates, and install available updates.
   In its settings, set **Install missing packages on-the-fly** to **Yes** so
   the template's required packages can be installed automatically. An internet
   connection is needed for those downloads.
3. Edit `lab_report.tex` in a text editor. MiKTeX also includes **TeXworks**, an
   editor with a PDF preview.
4. In File Explorer, open the folder containing `lab_report.tex`, right-click
   an empty area, and choose **Open in Terminal** (or **Open PowerShell window
   here**, depending on your Windows version).
5. Run:

   ```powershell
   pdflatex -interaction=nonstopmode -halt-on-error lab_report.tex
   ```

6. The output is `lab_report.pdf` in the same folder. Double-click it, or run:

   ```powershell
   Start-Process .\lab_report.pdf
   ```

After adding or changing citations or figure/table references, run the compile
command twice to update numbering and links. Save your `.tex` changes before
compiling.

**Using TeXworks instead of the terminal:** open `lab_report.tex` in TeXworks,
select **pdfLaTeX** in the typesetting dropdown, and click the green typeset
button. This also creates `lab_report.pdf` alongside the source file.

### Editing the template

- Replace the cover-page blank lines (`\hrulefill` and `\rule{4cm}{0.4pt}`) with
  your group members' details, PRA section, and dates. Add or remove member rows
  as needed.
- Write beneath the `\section`, `\subsection`, and `\subsubsection` headings.
  Lines starting with `%` are comments: they provide guidance but do not appear
  in the PDF.
- The template includes a temporary page break before Part 2. Remove its
  `\newpage` command if it is unnecessary after adding your report text.
- For references, follow the commented `thebibliography` instructions in the
  template and replace the existing References heading as directed.
- Follow the PDFs in `Lab_PDFs/`: the complete report is limited to 10 pages,
  the Introduction to 2 pages, and the Conclusion to 1 page. Filling the
  template does not automatically enforce these limits.
- The guidelines require acknowledgment of AI-assisted outlining. The template
  includes comments describing the required citation format.

### Common compilation issues

- **`pdflatex` is not recognized:** close and reopen your terminal after
  installing MiKTeX. If the issue persists, check that MiKTeX installed correctly
  and that its executable directory is on your Windows `PATH`, or use TeXworks.
- **A package is missing:** allow MiKTeX to install it when prompted, or install
  the named package through MiKTeX Console's Packages section.
- **Compilation stops:** read the first error in the terminal or
  `lab_report.log`. Common causes include unmatched braces, missing image
  files, and unescaped special characters. In ordinary text, write `\%`,
  `\&`, and `\_` for percent signs, ampersands, and underscores.
- **The PDF cannot be overwritten:** close it in your PDF viewer and compile
  again.

Files such as `.aux`, `.log`, and `.out` are normal compiler-generated helper
files. Keep `lab_report.tex` and any images as your editable source files;
submit the PDF according to the course instructions.
