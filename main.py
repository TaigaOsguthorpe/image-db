from PySide2 import QtCore, QtGui, QtWidgets
from dependencies.db import DB
from ui import about, v1_tag_maker
from ui.image_viewer_logic import ImageViewer
from ui.main_window import Ui_MainWindow
import os



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Database Settup
        self.db = DB()
        print("Backend Version: {0}".format(self.db.__version__))

        # UI Settup
        super(MainWindow, self).__init__()
        print("Loading UI...")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.update_tags_list()
        # Set up icons manually
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/ui/icons/info.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #icon.addPixmap(QtGui.QPixmap("MAIN FILE LOCATION/ui/icons/info.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)  This fixes icons
        # Icons being used are from the feathericons, open source project "https://github.com/feathericons/feather" under MIT
        # Icons will need to be in the source code on GitHub/GitLab
        self.ui.actionAbout.setIcon(icon)
        print("UI Loaded!")


        # search_box_1 Logic
        self.ui.search_button_1.clicked.connect(self.db_search)
        self.ui.search_box_1.returnPressed.connect(self.db_search)

        # Auto Complete Settup
        word_list = []
        with self.db:
            for line in self.db.get_all_tags():
                print("line: {0}".format(line))
                if line["removed"] == 0:
                    word_list.append(line["tag_name"])
                else:
                    pass

        print("word_list: {0}".format(word_list))
        auto_complete = QtWidgets.QCompleter(word_list, self)
        auto_complete.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        auto_complete.setCompletionMode(auto_complete.PopupCompletion)
        self.ui.search_box_1.setCompleter(auto_complete)


        # result_box_1 Logic
        self.ui.result_box_1.itemClicked.connect(self.open_file)

        # result_box_1 Context Menu setup (rb = Result Box. ctx = context.)
        self.ui.result_box_1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.result_box_1.customContextMenuRequested.connect(self.rb_ctx_menu_call)

        self.rb_ctx_menu = QtWidgets.QMenu(parent=self.ui.result_box_1)

        self.rb_ctx_assign_tag = QtWidgets.QAction("Assign Tag")
        self.rb_ctx_assign_tag.triggered.connect(lambda: self.db_assign_tag(self.ui.result_box_1))
        self.rb_ctx_menu.addAction(self.rb_ctx_assign_tag)

        self.rb_ctx_remove_tag = QtWidgets.QAction("Remove Tag")
        self.rb_ctx_remove_tag.triggered.connect(lambda: self.db_remove_assigned_tag(file=self.ui.result_box_1.currentItem(), tag=self.tags_list_view.currentItem()))
        self.rb_ctx_menu.addAction(self.rb_ctx_remove_tag)

        self.rb_ctx_get_info = QtWidgets.QAction("Get Info")
        self.rb_ctx_get_info.triggered.connect(lambda: self.get_info_(self.ui.result_box_1.currentItem()))
        self.rb_ctx_menu.addAction(self.rb_ctx_get_info)

        self.rb_ctx_remove = QtWidgets.QAction("Remove")
        self.rb_ctx_remove.triggered.connect(self.db_remove_file)
        self.rb_ctx_menu.addAction(self.rb_ctx_remove)

        self.rb_ctx_force_remove = QtWidgets.QAction("Force Remove")
        self.rb_ctx_force_remove.triggered.connect(self.db_force_remove_file)
        self.rb_ctx_menu.addAction(self.rb_ctx_force_remove)

        self.rb_ctx_clear = QtWidgets.QAction("Clear")
        self.rb_ctx_clear.triggered.connect(self.ui.result_box_1.clear)
        self.rb_ctx_menu.addAction(self.rb_ctx_clear)



    # Context menu
    def rb_ctx_menu_call(self):
        pos = QtGui.QCursor.pos()
        print("mouse pos: {0}".format(pos))
        self.rb_ctx_menu.exec_(pos)


    def ctx_menu_handler(self, menu):
        if type(menu) is not QtWidgets.QMenu:
            raise TypeError("menu argument type must be PySide2.QtWidget.QMenu")
        pos = QtGui.QCursor.pos()
        print("mouse pos: {0}".format(pos))
        menu.exec_(pos)


    def get_info_(self, object):
        print(object.data(QtCore.Qt.UserRole))



    def open_file(self):
        data = self.ui.result_box_1.currentItem().data(QtCore.Qt.UserRole)
        print(data)
        path = "{0}/{1}".format(data['file_path'], data['file_name'])
        print(path)

        ImageViewer(self, path, None)


    def clicked(self):
        print("Clicked!! :D")


    def update_tags_list(self):
        self.ui.tags_list_view.clear()
        with self.db:
            tags_list = self.db.get_all_tags()
            #print(self.db.get_all_tags())
            print("tags_list: {0}".format(tags_list))

            for tag in tags_list:
                if tag['removed'] == 1:
                    pass
                else:
                    c = self.db.fetch_from_files_tags(tag['tag_id'])
                    #print("c: {0}".format(c))
                    if c is None:
                        c = 0
                    else:
                        c = len(c)

                    text = "{0}  ({1})".format(tag['tag_name'], c)
                    item = QtWidgets.QListWidgetItem()
                    item.setData(QtCore.Qt.UserRole, tag)
                    item.setText(text)
                    self.ui.tags_list_view.addItem(item)


    # Database functions
    def db_search(self):
        # If multiple search windows want to be made
        # Need to make this modular and not static
        # "self.ui.result_box_1" etc needs to not be done here.
        self.ui.result_box_1.clear()

        with self.db:
            result = self.db.search(self.ui.search_box_1.text())

            if result is None:
                return print("Search found None")

            for id in result:
                print("id: {0}".format(id))
                file_ = self.db.get_file(file_id=id)
                if file_['removed'] == 1:
                    pass
                else:
                    icon = QtGui.QIcon()
                    image_path = "{0}/{1}".format(file_['file_path'], file_['file_name'])
                    print(image_path)
                    icon.addPixmap(QtGui.QPixmap(image_path).scaled(256, 256, aspectMode=QtCore.Qt.KeepAspectRatio), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    item = QtWidgets.QListWidgetItem()
                    item.setIcon(icon)
                    #print(help(item.setData))
                    item.setData(QtCore.Qt.UserRole, file_)
                    print(item.data(QtCore.Qt.UserRole))
                    #print(image)
                    self.ui.result_box_1.addItem(item)


    def db_add_file(self, path):
        """Add a file to the db with the givent path
        path must contain file name E.g: path = '/home/user/path/file.ext'"""
        p = os.path.split(path)
        file_path = p[0]
        file_name = p[1]
        with self.db:
            self.db.add_file(file_path=file_path, file_name=file_name)
            self.db.commit()


    def db_remove_file(self):
        """Calls 'db.remove_file' this sets the removed collum to 1"""
        item = self.ui.result_box_1.currentItem()
        data = item.data(QtCore.Qt.UserRole)
        file_path = data['file_path']
        file_name = data['file_name']
        print("data: {0}".format(data))
        with self.db:
            self.db.remove_file(file_path=file_path, file_name=file_name)
            self.db.commit()
            self.db.pretty_fetch_all()


    def db_force_remove_file(self):
        """Calls 'db.remove_file(force_remove=True)' this will DELETE THE ITEM FROM THE database PERMANENTLY!"""
        item = self.ui.result_box_1.currentItem()
        data = item.data(QtCore.Qt.UserRole)
        file_path = data['file_path']
        file_name = data['file_name']
        print("data: {0}".format(data))
        with self.db:
            self.db.remove_file(force_remove=True, file_path=file_path, file_name=file_name)
            self.db.commit()
            self.db.pretty_fetch_all()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
