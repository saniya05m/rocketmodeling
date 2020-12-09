import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QDateEdit, QRadioButton, QHBoxLayout, \
    QButtonGroup, QVBoxLayout
from rocketpy import Environment, SolidMotor, Rocket, Flight
import sqlite3
import datetime


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        con = sqlite3.connect("Launch_Data.db")
        self.cur = con.cursor()
        self.setGeometry(0, 0, 1500, 800)
        self.setWindowTitle('Моделирование движения ракеты')
        layout = QVBoxLayout()  # установка стиля расположения UI элементов вертикально

        # создание интерфэйса
        # Поле для ввода широты
        self.Latitudelabel = QLabel(self)
        self.Latitudelabel.setText("Latitude")
        self.Latitudelabel.move(20, 30)
        self.Latitudelabel.resize(120, 20)
        layout.addWidget(self.Latitudelabel)

        self.LatitudeInput = QLineEdit(self)
        self.LatitudeInput.setText('70')
        self.LatitudeInput.move(80, 30)
        self.LatitudeInput.resize(125, 20)
        layout.addWidget(self.LatitudeInput)
        # при изменений значения поля ввода вызывается функция adjustLatitude
        self.LatitudeInput.textChanged.connect(self.adjustLatitude)

        # поля для ввода долготы
        self.LongitudeLabel = QLabel(self)
        self.LongitudeLabel.setText("Longitude")
        self.LongitudeLabel.move(20, 60)
        layout.addWidget(self.LongitudeLabel)

        self.LongitudeInput = QLineEdit(self)
        self.LongitudeInput.setText('-90')
        self.LongitudeInput.move(80, 60)
        self.LongitudeInput.resize(125, 20)
        layout.addWidget(self.LongitudeInput)
        self.LongitudeInput.textChanged.connect(self.adjustLongitude)

        # поля для ввода высоты над уровнем моря
        self.ElevationLabel = QLabel(self)
        self.ElevationLabel.setText("Elevation")
        self.ElevationLabel.move(20, 90)
        layout.addWidget(self.ElevationLabel)

        self.ElevationInput = QLineEdit(self)
        self.ElevationInput.setText('560')
        self.ElevationInput.move(80, 90)
        self.ElevationInput.resize(125, 20)
        layout.addWidget(self.ElevationInput)

        # поля для ввода угла наклона ракеты
        self.InclinationLabel = QLabel(self)
        self.InclinationLabel.setText("Inclination")
        layout.addWidget(self.InclinationLabel)

        self.InclinationInput = QLineEdit(self)
        self.InclinationInput.setText('85')
        layout.addWidget(self.InclinationInput)
        self.InclinationInput.textChanged.connect(self.adjustInclination)

        # поля для ввода даты запуска
        self.DateLabel = QLabel(self)
        self.DateLabel.move(20, 120)
        self.DateLabel.setText("Date")
        layout.addWidget(self.DateLabel)

        # текущяя дата
        now = datetime.datetime.now()
        self.DateInput = QDateEdit(self)
        self.DateInput.setDate(now)
        self.DateInput.move(80, 120)
        self.DateInput.resize(125, 20)
        layout.addWidget(self.DateInput)
        self.DateInput.dateTimeChanged.connect(self.adjustDate)

        # кнопка для получения графиков об атмосферных условиях в ту дату
        self.EnvironmentInfo = QPushButton("Environment")
        self.EnvironmentInfo.move(20, 150)
        layout.addWidget(self.EnvironmentInfo)
        self.EnvironmentInfo.clicked.connect(self.EnvironmentD)

        # группирование все радио кнопок для выбора ввида мотора
        self.motorgroup = QButtonGroup()

        self.m7450 = QRadioButton("Cesaroni 7450M2505")
        self.m7450.move(20, 180)
        self.motorgroup.addButton(self.m7450)
        layout.addWidget(self.m7450)
        # заранее активирование одной радио кнопки
        self.m7450.setEnabled(True)
        # каждый раз при выборе этой радикнопки вызывается функция для установки текущего выбора
        self.m7450.toggled.connect(lambda: self.setMotor(self.m7450.text()))

        self.j360 = QRadioButton("Cesaroni J360")
        self.j360.move(20, 210)
        self.motorgroup.addButton(self.j360)
        layout.addWidget(self.j360)
        self.j360.toggled.connect(lambda: self.setMotor(self.j360.text()))

        self.m1300 = QRadioButton("Cesaroni M1300")
        self.motorgroup.addButton(self.m1300)
        layout.addWidget(self.m1300)
        self.m1300.toggled.connect(lambda: self.setMotor(self.m1300.text()))

        self.m1400 = QRadioButton("Cesaroni M1400")
        self.motorgroup.addButton(self.m1400)
        layout.addWidget(self.m1400)
        self.m1400.toggled.connect(lambda: self.setMotor(self.m1400.text()))

        self.m1540 = QRadioButton("Cesaroni M1540")
        self.motorgroup.addButton(self.m1540)
        layout.addWidget(self.m1540)
        self.m1540.toggled.connect(lambda: self.setMotor(self.m1540.text()))

        self.m1670 = QRadioButton("Cesaroni M1670")
        self.motorgroup.addButton(self.m1670)
        layout.addWidget(self.m1670)
        self.m1670.toggled.connect(lambda: self.setMotor(self.m1670.text()))

        self.m3100 = QRadioButton("Cesaroni M3100")
        self.motorgroup.addButton(self.m3100)
        layout.addWidget(self.m3100)
        self.m3100.toggled.connect(lambda: self.setMotor(self.m3100.text()))

        self.j115 = QRadioButton("Hypertek J115")
        self.motorgroup.addButton(self.j115)
        layout.addWidget(self.j115)
        self.j115.toggled.connect(lambda: self.setMotor(self.j115.text()))

        # кнопка для вывода графика сопротивления со временем мотора
        self.motorinfo = QPushButton("Motor")
        layout.addWidget(self.motorinfo)
        # при нажатий вызывается функция для вывода графика
        self.motorinfo.clicked.connect(self.motorInfo)

        # группирование всех радио кнопок для выбора ракеты
        self.rocketgroup = QButtonGroup()

        self.caldene = QRadioButton("Caldene")
        self.rocketgroup.addButton(self.caldene)
        layout.addWidget(self.caldene)
        self.caldene.toggled.connect(lambda: self.setRocket(self.caldene.text()))
        # заранее выбор одной из радио кнопок
        self.caldene.setEnabled(True)

        # создание радио кнопок для выбора вида ракеты
        self.calisto = QRadioButton("Calisto")
        self.rocketgroup.addButton(self.calisto)
        layout.addWidget(self.calisto)
        # при выборе вызов функций меняющий текущий вид ракеты
        self.calisto.toggled.connect(lambda: self.setRocket(self.calisto.text()))

        self.europia = QRadioButton("Euporia")
        self.rocketgroup.addButton(self.europia)
        layout.addWidget(self.europia)
        self.europia.toggled.connect(lambda: self.setRocket(self.europia.text()))

        self.jiboia = QRadioButton("Jiboia")
        self.rocketgroup.addButton(self.jiboia)
        layout.addWidget(self.jiboia)
        self.jiboia.toggled.connect(lambda: self.setRocket(self.jiboia.text()))

        self.keron = QRadioButton("Keron")
        self.rocketgroup.addButton(self.keron)
        layout.addWidget(self.keron)
        self.keron.toggled.connect(lambda: self.setRocket(self.keron.text()))

        self.mandioca = QRadioButton("Mandioca")
        self.rocketgroup.addButton(self.mandioca)
        layout.addWidget(self.mandioca)
        self.mandioca.toggled.connect(lambda: self.setRocket(self.mandioca.text()))

        # кнопка при нажатий выдаёт график траекторий полёта ракеты
        self.trajectory = QPushButton("Trajectory")
        layout.addWidget(self.trajectory)
        self.trajectory.clicked.connect(self.GetTrajectory)

        # кнопка при нажатий выдаёт график кинематических данных полёта
        self.kinematics = QPushButton("Kinematics data")
        layout.addWidget(self.kinematics)
        self.kinematics.clicked.connect(self.GetKinematics)

        # кнопка при нажатий выдаёт график скоростный данных
        self.altitude = QPushButton("Altitude data")
        layout.addWidget(self.altitude)
        self.altitude.clicked.connect(self.GetAltitude)

        # кнопка при нажатий выдаёт график данных об энергий во время полёта
        self.energy = QPushButton("Energy Data")
        layout.addWidget(self.energy)
        self.energy.clicked.connect(self.GetEnergy)

        # "растягиваем" расположение чтобы элементы UI оказались на верхней стороне окна
        layout.addStretch(1)
        # добавляем новый стиль горизонтального расположения
        horlayout = QHBoxLayout()
        # "растягиваем" горизонтальное расположение чтобы UI оказался на правой стороне
        horlayout.addStretch(1)
        # соедениям оба стиля расположения в одно
        horlayout.addLayout(layout)
        # устанавливаем расположение
        self.setLayout(horlayout)

    # функция проверяет поле широты на попадание в диапозон -90,90 иначе меняет значение на полях
    def adjustLatitude(self):
        latitude = self.LatitudeInput.text()
        if latitude != '' and latitude != '-':
            latitude = int(latitude)
            if latitude < -90:
                self.LatitudeInput.setText("-90")
            elif latitude > 90:
                self.LatitudeInput.setText("90")

    # функция проверяет поле долготы на попадание в диапозон -180,180 иначе меняет значение на полях
    def adjustLongitude(self):
        longitude = self.LongitudeInput.text()
        if longitude != '' and longitude != '-':
            longitude = int(longitude)
            if longitude < -180:
                self.LongitudeInput.setText("-180")
            elif longitude > 180:
                self.LongitudeInput.setText("180")

    # функция проверяет поле угла наклона ракеты на попадание в диапозон 0,90 иначе меняет значение на полях
    def adjustInclination(self):
        inclination = self.InclinationInput.text()
        if inclination != '' and inclination != '-':
            inclination = int(inclination)
            if inclination < 0:
                self.InclinationInput.setText("0")
            elif inclination > 90:
                self.InclinationInput.setText("90")

    # функция проверяет введенный год на попадание в диапозон 2017,2020 иначе меняет значение года
    def adjustDate(self):
        date = self.DateInput.date()
        if date.year() < 2017:
            date.setDate(2017, date.month(), date.day())
        elif date.year() > 2020:
            date.setDate(2020, date.month(), date.day())
        self.DateInput.setDate(date)

    # функция выводящее график об атмосферных данных в введенную дату и в введенных координатах
    def EnvironmentD(self):
        self.setEnvironment()
        self.Env.info()

    # функция инициализируещее атмосферные данные в модуле Environment
    def setEnvironment(self):
        self.longitude = int(self.LongitudeInput.text())
        self.elevation = int(self.ElevationInput.text())
        self.date = self.DateInput.date()
        self.latitude = int(self.LatitudeInput.text())

        # подстраивание значений под диапозоны имеющихся данных
        if self.latitude > -90 and self.latitude < -30:
            self.Env = Environment(railLength=5.2,
                                   date=(self.date.year() - 2, self.date.month(), self.date.day(), 6),
                                   latitude=-7.5 + 3 * (-90 - self.latitude) / -60,
                                   longitude=324 + (2.25 * (-180 - self.longitude) / -360),
                                   elevation=self.elevation)
            # получение значения файла о погоде из базы данных
            weatherfile = self.cur.execute(
                '''SELECT File_Path FROM WeatherFiles WHERE File_Path LIKE "%CLBI%" AND Year=?''',
                (self.date.year(),)).fetchone()

            self.Env.setAtmosphericModel(type='Reanalysis', file=weatherfile[0],
                                         dictionary='ECMWF')
        elif self.latitude >= -30 and self.latitude < 30:
            self.Env = Environment(railLength=5.2,
                                   date=(self.date.year() - 2, self.date.month(), self.date.day(), 6),
                                   latitude=-3.75 + 5.25 * (-30 - self.latitude) / -60,
                                   longitude=314.25 + 3 * (-180 - self.longitude) / -360,
                                   elevation=self.elevation)

            weatherfile = self.cur.execute(
                '''SELECT File_Path FROM WeatherFiles WHERE File_Path LIKE "%Alcantara%" AND Year=?''',
                (self.date.year(),)).fetchone()

            self.Env.setAtmosphericModel(type='Reanalysis', file=weatherfile[0],
                                         dictionary='ECMWF')
        elif self.latitude >= 30 and self.latitude <= 90:
            self.Env = Environment(railLength=5.2,
                                   date=(self.date.year() - 2, self.date.month(), self.date.day(), 6),
                                   latitude=31.5 + 3 * (90 - self.latitude) / 60,
                                   longitude=252 + 2.25 * (-180 - self.longitude) / -360,
                                   elevation=self.elevation)
            weatherfile = self.cur.execute(
                '''SELECT File_Path FROM WeatherFiles WHERE File_Path LIKE "%Spaceport%" AND Year=?''',
                (self.date.year(),)).fetchone()

            self.Env.setAtmosphericModel(type='Reanalysis', file=weatherfile[0],
                                         dictionary='ECMWF')

    # функция назначает имя текущего выбранного мотора из группы радиокнопок
    def setMotor(self, name):
        name = name.split()
        name = '_'.join(name)
        self.motorName = name

    # функция инициализирует модель ракеты внутри модуля SolidMotor
    def setMotorModel(self):
        motorfile = self.cur.execute('SELECT File_Path FROM Motors WHERE Motor_Name=?', (self.motorName,)).fetchone()
        motorfile = str(motorfile[0])
        self.motor_model = SolidMotor(
            thrustSource=motorfile,
            burnOut=3.9,
            grainNumber=5,
            grainSeparation=5 / 1000,
            grainDensity=1815,
            grainOuterRadius=33 / 1000,
            grainInitialInnerRadius=15 / 1000,
            grainInitialHeight=120 / 1000,
            nozzleRadius=33 / 1000,
            throatRadius=11 / 1000,
            interpolationMethod='linear'
        )

    # функция выводит график сопротивления мотора
    def motorInfo(self):
        self.setMotorModel()
        self.motor_model.info()

    # функция назначает текущее имя выбранного типа ракеты
    def setRocket(self, name):
        self.rocketName = name

    # функция инициализирует модель ракеты с помощью модуля Rocket
    def setRocketModel(self):
        self.inclination = int(self.InclinationInput.text())
        # получение файла толчка из базы данных
        thrustcurve = self.cur.execute('SELECT File_Path FROM Rockets WHERE Rocket_Name=?',
                                       (self.rocketName,)).fetchone()
        thrustcurve = str(thrustcurve[0])
        self.RocketModel = Rocket(
            motor=self.motor_model,
            radius=127 / 2000,
            mass=19.197 - 2.956,
            inertiaI=6.60,
            inertiaZ=0.0351,
            distanceRocketNozzle=-1.255,
            distanceRocketPropellant=-0.85704,
            powerOffDrag="data/calisto/powerOffDragCurve.csv",
            powerOnDrag=thrustcurve
        )
        self.RocketModel.setRailButtons([0.2, -0.5])
        # добавление деталей в модель ракеты по модулю Rocket
        NoseCone = self.RocketModel.addNose(length=0.55829, kind="vonKarman", distanceToCM=0.71971)

        FinSet = self.RocketModel.addFins(4, span=0.100, rootChord=0.120, tipChord=0.040, distanceToCM=-1.04956)

        Tail = self.RocketModel.addTail(topRadius=0.0635, bottomRadius=0.0435, length=0.060, distanceToCM=-1.194656)
        # добавление парашютов
        Main = self.RocketModel.addParachute('Main',
                                             CdS=10.0,
                                             trigger=self.mainTrigger,
                                             samplingRate=105,
                                             lag=1.5,
                                             noise=(0, 8.3, 0.5))

        Drogue = self.RocketModel.addParachute('Drogue',
                                               CdS=1.0,
                                               trigger=self.drogueTrigger,
                                               samplingRate=105,
                                               lag=1.5,
                                               noise=(0, 8.3, 0.5))

        self.TestFlight = Flight(rocket=self.RocketModel, environment=self.Env, inclination=self.inclination, heading=0)

    # функции активаций парашютов
    def drogueTrigger(self, p, y):
        return True if y[5] < 0 else False

    def mainTrigger(self, p, y):
        return True if y[5] < 0 and y[2] < 800 else False

    # функция выдаёт траекторию ракеты
    def GetTrajectory(self):
        self.setMotorModel()
        self.setEnvironment()
        self.setRocketModel()
        self.TestFlight.plot3dTrajectory()

    # функция выдаёт график кинематических данных
    def GetKinematics(self):
        self.setMotorModel()
        self.setEnvironment()
        self.setRocketModel()
        self.TestFlight.plotLinearKinematicsData()

    # функция выдаёт график скоростных данных
    def GetAltitude(self):
        self.setMotorModel()
        self.setEnvironment()
        self.setRocketModel()
        self.TestFlight.plotAttitudeData()

    # функция выдаёт график энергий во время полёта
    def GetEnergy(self):
        self.setMotorModel()
        self.setEnvironment()
        self.setRocketModel()
        self.TestFlight.plotEnergyData()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
