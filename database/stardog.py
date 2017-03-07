"""
Wrapper class and functions for interacting with a stardog database.
"""

__all__ = ["StardogDB"]
__version__ = '0.1'
__author__ = 'Tom Amon and Nanxi Zhang'

import subprocess

_STARDOG_INSTALL_PATH = "/home/stardog/bin/"


class StardogDB:

    def __init__(self, database_name):
        self._database_name = database_name

    def remove_all(self):
        #./stardog data add db filename.ttl
        path = _STARDOG_INSTALL_PATH + "stardog"
        command = [path, "data", "remove", "-a"]
        subprocess.call(command)

    def add(self, ttl_files):
        #./stardog data add db filename.ttl
        path = _STARDOG_INSTALL_PATH + "stardog"
        command = [path, "data", "add", self._database_name]
        subprocess.call(command + ttl_files)
         
    def query(self, str_query):
        #./stardog query chatbotDB
        path = _STARDOG_INSTALL_PATH + "stardog"
        out = subprocess.check_output([path, "query", self._database_name, str_query])
        value = str(out).split("|")[3].strip("\" ")
        return value


if __name__ == "__main__":
    test = """
    prefix cb: <http://drexelchatbot.com/rdf/>
    
    SELECT ?o
    WHERE
    {
        ?s cb:name "Marcello Balduccini" .
        ?s cb:title ?o .
    }
    """
    
    sdb = StardogDB("chatbotDB")
    sdb.query(test)