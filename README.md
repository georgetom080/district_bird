Source needed:<br>
Ebird Dataset of the entire state in tsv format (same format received via data download form ebird).

Usage:<br>
python3 district_top_species.py -n 100 -c Krishnagiri
> Generates list of most frequent 100 birds seen in Krishnagiri district.

python3 district_top_species.py -n 50 -i -c Krishnagiri
> Generates list of most frequent 50 birds seen in the state in all areas except Krishnagiri district.
