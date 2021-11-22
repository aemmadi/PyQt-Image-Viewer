# Import PyQT modules
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

# Import Pillow library for image manipulation
from PIL import Image, ImageQt, ImageEnhance

# Custom window for modifying contrast
import ContrastView

import sys
import io


class ImageViewer(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize Image Attributes
        self.imageLabel = qtw.QLabel()
        self.imageLabel.setScaledContents(True)
        self.imageScaleFactor = 1.0
        self.imageBuffer = qtc.QBuffer()
        self.pilImage = None
        self.isImageLoaded = False

        # Initialize Scroll Area To Move Around Image
        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(True)
        self.setCentralWidget(self.scrollArea)

        # Initialize Contrast View
        self.contrastView = ContrastView.ContrastView()

        # Initialize Main Window
        self.setWindowTitle("Image Viewer")
        self.resize(800, 600)

    # Initialize Options and Triggers for Menu Bar
    def menuOptions(self):
        # File Menu
        self.openImageAction = qtw.QAction(
            "&Open", self, shortcut="Ctrl+O", triggered=self.openImage)
        self.saveImageAction = qtw.QAction(
            "&Save Image", self, shortcut="Ctrl+S", triggered=self.saveImage)

        # View Menu
        self.zoomInAction = qtw.QAction(
            "&Zoom In", self, shortcut="Ctrl+=", triggered=lambda: self.zoom(zoomIn=True))
        self.zoomOutAction = qtw.QAction(
            "&Zoom Out", self, shortcut="Ctrl+-", triggered=lambda: self.zoom(zoomOut=True))
        self.resetZoomAction = qtw.QAction(
            "&Reset Zoom", self, shortcut="Ctrl+R", triggered=lambda: self.zoom(resetZoom=True))
        self.openFilterAction = qtw.QAction(
            "&Edit Image Contrast", self, shortcut="Ctrl+F", triggered=self.openContrastView)

        self.fileMenu = qtw.QMenu("&File", self)
        self.fileMenu.addAction(self.openImageAction)
        self.fileMenu.addAction(self.saveImageAction)

        self.viewMenu = qtw.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAction)
        self.viewMenu.addAction(self.zoomOutAction)
        self.viewMenu.addAction(self.resetZoomAction)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.openFilterAction)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)

    # Opens image and loads in PixMap to Image Label
    def openImage(self, fileName):
        # Open file dialog to select image
        fileDialogOptions = qtw.QFileDialog.Options()
        fileName = qtw.QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.jpg)", options=fileDialogOptions)

        if fileName[0]:
            image = qtg.QImage(fileName[0])
            if image.isNull():
                qtw.QMessageBox.information(
                    self, "Image Viewer", "Unable load in %s." % fileName[0])
                return

            # Reset values from previous image
            self.reset()

            # Open an image buffer for manipulation
            self.imageBuffer.open(qtc.QBuffer.ReadWrite)
            image.save(self.imageBuffer, "JPG")

            # Load in image pixmap to image label
            self.imageLabel.setPixmap(qtg.QPixmap.fromImage(image))
            self.imageLabel.adjustSize()
            self.isImageLoaded = True

    # If an edited image exists, save the image (Saves file in directory of program)
    def saveImage(self):
        if self.pilImage is None:
            return

        self.pilImage.save("edited_image.jpg")

    # Handle zooming behavior (Zoom In/Out/Reset)
    def zoom(self, zoomIn=False, zoomOut=False, resetZoom=False):

        # Check if any zoom constraint is violated
        # Constraints in place to avoid crashes
        if (self.imageScaleFactor > 3.0 and zoomIn) or (self.imageScaleFactor < 0.3 and zoomOut):
            return

        try:
            if zoomIn:
                # Increase by a factor of 25% everytime
                self.imageScaleFactor *= 1.25
                newScaleImage = self.imageScaleFactor * self.imageLabel.pixmap().size()
                self.imageLabel.resize(newScaleImage)

            elif zoomOut:
                # Decrease by a factor of 25% everytime
                self.imageScaleFactor *= 0.75
                newScaleImage = self.imageScaleFactor * self.imageLabel.pixmap().size()
                self.imageLabel.resize(newScaleImage)

            elif resetZoom:
                # Reset to original size
                self.imageScaleFactor = 1.0
                self.imageLabel.resize(self.imageLabel.pixmap().size())
        except:
            print("Something went wrong while performing zoom operation")

    # Open Contrast Window
    def openContrastView(self):
        if not self.isImageLoaded:
            return

        self.contrastView.show()
        self.contrastView.sld.valueChanged.connect(self.contrastValueChanged)

    # Gets the contrast value from slider and applies it to the image
    def contrastValueChanged(self):
        if self.contrastView.sld.value() >= 0:
            value = (self.contrastView.sld.value() + 100) / 100
        else:
            value = (self.contrastView.sld.value() - 100) / 100

        # Open image from buffer and send to PIL library for manipulation
        image = Image.open(io.BytesIO(self.imageBuffer.data()))
        image = ImageEnhance.Contrast(image).enhance(value)
        self.pilImage = image

        # Get image data from PIL library and convert to QImage (Render new image PixMap in image label)
        image = ImageQt.ImageQt(image)
        image = qtg.QPixmap.fromImage(image)
        self.imageLabel.setPixmap(image)

    # Reset values to original state, ready for another image to be loaded
    def reset(self):
        self.imageScaleFactor = 1.0

        # Close previous image buffer if exists
        if self.imageBuffer.isOpen():
            self.imageBuffer.close()

        self.contrastView.reset()


# Driver code
if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = ImageViewer()
    window.menuOptions()
    window.show()
    sys.exit(app.exec_())
