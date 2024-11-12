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