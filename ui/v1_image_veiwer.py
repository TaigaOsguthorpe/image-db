# -*- coding: utf-8 -*-
"""THIS FILE IS CURRENTLY NOT TO BE USED! THIS IS YOUR ONLY WARNING"""
"""
    Image-db - An image tagging/sorting program.
    Copyright (C) 2019 Taiga Osguthorpe

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

class Ui_ImageVeiwer(object):
    def __init__(self, ImageVeiwer, file):
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ImageVeiwer = ImageVeiwer
        self.file = file


    def setupUi(self):
        print("setupUi")

        # Prevent memory leaks by destroying window when it closes
        self.ImageVeiwer.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        ##


        ##
        self.ImageVeiwer.setObjectName("ImageVeiwer")
        self.ImageVeiwer.resize(1024, 768)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageVeiwer.sizePolicy().hasHeightForWidth())
        self.ImageVeiwer.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.ImageVeiwer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.ImageVeiwer)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 80, 80))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ImageLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageLabel.sizePolicy().hasHeightForWidth())
        self.ImageLabel.setSizePolicy(sizePolicy)
        self.ImageLabel.setObjectName("ImageLabel")
        self.verticalLayout_2.addWidget(self.ImageLabel)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)


        result = imghdr.what(self.file)
        if result is None:
            self.ImageLabel.setText("File Type Not Supported")

        elif result == 'gif':
            self.gif = QtGui.QMovie(self.file)
            self.ImageLabel.setMovie(self.gif)
            print(self.gif.state())

            #self.gif.setCacheMode(QtGui.QMovie.CacheAll)
            self.gif.setSpeed(100)
            self.ImageLabel.setMovie(self.gif)
            self.gif.start()
            print(self.gif.state())
        else:
            self.image = QtGui.QPixmap(self.file)#.scaled(1024, 1024, QtCore.Qt.KeepAspectRatio)
            self.ImageLabel.setPixmap(self.image)



        self.ImageVeiwer.setWindowTitle(QtWidgets.QApplication.translate("ImageVeiwer", "Form", None, -1))
        QtCore.QMetaObject.connectSlotsByName(self.ImageVeiwer)


if __name__ == "__main__":
    import sys
    sys.exit()
