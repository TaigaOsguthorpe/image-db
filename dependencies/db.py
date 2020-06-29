# -*- coding: utf-8 -*-
''' A note on Documentation.
    (Full documentation is not currently available)

    Documentation within this file is marked in two ways:
    1) The use of tripple quattion marks """Documentation String About a Function""".
       This is to (generally) be uses for functions, this enables the Python in built, "help()", function.
    Example:
        def important_task(argument):
            """Do an important task with the given argument."""


    2) A hashtag (#) with the note starting with 1 blank space character directly to the right.
    Exaple:
        # The loop below prints the vital "Hello World!" string out 5 times.
        for x in range(5):
            variable_1 = "Hello World!"
            print(variable_1

    Example:
        variable_1 = "Hello World!" # This variable holds the vital "Hello World!" string.
'''

import sqlite3
import os
from terminaltables import SingleTable


class DB(object):
    def __init__(self):
        self.__version__ = "2.0"
        self.commited = None
        #self.strict_search = True

    # Connection handling functions
    def _connect(self, path=None):
        """Opens or creates a databse if not allready there in the path specified if no path specified creates it in the smae folder as this file is located"""

        # Check path argument is specified
        if path:
            if type(path) is not str:
                raise TypeError("path argument must be a string!")

            if os.path.isdir(path):
                self.conn = sqlite3.connect(path)
            else:
                raise Warning("The path specified for the database file dose not exist!")

        else:
            self.conn = sqlite3.connect('{0}/sqlite3.db'.format(os.path.dirname(os.path.abspath(__file__))))  # current directory/sqlite3.db

        self.cur = self.conn.cursor()

        # Create "files" table (stores: id (+1 to the number that came before), file_path, file_name
        self.cur.execute('''CREATE TABLE IF NOT EXISTS files
                       (id INTEGER PRIMARY KEY AUTOINCREMENT, file_path TEXT, file_name TEXT, removed INTEGER)''')

        # Create "files_tags" table (tags table) (stores: file_id, tag_id) Used to bridge the gap between "tags" and the "files"
        self.cur.execute('''CREATE TABLE IF NOT EXISTS files_tags
                       (file_id INTEGER, tag_id INTEGER)''')

        # Create "tags" table (stores: id (+1 to the number that came before), tag_name (user input for the tag name)   used as the tag info used in the "files_tags" table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS tags
                       (id INTEGER PRIMARY KEY AUTOINCREMENT, tag_name TEXT, force_prefix INTEGER, removed INTEGER)''')


        # Categories A.K.A: cats
        self.cur.execute('''CREATE TABLE IF NOT EXISTS cats
                       (id INTEGER PRIMARY KEY AUTOINCREMENT, cat_name TEXT, removed INTEGER)''')

        # Categories_tags A.K.A: cats_tags
        self.cur.execute('''CREATE TABLE IF NOT EXISTS cats_tags
                       (cat_id INTEGER, tag_id INTEGER)''')

        print("Sucsessfully oppened a connection to the database.")


    def _exit(self):
        """This should not be called manually, please use 'with db'!
        Closes the connection to the database and returns True."""
        self.conn.close()
        print("Sucsessfully closed the connection to the database.")
        return True


    # Context Manager

    def __enter__(self, path=None):
        if path:
            self._connect(path)
        else:
            self._connect()
        return self


    def __exit__(self, type, value, traceback):
        self._exit()


    # Database inserting functions

    def add_tag(self, tag_name):
        """Adds a tag to the tags table in the database. WARNING THIS NEEDS TO BE WORKED ON!"""
        if type(tag_name) is not str:
            raise TypeError("tag_name must be string")
        else:
            allowed = "abcdefghijklmnopqrstuvwxyz-_/=+^0123456789"  # This is no longer used
            blacklist = [" ", "", ":"]
            #print(blacklist)

            def blacklist_check():
                """Checks if the string tag_name contains any charecters in the blacklist string. Returns True if none are found and False if any are found
                (This needs to be worked on)"""
                if not tag_name:
                    return False
                for c in tag_name:
                    for x in blacklist:
                        if c == x:
                            return False
                return True

            x = blacklist_check()  # Blacklist check is depreciated needs to be replaced
            if x is True:
                self.cur.execute("SELECT * from tags WHERE tag_name=?", (tag_name.replace("\\", ""), ))  # This whole check is depreciated. Use get_tag(tag_name)
                result = self.cur.fetchall()
                try:
                    if result[0][2] == 1:
                        self.cur.execute("UPDATE tags SET removed=0 WHERE tag_name=?", (tag_name, ))
                        return True
                except IndexError:
                    pass

                if len(result) > 0:
                    print("Tag allready exists!")
                    return

                self.cur.execute("INSERT INTO tags VALUES(NULL,?,0,0)", (tag_name,))
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

            file_name:
            - type: string
            - accepted image formats: all file types
            - example: file_name = 'image.png'

        response:
        - type: None"""

        if type(file_path) is not str:
            raise TypeError("file_path must be a string")

        if type(file_name) is not str:
            raise TypeError("file_name must be a string")

        blacklist_ = ["/", "\\"]

        for c in file_name:
            for x in blacklist_:
                if c == x:
                    raise Exception("file_name must not contain: {0}".format(blacklist_))
                else:
                    pass

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


    def get_cat(self, cat_name=None, cat_id=None):
        if cat_name:
            if type(cat_name) is not str:
                raise Exception("cat_name argument type must be string")

            self.cur.execute("SELECT * FROM cats WHERE cat_name=?", (cat_name, ))
            result = self.cur.fetchall()
            return result

        elif cat_id:
            if type(cat_id) is not int:
                raise Exception("cat_id argument tpye must be integer")

            self.cur.execute("SELECT * FROM cats WHERE id=?", (cat_id, ))
            result = self.cur.fetchall()
            return result


    def add_cat(self, cat_name, parent=None):
        if parent:
            raise Exception("cats cannot (yet) contain cats")

        blacklist = [" ", "", ":"]
        for c in cat_name:
            if c in blacklist:
                raise Exception("cat_name must not contain ({0})".format(c))

        result = self.get_cat(cat_name)
        if len(result) > 0:
            raise Exception('category with name "{0}" allready exists.'.format(cat_name))

        self.cur.execute("INSERT INTO cats VALUES (NULL,?,0)", (cat_name, ))
        self.commited = False
        return True


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

            self.cur.execute("SELECT * from files where id=?", (file_id, ))
            result = self.cur.fetchall()
            return {"file_id": file_id, "file_path": result[0][1], "file_name": result[0][2], "removed": result[0][3]}


        elif file_name:
            if type(file_name) is not str:
                raise TypeError("file_name must be str")

            self.cur.execute("SELECT * FROM files WHERE file_name=?", (file_name, ))
            result = self.cur.fetchall()
            return_list = []
            for x in result:
                r = {"file_id": x[0], "file_path": x[1], "file_name": x[2], "removed": result[0][3]}
                return_list.append(r)

            return return_list
        else:
            raise TypeError("get_file didnt get the right arguments :c")


        if len(result) == 0:
            print("No entry found with file_path: {0} and file_name: {1}".format(file_path, file_name))
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


    def remove_file(self, file_path, file_name, force_remove=False):
        """Changes the 'removed' column to 1 on."""

        if type(file_path) is not str:
            raise TypeError("file_path must be a string")

        if type(file_name) is not str:
            raise TypeError("file_name must be a string")

        if force_remove:
            self.cur.execute("DELETE FROM files where file_path=? and file_name=?", (file_path, file_name))
            self.commited = False
            return

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


    def get_all_tags(self):
        self.cur.execute("SELECT * from tags")
        result = self.cur.fetchall()
        #print("get_all_tags result: {0}".format(result))
        return_list = []
        for line in result:
            return_list.append({"tag_id": line[0], "tag_name": line[1], "removed": line[2]})
            #print(line)
        return return_list


    def fetch_all(self):
        return_list = []
        self.cur.execute("SELECT * from tags")
        return_list.append(self.cur.fetchall())
        self.cur.execute("SELECT * from files")
        return_list.append(self.cur.fetchall())
        self.cur.execute("SELECT * from files_tags")
        return_list.append(self.cur.fetchall())
        self.cur.execute("SELECT * from cats")
        return_list.append(self.cur.fetchall())
        self.cur.execute("SELECT * from cats_tags")
        return_list.append(self.cur.fetchall())
        return return_list


    def pretty_fetch_all(self):
        self.cur.execute("SELECT * from tags")
        return_tags_table = []
        return_tags_table.append(["id", "tag name", "force_prefix", "removed"])
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

        self.cur.execute("SELECT * from cats")
        return_cats_table = []
        return_cats_table.append(["id", "cat_name", "removed"])
        for data in self.cur.fetchall():
            return_cats_table.append(data)

        self.cur.execute("SELECT * from cats_tags")
        return_cats_tags_table = []
        return_cats_tags_table.append(["cat_id", "tag_id"])
        for data in self.cur.fetchall():
            return_cats_tags_table.append(data)

        # Create all the calsses for the created tables
        table_1 = SingleTable(return_tags_table, "tags")
        table_2 = SingleTable(return_files_table, "files")
        table_3 = SingleTable(return_files_tags_table, "files tags")
        table_4 = SingleTable(return_cats_table, "categories (cats)")
        table_5 = SingleTable(return_cats_tags_table, "cats_tags")
        # Return print functions for all created tables so they get displayed
        return print(table_1.table), print(table_2.table), print(table_3.table), print(table_4.table), print(table_5.table)


    def get_tag(self, tag_name=None, tag_id=None):
        """Returns a dictionary containing the 'tag_name', 'tag_id', and 'removed' with the specified tag_name or tag_id.
        If no tag was found with the given infomation, returns None"""

        # Check if tag_name argument was specified
        if tag_name:
            if type(tag_name) is not str:
                raise TypeError("tag_name must be a string.")

            self.cur.execute("SELECT * from tags WHERE tag_name=?", (tag_name,))
            result = self.cur.fetchall()

            if len(result) == 0:
                print("No tag found with tag_name: {0}".format(tag_name))
                return None

            return {"tag_id": result[0][0], "tag_name": result[0][1], "removed": result[0][2]}

        # Check if tag_id argument was specified
        elif tag_id:

            # Check if tag_id is an integer as it must be an integer
            if type(tag_id) is not int:
                raise TypeError("tag_id must be an integer")

            self.cur.execute("SELECT * from tags WHERE id=?", (tag_id,))
            result = self.cur.fetchall()

            # Empty result check
            if len(result) == 0:
                print("No tag found with tag_id: {0}".format(tag_id))
                return None

            return {"tag_id": result[0][0], "tag_name": result[0][1], "removed": result[0][2]}

        else:
            raise TypeError("get_tags must be called with tag_name or tag_id")


    def fetch_from_files_tags(self, tag_id=None, file_id=None):
        """Returns list e.g [1, 3]. WARNING! THIS NEEDS TO BE WORKED ON!"""
        r = None
        if tag_id and file_id:
            print("THIS IS A THING!!!!")
            self.cur.execute("SELECT * from files_tags WHERE tag_id=? and file_id=?", (tag_id, file_id))
            result = self.cur.fetchall()
            print("IMPORTANT!!!!!!!!!!!!!: {0}".format(result))
            return result

        elif tag_id:
            if type(tag_id) is not int:
                raise TypeError("tag_id argument type must be int")

            self.cur.execute("SELECT file_id from files_tags WHERE tag_id=?", (tag_id,))
            #return self.cur.fetchall()
            result = self.cur.fetchall()
            print("fetch_from_files_tags result: {0}".format(result))

            # Empty result check
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
        """Search the db with tags and get a list of file_id's that have the tag(s) linked to them.
        WARNING THIS NEEDS TO BE WORKED ON!'"""

        # Make sure query argument is a string
        if type(query) is not str:
            raise TypeError("query type must be string")

        # Empty query string check
        if query.replace(" ", "") == "":  # If search bar is empty (Needs to remove " " spaces in future) # What do you mean?
            result = self.get_all_files()
            return result

        # This block of code needs working on and should not yet be implemented!
        """
        split = query.split(":")
        if len(split) == 2:
            print("split[0]: {0}".format(split[0]))
            x = ("file", "file_name", "f")
            if split[0] in x:
                self.cur.execute("SELECT id FROM files WHERE file_name=?", (query.split(":")[1],))
                result = self.cur.fetchall()
                print("result: {0}".format(result))
                return_list = []
                for x in result:
                    return_list.append(x[0])
                return return_list
            return print("split[0] in x: False")
        """

        # Main search logic starts
        query_list = query.split(" ")  # Create a list of tags via spliting at spaces. E.g. "tag_1 tag_2" = [tag_1, tag_2
        print("query_list: {0}".format(query_list))

        tag_id_list = []  # A list used to store tag_id that are found from the loop below.

        # Get tag_id from each tag listed in the query_list.
        # This is then used for getting the files asosiated with the tags found.
        for tag in query_list:
            if tag == "":  # This negates empty strings caused by spliting double spaces
                pass

            else:
                result_tag = self.get_tag(tag_name=tag)  # self.get_tag returns a dictionary if found, returns None if nothing was found

                # No result check
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
            result = self.fetch_from_files_tags(tag_id=tag_id)
            print("Result: {0}".format(result))
            if len(result) == 0:
                print("tag_id '{0}' is not assigned to any file.".format(tag_id))
                return None
            else:
                files_list.append(result)

        print("files_list: {0}".format(files_list))


        # Single tag search checker
        if len(files_list) == 1:
            return list(set(files_list[0]))  # Return a list of a list 'set' stripes any duplicates if somehow there are any


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


    def assign_tag(self, file_id, tag_id):
        """Assigns a tag_id to a file_id in the \"files_tags\"."""  # \" escapes the " " syntax
        if type(file_id) and type(tag_id) is not int:
            raise TypeError("file_id and tag_id must be int")

        result = self.fetch_from_files_tags(tag_id=tag_id, file_id=file_id)
        print(result)
        if len(result) > 0:
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


    def remove_tag(self, tag_name, force_remove=None):
        """Sets removed to 1 in db unless force_remove is True then removes the entry from the db.
        If sucsessfull returns True. If not sucsesfull returns False"""
        if type(tag_name) is not str:
            raise TypeError("tag_name must be str")

        if self.get_tag(tag_name) is None:
            print("Unable to find specified tag to remove.")
            return False

        if force_remove:
            t = self.get_tag(tag_name)
            self.cur.execute("DELETE FROM files_tags WHERE tag_id=?", (t['tag_id'], ))
            self.cur.execute("DELETE FROM tags where tag_name=?", (tag_name, ))
            return True
        else:
            self.cur.execute("UPDATE tags SET removed=1 WHERE tag_name=?", (tag_name,))
            self.commited = False
            return True


    ## Databsse cleanup functions

    def cleanup_files(self, remove_file=False):
        """Deletes all files entries that have the removed column set to 1."""
        if remove_file:
            print("Removed file test.")
        self.cur.execute("DELETE FROM files WHERE removed=1")
        self.commited = False
        return True


    def cleanup_tags(self):
        """Deletes all tags that have the removed column set to 1"""
        self.cur.execute("DELETE FROM tags WHERE removed=1")
        self.commited = False
        return True


    """
    def cleanup_files_tags(self):
            self.get_all_tags()
            self.cur.execute("SELECT * FROM files_tags")
            result = self.cur.fetchall()
            for x in result:
                file_id = x[0]
                tag_id = x[1]
                print("x: file_id: {0} tag_id: {1}".format(file_id, tag_id))
    """


    # Database miscellaneous function

    def commit(self):
        """Saves (commit) changes to the database."""
        self.conn.commit()
        self.commited = True
        print("Sucsessfully saved the database.")
        return True



if __name__ == '__main__':
    import sys
    sys.exit()
