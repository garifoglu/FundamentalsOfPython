# Copyright (c) 2026 Gökhan Arifoglu
# License: MIT


from datetime import datetime, date

def read_data(filename: str) -> list:

    data = []
    with open(filename, "r", encoding="utf-8") as file:
        next(file)  
        for line in file:
            parts = line.strip().split(";")
            time = datetime.strptime(parts[0], "%Y-%m-%dT%H:%M:%S")
            values = [float(x) if x else 0.0 for x in parts[1:]]
            data.append([time] + values)
    return data

def main() -> None:

    data = read_data("week42.csv")
    
    print("Week 42 electricity consumption and production (kWh, by phase)\n")
    print("Day          Date        Consumption [kWh]               Production [kWh]")
    print("            (dd.mm.yyyy)  v1      v2      v3             v1     v2     v3")
    print("---------------------------------------------------------------------------")
    
    
    days = [
        date(2025, 10, 13),  # Monday
        date(2025, 10, 14),  # Tuesday
        date(2025, 10, 15),  # Wednesday
        date(2025, 10, 16),  # Thursday
        date(2025, 10, 17),  # Friday
        date(2025, 10, 18),  # Saturday
        date(2025, 10, 19),  # Sunday
    ]

    weekdays_fi = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]

    
    for i in range(len(days)):
        current_day = days[i]
        c1 = c2 = c3 = p1 = p2 = p3 = 0.0
        
        for row in data:
            if row[0].date() == current_day:
                c1 += row[1] / 1000  
                c2 += row[2] / 1000  
                c3 += row[3] / 1000  
                p1 += row[4] / 1000  
                p2 += row[5] / 1000  
                p3 += row[6] / 1000 
        
        c1_str = f"{c1:.2f}".replace(".", ",")
        c2_str = f"{c2:.2f}".replace(".", ",")
        c3_str = f"{c3:.2f}".replace(".", ",")
        p1_str = f"{p1:.2f}".replace(".", ",")
        p2_str = f"{p2:.2f}".replace(".", ",")
        p3_str = f"{p3:.2f}".replace(".", ",")
        
        print(f"{weekdays_fi[i]:<11} {current_day.strftime('%d.%m.%Y')} "
              f"{c1_str:>6}  {c2_str:>5}  {c3_str:>7}     "
              f"{p1_str:>10}  {p2_str:>5}  {p3_str:>5}")

if __name__ == "__main__":
    main()