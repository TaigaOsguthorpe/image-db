# -*- coding: utf-8 -*-
import sqlite3
import os
import sys
from terminaltables import SingleTable


class DB(object):
    def __init__(self):
        self.__author__ = "Taiga Osguthorpe"
        self.__copyright__ = "Copyright (c) 2019 Taiga Osguthorpe"
        self.__version__ = "2.0"
        self.commited = None
        #self.strict_search = True

    def _connect(self, path=None):
        """Opens or creates a databse if not allready there in the path specified if no path specified creates it in the smae folder as this file is located"""
        if path:
            if type(path) is not str:
                raise TypeError("path argument must be a string!")

            if os.path.isdir(path):
                self.conn = sqlite3.connect('{0}/sumo.db')
            else:
                raise UserWarning("The path specified for the database file dose not exist!")

        else:
            self.conn = sqlite3.connect('{0}/sumo.db'.format(os.path.dirname(os.path.abspath(__file__))))  # current directory/sumo.db

        self.cur = self.conn.cursor()

        # Create "files" table (stores: id (+1 to the number that came before), file_path, file_name
        self.cur.execute('''CREATE TABLE IF NOT EXISTS files
                       (id INTEGER PRIMARY KEY AUTOINCREMENT, file_path TEXT, file_name TEXT, removed INTEGER)''')

        # Create "files_tags" table (tags table) (stores: file_id, tag_id) Used to bridge the gap between "tags" and the "files"
        self.cur.execute('''CREATE TABLE IF NOT EXISTS files_tags
                       (file_id INTEGER, tag_id INTEGER)''')

        # Create "tags" table (stores: id (+1 to the number that came before), tag_name (user input for the tag name)   used as the tag info used in the "files_tags" table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS tags
                       (id INTEGER PRIMARY KEY AUTOINCREMENT, tag_name TEXT, removed INTEGER)''')


    def _exit(self):
        """Closes the connection to the database and returns None."""
        self.conn.close()
        print("Sucsessfully closed the connection to the database")
        return True


    # Context Manager

    def __enter__(self):
        self._connect()
        return self


    def __exit__(self, type, value, traceback):
        self._exit()


    # Database inserting functions

    def add_tag(self, tag_name):
        """Adds a tag to the tags table in the database"""
        if type(tag_name) is not str:
            raise TypeError("tag_name must be string")
        else:
            allowed = "abcdefghijklmnopqrstuvwxyz-_/=+^0123456789"
            #disallowed = "\\ "
            blacklist = [" ", ""]
            #print(blacklist)

            def blacklist_check():
                """Checks if the string tag_name contains any charecters in the blacklist string. Returns True if none are found and False if any are found"""
                if not tag_name:
                    return False
                for c in tag_name:
                    for x in blacklist:
                        if c == x:
                            return False
                return True

            x = blacklist_check()
            if x is True:
                self.cur.execute("SELECT * from tags WHERE tag_name=?", (tag_name.replace("\\", ""),))
                if len(self.cur.fetchall()) > 0:
                    print("Tag allready exists!")
                    return

                self.cur.execute("INSERT INTO tags VALUES(NULL,?,0)", (tag_name,))
                self.commited = False
                return True
            else:
                print('TagNameError! Tags can not be empty or contain backslashes "\\" or spaces " "')
                return None


    def add_file(self, file_path, file_name):
        """Adds an entry to the file table in the database with the given arguments and returns a dictionary with the args and the file_id.

        type: function
        args: 2 (file_path, file_name)
            file_path:
            - type: string (directory to file)
            - example: file_path = "/home/user/path/"
            - note: the ending '/' is required if you do not want to manually add it back in later on

            file_name:
            - type: string
            - accepted image formats: all file types
            - example: file_name = 'image.png'

        response:
        - type: dictionary
        - example: {'file_path': '/home/user/path/', 'file_name': 'image.png', 'file_id': 1}"""

        if type(file_path) is not str:
            raise TypeError("file_path must be a string")

        if type(file_name) is not str:
            raise TypeError("file_name must be a string")

        self.cur.execute("SELECT * from files WHERE file_path=? and file_name=?", (file_path, file_name))  # Search if file allready exists in the database

        if len(self.cur.fetchall()) > 0:
            return print("file allready exists error! the file trying to be added allready exists in the database")

        if os.path.isfile("{0}/{1}".format(file_path, file_name)):
            print("File exists!")
            self.cur.execute("INSERT INTO files VALUES (NULL,?,?,0)", (file_path, file_name))
            self.commited = False
            #return {'file_path': file_path, 'file_name': file_name, 'file_id': cur.lastrowid}
            #return File(file_path=file_path, file_name=file_name, file_id = cur.lastrowid)
            return
        else:
            raise Exception("file not found! Is the file_path correct or the file_name?")


    def fetch_all(self):
        return_list = []
        self.cur.execute("SELECT * from tags")
        return_list.append(self.cur.fetchall())
        self.cur.execute("SELECT * from files")
        return_list.append(self.cur.fetchall())
        return return_list


    def pretty_fetch_all(self):
        self.cur.execute("SELECT * from tags")
        return_tags_table = []
        return_tags_table.append(["id", "tag name", "removed"])
        for data in self.cur.fetchall():
            return_tags_table.append(data)

        self.cur.execute("SELECT * from files")
        return_files_table = []
        return_files_table.append(["id", "file path", "file name", "removed"])
        for data in self.cur.fetchall():
            return_files_table.append(data)

        self.cur.execute("SELECT * from files_tags")
        return_files_tags_table = []
        return_files_tags_table.append(["file_id", "tag_id"])
        for data in self.cur.fetchall():
            return_files_tags_table.append(data)

        table_1 = SingleTable(return_tags_table, "tags")
        table_2 = SingleTable(return_files_table, "files")
        table_3 = SingleTable(return_files_tags_table, "files tags")
        return print(table_1.table), print(table_2.table), print(table_3.table)


    def get_file(self, file_path=None, file_name=None, file_id=None):
        """Returns a dictionary with the infomation of the given entry containing the file_path and file_nameself.
        Returns None if nothing is found"""

        if file_path and file_name:
            if type(file_path) is not str:
                print("file_path must be a string!")
                raise TypeError("file_path must be str")

            if type(file_name) is not str:
                print("file_name must be a string!")
                raise TypeError("file_name must be str")

            self.cur.execute("SELECT * from files WHERE file_path=? and file_name=?", (file_path, file_name))
            result = self.cur.fetchall()
            return {"file_id": result[0][0], "file_path": result[0][1], "file_name": result[0][2], "removed": result[0][3]}

        elif file_id:
            if type(file_id) is not int:
                raise TypeError("file_id must be int")

            self.cur.execute("SELECT * from files where id=?", (file_id,))
            result = self.cur.fetchall()
            return {"file_id": file_id, "file_path": result[0][1], "file_name": result[0][2], "removed": result[0][3]}

        else:
            raise TypeError("get_file didnt get the right arguments :c")


        if len(result) == 0:
            print("No entry found with file_path: {0} and file_name: {1}".format(file_paath, file_name))
            return None

        if len(result) > 1:
            print("More than one entry with file_path: {0}  and file_name: {1}".format(file_path, file_name))
            return None
        else:
            #result example [(id, file_path, file_name, removed)]
            #id = int(id[0])
            #id = result[0][0]
            file_id = int(result[0][0])
            return {"file_id": file_id, "file_path": file_path, "file_name": file_name}


    def get_file_from_id(self, file_id):
        """get_file but with id instead of file_path and file_name"""
        if type(file_id) is not int:
            print("file_id must be a integer!")
            raise TypeError("file_id must be int")

        self.cur.execute("SELECT * from files where id=?", (file_id,))
        result = self.cur.fetchall()
        #result example [(id, file_path, file_name, removed)]
        return {"file_id": file_id, "file_path": result[0][1], "file_name": result[0][2], "removed": result[0][3]}


    def remove_file(self, file_path, file_name):
        """Changes the 'removed' column to 1 on."""

        if type(file_path) is not str:
            raise TypeError("file_path must be a string")

        if type(file_name) is not str:
            raise TypeError("file_name must be a string")

        self.cur.execute("UPDATE files SET removed=1 WHERE file_path=? AND file_name=?", (file_path, file_name))
        self.commited = False
        return


    def get_all_files(self):
        self.cur.execute("SELECT * from files")
        result = self.cur.fetchall()
        return_list = []
        for line in result:
            return_list.append(line[0])
            print(line)
        return return_list


    def get_tag(self, tag_name=None, tag_id=None):
        """Returns a dictionary containing the 'tag_name', 'tag_id', and 'removed' with the specified tag_name or tag_id.
        If no tag was found with the given infomation, returns None"""
        #print("tag_name = {0}\ntag_id = {1}".format(tag_name, tag_id))
        if tag_name:
            if type(tag_name) is not str:
                raise TypeError("tag_name must be a string.")

            self.cur.execute("SELECT * from tags WHERE tag_name=?", (tag_name,))
            result = self.cur.fetchall()

            if len(result) == 0:
                print("No tag found with tag_name: {0}".format(tag_name))
                return None

            return {"tag_id": result[0][0], "tag_name": result[0][1], "removed": result[0][2]}

        elif tag_id:
            if type(tag_id) is not int:
                raise TypeError("tag_id must be an integer")

            self.cur.execute("SELECT * from tags WHERE id=?", (tag_id,))
            result = self.cur.fetchall()

            if len(result) == 0:
                print("No tag found with tag_id: {0}".format(tag_id))
                return None

            return {"tag_id": result[0][0], "tag_name": result[0][1], "removed": result[0][2]}

        else:
            raise TypeError("get_tags must be called with tag_name or tag_id")


    def fetch_from_files_tags(self, tag_id=None, file_id=None):
        """Returns list e.g [1, 3]"""
        r = None
        if tag_id:
            if type(tag_id) is not int:
                raise TypeError("tag_id argument type must be int")

            self.cur.execute("SELECT file_id from files_tags WHERE tag_id=?", (tag_id,))
            #return self.cur.fetchall()
            result = self.cur.fetchall()
            print("fetch_from_files_tags result: {0}".format(result))
            if len(result) == 0:
                return None
            r = []
            [(lambda id: r.append(id[0]))(id) for id in result]
            #[(lambda s: print(" - {0} - ({1})".format(s.name, s.id)))(s) for s in client.guilds]
        elif file_id:
            raise Exception("file_id argument is not supported at this time")
#            if type(file_id) is not int:
#                raise TypeError("file_id argument must be int")
#            else:
#                self.cur.execute("SELECT tag_id from files_tags WHERE tag_id=?", (tag_id,))

        return r


    def search(self, query, strict_search=True, allow_removed=False):
        """Search the db with tags and get a list of file_id 's that have the tag linked to them.'"""
        if type(query) is not str:
            raise TypeError("query must be string")

        if query.replace(" ", "") == "":  # If search bar is empty (Needs to remove " " spaces in future)
            result = self.get_all_files()
            return result


        query_list = query.split(" ")
        print("query_list: {0}".format(query_list))

        tag_id_list = []
        for tag in query_list:
            """Get tags id from query string"""
            if tag == '':
                pass
            else:
                result_tag = self.get_tag(tag_name=tag)
                if result_tag is None:
                        print('"{0}" tag was not found'.format(tag))
                        #pass
                        return None

                else:
                    tag_id_list.append(result_tag['tag_id'])
                    print(result_tag)


        files_list = []
        print("Length tag_id_list: {0}".format(len(tag_id_list)))
        for tag_id in tag_id_list:
            self.cur.execute("SELECT file_id FROM files_tags WHERE tag_id=?", (tag_id,))
            result = self.cur.fetchall()
            print("Result: {0}".format(result))
            if len(result) > 0:
                #print("result[0][0]: {0}".format(result[0][0]))
                temp_file_list = []

                """if temp_file_list.__contains__(result[0][0]):
                    pass
                else:
                    temp_file_list.append(result[0][0])"""
                for file_id in result:
                    temp_file_list.append(file_id[0])
                #temp_file_list.append(result[0][0])
            else:
                raise Exception("tag_id '{0}' is not assigned to any file.\nUse get_tag(tag_id={0}) to learn more :)".format(tag_id))
            files_list.append(temp_file_list)
        print("files_list: {0}".format(files_list))


        # Single tag search checker
        if len(files_list) == 1:
            return list(set(files_list[0]))  # Return a list of a list 'set' stripes any duplicates if somehow there are any

        print("!!!!!!!!!!!!!!!!\n{0}".format(files_list))

        return_list = []
        for parent in files_list:
            """Comparing result lists"""
            parent_location = files_list.index(parent)

            for child in files_list:
                if files_list.index(child) == parent_location:
                    print("List {0}: Skiping self".format(parent_location))
                    pass  # Do nothing

                else:
                    print("List {0} comparing list {1}".format(parent_location, files_list.index(child)))
                    #print("Child list: {0}".format(child))

                    comparason = set(parent).intersection(child)  # maybe use intersection_update?

                    print("Comparason: {0}".format(comparason))
                    for x in comparason:
                        if return_list.__contains__(x):
                            pass
                        else:
                            return_list.append(x)
        print("return_list = {0}".format(return_list))
        return return_list




    def remove_tag(self, tag_name, force_remove=None):
        """Sets removed to 1 in db unless force_remove is True then removes the entry from the db. If sucsessfull returns True. If not sucsesfull returns False
        tag_name:
        - Required! str of tag_name being removed
        force_remove:"""
        if type(tag_name) is not str:
            raise TypeError("tag_name must be str")

        if self.get_tag(tag_name) is None:
            print("Unable to find specified tag to remove.")
            return False

        if force_remove == True:
            self.cur.execute("DELETE FROM tags where tag_name=?", (tag_name, ))
            return True
        else:
            self.cur.execute("UPDATE tags SET removed=1 WHERE tag_name=?", (tag_name,))
            self.commited = False
            return True



    def assign_tag(self, file_id, tag_id):
        """Assigns a tag_id to a file_id in the \"files_tags\"."""  # \" escapes the " " syntax
        if type(file_id) and type(tag_id) is not int:
            raise TypeError("file_id and tag_id must be int")

        result = self.fetch_from_files_tags()
        if result is not None:
            raise Exception("tag allready assigned with file")
            #return False

        self.cur.execute("INSERT INTO files_tags VALUES (?,?)", (file_id, tag_id))
        self.commited = False
        return True



    def remove_assigned_tag(self, tag_id, file_id):
        """Remove a tag from a file inside the files_tags table"""
        if type(tag_id) and type(file_id) is not int:
            raise TypeError("tag_id and file_id must be int!")

        self.cur.execute("DELETE FROM files_tags where tag_id=? and file_id=?", (tag_id, file_id))
        self.commited = False
        return


    # Database miscellaneous function

    def commit(self):
        """Saves (commit) changes to the database."""
        self.conn.commit()
        self.commited = True
        print("Sucsessfully saved the database")
        return True



if __name__ == '__main__':
    sys.exit()
