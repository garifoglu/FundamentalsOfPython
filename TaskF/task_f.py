# Copyright (c) 2026 Gökhan Arifoglu
# License: MIT

import csv
from datetime import datetime, date


def read_data(filename: str) -> list[list[str]]:
    """Read CSV file and returns all rows."""

    rows = []

    with open(filename, "r", encoding="utf-8") as file:

        reader = csv.reader(file, delimiter=";")

        for row in reader:
            rows.append(row)

    return rows


def format_number(value: float) -> str:
    """Formats number with comma and two decimals."""

    return f"{value:.2f}".replace(".", ",")


def parse_date(text: str) -> date:
    """Converts dd.mm.yyyy string to date."""

    return datetime.strptime(text, "%d.%m.%Y").date()


def show_main_menu() -> str:
    """Shows main menu."""

    print("\nChoose report type:")
    print("1) Daily summary for a date range")
    print("2) Monthly summary for one month")
    print("3) Full year 2025 summary")
    print("4) Exit the program")

    return input("Choice: ").strip()


def show_after_menu() -> str:
    """Shows menu after report."""

    print("\nWhat would you like to do next?")
    print("1) Write the report to the file report.txt")
    print("2) Create a new report")
    print("3) Exit")

    return input("Choice: ").strip()


def calculate_daily(rows: list[list[str]]) -> dict:
    """Calculates daily totals."""

    daily = {}

    for row in rows[1:]:

        time_str = row[0][:19]
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
        d = dt.date()

        c = float(row[1].replace(",", "."))
        p = float(row[2].replace(",", "."))
        t = float(row[3].replace(",", "."))

        if d not in daily:
            daily[d] = [0.0, 0.0, 0.0, 0]

        daily[d][0] += c
        daily[d][1] += p
        daily[d][2] += t
        daily[d][3] += 1

    return daily


def create_daily_report(daily: dict) -> list[str]:
    """Creates daily report."""

    start_s = input("Enter start date (dd.mm.yyyy): ")
    end_s = input("Enter end date (dd.mm.yyyy): ")

    start = parse_date(start_s)
    end = parse_date(end_s)

    if end < start:
        start, end = end, start

    total_c = 0.0
    total_p = 0.0
    temp_sum = 0.0
    count = 0

    for d in daily:

        if start <= d <= end:

            total_c += daily[d][0]
            total_p += daily[d][1]
            temp_sum += daily[d][2]
            count += daily[d][3]

    avg_temp = temp_sum / count if count > 0 else 0

    lines = []

    lines.append("-" * 50)
    lines.append(f"Report for the period {start_s}–{end_s}")
    lines.append(f"- Total consumption: {format_number(total_c)} kWh")
    lines.append(f"- Total production: {format_number(total_p)} kWh")
    lines.append(f"- Average temperature: {format_number(avg_temp)} °C")

    return lines


def create_monthly_report(daily: dict) -> list[str]:
    """Creates monthly report."""

    month = int(input("Enter month number (1-12): "))

    total_c = 0.0
    total_p = 0.0
    temp_sum = 0.0
    days = 0

    for d in daily:

        if d.year == 2025 and d.month == month:

            total_c += daily[d][0]
            total_p += daily[d][1]

            day_avg = daily[d][2] / daily[d][3]
            temp_sum += day_avg

            days += 1

    avg_temp = temp_sum / days if days > 0 else 0

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    lines = []

    lines.append("-" * 50)
    lines.append(f"Report for the month: {months[month - 1]}")
    lines.append(f"- Total consumption: {format_number(total_c)} kWh")
    lines.append(f"- Total production: {format_number(total_p)} kWh")
    lines.append(f"- Average temperature: {format_number(avg_temp)} °C")

    return lines


def create_yearly_report(daily: dict) -> list[str]:
    """Creates yearly report."""

    total_c = 0.0
    total_p = 0.0
    temp_sum = 0.0
    count = 0

    for d in daily:

        if d.year == 2025:

            total_c += daily[d][0]
            total_p += daily[d][1]
            temp_sum += daily[d][2]
            count += daily[d][3]

    avg_temp = temp_sum / count if count > 0 else 0

    lines = []

    lines.append("-" * 50)
    lines.append("Report for the year 2025")
    lines.append(f"- Total consumption: {format_number(total_c)} kWh")
    lines.append(f"- Total production: {format_number(total_p)} kWh")
    lines.append(f"- Average temperature: {format_number(avg_temp)} °C")

    return lines


def print_report(lines: list[str]) -> None:
    """Prints report."""

    print()

    for line in lines:
        print(line)


def write_report(lines: list[str]) -> None:
    """Writes report to file."""

    with open("report.txt", "w", encoding="utf-8") as file:

        for line in lines:
            file.write(line + "\n")


def main() -> None:
    """Main program."""

    rows = read_data("2025.csv")

    daily = calculate_daily(rows)

    last_report = []

    while True:

        choice = show_main_menu()

        if choice == "1":
            last_report = create_daily_report(daily)

        elif choice == "2":
            last_report = create_monthly_report(daily)

        elif choice == "3":
            last_report = create_yearly_report(daily)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Wrong choice!")
            continue

        print_report(last_report)

        while True:

            after = show_after_menu()

            if after == "1":
                write_report(last_report)
                print("Saved to report.txt")

            elif after == "2":
                break

            elif after == "3":
                return

            else:
                print("Wrong choice!")


if __name__ == "__main__":
    main()