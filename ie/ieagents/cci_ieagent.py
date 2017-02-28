"""
Implementation of the IEAgent interface for the College of computing and
infomatics faculty website, located here: http://drexel.edu/cci/contact/Faculty/

Data is stored in an html table, with each person have a single row(tr).
The data, very conviently, is all in their own div. So just going through 
each div of the row should everything. The data is in the order:
Name
Title
Department
Interests
Email
Phone
Office

"""

__all__ = ['CciIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, DatabaseRow


class CciIEAgent(IEAgent):

    _link = "http://drexel.edu/cci/contact/Faculty/"
        
    #TODO: Remove this when database in place
    _info_filename = "results/cci.txt"

    def refresh(self, database):
        #TODO: Remove this when database in place
        database = open (self._info_filename, 'w')

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.select('tr')
        for i in range(1, len(elems)):
            data = elems[i].select('div')
            data = list(map(lambda x: x.getText().strip(' \t\n\r'), data))

            prof = DatabaseRow()

            prof.name = data[1]
            prof.title = data[2]
            prof.department = data[3]
            prof.interests = data[4].split(':')[1]
            prof.email = data[5].split(":")[1]
            if data[6]:
                prof.phone = data[6].split(":")[1]
            if data[7]:
                prof.office = data[7].split(":")[1]
            prof.store(database)
    
        #TODO: Remove this when database in place
        database.close()
