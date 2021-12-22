# La Strutturina Commedia

Just a little effort to structure the Divine Comedy (Divina Commedia) di Dante Alighieri. Maybe someone will use this to spread the beauty in it.

I always thought that there was something really beautiful in the way dant wrote his Comedy.
- 3 *cantiche* (the main division in the Comedy).
- Every *cantica* divided in 33 *canti* (plus 1 *canto* in the first *cantica*).
- Every *canto* composed of about 142 *versi* each (14235 in total).
- Every *verso* "almost" the same length of 11 syllables (it's a little complicated, it can be also longer, but the last accent has to be on the 11th syllable).
- These *versi* are grouped by 3 in *terzine*.
- Every *terzina* with a precise rhyme structure: *ABA BCB ... VZV Z*  

And, also, the amount of meaning Dante put in every *terzina* (but this is harder to appreciate, the structure is undoubtedly wonderfull).

C'mon! It is amazing!🤤

## Everything is in an SQLite database

There is only a table called `divina_commedia`.

Every entry is uniquely identified by the combination of `num_cantica`, `num_canto`, `num_verso`.

Every `num_cantica`, `num_canto`, `num_verso` has a corresponding `TEXT` version.
- `num_cantica`, goes from 1 to 3 and corresponds to one of *"Inferno" "Purgatorio" "Paradiso"* in `nome_cantica`
- `num_canto`, goes from 1 to 34 for `num_cantica = 1` (aka "Inferno")



	"nome_cantica" TEXT NULL,
	"num_rom_canto" TEXT NULL,
	"verso" TEXT NULL,
	"num_terzina" INTEGER NULL,
	PRIMARY KEY ("num_libro", "num_canto", "num_verso")



## Examples

#### How to get the last *terzina* of every *cantica*.

```sql
SELECT dc.nome_libro, dc.num_rom_canto, dc.num_terzina, verso FROM divina_commedia AS DC JOIN (
	SELECT c.num_libro,  max(D.canto) AS canto, max(num_terzina) AS terzina
	FROM divina_commedia C
	JOIN (select num_libro, max(num_canto) as canto from divina_commedia GROUP BY  nome_libro ) D
	WHERE c.num_libro = d.num_libro AND d.canto = c.num_canto
	GROUP BY c.num_libro
) as UT
where dc.num_libro = ut.num_libro AND dc.num_canto = ut.canto AND dc.num_terzina = ut.terzina
```

| nome_libro |  num_rom_canto | num_terzina |                 verso                |
|:----------:|:---------:|:-----------:|:-----------------------------------------:|
|   Inferno  |   XXXIV   |      47     |   E quindi uscimmo a riveder le stelle.   |
| Purgatorio |  XXXIII   |      49     |   puro e disposto a salire a le stelle.   |
|  Paradiso  |  XXXIII   |      49     | l’amor che move il sole e l’altre stelle. |

Every *cantica* ends in 'stelle' (🌟🌟) !!!
