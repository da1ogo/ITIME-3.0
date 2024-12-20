import sys
from datetime import datetime

import pygame
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractSpinBox, QMessageBox
from PyQt5.QtCore import QTimer

from view.bud import Ui_Dialog
from model.database import Database
from Widgets import ToggleSwitch


class MyClock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.session = Database("clock.db")
        self.session.drop_tables()
        self.session.create_tables()
        self.session.init_values()

        self.ui.timeEdit_4.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.ui.timeEdit_5.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.ui.timeEdit_6.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.ui.toggleSwitch_1 = ToggleSwitch(self.ui.widget_4, on_text="", off_text="")
        self.ui.toggleSwitch_2 = ToggleSwitch(self.ui.widget_5, on_text="", off_text="")
        self.ui.toggleSwitch_3 = ToggleSwitch(self.ui.widget_6, on_text="", off_text="")

        self.correct_answers_count = 0
        self.current_question = None
        self.last_alarm_time = None

        pygame.mixer.init()
        self.alarm_sound = pygame.mixer.Sound('materials/media/1.mp3')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_times)
        self.timer.start(1000)
    
        self.ui.pushButton.clicked.connect(self.check_answer)
        self.ui.pushButton_2.clicked.connect(self.record_time)

    def current_time(self):
        data = datetime.now()
        hours = data.hour
        mins = data.minute
        return f"{hours:0>2}:{mins:0>2}:00"

    def check_times(self):
        if self.last_alarm_time and self.last_alarm_time != self.current_time():
            print(self.last_alarm_time)
            print(self.current_time())
            self.last_alarm_time = None

        active_alarms = self.session.get_enables_clocks()
        for time in active_alarms:
            if (
                time[0] == self.current_time()
                and self.current_question is None
                and self.last_alarm_time is None
            ):
                self.last_alarm_time = time[0]
                self.get_question()
                self.alarm_sound.play(-1)

    def get_question(self):
        question = self.session.get_random_question()
        if question:
            self.current_question = question
            self.ui.label.setText(question[0])
            self.ui.textEdit.clear()

    def check_answer(self):
        if self.current_question is None:
            return

        user_answer = self.ui.textEdit.toPlainText().strip().lower()
        correct_answer = self.current_question[1].lower()
        
        if user_answer == correct_answer:
            self.correct_answers_count += 1
            if self.correct_answers_count >= 3:
                self.correct_answers_count = 0
                self.current_question = None
                self.alarm_sound.stop()
                QMessageBox.information(self, "Congratulations!", "Будильник отключен")
                self.ui.label.setText("")
                self.ui.textEdit.clear()
            else:
                self.get_question()
        else:
            QMessageBox.warning(self, "Result", "Неправильный ответ. Попробуйте снова.")
            self.get_question()

    def record_time(self):
        data = [
            [self.ui.timeEdit_4.time().toString(), self.ui.toggleSwitch_1.isChecked()],
            [self.ui.timeEdit_5.time().toString(), self.ui.toggleSwitch_2.isChecked()],
            [self.ui.timeEdit_6.time().toString(), self.ui.toggleSwitch_3.isChecked()]
        ]
        self.session.update_times(data)

    def closeEvent(self, event):
        self.timer.stop()
        self.session.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myClock = MyClock()
    myClock.show()
    sys.exit(app.exec_())
