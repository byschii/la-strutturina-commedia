
import sqlite3
from sqlite3.dbapi2 import Connection
from numpy import array

from pathlib import Path
from os      import remove  as remove_file
from os.path import exists  as file_exists

from typing import Any, List, Literal, Optional, Union

import requests
from bs4 import BeautifulSoup


class DbManager:
    def __init__(self, sqlite_file_name:Path):
        assert sqlite_file_name.suffix == ".db", "Not a valid db file name ({sqlite_file_name})" 
        self.sqlite_file_name = sqlite_file_name
        self.sqlite_conn: Connection = self._init_sqlite()

    def _init_sqlite(self, first_sql:Optional[str]=None) -> Connection:
        sqlite_conn = sqlite3.connect(self.sqlite_file_name)
        if first_sql is not None:
            self.write_on_db(first_sql)
        return sqlite_conn

    def _detach_sqlite(self)-> bool:
        self.sqlite_conn.close()
        if file_exists(self.sqlite_file_name):
            remove_file(self.sqlite_file_name)
        return file_exists(self.sqlite_file_name)

    def write_on_db(self, sql:str, args:Optional[tuple]=None)-> None:
        if self.sqlite_conn is not None:
            if args is None:
                self.sqlite_conn.execute(sql)
            else:
                self.sqlite_conn.execute(sql, args)
            self.sqlite_conn.commit()
        else:
            raise Exception("Writing sql without connection")

    def get_num_elements(self, table_name:str)-> int:
        return self.sqlite_conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]


def get_versi_canto(link_canto):
	cantico = BeautifulSoup(
			requests.get(link_canto).text, "lxml"
		).find("div", {"class":"poem"})

	for span in cantico.find_all("span"):
		if len(span.text) < 4:
			span.decompose()

	endecasillabi = list(map(
		lambda verso: (verso[0]+1 , verso[1]),
		enumerate(
			map(lambda s:s.strip(),
				filter( lambda el : el.replace(u'\xa0', u' ') not in ["", " "] ,
				cantico.text.split("\n")
			)
	))))
	return endecasillabi


def get_all_links(link_libro):
	cantico = BeautifulSoup(
			requests.get(link_libro).text, "lxml"
		).find_all("ul")

	ahrefs = []
	for c in cantico:
		if c.a is not None and c.a.attrs.keys() == set(["href", "title"]):
			if "Commedia" in str(c.a):
				ahrefs.append(c.a)
	return ahrefs

db = DbManager(Path("divinacommedia.db"))


# num_libro
# nome_libro
# num_rom_canto, num_canto
# num_verso
# verso
# num_terzina
db.write_on_db(f"""
CREATE TABLE IF NOT EXISTS divina_commedia (
	num_libro INTEGER, nome_libro TEXT, num_rom_canto TEXT, num_canto INTEGER, num_verso INTEGER, verso TEXT, num_terzina INTEGER,
	PRIMARY KEY (num_libro, num_canto, num_verso)
);""")



link_libri = [
	("Inferno", "https://it.wikisource.org/wiki/Divina_Commedia/Inferno"),
	("Purgatorio", "https://it.wikisource.org/wiki/Divina_Commedia/Purgatorio"),
	("Paradiso", "https://it.wikisource.org/wiki/Divina_Commedia/Paradiso")
]


for j, (nome_libro, link_libro) in enumerate(link_libri):
	for i, a in enumerate(get_all_links(link_libro)):
		link_canto = "https://it.wikisource.org" + a["href"]

		for nv, versi in get_versi_canto(link_canto):
			print(
				j+1, nome_libro,
				link_canto.split("_")[-1], i+1,
				nv, versi, int(nv//3.01+1 )
			)

			db.write_on_db(f"""
				INSERT INTO divina_commedia (num_libro, nome_libro, num_rom_canto, num_canto, num_verso, verso, num_terzina) VALUES (?, ?, ?, ?, ?, ?, ?);""",
				(
					j+1, nome_libro,
					link_canto.split("_")[-1], i+1,
					nv, versi, int(nv//3.01+1 )
				)
				)




