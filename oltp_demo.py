from pathlib import Path
import sqlite3

p = Path(__file__).resolve().parent / 'data' / 'oltp.db'
if not p.exists():
    raise SystemExit('Run lab.py first')

with sqlite3.connect(p) as con:
    print('Before:', con.execute('SELECT * FROM orders').fetchall())
    cur = con.execute(
        "UPDATE orders SET status='PAID' WHERE order_id=? AND status=?",
        ('O1004', 'PENDING')
    )
    print('Rows affected:', cur.rowcount)
    con.commit()
    print('After:', con.execute('SELECT * FROM orders').fetchall())
