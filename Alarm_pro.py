import tkinter
import threading
import winsound
import time

class Clock:
    def __init__(self):
        '''
        Создается окно tkinter;
        Инициализируются атрибуты объекта;
        '''
        self.main_window = tkinter.Tk()
        
        self.main_window.title('Alarm')
        self.main_window.geometry('345x150')
        self.main_window.configure(background = 'gray')

        self.f_top = tkinter.Frame()
        self.f_bot = tkinter.Frame()
        
        self.hour = 0
        self.mint = 0
        self.mode = 0
        self.thrd = 0
        self.hourNowLeft = 0
        self.hourNowRight = 0
        self.alarmMint = 0
        self.hourNow = 0
        self.mintNow = 0
        self.alarmHour = 'check'

        self.valueH1 = tkinter.StringVar()
        self.hour1 = tkinter.Label(self.f_top, width=1, height=1, textvariable = self.valueH1, font = ('Arial',80),fg = 'green',bg = 'black')
        self.hour1.pack(side = 'left')

        self.valueH2 = tkinter.StringVar()
        self.hour2 = tkinter.Label(self.f_top, width=1, height=1, textvariable = self.valueH2, font = ('Arial',80),fg = 'green',bg = 'black')
        self.hour2.pack(side = 'left')

        self.points = tkinter.Label(self.f_top, width=1, height=1, text = ':', font = ('Arial',80),fg = 'green',bg = 'black')
        self.points.pack(side = 'left')

        self.valueM1 = tkinter.StringVar()
        self.mint1 = tkinter.Label(self.f_top, width=1, height=1, textvariable = self.valueM1, font = ('Arial',80),fg = 'green',bg = 'black')
        self.mint1.pack(side = 'left')

        self.valueM2 = tkinter.StringVar()
        self.mint2 = tkinter.Label(self.f_top, width=1, height=1, textvariable = self.valueM2, font = ('Arial',80),fg = 'green',bg = 'black')
        self.mint2.pack(side = 'left')

        self.buttonHour = tkinter.Button(self.f_bot, text="H", width=10, height=1, overrelief = 'flat', command = self.hourUp)
        self.buttonHour.pack(side = 'left')
        self.buttonMin = tkinter.Button(self.f_bot, text="M", width=10, height=1, overrelief = 'flat', command = self.mintUp)
        self.buttonMin.pack(side = 'left')
        self.buttonAlarm = tkinter.Button(self.f_bot, text="A", width=10, height=1, overrelief = 'flat', command = self.alarmOn)
        self.buttonAlarm.pack(side = 'left')
        
        self.f_top.pack()
        self.f_bot.pack()

        self.valueH1.set(0)
        self.valueH2.set(0)
        self.valueM1.set(0)
        self.valueM2.set(0)

        def timeNow():
            '''
            Функция осуществляет подсчет времени с момента создания объекта.
            Так же сравнивает значения времени будильника с текущем временем и
            вызывает функцию, запускающую будильник.
            Работает, пока открыто окно tkinter. При его закрытии завершает все
            процессы.
            '''
            global thrd
            thrd = self.thrd
            while True:
                alarmHour = self.alarmHour
                alarmMint = self.alarmMint
                if thrd == 0:
                    hNext = self.hour
                    self.mint = (self.mint + 1) % 60
                    if self.mint == 0:
                        self.hour = (self.hour + 1) % 24
                    if hNext != self.hour:
                        self.outHour()
                    self.outMint()
                    if type(alarmHour) == int:
                        if alarmHour == self.hour and alarmMint == self.mint:
                            self.mode = 2
                            time.sleep(60 - self.beep())
                            self.mint += 1
                            self.outMint()
                    time.sleep(60.0)
                else:
                    exit()
        '''
        t.start запускает фунцию timeNow, которая работает на протяжении всего
        времени, при котором запущено окно tkinter
        '''
        t = threading.Timer(60.0, timeNow)
        t.start()
        
        tkinter.mainloop()

    def beep(self):
        '''
        Осуществляет звуковой сигнал.
        Фунция работает, пока пользователь не отключит его, или пока не
        закончится фиксированное время сигнала(1 мин).
        '''
        global thrd
        tm = 0
        while self.mode == 2 and tm < 59:
            winsound.Beep(1200,1000)
            tm += 1
            if thrd == 1:
                exit()
        if self.mode == 2:
            self.alarmOn()
        return tm
        
    def hourUp(self):
        '''
        Повышает занчение часа на единицу.
        '''
        if self.mode == 0:
            self.hour = (self.hour + 1) % 24
            self.outHour()
        else:
            self.hourNow = (self.hourNow + 1) % 24
            if len(str(self.hourNow)) == 1:
                self.hourNowLeft = 0
                self.hourNowRight = self.hourNow
            else:
                self.hourNowLeft = int(str(self.hourNow)[0])
                self.hourNowRight = int(str(self.hourNow)[1])
        self.outHour()

    def mintUp(self):
        '''
        Повышает занчение минуты на единицу.
        '''
        if self.mode == 0:
            self.mint = (self.mint + 1) % 60
            self.outMint()
        else:
            self.mintNow = (self.mintNow + 1) % 60
            if len(str(self.mintNow)) == 1:
                self.mintNowLeft = 0
                self.mintNowRight = self.mintNow
            else:
                self.mintNowLeft = int(str(self.mintNow)[0])
                self.mintNowRight = int(str(self.mintNow)[1])
        self.outMint()

    def alarmOn(self):
        '''
        Функция осуществялет запуск и отключение будильника.
        Меняет режим вывода информации о времени.(Часы/будильник)
        '''
        if self.mode == 0:
            self.hourNow = self.hour
            self.mintNow = self.mint
            self.mode = 1
            if len(str(self.hourNow)) == 1:
                self.hourNowLeft = 0
                self.hourNowRight = self.hourNow
                self.outHour()
            else:
                self.hourNowLeft = int(str(self.hourNow)[0])
                self.hourNowRight = int(str(self.hourNow)[1])
                self.outHour()
            if len(str(self.mintNow)) == 1:
                self.mintNowLeft = 0
                self.mintNowRight = self.mintNow
                self.outMint()
            else:
                self.mintNowLeft = int(str(self.mintNow)[0])
                self.mintNowRight = int(str(self.mintNow)[1])
                self.outMint()
        elif self.mode == 1:
            self.mode = 0
            self.alarmHour = self.hourNow
            self.alarmMint = self.mintNow
            self.outHour()
            self.outMint()
        else:
            self.mode = 0
            self.outHour()
            self.outMint()
            
    def outHour(self):
        '''
        Выводит значение часа на экран в зависимости от режима(mode)
        '''
        if self.mode == 0:
            if len(str(self.hour)) == 1:
                self.valueH1.set(0)
                self.valueH2.set(self.hour)
            else:
                self.valueH1.set(int(str(self.hour)[0]))
                self.valueH2.set(int(str(self.hour)[1]))
        else:
            self.valueH1.set(self.hourNowLeft)
            self.valueH2.set(self.hourNowRight)            
    
    def outMint(self):
        '''
        Выводит значение минут на экран в зависимости от режима(mode)
        '''
        if self.mode == 0:
            if len(str(self.mint)) == 1:
                self.valueM1.set(0)
                self.valueM2.set(self.mint)
            else:
                self.valueM1.set(int(str(self.mint)[0]))
                self.valueM2.set(int(str(self.mint)[1]))
        else:
            self.valueM1.set(self.mintNowLeft)
            self.valueM2.set(self.mintNowRight)
            
clock1 = Clock()
thrd = 1
