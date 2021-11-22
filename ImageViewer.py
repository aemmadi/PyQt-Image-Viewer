import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

import FilterView as fv
import sys


class ImageViewer(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.imageLabel = qtw.QLabel()
        self.imageLabel.setScaledContents(True)
        self.imageScaleFactor = 1.0

        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(True)
        self.setCentralWidget(self.scrollArea)

        self.filterView = fv.FilterView()

        self.setWindowTitle("Image Viewer")
        self.resize(800, 600)

    def menuOptions(self):
        self.openImageAction = qtw.QAction(
            "&Open", self, shortcut="Ctrl+O", triggered=self.openImage)

        self.zoomInAction = qtw.QAction(
            "&Zoom In", self, shortcut="Ctrl++", triggered=lambda: self.zoom(zoomIn=True))
        self.zoomOutAction = qtw.QAction(
            "&Zoom Out", self, shortcut="Ctrl+-", triggered=lambda: self.zoom(zoomOut=True))
        self.resetZoomAction = qtw.QAction(
            "&Reset Zoom", self, shortcut="Ctrl+R", triggered=lambda: self.zoom(resetZoom=True))
        self.openFilterAction = qtw.QAction(
            "&Filters", self, shortcut="Ctrl+F", triggered=self.openFilter)

        self.fileMenu = qtw.QMenu("&File", self)
        self.fileMenu.addAction(self.openImageAction)

        self.viewMenu = qtw.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAction)
        self.viewMenu.addAction(self.zoomOutAction)
        self.viewMenu.addAction(self.resetZoomAction)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.openFilterAction)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)

    def openImage(self, fileName):
        fileDialogOptions = qtw.QFileDialog.Options()
        fileName = qtw.QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)", options=fileDialogOptions)

        if fileName[0]:
            image = qtg.QImage(fileName[0])

            if image.isNull():
                qtw.QMessageBox.information(
                    self, "Image Viewer", "Unable load in %s." % fileName[0])
                return

            self.imageLabel.setPixmap(qtg.QPixmap.fromImage(image))
            self.imageLabel.adjustSize()

    def zoom(self, zoomIn=False, zoomOut=False, resetZoom=False):

        # Check if any zoom constraint is violated
        # Constraints in place to avoid crashes
        if (self.imageScaleFactor > 3.0 and zoomIn) or (self.imageScaleFactor < 0.3 and zoomOut):
            return

        try:
            if zoomIn:
                self.imageScaleFactor *= 1.25
                newScaleImage = self.imageScaleFactor * self.imageLabel.pixmap().size()
                self.imageLabel.resize(newScaleImage)

            elif zoomOut:
                self.imageScaleFactor *= 0.75
                newScaleImage = self.imageScaleFactor * self.imageLabel.pixmap().size()
                self.imageLabel.resize(newScaleImage)

            elif resetZoom:
                self.imageScaleFactor = 1.0
                self.imageLabel.resize(self.imageLabel.pixmap().size())
        except:
            print("Something went wrong while zoom operation")

    def openFilter(self):
        self.filterView.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = ImageViewer()
    window.menuOptions()
    window.show()
    sys.exit(app.exec_())
