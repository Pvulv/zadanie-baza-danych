import csv
from sqlalchemy import Table, Column, Float, Integer, DATE, String, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy import insert
from datetime import datetime

csv_file1 = 'clean_stations.csv'
csv_file2 = 'clean_measure.csv'

engine = create_engine('sqlite:///cleaning_stations.db')
connection = engine.connect()

meta = MetaData(bind=engine)

Clean_stations = Table(
    'Clean_stations', meta,
    Column('station', String, primary_key = True),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('elevation', Float),
    Column('name', String),
    Column('country', String),
    Column('state', String)
)

Clean_measure = Table(
    'Clean_measure', meta,
    Column('id', Integer, primary_key=True),
    Column('station', String, ForeignKey('Clean_stations.station')),
    Column('date', DATE),
    Column('precip', Float),
    Column('tobs', Integer),
    UniqueConstraint('station', 'date', name='uix_station_date')
)

meta.create_all(engine)

with open(csv_file1, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    records = []
    for row in reader:
        records.append({
            'station': row['station'],
            'latitude': float(row['latitude']) if row['latitude'] else None,
            'longitude': float(row['longitude']) if row['longitude'] else None,
            'elevation': float(row['elevation']) if row['elevation'] else None,
            'name': row['name'],
            'country': row['country'],
            'state': row['state']
        })
    with connection.begin() as transaction:
        try:
            connection.execute(insert(Clean_stations).prefix_with("OR IGNORE"), records)
        except Exception as e:
            print(f"Błąd przy wstawianiu do Clean_stations: {e}")
            transaction.rollback()

with open(csv_file2, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    records = []
    for row in reader:
        records.append({
            'station': row['station'],
            'date': datetime.strptime(row['date'], '%Y-%m-%d') if row['date'] else None,
            'precip': float(row['precip']) if row['precip'] else None,
            'tobs': int(row['tobs']) if row['tobs'] else None
        })
    with connection.begin() as transaction:
        try:
            connection.execute(insert(Clean_measure).prefix_with("OR IGNORE"), records)
        except Exception as e:
            print(f"Błąd przy wstawianiu do Clean_measure: {e}")
            transaction.rollback()

result = connection.execute("SELECT * FROM Clean_stations LIMIT 5").fetchall()
for row in result:
    print(row)

connection.close()