import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from PIL import Image, ImageEnhance


class ContrastView(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modify Contrast")
        self.setMinimumSize(300, 100)

        hbox = qtw.QHBoxLayout()

        self.sld = qtw.QSlider(qtc.Qt.Horizontal, self)
        self.sld.setRange(-100, 100)
        self.sld.setFocusPolicy(qtc.Qt.NoFocus)
        self.sld.setPageStep(5)
        self.sld.setValue(0)

        self.sld.valueChanged.connect(self.updateLabel)

        self.label = qtw.QLabel('0', self)
        self.label.setAlignment(qtc.Qt.AlignCenter | qtc.Qt.AlignVCenter)
        self.label.setMinimumWidth(100)

        hbox.addWidget(self.sld)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)
        self.setLayout(hbox)

    def updateLabel(self, value):
        self.label.setText(str(value))
