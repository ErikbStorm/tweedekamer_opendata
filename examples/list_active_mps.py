"""List currently active Tweede Kamer members."""

from tweedekamer import Client


def main() -> None:
    with Client() as client:
        mps = (
            client.personen.exclude_deleted()
            .filter("FractieZetelPersoon/any(a: a/TotEnMet eq null)")
            .select("Id", "Roepnaam", "Tussenvoegsel", "Achternaam", "Functie")
            .order_by("Achternaam")
            .top(50)
            .all()
        )

    for person in mps:
        name_parts = [person.roepnaam, person.tussenvoegsel, person.achternaam]
        name = " ".join(p for p in name_parts if p)
        print(f"{name:40} {person.functie or ''}")


if __name__ == "__main__":
    main()
