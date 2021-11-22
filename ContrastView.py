# Import PyQt modules
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc


class ContrastView(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # Initialize window attributes
        self.setWindowTitle("Modify Contrast")
        self.setMinimumSize(300, 100)

        # Initialize slider attributes
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

    # Update display number with changed slider value
    def updateLabel(self, value):
        self.label.setText(str(value))

    # Reset slider to 0
    def reset(self,):
        self.sld.setValue(0)
        self.label.setText(str(0))
