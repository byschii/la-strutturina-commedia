# La Strutturina Commedia

Just a little effort to structure the Divine Comedy (Divina Commedia) di Dante Alighieri. Maybe someone will use this to spread the beauty in it.

I always thought that there was something really beautiful in the way dant wrote his Comedy.
- 3 *cantiche* (the main division in the Comedy).
- Every *cantica* divided in 33 *canti* (plus 1 *canto* in the first *cantica*).
- Every *canto* composed (on average) of 142 *versi* each (14235 in total).
- Every *verso* "almost" the same length of 11 syllables (it's a little complicated, it can be also longer, but the last accent has to be on the 11th syllable).
- These *versi* are grouped by 3 in *terzine*.
- Every *terzina* with a precise rhyme structure: *ABA BCB ... VZV Z*  

And, also, the amount of meaning Dante put in every *terzina* (but this is harder to appreciate, the structure is undoubtedly wonderfull).

C'mon! It is amazing!🤤

## Everything is in an SQLite database

There is only a table called `divina_commedia`.

Every entry is uniquely identified by the combination of `num_cantica`, `num_canto`, `num_verso`.
- `num_cantica` goes from 1 to 3
- `num_canto`, goes from 1 to 34 for `num_cantica = 1` and from 1 to 33 for `num_cantica = 2  or num_cantica = 3`
- `num_verso`, goes from 1 to 160, depending on `num_canto`

Every `num_cantica`, `num_canto`, `num_verso` has a corresponding `TEXT` version.
- `nome_cantica` corresponds to one of *Inferno, Purgatorio, Paradiso* depending on `num_cantica`
- `nome_canto`, corresponds to *I* if `num_cantica = 1`, to *X* if `num_cantica = 10`, to *XXXIV* if `num_cantica = 34` (it's based on [how romans counted](https://en.wikipedia.org/wiki/Roman_numerals)) 
- `verso` is what actually Dante wrote. *Technically, how Giorgio Petrocchi (Firenze, 1994) wrote. Which is kind of the official version.*

I also added `num_terzina`, which is usefull to get *vers* grouped by 3... it's just a function of `num_verso`.


## Query Examples

#### How to get the last *terzina* of every *cantica*.

```sql
SELECT dc.nome_cantica, dc.num_rom_canto, dc.num_terzina, verso FROM divina_commedia AS DC JOIN (
	SELECT c.num_cantica,  max(D.canto) AS canto, max(num_terzina) AS terzina
	FROM divina_commedia C
	JOIN (select num_cantica, max(num_canto) as canto from divina_commedia GROUP BY  nome_cantica ) D
	WHERE c.num_cantica = d.num_cantica AND d.canto = c.num_canto
	GROUP BY c.num_cantica
) as UT
where dc.num_cantica = ut.num_cantica AND dc.num_canto = ut.canto AND dc.num_terzina = ut.terzina
```

| nome_cantica |  num_rom_canto | num_terzina |               verso                |
|:----------:|:---------:|:-----------:|:-----------------------------------------:|
|   Inferno  |   XXXIV   |      47     |   E quindi uscimmo a riveder le stelle.   |
| Purgatorio |  XXXIII   |      49     |   puro e disposto a salire a le stelle.   |
|  Paradiso  |  XXXIII   |      49     | l’amor che move il sole e l’altre stelle. |

Also take a moment to notice that every *cantica* ends in 'stelle' (🌟🌟) !!!


#### How to get the number of *versi* for every *canto*

```sql
SELECT nome_cantica, num_rom_canto, max(num_verso)
FROM divina_commedia
GROUP BY num_canto
```

| nome_cantica |  num_rom_canto | num_terzina |                 verso              |
|:----------:|:---------:|:-----------:|:-----------------------------------------:|
|   Inferno  |   XXXIV   |      47     |   E quindi uscimmo a riveder le stelle.   |
| Purgatorio |  XXXIII   |      49     |   puro e disposto a salire a le stelle.   |
|  Paradiso  |  XXXIII   |      49     | l’amor che move il sole e l’altre stelle. |