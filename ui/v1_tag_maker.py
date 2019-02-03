# -*- coding: utf-8 -*-
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

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_TagMakerDialog(object):

    def db_add_tag(self):
        #print(self.db.__version__)
        with self.db:
            x = self.db.add_tag(tag_name=self.line_edit.text())
            print("x: {0}".format(x))
            if x:
                self.db.commit()
                self.db.pretty_fetch_all()


    def setupUi(self, TagMakerDialog, db):
        TagMakerDialog.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        TagMakerDialog.setObjectName("TagMakerDialog")
        TagMakerDialog.resize(370, 80)
        font = QtGui.QFont()
        font.setUnderline(False)
        TagMakerDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(TagMakerDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(TagMakerDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit = QtWidgets.QLineEdit(self.frame)
        self.line_edit.setObjectName("line_edit")
        self.horizontalLayout.addWidget(self.line_edit)
        self.add_tag_button = QtWidgets.QPushButton(self.frame)
        self.add_tag_button.setObjectName("add_tag_button")
        self.horizontalLayout.addWidget(self.add_tag_button)
        self.verticalLayout.addWidget(self.frame)
        self.label = QtWidgets.QLabel(TagMakerDialog)
        self.label.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(50)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(199, 0, 0)")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(TagMakerDialog)
        QtCore.QMetaObject.connectSlotsByName(TagMakerDialog)

        self.db = db
        self.line_edit.returnPressed.connect(self.db_add_tag)

        self.add_tag_button.clicked.connect(self.db_add_tag)

    def retranslateUi(self, TagMakerDialog):
        TagMakerDialog.setWindowTitle(QtWidgets.QApplication.translate("TagMakerDialog", "Dialog", None, -1))
        self.line_edit.setText(QtWidgets.QApplication.translate("TagMakerDialog", "tag_name", None, -1))
        self.add_tag_button.setText(QtWidgets.QApplication.translate("TagMakerDialog", "Add Tag", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("TagMakerDialog", "Tag Name Must Not Contain Spaces!", None, -1))


if __name__ == "__main__":
    import sys
    sys.exit()
    """import sys
    app = QtWidgets.QApplication(sys.argv)
    TagMakerDialog = QtWidgets.QDialog()
    ui = Ui_TagMakerDialog()
    ui.setupUi(TagMakerDialog)
    TagMakerDialog.show()
    sys.exit(app.exec_())"""
