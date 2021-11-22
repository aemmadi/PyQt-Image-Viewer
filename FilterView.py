import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc


class FilterView(qtw.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Manage Filters")
        self.setMinimumSize(400, 400)
