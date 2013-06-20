bibliocoord
===========

Script to scrape Italian public libraries coordinates.

##############################################################################
#
# == ENGLISH ==
# (italiano sotto)
#
# === LICENCE ===
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
#
# === INFO ===
# Scraping data from: 
# http://anagrafe.iccu.sbn.it/opencms/opencms/
# Even if the footer says:
# « È libera la riproduzione dei dati per uso personale e a scopo didattico 
# e di ricerca a condizione che sia citata la fonte.
# Ogni altra riproduzione integrale o parziale dei dati, mediante qualsiasi 
# procedimento, deve essere autorizzata dall'ICCU»
#
# Scraped data are open under CC0 1.0 Universal Public Domain Dedication
# {{it}} http://www.beniculturali.it/ \
#            mibac/export/MiBAC/sito-MiBAC/ \
#                MenuPrincipale/Trasparenza/Open-Data/index.html
#
#
# == ITALIANO == 
#
# === LICENZA ===
# Questo scraper è rilasciato con licenza GPL (v.sopra)
#
# === INFO ===
# Scraper dei dati da: 
# http://anagrafe.iccu.sbn.it/opencms/opencms/
# 
# Anche se il footer dice:
# «È libera la riproduzione dei dati per uso personale e a scopo didattico 
# e di ricerca a condizione che sia citata la fonte.
# Ogni altra riproduzione integrale o parziale dei dati, mediante qualsiasi 
# procedimento, deve essere autorizzata dall'ICCU»
#
# {{it}} http://www.beniculturali.it/ \
#            mibac/export/MiBAC/sito-MiBAC/ \
#                MenuPrincipale/Trasparenza/Open-Data/index.html
#
##############################################################################

This script contains a (rather complicated) trick to get library coordinates
from the pages. 
This was used to get just the coordinates, while the other data were collected 
using a scraper on scraperwiki.com.
Now it has been superseded by the easier method implemented in
https://scraperwiki.com/scrapers/anagrafebiblioteche.
