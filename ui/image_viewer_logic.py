from PySide2 import QtCore, QtGui, QtWidgets
from ui.image_viewer import Ui_MainWindow


class ImageViewer(QtWidgets.QMainWindow):
    def __init__(self, parent, file, tags):
        # UI Settup
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        super(ImageViewer, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        print("Loading UI...")
        self.ui = Ui_MainWindow()
        #self.ui.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui.setupUi(self)
        self.file = file


        self.show()
        self.update_image()
        print("UI Loaded!")


    # Image Settup
    def update_image(self):
        print("update_image")
        print("iamge_label: \nW: {0}\nH: {1}".format(self.ui.image_label.width(), self.ui.image_label.height()))
        self.ui.image_label.setPixmap(QtGui.QPixmap(self.file).scaled(self.ui.image_label.width(), self.ui.image_label.height(),
                                                      QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))


    def resizeEvent(self, event):
        print("resizeEvent")
        self.update_image()

"""
    def update_tags_list(self):
        with self.parent.db.cur.execute("SELECT * from files_tags WHERE file_id=?", (file_id)):
            tags_list = db.get_all_tags()

        for tag in tags_list:
            if tag["removed"] == 0:
                item = QtWidgets.QListWidgetItem()
                item.setData(QtCore.Qt.UserRole, tag)
                item.setText(tag["tag_name"])
                self.ui.tags_list_widget.addItem(item)
"""
