from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)

with sqlite3.connect((ROOT/'data'/'warehouse.db').as_uri()+'?mode=ro', uri=True) as con:
    df = pd.read_sql_query('SELECT * FROM sales', con)

print(df.head())

# P1: province x month, sum(amount), fill_value=0, margins=True
p1 = pd.pivot_table(
    df,
    index='province',
    columns='month',
    values='amount',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Total'
)
print('\nP1 - Province x Month')
print(p1)
p1.to_csv(OUT/'pivot_province_month.csv', encoding='utf-8-sig')

# P2: September only, category x province
sep = df[df['month'] == '2026-09']
p2 = pd.pivot_table(
    sep,
    index='category',
    columns='province',
    values='amount',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Total'
)
print('\nP2 - September Category x Province')
print(p2)
p2.to_csv(OUT/'pivot_september.csv', encoding='utf-8-sig')

# P3: Grand Total validation
assert p1.loc['Total', 'Total'] == df['amount'].sum()
print('\nASSERT PASSED:', p1.loc['Total', 'Total'], '==', df['amount'].sum())

# Optional substitute for Excel activity: Drink-only pivot
p_drink = pd.pivot_table(
    df[df['category'] == 'Drink'],
    index='province',
    columns='month',
    values='amount',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Total'
)
print('\nDrink-only Pivot')
print(p_drink)
p_drink.to_csv(OUT/'pivot_drink.csv', encoding='utf-8-sig')
