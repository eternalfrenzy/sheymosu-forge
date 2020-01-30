
from required import *

"""Class for events in gameplay"""
class gameplay_events():

    """Creating the timers for events and etc"""
    def create_eventTimers(self):
        self.enemyTimer_1 = QTimer()
        self.enemyTimer_1.setTimerType(Qt.PreciseTimer)
        self.enemyTimer_1.setInterval(100)
        self.enemyTimer_1.timeout.connect(self.enemyTick_1)
        self.enemyTime_1 = 0
        
        self.enemyTimer_2 = QTimer()
        self.enemyTimer_2.setTimerType(Qt.PreciseTimer)
        self.enemyTimer_2.setInterval(100)
        self.enemyTimer_2.timeout.connect(self.enemyTick_2)
        self.enemyTime_2 = 0

        self.enemyTimer_3 = QTimer()
        self.enemyTimer_3.setTimerType(Qt.PreciseTimer)
        self.enemyTimer_3.setInterval(100)
        self.enemyTimer_3.timeout.connect(self.enemyTick_3)
        self.enemyTime_3 = 0

        self.backgroundTimer = QTimer()
        self.backgroundTimer.setTimerType(Qt.PreciseTimer)
        self.backgroundTimer.setInterval(100)
        self.backgroundTimer.timeout.connect(self.backgroundTimeOut)
        self.backgroundTime = 0


        self.gameplayTimeCounter = QTimer()
        self.gameplayTimeCounter.setTimerType(Qt.PreciseTimer)
        self.gameplayTimeCounter.setInterval(100)
        self.gameplayTimeCounter.timeout.connect(self.gameplayTick)

        
        self.enemy_1.clicked.connect(self.enemyClicked_1)
        self.enemy_2.clicked.connect(self.enemyClicked_2)
        self.enemy_3.clicked.connect(self.enemyClicked_3)
    
    """Calls if targets is clicked"""
    
    def enemyClicked_1(self):
        self.enemy1_clicked()
        self.score += self.enemyScore_1
        self.score_lbl.setText("Счёт: " + str(self.score))
        self.enemy_1.move(random.randint(20, 1200), random.randint(20, 550))

        self.enemyTime_1 = 0
        self.enemyTimer_1.start()

    def enemyClicked_2(self):
        self.enemy2_clicked()
        self.score += self.enemyScore_2
        self.score_lbl.setText("Счёт: " + str(self.score))
        self.enemy_2.move(random.randint(20, 1200), random.randint(20, 550))

        self.enemyTime_2 = 0
        self.enemyTimer_2.start()

    def enemyClicked_3(self):
        self.enemy3_clicked()
        self.score += self.enemyScore_3
        self.score_lbl.setText("Счёт: " + str(self.score))
        self.enemy_3.move(random.randint(20, 1200), random.randint(20, 550))

        self.enemyTime_3 = 0
        self.enemyTimer_3.start()

    """Counting the time for time-outs
    of enemies and their movements"""

    def enemyTick_1(self):
        self.enemyTime_1 = round(self.enemyTime_1 + 0.1, 1) # Rounding the time
        if self.enemyTime_1 >= self.enemyTimeout_1:
            self.enemy_1.move(random.randint(20, 1200), random.randint(20, 550))
            self.enemyTime_1 = 0

    def enemyTick_2(self):
        self.enemyTime_2 = round(self.enemyTime_2 + 0.1, 1)
        if self.enemyTime_2 >= self.enemyTimeout_2:
            self.enemy_2.move(random.randint(20, 1200), random.randint(20, 550))
            self.enemyTime_2 = 0

    def enemyTick_3(self):
        self.enemyTime_3 = round(self.enemyTime_3 + 0.1, 1)
        if self.enemyTime_3 >= self.enemyTimeout_3:
            self.enemy_3.move(random.randint(20, 1200), random.randint(20, 550))
            self.enemyTime_3 = 0

    """Counting the time for
    time-out of background"""
    def backgroundTimeOut(self):
        self.backgroundTime = round(self.backgroundTime + 0.1, 1)
        if self.backgroundTime >= 2:
            self.gameplay_background.setPixmap(
                self.load_img("backgrounds", random.randint(0,16))
            )
            self.backgroundTime = 0

    """Counting the time in gameplay"""
    def gameplayTick(self):
        self.time = round(self.time + 0.1, 1)
