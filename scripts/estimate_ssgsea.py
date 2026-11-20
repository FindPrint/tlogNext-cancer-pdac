#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.54 — Port Python fidèle de tidyestimate::estimate_score (ssGSEA).
Source de l'algorithme : tidyestimate 1.1.1, R/estimate_score.R
(GitHub KaiAragaki/tidyestimate, main), lui-même implémentation de
Yoshihara et al. 2013 (Nat Commun 4:2612, doi 10.1038/ncomms3612),
ssGSEA de Barbie et al. 2009 (Nature 462:108).
Étapes (identiques au R) :
  1. rangs par échantillon, ex æquo moyennés (R rank, ties.method="average")
  2. rangs remis à l'échelle : 10000 * rang / n_gènes
  3. par échantillon : gènes triés par rang DÉCROISSANT (ordre stable, comme
     R order() radix) ; hit = gène dans la signature ; valeurs ^ 0.25
  4. ES = somme (cumsum(récompense hits) - cumsum(pénalité non-hits))
     récompense = (hit * valeur) / somme(valeurs des hits)
     pénalité   = (non-hit) / nombre de non-hits
  5. ESTIMATE = stromal + immune. Pas de pureté (is_affymetrix = FALSE :
     la formule cosinus est réservée aux puces Affymetrix par Yoshihara).
Ne dépend que de numpy/pandas/scipy.
"""
import numpy as np
import pandas as pd
from scipy import stats


def ssgsea_es(scaled_ranks, genes, gene_set):
    """ES ssGSEA pour UN échantillon.
    scaled_ranks : (n_genes,) rangs remis à l'échelle, dans l'ordre des lignes.
    genes : (n_genes,) symboles correspondants.
    gene_set : set de symboles de la signature.
    """
    order = np.argsort(-scaled_ranks, kind="stable")
    vals = scaled_ranks[order] ** 0.25
    hit = np.isin(genes[order], list(gene_set))
    n_hit = int(hit.sum())
    if n_hit == 0:
        return float("nan")
    hit_exp = vals[hit]
    hit_reward = np.cumsum(np.where(hit, vals, 0.0) / hit_exp.sum())
    no_hit_penalty = np.cumsum((~hit).astype(float) / float((~hit).sum()))
    return float(np.sum(hit_reward - no_hit_penalty))


def filter_common_genes(expr_df, common_df):
    """Port fidèle de tidyestimate::filter_common_genes(id = "hgnc_symbol",
    find_alias = TRUE) — tel qu'utilisé dans la vignette (ov : 9 903 exacts
    + 461 par alias = 10 364 trouvés sur 10 391).
    expr_df : DataFrame gènes (index = symboles) x échantillons.
    common_df : DataFrame (entrezgene_id, hgnc_symbol, external_synonym).
    Retourne (filtered_df, info) où filtered_df ne garde que les gènes
    communs (symboles renommés vers le symbole canonique en cas d'alias),
    et info donne n_exact, n_alias, total, et la liste des renommages.
    Règle d'alias conservatrice (find_alias) : un gène commun manquant n'est
    récupéré via un synonyme que si ce synonyme ne correspond qu'à UN gène
    des données ET que ce gène des données ne correspond qu'à UN gène commun.
    """
    common_symbols = set(common_df["hgnc_symbol"])
    exact_idx = [s for s in expr_df.index if s in common_symbols]
    filtered = expr_df.loc[exact_idx]
    missing = sorted(common_symbols - set(expr_df.index))
    # Candidats alias : lignes common_genes des gènes manquants dont le
    # synonyme externe égale un symbole présent dans les données.
    sub = common_df[common_df["hgnc_symbol"].isin(missing)]
    data_symbols = list(expr_df.index)
    data_pos = {s: i for i, s in enumerate(data_symbols)}
    pairs = []  # (common_gene, data_symbol, data_pos)
    for _, row in sub.iterrows():
        alias = row["external_synonym"]
        if alias in data_pos:
            pairs.append((row["hgnc_symbol"], alias, data_pos[alias]))
    pair_df = pd.DataFrame(pairs, columns=["common_gene", "data_symbol", "pos"])
    renamed = {}
    if len(pair_df):
        cnt_common = pair_df.groupby("common_gene").size()
        cnt_data = pair_df.groupby("pos").size()
        ok = pair_df[
            pair_df["common_gene"].map(cnt_common).eq(1)
            & pair_df["pos"].map(cnt_data).eq(1)
        ]
        for _, r in ok.iterrows():
            renamed[r["data_symbol"]] = r["common_gene"]
    alias_rows = []
    for old, new in renamed.items():
        row = expr_df.loc[[old]].copy()
        row.index = [new]
        alias_rows.append(row)
    if alias_rows:
        filtered = pd.concat([filtered] + alias_rows)
    info = {"n_exact": int(len(exact_idx)),
            "n_missing_before_alias": int(len(missing)),
            "n_alias": int(len(renamed)),
            "n_total": int(filtered.shape[0]),
            "renamed": renamed}
    return filtered, info


def estimate_scores(expr_df, stromal_set, immune_set):
    """expr_df : DataFrame gènes (index = symboles) x échantillons (colonnes),
    valeurs d'expression numériques brutes (log2(RSEM+1) ici).
    Retourne DataFrame : sample, stromal, immune, estimate.
    """
    genes = np.array(expr_df.index, dtype=object)
    mat = expr_df.values.astype(float)
    n_genes = mat.shape[0]
    ranks = np.apply_along_axis(stats.rankdata, 0, mat)
    scaled = 10000.0 * ranks / float(n_genes)
    out = []
    for j, sample in enumerate(expr_df.columns):
        s_stromal = ssgsea_es(scaled[:, j], genes, stromal_set)
        s_immune = ssgsea_es(scaled[:, j], genes, immune_set)
        out.append({"sample": sample, "stromal": s_stromal,
                    "immune": s_immune, "estimate": s_stromal + s_immune})
    return pd.DataFrame(out)
