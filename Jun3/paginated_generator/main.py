import sqlite3
from dataclasses import dataclass
from typing import Generator, Generic, TypeVar

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    number: int
    rows: list[T]
    has_next: bool


def paginated_sql(
    conn: sqlite3.Connection,
    query: str,
    params: tuple = (),
    page_size: int = 100,
) -> Generator[Page, None, None]:
    """Yield pages of dicts from a raw SQL query."""
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    page_num = 0
    while True:
        offset = page_num * page_size
        cursor.execute(f"{query} LIMIT {page_size} OFFSET {offset}", params)
        rows = [dict(r) for r in cursor.fetchall()]
        if not rows:
            return
        has_next = len(rows) == page_size
        yield Page(number=page_num, rows=rows, has_next=has_next)
        if not has_next:
            return
        page_num += 1


conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE orders (
        id     INTEGER PRIMARY KEY,
        item   TEXT,
        status TEXT
    )
""")
conn.executemany(
    "INSERT INTO orders (item, status) VALUES (?, ?)",
    [(f"Item-{i}", "pending" if i % 3 != 0 else "shipped") for i in range(1, 250)],
)
conn.commit()

for page in paginated_sql(
    conn,
    query="SELECT * FROM orders WHERE status = ?",
    params=("pending",),
    page_size=50,
):
    print(f"Page {page.number}: {len(page.rows)} rows  |  has_next={page.has_next}")
    if page.number == 0:
        print(f"  first row → {page.rows[0]}")

conn.close()
