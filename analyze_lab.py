"""Graph CHE260 measurements and integrate the mass-flow rate.

Usage: python analyze_lab.py lab-part1a
"""

import argparse
import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Save figures without requiring a desktop display.
import matplotlib.pyplot as plt


COLUMNS = (
    "Time(s)",
    "T1(Deg C)",
    "T2(Deg C)",
    "P1(PSI)",
    "P2(PSI)",
    "Mass Flowrate(g/min)",
)


def read_measurements(path: Path) -> list[dict[str, float]]:
    """Read a comma- or tab-delimited file, skipping ambient metadata."""
    with path.open(encoding="utf-8-sig", newline="") as source:
        lines = source.readlines()

    header_line = next(
        (index for index, line in enumerate(lines) if line.startswith("Time(s)")),
        None,
    )
    if header_line is None:
        raise ValueError("Missing measurement header beginning with Time(s)")

    delimiter = "\t" if "\t" in lines[header_line] else ","
    reader = csv.DictReader(lines[header_line:], delimiter=delimiter)
    if reader.fieldnames is None or any(name not in reader.fieldnames for name in COLUMNS):
        raise ValueError(f"Expected columns: {', '.join(COLUMNS)}")

    measurements = []
    for row in reader:
        if not any(value and value.strip() for value in row.values() if isinstance(value, str)):
            continue
        try:
            measurement = {name: float(row[name]) for name in COLUMNS}
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid measurement on line {reader.line_num + header_line}") from error
        if not all(math.isfinite(value) for value in measurement.values()):
            raise ValueError(f"Non-finite measurement on line {reader.line_num + header_line}")
        if measurements and measurement["Time(s)"] <= measurements[-1]["Time(s)"]:
            raise ValueError("Measurement times must be strictly increasing")
        measurements.append(measurement)

    if len(measurements) < 2:
        raise ValueError("At least two measurements are required")
    return measurements


def mass_from_flow(
    measurements: list[dict[str, float]],
    start: float | None = None,
    end: float | None = None,
) -> float:
    """Integrate flow over a time range, interpolating at its endpoints."""
    start = measurements[0]["Time(s)"] if start is None else start
    end = measurements[-1]["Time(s)"] if end is None else end
    if not (measurements[0]["Time(s)"] <= start < end <= measurements[-1]["Time(s)"]):
        raise ValueError("Section must lie within the recorded times, with start < end")

    mass_g = 0.0
    for earlier, later in zip(measurements, measurements[1:]):
        t0, t1 = earlier["Time(s)"], later["Time(s)"]
        left, right = max(t0, start), min(t1, end)
        if left >= right:
            continue
        flow0, flow1 = earlier["Mass Flowrate(g/min)"], later["Mass Flowrate(g/min)"]
        left_flow = flow0 + (flow1 - flow0) * (left - t0) / (t1 - t0)
        right_flow = flow0 + (flow1 - flow0) * (right - t0) / (t1 - t0)
        mass_g += (left_flow + right_flow) / 2 * (right - left) / 60
    return mass_g


def parse_section(text: str) -> tuple[float, float]:
    try:
        start_text, end_text = text.split(":")
        start, end = float(start_text), float(end_text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use START:END in seconds, e.g. 8.3:45.7") from error
    if not (math.isfinite(start) and math.isfinite(end) and start < end):
        raise argparse.ArgumentTypeError("Section times must be finite, with start < end")
    return start, end


def save_graph(
    measurements: list[dict[str, float]],
    columns: tuple[str, ...],
    title: str,
    ylabel: str,
    destination: Path,
    sections: list[tuple[float, float]] | None = None,
) -> None:
    times = [row["Time(s)"] for row in measurements]
    figure, axis = plt.subplots(figsize=(10, 5))
    for column in columns:
        axis.plot(times, [row[column] for row in measurements], label=column)
    for index, (start, end) in enumerate(sections or [], start=1):
        axis.axvspan(start, end, alpha=0.12, label=f"Section {index}")
    axis.set(title=title, xlabel="Time (s)", ylabel=ylabel)
    axis.grid(True, alpha=0.3)
    if len(columns) > 1 or sections:
        axis.legend()
    figure.tight_layout()
    figure.savefig(destination, dpi=150)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="CSV or tab-separated lab measurements")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for the three PNG graphs (default: <input name>_plots)",
    )
    parser.add_argument(
        "--section",
        type=parse_section,
        action="append",
        default=[],
        metavar="START:END",
        help="Integrate mass flow in this time range (seconds); repeat for multiple sections",
    )
    args = parser.parse_args()

    try:
        measurements = read_measurements(args.file)
        section_results = [
            (start, end, mass_from_flow(measurements, start, end))
            for start, end in args.section
        ]
        output_dir = args.output_dir or args.file.parent / f"{args.file.stem}_plots"
        output_dir.mkdir(parents=True, exist_ok=True)
        graphs = (
            (("P1(PSI)", "P2(PSI)"), "Pressure vs time", "Pressure (PSI)", "pressure.png"),
            (("T1(Deg C)", "T2(Deg C)"), "Temperature vs time", "Temperature (°C)", "temperature.png"),
            (("Mass Flowrate(g/min)",), "Mass flow rate vs time", "Mass flow rate (g/min)", "mass_flow_rate.png"),
        )
        for columns, title, ylabel, filename in graphs:
            save_graph(
                measurements, columns, title, ylabel, output_dir / filename,
                args.section if filename == "mass_flow_rate.png" else None,
            )

        summary = (
            f"Loaded {len(measurements)} measurements from {args.file}\n"
            f"Mass-flow integral: {mass_from_flow(measurements):.6f} g\n"
        )
        for index, (start, end, mass_g) in enumerate(section_results, start=1):
            summary += f"Section {index} ({start:g}-{end:g} s): {mass_g:.6f} g\n"
        summary += f"Graphs saved to {output_dir}\n"
        (output_dir / "summary.txt").write_text(summary, encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")

    print(summary, end="")


if __name__ == "__main__":
    main()
