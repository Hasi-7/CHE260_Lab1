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
from matplotlib.ticker import MaxNLocator


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


def state_averages(
    measurements: list[dict[str, float]], window: tuple[float, float]
) -> tuple[int, dict[str, float]]:
    """Average each tank's sampled pressure and temperature within a time window."""
    start, end = window
    if start < measurements[0]["Time(s)"] or end > measurements[-1]["Time(s)"]:
        raise ValueError("State window must lie within the recorded times")
    rows = [row for row in measurements if start <= row["Time(s)"] <= end]
    if len(rows) < 2:
        raise ValueError("State window must contain at least two measurements")
    columns = ("P1(PSI)", "T1(Deg C)", "P2(PSI)", "T2(Deg C)")
    return len(rows), {column: sum(row[column] for row in rows) / len(rows) for column in columns}


def save_graph(
    measurements: list[dict[str, float]],
    columns: tuple[str, ...],
    title: str,
    ylabel: str,
    destination: Path,
    sections: list[tuple[float, float]] | None = None,
    state_windows: dict[str, tuple[float, float]] | None = None,
) -> None:
    times = [row["Time(s)"] for row in measurements]
    # Match the report's column width so 12 pt text stays readable after embedding.
    figure = plt.figure(figsize=(3.2, 3.1), layout="constrained")
    has_legend = len(columns) > 1 or sections or state_windows
    if has_legend:
        legend_entries = len(columns) + len(sections or []) + len(state_windows or {})
        legend_rows = math.ceil(legend_entries / 2)
        grid = figure.add_gridspec(2, 1, height_ratios=(1, 0.15 * legend_rows))
        axis = figure.add_subplot(grid[0])
        legend_axis = figure.add_subplot(grid[1])
        legend_axis.set_axis_off()
    else:
        axis = figure.add_subplot()
    for column in columns:
        axis.plot(times, [row[column] for row in measurements], label=column)
    for index, (start, end) in enumerate(sections or [], start=1):
        axis.axvspan(start, end, alpha=0.12, label=f"Section {index}")
    for label, (start, end) in (state_windows or {}).items():
        color = "tab:green" if label == "Initial" else "tab:red"
        axis.axvline(start, color=color, linestyle=":", linewidth=2, label=label)
        axis.axvline(end, color=color, linestyle=":", linewidth=2)
    axis.set_title(title, fontsize=13, pad=8)
    axis.set_xlabel("Time (s)", fontsize=12)
    axis.set_ylabel(ylabel, fontsize=12)
    axis.tick_params(axis="both", labelsize=12)
    axis.xaxis.set_major_locator(MaxNLocator(nbins=4))
    axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.grid(True, alpha=0.3)
    if has_legend:
        legend_axis.legend(
            *axis.get_legend_handles_labels(), loc="center", ncol=2,
            fontsize=12, handlelength=1.2, handletextpad=0.4, columnspacing=0.8,
        )
    figure.savefig(destination, dpi=300)
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
    parser.add_argument(
        "--initial-window", type=parse_section, metavar="START:END",
        help="Time range (seconds) to average initial P1, T1, P2 and T2",
    )
    parser.add_argument(
        "--final-window", type=parse_section, metavar="START:END",
        help="Time range (seconds) to average final recorded P1, T1, P2 and T2",
    )
    args = parser.parse_args()

    try:
        measurements = read_measurements(args.file)
        section_results = [
            (start, end, mass_from_flow(measurements, start, end))
            for start, end in args.section
        ]
        state_windows = {
            label: window for label, window in (
                ("Initial", args.initial_window), ("Final", args.final_window)
            ) if window is not None
        }
        state_results = {
            label: state_averages(measurements, window)
            for label, window in state_windows.items()
        }
        output_dir = args.output_dir or args.file.parent / f"{args.file.stem}_plots"
        output_dir.mkdir(parents=True, exist_ok=True)
        graphs = (
            (("P1(PSI)", "P2(PSI)"), "Pressure Vs. Time", "Pressure (PSI)", "pressure.png"),
            (("T1(Deg C)", "T2(Deg C)"), "Temperature Vs. Time", "Temperature (°C)", "temperature.png"),
            (("Mass Flowrate(g/min)",), "Mass Flow Rate Vs. Time", "Mass Flow Rate (g/min)", "mass_flow_rate.png"),
        )
        for columns, title, ylabel, filename in graphs:
            save_graph(
                measurements, columns, title, ylabel, output_dir / filename,
                args.section if filename == "mass_flow_rate.png" else None,
                state_windows if filename != "mass_flow_rate.png" else None,
            )

        summary = (
            f"Loaded {len(measurements)} measurements from {args.file}\n"
            f"Mass-flow integral: {mass_from_flow(measurements):.6f} g\n"
        )
        for index, (start, end, mass_g) in enumerate(section_results, start=1):
            summary += f"Section {index} ({start:g}-{end:g} s): {mass_g:.6f} g\n"
        for label, (start, end) in state_windows.items():
            count, averages = state_results[label]
            summary += f"{label} recorded window ({start:g}-{end:g} s; {count} samples):\n"
            summary += (
                f"  Left tank: P1 = {averages['P1(PSI)']:.2f} psig, "
                f"T1 = {averages['T1(Deg C)']:.2f} °C\n"
                f"  Right tank: P2 = {averages['P2(PSI)']:.2f} psig, "
                f"T2 = {averages['T2(Deg C)']:.2f} °C\n"
            )
        summary += f"Graphs saved to {output_dir}\n"
        (output_dir / "summary.txt").write_text(summary, encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")

    print(summary, end="")


if __name__ == "__main__":
    main()
