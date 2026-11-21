#!/usr/bin/env python3
"""Examen §8.89 — suppléments Chen non téléchargés (MOESM1/2/16) + dépôts.

Reproduit toutes les mesures de la section §8.89 à partir des fichiers
détenus dans chen884_scratch/ (déjà vérifiés §8.84) et chen889_scratch/
(nouveaux téléchargements du 21 nov. 2026). Aucun téléchargement ici.
Sortie : examine_889.json (ce script) + sorties texte déjà produites
par pdftotext (MOESM1.txt, MOESM2.txt, MOESM16.txt).
"""
import hashlib, json, os, re
import openpyxl

BASE = os.path.expanduser('~/workspace/runs/pdac-v6')
S84 = os.path.join(BASE, 'chen884_scratch')
S89 = os.path.join(BASE, 'chen889_scratch')
out = {}

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

# 1. Empreintes des 3 nouveaux fichiers + re-vérification des détenus
new = {
    'MOESM1_SupplInfo.pdf': '4b70d25b078f21cc2612963d807e9a1ab27782ccc8aa721482043b16e60aa61f',
    'MOESM2_PeerReview.pdf': 'ce939f2227d92a7147e3d5c6681bd9fe0e8ab70c5a8c7fad99695016bfd65d67',
    'MOESM16_ReportingSummary.pdf': '69a959c3ff56eff607dfa561b8734f537780e16dcf8376ade26c1b0afb95c499',
}
out['new_files'] = {}
for fn, exp in new.items():
    p = os.path.join(S89, fn)
    got = sha256(p)
    out['new_files'][fn] = {'bytes': os.path.getsize(p), 'sha256': got,
                            'matches_download_receipt': got == exp}
held = {
    'MOESM3_description.pdf': '3a84243b7b4c3bbab172a4ead61725663fd076cd00664091ea0fad3c5313c569',
    'MOESM4.xlsx': '09968fbc39659f2ddf79bc40b7269e4cb5899e719bfb9d4b869ae1d55c171dfd',
    'MOESM5.xlsx': 'c759ab51256b69605fcaba96e30d0f90a95c3737db4cb16eb46ce4b4d8ef25eb',
    'MOESM6.xlsx': 'af69c390a301f390a7c0d5b2e949057af813300f75669b62321c7ec55cb01392',
    'MOESM7.xlsx': 'bf5cab3f8f874451bcbc5aedbf4820481575d73fa079292797de5c63aca194fe',
    'MOESM8.xlsx': '9b440dd95795d33585f3ae712dc1aa457bf5bc079dea704125a7c98a99d5e389',
    'MOESM9.xlsx': '017632df49433135102830813ca7dfaaee56684264c1540b2614a79b802a1957',
    'MOESM10.xlsx': '2e65713b3c575be73f81d4cf21b704a235315f6220472f64db0972465a48ccaa',
    'MOESM11.xlsx': 'da2c45834835df838c5d7555c5ed45a4642bca1be2d7e788520e066ed12ff25c',
    'MOESM12.xlsx': '70a0ff03362fe595f8b93662a2eec30b5978631a2077deb0d46dadecd8ff904b',
    'MOESM14.xlsx': '55c35f4a2b49e5622b3d297fdffe1d7b7c7a66d8347edfc54f06e34b72de3864',
    'MOESM15.xlsx': '10ce1ef81e6c75841419bafbbee1c52d86550a63474d76a634509bbccb8d7a44',
    'MOESM17_sourcedata.xlsx': '917a1011426c5ee749343ccabf8126e35923a65c4719ec929f84aa29a511f7b1',
}
out['held_files_reverified'] = {}
for fn, exp in held.items():
    got = sha256(os.path.join(S84, fn))
    out['held_files_reverified'][fn] = {'sha256': got, 'matches_PROVENANCE_884': got == exp}
mo13 = sha256(os.path.join(BASE, 'data', 'Chen2025_MOESM13_SupplData10.xlsx'))
out['MOESM13'] = {'sha256': mo13,
                  'matches_PROVENANCE_884': mo13 == '0e009cd56d2f6c25b0b355590becc4abfee3e1080633173bc33606d1bf325340'}

# 2. Comptages de mots-clés dans les textes extraits (pdftotext -layout)
def counts(path):
    t = open(path, encoding='utf-8', errors='ignore').read()
    out_c = {}
    for pat in ['DAC', 'KRAS', 'MTAP', '9p21', 'G12C', 'CDKN2A',
                'organoid', 'Organoid', 'Supplementary Table', 'Supplementary Fig']:
        out_c[pat] = t.count(pat)
    return t, out_c
