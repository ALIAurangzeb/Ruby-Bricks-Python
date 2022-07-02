import sqlite3

conn = sqlite3.connect("RubyBricks.db")
print("Opened database successfully")

#query for Creating Contacts table
#conn.execute("Create table Contact (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name Text,Email Text,Subject Text,Message Text)")

#query for Creating Property table
#conn.execute("Create table Property (Id integer Primary key Autoincrement Not Null, Area integer,Bedrooms integer,Bathrooms integer,Garage integer,Stories integer,YearBuild integer,PropertyFor integer,Images Blob,Description Text,Furnished integer,PostCode Text,PropertyType Text,ImagePath Text,ImageName Text)")

print("Table Created successfully")

conn.close() 