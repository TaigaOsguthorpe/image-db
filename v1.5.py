# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtGui, QtWidgets
from dependencies.db import DB
#import image_veiwer
#from multiprocessing import Process
import imghdr
import sys
#import atexit



try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s




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






class Ui_MainWindow(object):
    def __init__(self):
        self.db = DB()
        print("Backend Version: {0}".format(self.db.__version__))

    def db_search(self):
        self.result_box_1.clear()

        with self.db:
            result = self.db.search(self.search_box_1.text())

            for id in result:
                print("id: {0}".format(id))
                file_ = self.db.get_file(file_id=id)
                icon = QtGui.QIcon()
                image_path = "{0}/{1}".format(file_['file_path'], file_['file_name'])
                print(image_path)
                icon.addPixmap(QtGui.QPixmap(_fromUtf8(image_path)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item = QtWidgets.QListWidgetItem()
                item.setIcon(icon)
                #print(help(item.setData))
                item.setData(QtCore.Qt.UserRole, file_)
                print(item.data(QtCore.Qt.UserRole))
                #print(image)
                self.result_box_1.addItem(item)


    def get_info(self):
        data = self.result_box_1.currentItem().data(QtCore.Qt.UserRole)
        print(data)
        path = "{0}/{1}".format(data['file_path'], data['file_name'])
        print(path)


        self._ImageViewer = QtWidgets.QWidget()
        self._ui = Ui_ImageVeiwer(file=path, ImageVeiwer=self._ImageViewer)
        self._ui.setupUi()
        self._ImageViewer.show()


    def setupUi(self, MainWindow):
        print("setting up main window UI")

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1073, 686)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_3.addItem(spacerItem1)
        self.tag_label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tag_label.sizePolicy().hasHeightForWidth())
        self.tag_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.tag_label.setFont(font)
        self.tag_label.setObjectName("tag_label")
        self.verticalLayout_3.addWidget(self.tag_label)
        self.tags_tree_view = QtWidgets.QListWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tags_tree_view.sizePolicy().hasHeightForWidth())
        self.tags_tree_view.setSizePolicy(sizePolicy)
        self.tags_tree_view.setObjectName("tags_tree_view")
        self.verticalLayout_3.addWidget(self.tags_tree_view)





        self.widget_3 = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMaximumSize(QtCore.QSize(155, 16777215))
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setContentsMargins(0, 2, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.remove_tag_button = QtWidgets.QPushButton(self.widget_3)
        self.remove_tag_button.setMinimumSize(QtCore.QSize(25, 0))
        self.remove_tag_button.setObjectName("remove_tag_button")
        self.horizontalLayout_2.addWidget(self.remove_tag_button)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.add_tag_button = QtWidgets.QPushButton(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_tag_button.sizePolicy().hasHeightForWidth())
        self.add_tag_button.setSizePolicy(sizePolicy)
        self.add_tag_button.setMinimumSize(QtCore.QSize(25, 0))
        self.add_tag_button.setObjectName("add_tag_button")
        self.horizontalLayout_2.addWidget(self.add_tag_button)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout_3.addWidget(self.widget_3)
        spacerItem4 = QtWidgets.QSpacerItem(0, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_3.addItem(spacerItem4)
        self.horizontalLayout.addWidget(self.widget)
        self.tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_widget.setObjectName("tab_widget")
        self.search_tab = QtWidgets.QWidget()
        self.search_tab.setObjectName("search_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.search_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_4 = QtWidgets.QWidget(self.search_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.search_box_1 = QtWidgets.QLineEdit(self.widget_4)
        self.search_box_1.setObjectName("search_box_1")
        self.horizontalLayout_3.addWidget(self.search_box_1)
        self.previus_page_button = QtWidgets.QPushButton(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previus_page_button.sizePolicy().hasHeightForWidth())
        self.previus_page_button.setSizePolicy(sizePolicy)
        self.previus_page_button.setMaximumSize(QtCore.QSize(35, 16777215))
        self.previus_page_button.setObjectName("previus_page_button")
        self.horizontalLayout_3.addWidget(self.previus_page_button)
        self.page_indicator_1 = QtWidgets.QLabel(self.widget_4)
        self.page_indicator_1.setObjectName("page_indicator_1")
        self.horizontalLayout_3.addWidget(self.page_indicator_1)
        self.page_spin_box = QtWidgets.QSpinBox(self.widget_4)
        self.page_spin_box.setMaximum(9999)
        self.page_spin_box.setObjectName("page_spin_box")
        self.horizontalLayout_3.addWidget(self.page_spin_box)
        self.page_indicator_2 = QtWidgets.QLabel(self.widget_4)
        self.page_indicator_2.setObjectName("page_indicator_2")
        self.horizontalLayout_3.addWidget(self.page_indicator_2)
        self.next_page_button = QtWidgets.QPushButton(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_page_button.sizePolicy().hasHeightForWidth())
        self.next_page_button.setSizePolicy(sizePolicy)
        self.next_page_button.setMaximumSize(QtCore.QSize(35, 16777215))
        self.next_page_button.setObjectName("next_page_button")
        self.horizontalLayout_3.addWidget(self.next_page_button)
        self.search_button_1 = QtWidgets.QPushButton(self.widget_4)
        self.search_button_1.setMinimumSize(QtCore.QSize(90, 0))
        self.search_button_1.setObjectName("search_button_1")
        self.horizontalLayout_3.addWidget(self.search_button_1)
        self.verticalLayout_4.addWidget(self.widget_4)
        self.result_box_1 = QtWidgets.QListWidget(self.search_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.result_box_1.sizePolicy().hasHeightForWidth())
        self.result_box_1.setSizePolicy(sizePolicy)
        self.result_box_1.setObjectName("result_box_1")
        self.verticalLayout_4.addWidget(self.result_box_1)
        self.tab_widget.addTab(self.search_tab, "")
        self.add_files_tab = QtWidgets.QWidget()
        self.add_files_tab.setObjectName("add_files_tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.add_files_tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_5 = QtWidgets.QWidget(self.add_files_tab)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.add_images_button = QtWidgets.QPushButton(self.widget_5)
        self.add_images_button.setObjectName("add_images_button")
        self.horizontalLayout_5.addWidget(self.add_images_button)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.verticalLayout.addWidget(self.widget_5)
        self.add_images_widget = QtWidgets.QListWidget(self.add_files_tab)
        self.add_images_widget.setObjectName("add_images_widget")
        self.verticalLayout.addWidget(self.add_images_widget)
        self.tab_widget.addTab(self.add_files_tab, "")
        self.horizontalLayout.addWidget(self.tab_widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1073, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAdd_Image = QtWidgets.QAction(MainWindow)
        self.actionAdd_Image.setObjectName("actionAdd_Image")
        self.actionAdd_tag = QtWidgets.QAction(MainWindow)
        self.actionAdd_tag.setObjectName("actionAdd_tag")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionAdd_Image)
        self.menuFile.addAction(self.actionAdd_tag)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionPreferences)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        ###     c:     ###

        self.search_button_1.clicked.connect(self.db_search)
        self.search_box_1.returnPressed.connect(self.db_search)

        self.result_box_1.setViewMode(QtWidgets.QListView.IconMode)
        self.result_box_1.setIconSize(QtCore.QSize(125, 125))
        self.result_box_1.setMovement(QtWidgets.QListView.Static)

        self.result_box_1.itemClicked.connect(self.get_info)


    def retranslateUi(self, MainWindow):
        print("retranslating Ui")
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.tag_label.setText(QtWidgets.QApplication.translate("MainWindow", "Tags", None, -1))
        self.remove_tag_button.setText(QtWidgets.QApplication.translate("MainWindow", "-", None, -1))
        self.add_tag_button.setText(QtWidgets.QApplication.translate("MainWindow", "+", None, -1))
        self.pushButton_3.setText(QtWidgets.QApplication.translate("MainWindow", "Search", None, -1))
        self.previus_page_button.setText(QtWidgets.QApplication.translate("MainWindow", "<--", None, -1))
        self.page_indicator_1.setText(QtWidgets.QApplication.translate("MainWindow", "Page", None, -1))
        self.page_indicator_2.setText(QtWidgets.QApplication.translate("MainWindow", "/XX", None, -1))
        self.next_page_button.setText(QtWidgets.QApplication.translate("MainWindow", "-->", None, -1))
        self.search_button_1.setText(QtWidgets.QApplication.translate("MainWindow", "Search", None, -1))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.search_tab), QtWidgets.QApplication.translate("MainWindow", "Search", None, -1))
        self.add_images_button.setText(QtWidgets.QApplication.translate("MainWindow", "Add", None, -1))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.add_files_tab), QtWidgets.QApplication.translate("MainWindow", "Add Images", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("MainWindow", "Edit", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("MainWindow", "Help", None, -1))
        self.actionPreferences.setText(QtWidgets.QApplication.translate("MainWindow", "Preferences", None, -1))
        self.actionAbout.setText(QtWidgets.QApplication.translate("MainWindow", "About", None, -1))
        self.actionAdd_Image.setText(QtWidgets.QApplication.translate("MainWindow", "Add Image", None, -1))
        self.actionAdd_tag.setText(QtWidgets.QApplication.translate("MainWindow", "Add tag", None, -1))
        self.actionExit.setText(QtWidgets.QApplication.translate("MainWindow", "Exit", None, -1))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
