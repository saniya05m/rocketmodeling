import sqlite3

conn = sqlite3.connect('Launch_Data.db')  # создание базы данных со всеми нужными файлами
c = conn.cursor()

# создание таблицы WeatherFiles для файлов об атмосферных данных
c.execute('''CREATE TABLE WeatherFiles
             ([generated_id] INTEGER PRIMARY KEY,[File_Path] text, [Year] integer)''')

# создание таблицы Motors для файлов с информацией о характеристиках моторов
c.execute('''CREATE TABLE Motors
             ([generated_id] INTEGER PRIMARY KEY,[File_Path] text, [Motor_Name] text)''')
c.execute('''CREATE TABLE Rockets
             ([generated_id] INTEGER PRIMARY KEY,[File_Path] text, [Rocket_Name] text)''')
# вставка всех необходимых файлов
c.execute("INSERT INTO WeatherFiles (File_Path, Year) VALUES ('../data/weather/Alcantara_2018_"
          "ERA-5.nc', 2018)")
conn.commit()
c.execute("""INSERT INTO WeatherFiles (File_Path, Year) VALUES ('data/weather/Alcantara_2017_ERA-5.nc', 2017)""")
conn.commit()
c.execute("""INSERT INTO WeatherFiles (File_Path, Year) VALUES ('data/weather/Alcantara_2019_ERA-5.nc', 2019)""")
conn.commit()
c.execute("""INSERT INTO WeatherFiles (File_Path, Year) VALUES ('data/weather/Alcantara_2020_ERA-5.nc', 2020)""")
conn.commit()
c.execute(
    """INSERT INTO WeatherFiles (File_Path, Year) VALUES ('data/weather/CLBI_2018_ERA-5.nc', 2018)""")
conn.commit()
c.execute(
    """INSERT INTO WeatherFiles (File_Path, Year) VALUES ('data/weather/CLBI_2019_ERA-5.nc', 2019)""")
conn.commit()
c.execute(
    """INSERT INTO WeatherFiles (File_Path, Year) VALUES ('data/weather/CLBI_2020_ERA-5.nc', 2020)""")
conn.commit()
c.execute(
    """INSERT INTO WeatherFiles (File_Path, Year) VALUES ('data/weather/CLBI_2017_ERA-5.nc', 2017)""")
conn.commit()
c.execute("""INSERT INTO WeatherFiles (File_Path, Year) VALUES ('data/weather/SpaceportAmerica_2018_ERA-5.nc', 2018)""")
conn.commit()
c.execute("""INSERT INTO WeatherFiles (File_Path, Year) VALUES ('data/weather/SpaceportAmerica_2017_ERA-5.nc', 2017)""")
conn.commit()
c.execute("""INSERT INTO WeatherFiles (File_Path, Year) VALUES ('data/weather/SpaceportAmerica_2020_ERA-5.nc', 2020)""")
conn.commit()
c.execute("""INSERT INTO WeatherFiles (File_Path, Year) VALUES ('data/weather/SpaceportAmerica_2019_ERA-5.nc', 2019)""")
conn.commit()

c.execute("""INSERT INTO Motors (File_Path, Motor_Name) VALUES ('data/motors/Hypertek_J115.eng', 'Hypertek_J115')""")
conn.commit()
c.execute("""INSERT INTO Motors (File_Path, Motor_Name) VALUES ('data/motors/Cesaroni_M1400.eng', 'Cesaroni_M1400')""")
conn.commit()
c.execute("""INSERT INTO Motors (File_Path, Motor_Name) VALUES ('data/motors/Cesaroni_J360.eng', 'Cesaroni_J360')""")
conn.commit()
c.execute("""INSERT INTO Motors (File_Path, Motor_Name) VALUES ('data/motors/Cesaroni_M1300.eng', 'Cesaroni_M1300')""")
conn.commit()
c.execute(
    """INSERT INTO Motors (File_Path, Motor_Name) VALUES ('data/motors/Cesaroni_7450M2505-P.eng', 
    'Cesaroni_7450M2505')""")
conn.commit()
c.execute("""INSERT INTO Motors (File_Path, Motor_Name) VALUES ('data/motors/Cesaroni_M3100.eng', 'Cesaroni_M3100')""")
conn.commit()
c.execute(
    """INSERT INTO Motors (File_Path, Motor_Name) VALUES ('data/motors/Cesaroni_7450M2505-P.csv', 'Cesaroni_M1540')""")
conn.commit()
c.execute("""INSERT INTO Motors (File_Path, Motor_Name) VALUES ('data/motors/Cesaroni_M1540.eng', 'Cesaroni_M1540')""")
conn.commit()
c.execute("""INSERT INTO Motors (File_Path, Motor_Name) VALUES ('data/motors/Cesaroni_M1670.eng', 'Cesaroni_M1670')""")
conn.commit()
c.execute(
    """INSERT INTO Rockets (File_Path, Rocket_Name) VALUES ('data/caldene/drag.csv', 'Caldene')""")
conn.commit()
c.execute(
    """INSERT INTO Rockets (File_Path, Rocket_Name) VALUES ('data/euporia/euporiaDrag.csv', 'Euporia')""")
conn.commit()
c.execute(
    """INSERT INTO Rockets (File_Path, Rocket_Name) VALUES ('data/jiboia/thrustCurve.csv', 'Jiboia')""")
conn.commit()
c.execute(
    """INSERT INTO Rockets (File_Path, Rocket_Name) VALUES ('data/keron/thrustCurve.csv', 'Keron')""")
conn.commit()
c.execute("""INSERT INTO Rockets (File_Path, Rocket_Name) VALUES ('data/mandioca/thrustCurve.csv', 'Mandioca')""")
conn.commit()
c.execute("""INSERT INTO Rockets (File_Path, Rocket_Name) VALUES ('data/calisto/powerOnDragCurve.csv', 'Calisto')""")
conn.commit()
