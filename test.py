from PyQt6.QtWidgets import QApplication, QWidget, QCalendarWidget, QVBoxLayout, QPushButton, QInputDialog, QDateEdit, QTextEdit
from PyQt6.QtCore import QDate, Qt, QLocale, QCoreApplication
from PyQt6 import QtCore

class CalendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        locale = QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)
        self.calendar.setVerticalHeaderFormat(locale.dayName(Qt.DayOfWeek.Sunday, QLocale.standaloneDayName()), QLocale.LongFormat)
        self.calendar.setFirstDayOfWeek(Qt.DayOfWeek.Sunday)

        self.calendar_dict = {}

        self.calendar.selectionChanged.connect(self.repaintCalendar)

        vbox = QVBoxLayout()
        vbox.addWidget(self.calendar)
        self.setLayout(vbox)


    def showInputDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your event:')
        if ok:
            date = self.calendar.selectedDate()
            date_str = date.toString('yyyy-MM-dd')
            event_str = f"{date_str}: {text}"
            self.calendar_dict[date] = event_str
            self.repaintCalendar()

    def paintCell(self, painter, rect, date):
        if date in self.calendar_dict:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(Qt.SolidPattern)
            painter.drawRect(rect)
            painter.setPen(Qt.black)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.calendar_dict[date])

    def repaintCalendar(self):
        self.calendar.repaint()

    def sizeHint(self):
        return self.calendar.sizeHint()

if __name__ == '__main__':
    app = QApplication([])
    cal = CalendarWidget()
    cal.show()
    app.exec()
