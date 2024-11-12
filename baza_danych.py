import csv
from sqlalchemy import Table, Column, Float, Integer, DATE, String, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy import insert
from datetime import datetime

csv_file1 = 'clean_stations.csv'
csv_file2 = 'clean_measure.csv'

engine = create_engine('sqlite:///cleaning_stations.db')
connection = engine.connect()