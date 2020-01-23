
from required import *

class statistics():
    """Statistics collecting"""

    def mouseReleaseEvent(self, event): # Counting of not-target clicks
        if (self.mainMenu_status == False) and (self.pause_status == False):
            self.background_clicks += 1

    # Counting of target-clicks
    def enemy1_clicked(self):
        self.enemies1_clicks += 1

    def enemy2_clicked(self):
        self.enemies2_clicks += 1

    def enemy3_clicked(self):
        self.enemies3_clicks += 1
