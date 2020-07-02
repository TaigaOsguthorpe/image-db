# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'v3_image_viewer.ui',
# licensing of 'v3_image_viewer.ui' applies.
#
# Created: Sun Feb 16 16:01:05 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(978, 630)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy)
        self.image_label.setMinimumSize(QtCore.QSize(1, 1))
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)
        self.open_in_default_frame = QtWidgets.QFrame(self.centralwidget)
        self.open_in_default_frame.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_in_default_frame.sizePolicy().hasHeightForWidth())
        self.open_in_default_frame.setSizePolicy(sizePolicy)
        self.open_in_default_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.open_in_default_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.open_in_default_frame.setObjectName("open_in_default_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.open_in_default_frame)
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.open_in_default_button = QtWidgets.QPushButton(self.open_in_default_frame)
        self.open_in_default_button.setObjectName("open_in_default_button")
        self.horizontalLayout_3.addWidget(self.open_in_default_button)
        spacerItem = QtWidgets.QSpacerItem(617, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addWidget(self.open_in_default_frame)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tags_list_widget = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tags_list_widget.sizePolicy().hasHeightForWidth())
        self.tags_list_widget.setSizePolicy(sizePolicy)
        self.tags_list_widget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.tags_list_widget.setObjectName("tags_list_widget")
        self.verticalLayout_2.addWidget(self.tags_list_widget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.remove_tag_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_tag_button.setObjectName("remove_tag_button")
        self.horizontalLayout_2.addWidget(self.remove_tag_button)
        self.add_tag_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_tag_button.setObjectName("add_tag_button")
        self.horizontalLayout_2.addWidget(self.add_tag_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.image_label.setText(QtWidgets.QApplication.translate("MainWindow", "TextLabel", None, -1))
        self.open_in_default_button.setText(QtWidgets.QApplication.translate("MainWindow", "Open In Default", None, -1))
        self.remove_tag_button.setText(QtWidgets.QApplication.translate("MainWindow", "Remove Tag", None, -1))
        self.add_tag_button.setText(QtWidgets.QApplication.translate("MainWindow", "Add Tag", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

