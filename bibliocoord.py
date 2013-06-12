#!/usr/bin/python
# -*- coding: utf-8 -*-
#
###############################################################################
# Copyright (C) 2013 Cristian Consonni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# If not, see <http://www.gnu.org/licenses/>.
###############################################################################

import sys
import time
import urllib2
import urlparse
import sqlite3 as sqlite
import lxml.html as html
import selenium
from selenium import webdriver


MAXTRIES = 10
def get_page(url):
    fpage = None
    i=1
    while (not fpage) or (i > MAXTRIES):
        try:
            fpage = urllib2.urlopen(url)
        except Exception as e:
            print '%s' %str(e)
            fpage = None
            i=i+1

    return fpage

BASEURL='http://anagrafe.iccu.sbn.it/opencms/opencms/ricerche/'

SEARCHURL='http://anagrafe.iccu.sbn.it/opencms/opencms/ricerche/risultati.html?monocampo=&regione=&provincia=&comune=&codice_isil=&ricerca_tipo=home&monocampo:tipo=AND&start={start}'

maxidd=-1

con = None
try:
    con = sqlite.connect('bibliocoord.db')
    cur = con.cursor()

except sqlite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)

try:
    cur.execute('SELECT max(id) AS max FROM biblioteche')
    data = cur.fetchall()
    print data
    maxidd=data[0][0]
except Exception as e:
    print "No table, starting from zero"
    print e


if maxidd < 1:
    print "Starting from zero"
    maxidd=0
else:
    maxidd += 1
    print "Starting from: %d" %maxidd

TOTBIBLIO=17243
driver = webdriver.Firefox()
for s in range(maxidd,TOTBIBLIO+1,40):
    searchurl = SEARCHURL.format(start=s)
    print 'SEARCHURL:', searchurl

    fpage=get_page(searchurl)

    page = fpage.read()

    doc = html.document_fromstring(page)
    contenuto = doc.xpath("//div[@class='contenuto']")[0]
    lista=[(a,a.getchildren()) for a in contenuto.getchildren() if a.tag=='a']

        
    for a,riga in lista:
        link=a.values()[0]
        bibliourl=BASEURL+link
        print 'BIBLIOURL:', bibliourl
        par = urlparse.parse_qs(urlparse.urlparse(bibliourl).query)
        idd=int(par['start'][0])
        biblio = dict()
        biblio['id']=idd
        driver.get(bibliourl)
        retry = True
        for i in range(0,MAXTRIES):
            if not retry:
              break
            try:
                driver.execute_script(""" 
                var oldFunction = createBiblioLabel;
                createBiblioLabel = function(biblioteca) {
                  window.myVar = + biblioteca.lat.toString() + ',' + biblioteca.lng.toString();
                  return createBiblioLabel(biblioteca);
                };""")
            except Exception:
                print 'excute_script failed'
                retry = True
                time.sleep(2)
                continue
            try:
                elem = driver.find_element_by_class_name("google")
            except selenium.common.exceptions.NoSuchElementException:
                print 'No such element'
                retry = True
                time.sleep(2)
                continue
            link = elem.find_element_by_tag_name('a')
            time.sleep(1)
            link.click()
            time.sleep(1)
            name = driver.find_element_by_class_name("titolo").text
            try:
                coords = driver.execute_script("return window.myVar;").split(',')
            except:
                print 'Error with coords'
                retry = True
                time.sleep(2)
                continue
            biblio['name'] = name.strip()
            biblio['lat'] = coords[0]
            biblio['lon'] = coords[1]
            query="""INSERT INTO biblioteche VALUES({idd},{lat},{lon},"{name}")
                  """.format(idd=biblio['id'],
                                   lat=biblio['lat'],
                                   lon=biblio['lon'],
                                   name=biblio['name'].encode('utf-8')
                                  )
            print query
            try:
                cur.execute(query)
            except Exception:
                print 'Error executing query'
                retry = True
                time.sleep(2)
                continue

            try:
                con.commit()
            except Exception:
                print 'Error commiting'
                retry = True
                time.sleep(2)
                continue

            retry = False

        time.sleep(3)

driver.close()
con.close()
