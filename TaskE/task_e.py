# Copyright (c) 2026 Your Name
# License: MIT

from datetime import datetime, date

# Finnish weekday names (Mon ... Sun)
DAYS_FI = [
    "maanantai", "tiistai", "keskiviikko",
    "torstai", "perjantai", "lauantai", "sunnuntai"
]


def read_data(filename: str) -> list:
    """ Reads CSV file and returns data """

    data = []

    with open(filename, "r", encoding="utf-8") as file:
        next(file)  # skip header

        for line in file:
            parts = line.strip().split(";")
            time = datetime.strptime(parts[0], "%Y-%m-%dT%H:%M:%S")
            values = [float(x) if x else 0.0 for x in parts[1:]]
            data.append([time] + values)

    return data


def format_number(value: float) -> str:
    """ Changes dot to comma and formats number """
    return f"{value:.2f}".replace(".", ",")


def calculate_day(data: list, day: date) -> list:
    """ Calculates daily totals for one day """

    c1 = c2 = c3 = p1 = p2 = p3 = 0.0

    for row in data:
        if row[0].date() == day:
            c1 += row[1]
            c2 += row[2]
            c3 += row[3]
            p1 += row[4]
            p2 += row[5]
            p3 += row[6]

    return [c1, c2, c3, p1, p2, p3]


def build_week(week_no: int, filename: str, days: list) -> str:
    """ Builds report for one week """

    data = read_data(filename)
    lines = []

    lines.append(f"Week {week_no} electricity consumption and production (kWh, by phase)\n")
    lines.append("Day          Date        Consumption [kWh]               Production [kWh]")
    lines.append("            (dd.mm.yyyy)  v1      v2      v3             v1     v2     v3")
    lines.append("-" * 75)

    for day in days:
        values = calculate_day(data, day)
        weekday = DAYS_FI[day.weekday()]

        # convert Wh → kWh
        c1 = format_number(values[0] / 1000)
        c2 = format_number(values[1] / 1000)
        c3 = format_number(values[2] / 1000)
        p1 = format_number(values[3] / 1000)
        p2 = format_number(values[4] / 1000)
        p3 = format_number(values[5] / 1000)

        line = (
            f"{weekday:<11} "
            f"{day.strftime('%d.%m.%Y'):<12} "
            f"{c1:>5}  {c2:>5}  {c3:>7}     "
            f"{p1:>10}  {p2:>5}  {p3:>5}"
        )
        lines.append(line)

    lines.append("")
    return "\n".join(lines)


def write_report(text: str) -> None:
    """ Writes report to file """
    with open("summary.txt", "w", encoding="utf-8") as file:
        file.write(text)


def main() -> None:
    """ Builds reports for all weeks """

    weeks = [
        (41, "week41.csv", [date(2025, 10, d) for d in range(6, 13)]),
        (42, "week42.csv", [date(2025, 10, d) for d in range(13, 20)]),
        (43, "week43.csv", [date(2025, 10, d) for d in range(20, 27)]),
    ]

    report = ""
    for week_no, filename, days in weeks:
        report += build_week(week_no, filename, days)
        report += "\n"

    write_report(report)


if __name__ == "__main__":
    main()
