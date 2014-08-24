#!/usr/bin/python
import pygal
import sqlite3

# Create or open a data.db database 
db = sqlite3.connect('/home/pi/MyPi/sensors/data.db')
db.row_factory = sqlite3.Row

curs = db.cursor()
curs.execute("SELECT * FROM sensors WHERE sensors.timestamp > datetime('now', '-1 hour')")

light = []
pot = []
for row in curs:
	#print('{0} : {1} : {2}'.format(row['timestamp'], row['pot'], row['light']))
	light.append(row['light'])
	pot.append(row['pot'])
#db.commit()
db.close()

line_chart = pygal.Line(range=(0, 1023))
line_chart.title = 'Light and Pot'
line_chart.add('light', light)
line_chart.add('pot', pot)

line_chart.render_to_file('/var/www/images/sensors.svg')
