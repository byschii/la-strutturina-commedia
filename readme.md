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

