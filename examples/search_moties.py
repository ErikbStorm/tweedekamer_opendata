"""Search recent motions (moties)."""

from tweedekamer import Client


def main() -> None:
    with Client() as client:
        moties = (
            client.zaken.exclude_deleted()
            .filter("Soort eq 'Motie'")
            .order_by("GestartOp", desc=True)
            .select("Id", "Nummer", "Titel", "GestartOp", "Status")
            .top(10)
            .all()
        )

        total = client.zaken.exclude_deleted().filter("Soort eq 'Motie'").count()
        print(f"Showing {len(moties)} recent moties (total matching: {total})")
        for zaak in moties:
            title = (zaak.titel or "")[:80]
            print(f"{zaak.nummer}  {zaak.gestart_op}  {title}")


if __name__ == "__main__":
    main()
