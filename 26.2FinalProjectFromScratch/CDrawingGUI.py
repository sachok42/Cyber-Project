from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor

from protocol import *
from config import *


class CDrawingGUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drawing")
        self.frameCanvas = None

        # palette
        self.RedBtn = None
        self.OrangeBtn = None
        self.YellowBtn = None
        self.GreenBtn = None
        self.BlueBtn = None
        self.PurpleBtn = None
        self.PinkBtn = None
        self.BlackBtn = None

        # buttons
        self.EraserBtn = None
        self.ClearBtn = None

        self.setupUi(self)

    def setupUi(self, Form):
        # Set up the main window properties
        Form.setObjectName("Drawing")
        Form.resize(657, 388)  # Set the window size

        # Create a QFrame for the drawing canvas area
        self.frameCanvas = QtWidgets.QFrame(Form)
        self.frameCanvas.setGeometry(QtCore.QRect(30, 70, 481, 281))  # Position and size of the canvas
        self.frameCanvas.setFrameShape(QtWidgets.QFrame.StyledPanel)  # Set frame style
        self.frameCanvas.setFrameShadow(QtWidgets.QFrame.Plain)  # Set shadow style
        self.frameCanvas.setObjectName("frameCanvas")  # Name the frame

        # Create a QWidget to hold the color buttons and other controls
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(540, 90, 91, 174))  # Position and size of the widget
        self.widget.setObjectName("widget")  # Name the widget

        # Create a vertical layout to organize widgets inside the widget
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Create a grid layout to arrange color buttons in a grid
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        # set color picking buttons
        for i, color in enumerate(PALETTE_COLORS):
            btn = QtWidgets.QPushButton()
            btn.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            btn.setFixedSize(30, 20)  # Square buttons
            btn.clicked.connect(lambda checked, col=color: self.set_pen_color(QColor(col)))
            self.gridLayout.addWidget(btn, i // 2, i % 2)  # Arrange in 4 columns

        # Add the grid layout to the vertical layout
        self.verticalLayout_2.addLayout(self.gridLayout)

        # Create another vertical layout for buttons like Eraser and Clear Canvas
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # Create an Eraser button and add it to the layout
        self.EraserBtn = QtWidgets.QPushButton(self.widget)
        self.EraserBtn.setObjectName("EraserBtn")
        self.verticalLayout.addWidget(self.EraserBtn)

        # Create a Clear Canvas button and add it to the layout
        self.ClearBtn = QtWidgets.QPushButton(self.widget)
        self.ClearBtn.setObjectName("pushButton_10")
        self.verticalLayout.addWidget(self.ClearBtn)

        # Add the vertical layout (Eraser + Clear) to the main vertical layout
        self.verticalLayout_2.addLayout(self.verticalLayout)

        # Call retranslate function to set up the text for buttons
        self.retranslateUi(Form)

        # Connect the slots by object names (auto connection for signals/slots)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # set style
        buttons = [self.ClearBtn, self.EraserBtn]
        fields = [self.frameCanvas]
        labels = []
        set_designs(buttons, fields, labels)
        Form.setStyleSheet(f"background-color: {LIGHTBEIGE_BG};")


    def retranslateUi(self, Form):
        # Set window title and button text
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.EraserBtn.setText(_translate("Form", "Eraser"))
        self.ClearBtn.setText(_translate("Form", "Clear canvas"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)  # Create the application instance
    window = CDrawingGUI()  # Create an instance of your window
    window.show()  # Show the window
    sys.exit(app.exec_())  # Start the application's event loop