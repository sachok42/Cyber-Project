from PyQt5 import QtCore, QtGui, QtWidgets
from protocol import *
from config import *
from CClientGUI import CClientGUI


class CDrawingGUI(CClientGUI):

    def __init__(self):
        super().__init__()

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

        # Create color buttons (set text to empty and assign object names)
        self.Yellowbtn = QtWidgets.QPushButton(self.widget)
        self.Yellowbtn.setText("")  # No text, just a color button
        self.Yellowbtn.setObjectName("Yellowbtn")  # Name the button
        self.gridLayout.addWidget(self.Yellowbtn, 1, 0, 1, 1)  # Add button to grid layout

        self.PinkBtn = QtWidgets.QPushButton(self.widget)
        self.PinkBtn.setText("")  # No text
        self.PinkBtn.setObjectName("PinkBtn")  # Name the button
        self.gridLayout.addWidget(self.PinkBtn, 4, 0, 1, 1)

        self.RedBtn = QtWidgets.QPushButton(self.widget)
        self.RedBtn.setText("")  # No text
        self.RedBtn.setObjectName("RedBtn")  # Name the button
        self.gridLayout.addWidget(self.RedBtn, 0, 0, 1, 1)

        self.BlackBtn = QtWidgets.QPushButton(self.widget)
        self.BlackBtn.setText("")  # No text
        self.BlackBtn.setObjectName("BlackBtn")  # Name the button
        self.gridLayout.addWidget(self.BlackBtn, 4, 1, 1, 1)

        self.BlueBtn = QtWidgets.QPushButton(self.widget)
        self.BlueBtn.setText("")  # No text
        self.BlueBtn.setObjectName("BlueBtn")  # Name the button
        self.gridLayout.addWidget(self.BlueBtn, 3, 0, 1, 1)

        self.OrangeBtn = QtWidgets.QPushButton(self.widget)
        self.OrangeBtn.setText("")  # No text
        self.OrangeBtn.setObjectName("OrangeBtn")  # Name the button
        self.gridLayout.addWidget(self.OrangeBtn, 0, 1, 1, 1)

        self.GreenBtn = QtWidgets.QPushButton(self.widget)
        self.GreenBtn.setText("")  # No text
        self.GreenBtn.setObjectName("GreenBtn")  # Name the button
        self.gridLayout.addWidget(self.GreenBtn, 1, 1, 1, 1)

        self.PurpleBtn = QtWidgets.QPushButton(self.widget)
        self.PurpleBtn.setText("")  # No text
        self.PurpleBtn.setObjectName("PurpleBtn")  # Name the button
        self.gridLayout.addWidget(self.PurpleBtn, 3, 1, 1, 1)

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

    def retranslateUi(self, Form):
        # Set window title and button text
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.EraserBtn.setText(_translate("Form", "Eraser"))
        self.pushButton_10.setText(_translate("Form", "Clear canvas"))
