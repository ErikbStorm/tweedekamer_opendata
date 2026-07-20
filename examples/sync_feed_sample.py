"""Fetch one SyncFeed page for Zaak entities."""

from tweedekamer import SyncFeedClient


def main() -> None:
    with SyncFeedClient() as feed:
        page = feed.fetch(category="Zaak")
        print(f"Title: {page.title}")
        print(f"Entries: {len(page.entries)}")
        print(f"Next skiptoken: {page.skip_token}")
        for entry in page.entries[:5]:
            payload = entry.payload
            nummer = payload.get("nummer")
            soort = payload.get("soort")
            print(f"  {entry.updated}  {soort!s:20}  {nummer}")


if __name__ == "__main__":
    main()
