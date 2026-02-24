# Copyright (c) 2026 Ville Heikkiniemi, Luka Hietala, Luukas Kola
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by Gökhan Arifoglu according to given task

"""
A program that prints reservation information according to requirements

The data structure and example data record:

reservationId | name | email | phone | reservationDate | reservationTime | durationHours | price | confirmed | reservedResource | createdAt
------------------------------------------------------------------------
201 | Moomin Valley | moomin@whitevalley.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Forest Area 1 | 2025-08-12 14:33:20
int | str | str | str | date | time | int | float | bool | str | datetime

"""




from datetime import datetime

def convert_reservation(data: list[str]) -> dict:
    """
    Convert one reservation (list of strings) to a dictionary.
    """
    return {
        "id": int(data[0]),                                          # reservation ID (str to int)
        "name": data[1],                                             # guest name (str)
        "email": data[2],                                            # guest email (str)
        "phone": data[3],                                            # guest phone (str)
        "date": datetime.strptime(data[4], "%Y-%m-%d").date(),        # reservation date
        "time": datetime.strptime(data[5], "%H:%M").time(),          # reservation time
        "duration": int(data[6]),                                    # duration in hours (int)
        "price": float(data[7]),                                     # price per hour (float)
        "confirmed": data[8].strip() == "True",                      # confirmed or not (boolean)
        "resource": data[9],                                         # reserved resource/room (str)
        "created": datetime.strptime(data[10].strip(), "%Y-%m-%d %H:%M:%S"), # created timestamp (datetimem)
    }

def fetch_reservations(filename: str) -> list[dict]:

    """ read reservations from a file and return list of dictionaries """

    reservations = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():  # empty lines
                fields = line.split("|")
                reservations.append(convert_reservation(fields))
    return reservations



def confirmed_reservations(reservations: list[dict]):
    """ Print all confirmed reservations """
    for r in reservations:
        if r["confirmed"]:
            print(f"- {r['name']}, {r['resource']}, {r['date'].strftime('%d.%m.%Y')} at {r['time'].strftime('%H.%M')}")



def long_reservations(reservations: list[dict]):
    """ Print reservations that is longer than 3 hours or more """
    for r in reservations:
        if r["duration"] >= 3:
            print(f"- {r['name']}, {r['date'].strftime('%d.%m.%Y')} at {r['time'].strftime('%H.%M')}, duration {r['duration']} h, {r['resource']}")



def confirmation_statuses(reservations: list[dict]):
    """ Print if each reservation is confirmed or not """
    for r in reservations:
        print(f"{r['name']} → {'Confirmed' if r['confirmed'] else 'NOT Confirmed'}")



def confirmation_summary(reservations: list[dict]):
    """ Print how many reservations are confirmed and not confirmed """

    confirmed_count = sum(1 for r in reservations if r["confirmed"])
    print(f"- Confirmed reservations: {confirmed_count} pcs")
    print(f"- Not confirmed reservations: {len(reservations) - confirmed_count} pcs")



def total_revenue(reservations: list[dict]):
    """ Print total revenue of confirmed reservations """

    revenue = sum(r["duration"] * r["price"] for r in reservations if r["confirmed"])
    print(f"Total revenue from confirmed reservations: {revenue:.2f} €".replace(".", ","))



def main():

    """ read reservations and print all reports """
    reservations = fetch_reservations("reservations.txt")

    print("1) Confirmed Reservations")
    confirmed_reservations(reservations)

    print("2) Long Reservations (≥ 3 h)")
    long_reservations(reservations)

    print("3) Reservation Confirmation Status")
    confirmation_statuses(reservations)

    print("4) Confirmation Summary")
    confirmation_summary(reservations)

    print("5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)



if __name__ == "__main__":
    main()