#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.66 — Mapping sondes -> symboles pour GPL13667 (HG-U219, GSE62165).
Sources (voir PROVENANCE_866.md) :
- hgu219.db 3.2.3 (Bioconductor, Marc Carlson) : table `probes`
  (probe_id -> Entrez gene_id), source Entrez Gene 2015-Sep-27.
- org.Hs.eg.db 3.23.1 (Bioconductor, Marc Carlson) : `genes`
  (gene_id -> _id) + `gene_info` (_id -> symbol), symboles courants.
Règles gelées ici, avant toute construction :
- une sonde mappant vers PLUSIEURS Entrez ID est EXCLUE (ambiguë,
  jamais choisie à la main) ;
- une sonde sans Entrez ID est non mappée (exclue) ;
- plusieurs sondes vers un même symbole : agrégées par MÉDIANE
  au moment de la construction des flux (règle du projet).
Sortie : data/GPL13667_probe2symbol.tsv (probe_id<TAB>symbol),
+ journal des exclusions.
"""
import hashlib
import sqlite3

DATA = "/home/hatch/workspace/runs/pdac-v6/data"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    c = sqlite3.connect("/tmp/hgu219.db/inst/extdata/hgu219.sqlite")
    rows = c.execute("SELECT probe_id, gene_id FROM probes").fetchall()
    from collections import defaultdict
    by_probe = defaultdict(set)
    for pid, gid in rows:
        by_probe[pid].add(gid)
    n_distinct = len(by_probe)
    multi = {p: g for p, g in by_probe.items() if len(g) > 1}
    single = {p: next(iter(g)) for p, g in by_probe.items() if len(g) == 1}
    print(f"sondes distinctes : {n_distinct} ; multi-gènes exclues : {len(multi)} ; "
          f"à un seul gène : {len(single)}")

    c2 = sqlite3.connect("/tmp/org.Hs.eg.db/inst/extdata/org.Hs.eg.sqlite")
    gid2id = dict(c2.execute("SELECT gene_id, _id FROM genes").fetchall())
    id2sym = dict(c2.execute("SELECT _id, symbol FROM gene_info").fetchall())
    out = {}
    no_sym = []
    for pid, gid in single.items():
        _id = gid2id.get(gid)
        sym = id2sym.get(_id) if _id is not None else None
        if sym:
            out[pid] = sym
        else:
            no_sym.append((pid, gid))
    print(f"mappées vers un symbole : {len(out)} ; sans symbole : {len(no_sym)}")
    print(f"symboles distincts mappés : {len(set(out.values()))}")
    with open(f"{DATA}/GPL13667_probe2symbol.tsv", "w") as f:
        f.write("probe_id\tsymbol\n")
        for pid in sorted(out):
            f.write(f"{pid}\t{out[pid]}\n")
    with open("/home/hatch/workspace/runs/pdac-v6/GPL13667_mapping_866.txt", "w") as f:
        f.write("Mapping GPL13667 (HG-U219) — §8.66\n")
        f.write(f"hgu219.db_3.2.3.tar.gz SHA256 {sha(f'{DATA}/hgu219.db_3.2.3.tar.gz')}\n")
        f.write(f"org.Hs.eg.db_3.23.1.tar.gz SHA256 {sha(f'{DATA}/org.Hs.eg.db_3.23.1.tar.gz')}\n")
        f.write(f"sondes distinctes (table probes) : {n_distinct}\n")
        f.write(f"sondes multi-gènes exclues : {len(multi)}\n")
        f.write(f"sondes à un seul gène : {len(single)}\n")
        f.write(f"sondes mappées vers un symbole : {len(out)}\n")
        f.write(f"sondes sans symbole (Entrez sans entrée org.Hs.eg) : {len(no_sym)}\n")
        f.write(f"symboles distincts : {len(set(out.values()))}\n")
        f.write("Règle : sonde multi-gènes exclue ; agrégation par médiane par symbole.\n")
    print("Écrit : data/GPL13667_probe2symbol.tsv")


if __name__ == "__main__":
    main()