t1, c1 = counts(os.path.join(S89, 'MOESM1.txt'))
t2, c2 = counts(os.path.join(S89, 'MOESM2.txt'))
t16, c16 = counts(os.path.join(S89, 'MOESM16.txt'))
out['keyword_counts'] = {'MOESM1': c1, 'MOESM2': c2, 'MOESM16': c16}
out['MOESM16_text_chars'] = len(t16.strip())

# 3. Liste DAC de la Fig. 14c (MOESM1) : ordre visuel = ordre d'extraction
#    vérifié par pdftotext -bbox p.21 (x croissant) — voir section §8.89.
fig14 = re.findall(r'DAC_\d+', t1)
fig14_unique = sorted(set(fig14), key=lambda x: int(x.split('_')[1]))
# ordre d'apparition (visuel, vérifié par bbox)
seen = []
for d in fig14:
    if d not in seen:
        seen.append(d)
out['fig14c'] = {'n_tokens': len(fig14), 'n_unique': len(fig14_unique),
                 'order_visual': seen}

# 4. Colonnes MOESM13 (46 PDO criblés) + recoupement Fig. 14c
wb = openpyxl.load_workbook(os.path.join(BASE, 'data', 'Chen2025_MOESM13_SupplData10.xlsx'),
                            read_only=True, data_only=True)
ws = wb['All Drugs AUC']
rows = list(ws.iter_rows(values_only=True))
cols46 = [c for c in rows[0][2:] if c]
out['MOESM13_columns'] = {'n': len(cols46), 'cols': cols46}
inter = [d for d in seen if d in set(cols46)]
out['fig14c_overlap_screened'] = {
    'n_fig14c': len(seen), 'n_screened': len(cols46),
    'n_covered': len(inter),
    'screened_not_in_fig14c': sorted(set(cols46) - set(seen)),
    'fig14c_not_screened': sorted(set(seen) - set(cols46))}

# 5. Groupe MT Fig. 14c (barre d'annotation mesurée sur le rendu p.21,
#    200 dpi : teal x_pts 51,9-74,8 ; orange dès 74,9 ; pas 5,719 ; bord
#    gauche de la barre 51,9 -> (74,9-51,9)/5,719 = 4,02 colonnes).
mt14 = seen[:4]
out['fig14c_MT'] = {'MT': mt14, 'n_MT': len(mt14),
                    'MT_in_screened': [d for d in mt14 if d in set(cols46)],
                    'bar_teal_x_pts': [51.9, 74.8], 'bar_orange_from_x_pts': 74.9,
                    'column_pitch_pts': 5.719, 'MT_columns_measured': 4.02}

# 6. Statut CFTR Fig. 6e relu dans MOESM17 (vérification du §8.84)
wb2 = openpyxl.load_workbook(os.path.join(S84, 'MOESM17_sourcedata.xlsx'),
                             read_only=True, data_only=True)
ws2 = wb2['Figure 6']
r2 = list(ws2.iter_rows(values_only=True))
fig6e = {}
for row in r2[100:125]:
    if row and isinstance(row[0], str) and row[0].startswith('DAC') and len(row) > 1:
        fig6e[row[0]] = row[1]
out['fig6e_CFTR'] = fig6e
out['fig6e_MT'] = sorted([k for k, v in fig6e.items() if v == 'MT'])
_fig6e_norm = set('DAC_' + k[3:] for k in fig6e)
out['fig6e_MT_vs_fig14c'] = {
    'MT_fig6e_but_WT_fig14c': sorted(
        set('DAC_' + k[3:] for k in out['fig6e_MT']) - set(mt14)),
    'MT_fig14c_but_not_in_fig6e_15': sorted(set(mt14) - _fig6e_norm),
    'MT_in_both': sorted(
        set('DAC_' + k[3:] for k in out['fig6e_MT']) & set(mt14))}

# 7. Article détenu : comptages de référence (article.html §8.84)
ta = open(os.path.join(S84, 'article.html'), encoding='utf-8', errors='ignore').read()
import html as _html
ta2 = _html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', ta)))
out['article_html_counts'] = {p: ta2.count(p) for p in
                              ['MTAP', 'G12C', 'Supplementary Table', 'HRA005195',
                               'HRA010277', 'ST003734', 'Code Ocean']}
out['article_html_MOESM'] = sorted(set(re.findall(r'MOESM\d+', ta)))

with open(os.path.join(S89, 'examine_889.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(json.dumps({k: out[k] for k in
                  ['fig14c_overlap_screened', 'fig14c_MT', 'fig6e_MT',
                   'fig6e_MT_vs_fig14c', 'article_html_MOESM']}, indent=2, ensure_ascii=False))
print('keyword MOESM1:', c1)
print('keyword MOESM2:', c2)
print('MOESM16 chars:', len(t16.strip()))
print('all held match:', all(v['matches_PROVENANCE_884'] for v in out['held_files_reverified'].values()))
print('all new match receipt:', all(v['matches_download_receipt'] for v in out['new_files'].values()))
