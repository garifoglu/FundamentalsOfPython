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

class Reservation:
    """ store one reservation """
    

    def __init__(self, reservation_id, name, email, phone, date, time, duration, price, confirmed, resource, created):
        self.id = reservation_id        # reservation ID
        self.name = name                # name
        self.email = email              # email
        self.phone = phone              # phone
        self.date = date                # reservation date
        self.time = time                # reservation time
        self.duration = duration        # duration
        self.price = price              # price per hour
        self.confirmed = confirmed      # confirmed or not
        self.resource = resource        # reserved resource
        self.created = created          # created timestamp

    def is_confirmed(self):
        """ return true if reservation is confirmed """
        return self.confirmed

    def is_long(self):
        """ return true if reservation is longer than 3 hours or more """
        return self.duration >= 3

    def total_price(self):
        """ Calculate total price """
        return self.duration * self.price

def convert_reservation(data: list[str]) -> Reservation:
    """ Convert a line from file into a Reservation object """


    return Reservation(
        
        reservation_id=int(data[0]),
        name=data[1],
        email=data[2],
        phone=data[3],
        date=datetime.strptime(data[4], "%Y-%m-%d").date(),
        time=datetime.strptime(data[5], "%H:%M").time(),
        duration=int(data[6]),
        price=float(data[7]),
        confirmed=data[8].strip() == "True",
        resource=data[9],
        created=datetime.strptime(data[10].strip(), "%Y-%m-%d %H:%M:%S")
    )

def fetch_reservations(filename: str) -> list[Reservation]:
    """ read reservations from file and return a list of Reservation """


    reservations = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                fields = line.split("|")
                reservations.append(convert_reservation(fields))
    return reservations



def confirmed_reservations(reservations: list[Reservation]):
    """ Print all confirmed reservations """

    for r in reservations:
        if r.is_confirmed():
            print(f"- {r.name}, {r.resource}, {r.date.strftime('%d.%m.%Y')} at {r.time.strftime('%H.%M')}")

def long_reservations(reservations: list[Reservation]):
    """ Print reservations that is longer than 3 hours or more """

    for r in reservations:
        if r.is_long():
            print(f"- {r.name}, {r.date.strftime('%d.%m.%Y')} at {r.time.strftime('%H.%M')}, duration {r.duration} h, {r.resource}")


def confirmation_statuses(reservations: list[Reservation]):
    """ Print if each reservation is confirmed or not """

    for r in reservations:
        print(f"{r.name} → {'Confirmed' if r.is_confirmed() else 'NOT Confirmed'}")



def confirmation_summary(reservations: list[Reservation]):
    """ Print summary of confirmed and not confirmed reservations """


    confirmed_count = sum(1 for r in reservations if r.is_confirmed())
    print(f"- Confirmed reservations: {confirmed_count} pcs")
    print(f"- Not confirmed reservations: {len(reservations) - confirmed_count} pcs")



def total_revenue(reservations: list[Reservation]):
    """ Print total revenue from confirmed reservations """


    revenue = sum(r.total_price() for r in reservations if r.is_confirmed())
    print(f"Total revenue from confirmed reservations: {revenue:.2f} €".replace(".", ","))



def main():
    """ read reservations and print all report """

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