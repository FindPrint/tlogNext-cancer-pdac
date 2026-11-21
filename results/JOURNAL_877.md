# JOURNAL_877 — §8.77 réparation de la reproductibilité

Protocole gelé : PROTOCOL_reproductibilite_877.md (SHA ci-dessous, à compléter après écriture).
Pipeline v6.2 SHA vérifié avant le gel : f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf.

## Téléchargements et vérifications

(entrées ajoutées au fur et à mesure, date UTC, URL, taille, SHA, conforme ou non)

dbe1746f7233e69a3052407576ebf6043080016c97a12d41f76244fc569a4030  PROTOCOL_reproductibilite_877.md

## 2026-11-21 01:38–01:44 UTC — récupération des gaps (toutes vérifiées par SHA)

- G4 PRISM 24Q2 meta : API figshare 25917643 lue ; fichier 46630978,
  URL https://ndownloader.figshare.com/files/46630978 ; taille 157 294 o ;
  SHA-256 13a85da9e45656c455d3911a4491f3636d7d0975a9d2333dc3d0a3e2cd3b0526
  = §7. FERME 1/1.
- G5 PRISM 19Q4 : API figshare 9393293 lue ; 4 download_url directs :
  dose-response 20237739, replicate-collapsed 20237763, cell-line-info
  20237769, readme 20238123. Re-téléchargés : cell-line-info SHA
  b93436b5…8d27 + MD5 6737b4aa… = §8 ; readme SHA ed453e2b…9c99 + MD5
  421d0bba… = §8 ; replicate-collapsed SHA 9d0d1fb4…84f7 + MD5
  54765b36… = §8 ; dose-response (264 340 589 o, unité systemd
  repro877-dose-response, Result=success) SHA 88d10135…fec8 + MD5
  e629b9d5… = §8. FERME 4/4.
- G6 QCMG : API GitHub datahub, dossier public/paad_qcmg_uq_2016 lu ;
  fichiers LFS : contenu réel via media.githubusercontent.com (le
  download_url raw renvoie le pointeur LFS de 130 o). patient SHA
  ae7fc6d7…6a95, échantillon SHA c70daf3e…ceca = §12. FERME 2/2.
- G8 data_clinical_patient.txt (test C) : hypothèse testée — étude
  paad_tcga_pan_can_atlas_2018 dans datahub ; contenu réel via
  media.githubusercontent.com ; taille 58 621 o ; SHA
  0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5
  = SHA consigné §11. Le pointeur LFS lu via raw.githubusercontent.com
  (130 o) porte lui-même `oid sha256:0c274268…` — double confirmation.
  FERME. La lacune de provenance la plus grave du projet est close :
  source = dépôt GitHub cBioPortal/datahub, étude
  paad_tcga_pan_can_atlas_2018.
- G9 mit_test.csv : URL reconstruite
  https://raw.githubusercontent.com/ncats/PANC1/main/MIT/test.csv ;
  taille 3 249 228 o ; SHA 9f3ae189…6e27 = §10. FERME (URL vérifiée).
- G10 CPTAC : API Zenodo 8394329 lue ; 4 fichiers présents, tailles et
  MD5 conformes au §6 ; links.self consignés (voir section). FERME par
  consignation (le script télécharge déjà via cette API).
- G2 Birnbaum : page PMC5674743 lue (DOI 10.1186/s12943-017-0739-z,
  Mol Cancer 2017 ; figure 12943_2017_739) ; Europe PMC
  supplementaryFiles = HTTP 500 (échec consigné) ; URLs reconstruites
  selon le patron Springer attesté (Bailey MOESM270, §5.5) :
  static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM{i}_ESM.xlsx ;
  5/5 tailles et SHA-256 identiques au §13. FERME 5/5.
- G1 ng3398 : page Nature ng.3398 lue (titre confirmé) ; curl page = HTTP
  303, section suppléments non lisible par ce moyen (consigné) ; URLs
  reconstruites selon le même patron Springer, code revue 41588 :
  static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM{n}_ESM.{ext} ;
  5/5 tailles et SHA-256 identiques au §3.2. FERME 5/5.
- G3 ICGC Xena : listing S3 = HTTP 403 (consigné) ; candidats S3 directs
  = 403 (consignés) ; hub icgc.xenahubs.net : probe map .gz = 200,
  NMF .txt = 404, NMF .txt.gz = 200 (le fichier local est bien .txt.gz).
  URLs retenues : https://icgc.xenahubs.net/download/PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp.gz
  et https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_NMF_class_assignment.txt.gz ;
  tailles 353 314 o / 447 o ; SHA b09a746f…75537 / f1e84b99…21e2f = §5.3/§5.4.
  FERME 2/2.
- G7 SOFT GPL20769 : chemin deviné au §15.4 (GPL2nnn) = 404 (consigné) ;
  règle de regroupement GEO vérifiée (masquer les 3 derniers chiffres :
  20769 -> GPL20nnn, comme 6244 -> GPL6nnn au §4.1) ;
  URL https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL20nnn/GPL20769/soft/GPL20769_family.soft.gz ;
  taille 37 588 662 o exactement = §3.1 ; titre plateforme confirmé
  (Agilent-014850 Whole Human Genome Microarray 4x44K G4112F, Gene Symbol
  Version, July 2014) ; table 19 750 lignes = en-tête + 19 749 lignes ;
  MD5 4c39e802ec78170d7ed5c8c2cc2b0bec, SHA-256
  ecb1b79a6b89e521a1116a3113fcb9a5af1c181329eec8257e044e0683822d3e
  (nouveaux, à consigner). FERME.

Bilan gaps : 19/19 fichiers du §17 FERMES + G7 + G8 + G9 + G10 fermés.
Aucun gap irrécupérable. Aucune URL inventée sans vérification SHA.

## 2026-11-21 01:43–01:44 UTC — script corrigé + test à froid (TCGA)

- Copie corrigée : repro_877/download_data_877.sh, SHA initial
  48a1c41c… (diff 147 lignes), puis 5805aa1b… après durcissement
  --retry-all-errors (diff 218 lignes). Original staging-pdac intact
  (SHA 4e151d59…). bash -n OK.
- Extrait littéral TCGA : cold/cold_tcga.sh — 4 tarballs OK (MD5
  vérifiés) ; PAAD RSEM SHA-256 c3dd138b…62c9 = §2.1.
- Reconstruction des flux : copie cold/build_fluxes_tcga_v4_cold.py
  (seules DATA/OUT changées, diff consigné) — flux reconstruits
  SHA-IDENTIQUES aux tenus : e7a2adab…0b0 et 895a4562…da4.
- Runs v6.2 froids (unité repro877-cold-runs, journal
  cold/runs_cold_877.log) : réel EXIT 0 (01:44:30–~01:48), nul EXIT 0
  (01:48:10–01:51:36Z), SHA v6.2 avant = après = f07567c4….
- Extraction cold/extract_cold_877.py (extract_858.extract, original
  intact) : réel MC 0,3720465146241378 maxsep 0,46234232096887146
  S_sep 0,4548206606358036 Delta 4,181387 L7a down 0,4051910172618019
  fals 0,849386 cascade [0,0 ; 74,0617 ; 93,2217 ; 98,4358 ; 98,9572] ;
  nul MC 0,326773250583873 maxsep 0,1695801283296793 S_sep
  0,1687743461786773 Delta 3,765664 L7a up 0,16715778704330952 fals
  0,642205 cascade [0,0 ; 10,6496 ; 15,9571 ; 67,119 ; 67,119] ;
  d_maxsep froid +0,2927621926391921 = tenu. CHIFFRES IDENTIQUES A 0,0
  EXACT. Comparaison au champ près des master_results.json : seuls
  divergent les diagnostics worker_budget/mémoire (3 workers tenus
  contre 2 froids, mémoire disponible différente) et les chemins
  runtime (nom du dossier de sortie) ; 2 champs Q6 MUC2 NaN des deux
  côtés. Aucun champ scientifique ne diverge. TEST A FROID PASSE.

## 2026-11-21 01:43–01:48 UTC — incident 403 transitoire, script complet

- Première exécution du script corrigé complet (unité
  repro877-cold-full, journal cold/full_script_877.log) : arrêtée au
  1er fichier (CRISPRGeneEffect.csv, ndownloader 51064667) sur HTTP 403
  après ~90 s à 0 octet ; EXIT:22. Même URL = 302 quelques minutes
  plus tard (cause probable : limitation de débit figshare après ~10
  téléchargements rapprochés).
- Correctif : --retry-all-errors --retry-delay 5 sur tous les appels
  curl du script (get() + 2 blocs python) ; script SHA 5805aa1b… ;
  relance en entier (unité repro877-cold-full2, journal
  cold/full_script_877b.log). État à 01:54 UTC : CRISPRGeneEffect.csv
  428 678 699 o OK, Model.csv OK, OmicsCN (1,39 Go) en cours.
  Résultat final à consigner ici à la fin du chantier.

## 2026-11-21 01:48–02:00 UTC — endpoint API figshare bloqué (OmicsCN)

- Relance full2 : CRISPRGeneEffect.csv OK, Model.csv OK, puis le
  téléchargement OmicsCNGene.csv via
  https://api.figshare.com/v2/file/download/51065324 est resté bloqué
  à 0 octet pendant 9+ min (curl en attente des en-têtes, aucun fichier
  créé ; HEAD sur cet endpoint = 400, normal : HEAD non supporté).
- Test : https://ndownloader.figshare.com/files/51065324 (même fichier,
  ID 51065324) avec range 0-2 000 000 o : HTTP 206, 672 Ko/s, 2 s.
  L'endpoint API est le problème, pas le fichier.
- Décision : unité full2 arrêtée proprement (systemctl stop, 0 processus
  restant) ; script corrigé : OmicsCN passe par ndownloader (même ID,
  même vérification MD5+SHA), commentaire consigné ; SHA du script
  42e9ce5b… (diff 241 lignes). DATA_SOURCES §1 mis à jour (les deux URL
  consignées, API d'origine + ndownloader vérifiée).
- Relance en entier (unité repro877-cold-full3, journal
  cold/full_script_877c.log). Résultat final à consigner ici.

## 2026-11-21 02:07–02:25 UTC — GDAC bloqué à 0 o/s (full3)

- full3 : 6 fichiers OK (dont OmicsCN via ndownloader — le correctif
  (9) fonctionne), puis le tarball TCGA PAAD RSEM via
  gdac.broadinstitute.org est resté bloqué à 0 octet pendant 13+ min
  (curl PID 5005, connexion ESTABLISHED vers le proxy, aucun octet).
- Test immédiat : range 0-1 000 000 o sur la même URL : HTTP 206,
  768 Ko/s, 1,3 s. L'hôte fonctionnait ; c'était la connexion qui
  était morte. Le même hôte avait servi les 4 tarballs en quelques
  secondes à 01:44 (extrait cold_tcga.sh).
- Cause : curl sans limite de vitesse attend indéfiniment une
  connexion morte ; --retry ne se déclenche jamais. Correctif (10) :
  --speed-limit 1000 --speed-time 300 sur get() — une connexion à
  0 o/s pendant 5 min échoue et le retry ouvre une connexion fraîche.
  Un transfert lent mais qui avance n'est pas coupé (pas de --max-time).
- Unité full3 arrêtée proprement (0 processus restant). Script SHA
  `3100d99ca10fc14608c59dd95e51debc01f5c40996c074214f783aebd9306c52`
  — diff 249 lignes, régénéré.
- Relance en entier (unité repro877-cold-full4, journal
  cold/full_script_877d.log). Résultat final à consigner ici.

## 2026-11-21 02:30–02:50 UTC — DIAGNOSTIC : les blocages venaient du proxy manquant dans l'unité

- Test décisif : un curl GDAC lancé DANS une unité systemd (sans
  variables proxy) donne HTTP 000, timeout 30 s ; le même curl depuis
  l'outil exec (variables https_proxy/http_proxy définies) télécharge
  le fichier en 7 s à 2,17 Mo/s. Même test sur l'endpoint API
  figshare (readme 20238123) depuis une unité : HTTP 000, timeout.
- Cause unifiée des trois incidents : les unités systemd lancées par
  systemd-run n'héritent PAS des variables proxy de l'environnement
  d'exécution. En accès direct (sans proxy), ndownloader.figshare.com
  fonctionne, mais api.figshare.com et gdac.broadinstitute.org restent
  bloqués à 0 octet. Ce n'est donc PAS un défaut des hôtes ni du
  script : c'est un artefact de la méthode de lancement.
- Vérification : le proxy http://hatch-egress-proxy:3128 fonctionne
  SANS identifiants (test GDAC range : HTTP 206, 395 Ko/s). Aucun
  secret n'est donc nécessaire pour corriger le lancement.
- Correctifs conservés : (8) retry 403, (9) OmicsCN via ndownloader
  (voie équivalente, même fichier vérifié — reste valable même si le
  blocage venait du proxy), (10) speed-limit (garde-fou général
  contre les connexions mortes). Le script n'a PAS besoin de coder le
  proxy en dur (c'est propre à l'environnement d'exécution ; le
  shell de l'utilisateur aura son propre réseau).
- full4 arrêtée (tentative GDAC n°3 bloquée, comme les deux
  précédentes). Relance full5 AVEC proxy (sans identifiants) :
  systemd-run --setenv=https_proxy=http://hatch-egress-proxy:3128
  --setenv=http_proxy=http://hatch-egress-proxy:3128, journal
  cold/full_script_877e.log. Résultat final à consigner ici.

## 2026-11-21 03:06 UTC — full5 : 12 OK puis 403 S3 ICGC (défaut du script corrigé, trouvé par le test)

- full5 (avec proxy) : 12 fichiers OK — 6 DepMap, 4 tarballs TCGA
  (GDAC passe désormais), GSE71729, GSE62452 — puis arrêt sur
  l'URL S3 directe ICGC
  https://icgc-xena-hub.s3.amazonaws.com/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz
  : HTTP 403, 4 tentatives, EXIT:22.
- Cause : le script corrigé gardait la section ICGC d'origine (ligne
  119) avec l'URL S3 directe, alors que la section AJOUTÉE (lignes
  286-293, probe map + NMF) utilisait déjà le hub. L'URL S3 directe
  est morte (403) ; l'URL du hub pour le même fichier
  https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz
  fonctionne (302 vers le bucket) : re-téléchargé 9 841 881 o,
  SHA-256 c2cb57af… identique au consigné.
- Correctif (11) : section ICGC d'origine basculée sur l'URL du hub,
  commentaire consigné ; DATA_SOURCES §5.2 mis à jour (ancienne URL
  S3 marquée 403, ne plus utiliser). Fichier vérifié conservé dans
  downloads/icgc/icgc_pacaau_exp.txt.gz.
- Relance en entier (unité repro877-cold-full6, avec proxy, journal
  cold/full_script_877f.log). Résultat final à consigner ici.

## 2026-11-21 ~03:18–03:22 UTC — RESTART machine pendant full6

- full6 (avec proxy) : 27 fichiers OK — 6 DepMap, 4 TCGA, GSE71729,
  GSE62452, ICGC exp (hub, correctif 11 VALIDÉ), Bailey MOESM270,
  3 PRISM 24Q2, 4 PRISM 19Q4, GDSC2, screened_compounds, 4 CPTAC —
  puis la machine a redémarré (uptime 0 min à 03:22:33Z) pendant le
  téléchargement PANC-1 calc.csv (curl 52 Empty reply, en retry).
  L'unité transiente n'a pas survécu au redémarrage ; aucune ligne
  EXIT dans le journal full_script_877f.log (coupé net).
- Le script re-télécharge tout depuis zéro (pas de reprise) : relance
  en entier (unité repro877-cold-full7, avec proxy, journal
  cold/full_script_877g.log). Résultat final à consigner ici.

## 2026-11-21 03:43–04:05 UTC — full7 bloqué sur PANC-1 calc.csv + reprise (12)

- full7 (avec proxy) : 27 fichiers OK (même point que full6), puis
  PANC-1 calc.csv (24 780 o) bloqué à 0 octet : 4 tentatives, toutes
  tuées par le speed-limit (28 Operation too slow). Unité arrêtée
  proprement avant la 4e fin (0 processus restant).
- Diagnostic : le même fichier se télécharge en 0,3–1,3 s depuis
  l'outil exec — avec proxy authentifié, sans identifiants, en IPv4
  comme en IPv6. Le curl bloqué de l'unité avait pourtant les bonnes
  variables proxy (vérifié dans /proc/PID/environ) et une connexion
  ESTABLISHED vers le proxy. Cause exacte non élucidée (connexion
  morte côté proxy pour ce couple unité/hôte ?) — consigné comme tel.
  Les tests directs prouvent que l'URL et l'hôte fonctionnent.
- Correctif (12) REPRISE : get_checked() remplace les 44 paires
  get + check — fichier déjà présent et vérifié (taille + SHA) sauté,
  fichier partiel/corrompu re-téléchargé. Script SHA 922bc270…,
  diff 323 lignes, bash -n OK.
- Relance en REPRISE depuis l'outil exec (proxy authentifié de
  l'environnement, qui fonctionne pour tous les hôtes testés),
  journal cold/full_script_877h.log, même dossier data_full (27
  fichiers déjà vérifiés sur place). Résultat final à consigner ici.

## 2026-11-21 04:07–04:15 UTC — reprise interrompue par une FAUTE DE FRAPPE dans un SHA consigné (MOESM3)

- Reprise 877h (depuis exec) : 19 fichiers « DÉJÀ PRÉSENT ET VÉRIFIÉ »,
  24 OK, puis arrêt sur `birnbaum_springer_MOESM3.xlsx` : SHA-256
  INCORRECT. Enquête : le fichier re-téléchargé (9 119 o) porte
  `8bfbdcd618ea2a9d9b8ae480c763b857c3e23e2022462ab61cff0aaa8c6b1a13`
  (64 car.), IDENTIQUE au fichier local d'origine (16 nov. 2026) et
  au fichier vérifié à 01:40 — trois téléchargements indépendants
  d'accord. La valeur consignée au §13 et recopiée dans le script
  ne faisait que 62 caractères (`…a9b8ae…` au lieu de `…a9d9b8ae…`) :
  faute de frappe dans la consignation, que la comparaison par SHA
  tronqués (`8bfbdcd6…6b1a13`) n'avait pas vue. Le fichier est bon ;
  c'est la consignation qui était fausse. Corrigé dans DATA_SOURCES
  §13 et dans le script.
- Balayage systématique : une deuxième faute trouvée, préexistante
  (19 nov. 2026) — SHA-256 LUAD §2.3 consigné sur 65 caractères
  (`…cf73f1daf2`, un `d` en trop) ; vrai SHA `…cf73f1af2`, vérifié
  sur le fichier local et le re-téléchargement à froid, identiques.
  Corrigé dans DATA_SOURCES §2.3. Aucune autre chaîne hex suspecte
  dans le script (balayage : 0) ni dans DATA_SOURCES (après correction).
- Le test du script complet a donc déjà servi : il a attrapé une
  erreur latente que les comparaisons tronquées avaient manquée.
- Script SHA 55811136…, diff 323 lignes, bash -n OK. Relance en
  reprise (journal cold/full_script_877i.log). Résultat à consigner.

## 2026-11-21 04:15–04:17 UTC — RÉSULTAT FINAL : script complet EXIT:0

- Reprise 877i (depuis exec, proxy authentifié) : 36 fichiers
  « DÉJÀ PRÉSENT ET VÉRIFIÉ » + 16 OK (frais), 0 erreur, ligne
  finale « TERMINE : tous les jeux de données téléchargés et
  vérifiés », EXIT:0. Dossier cold/data_full : 52 fichiers, 2,4 Go.
- Bilan des exécutions du script complet : full (403 transitoire),
  full2 (API bloquée), full3 (GDAC bloqué), full4 (GDAC bloqué),
  full5 (12 OK puis S3 ICGC 403), full6 (27 OK puis redémarrage
  machine), full7 (27 OK puis PANC-1 calc.csv bloqué), 877h (reprise,
  arrêt sur faute de frappe SHA MOESM3), 877i (reprise, EXIT:0).
  Chaque fichier a été vérifié par taille + SHA/MD5 dans
  l'invocation finale (36 vérifiés sur place + 16 re-téléchargés).
- Pipeline v6.2 SHA vérifié inchangé à la fin : f07567c4…

## 2026-11-21 04:20 UTC — LIVRAISON §8.77 (fin du chantier)

- Section `section_8.77_reproductibilite.md` finalisée (649 lignes) :
  verdict REPRODUCTIBILITÉ RÉPARÉE ; 19/19 gaps + G7/G8/G9/G10
  fermés ; script complet EXIT:0 (52 fichiers, 2,4 Go) ; test à
  froid TCGA v4 PASSE (chiffres identiques à 0,0 exact).
- Fichiers livrés au coordinateur (fusion + PDF + poussée par lui) :
  section, DATA_SOURCES_877.md (900 lignes), script corrigé
  (SHA 55811136…, diff 323 lignes), diff résumé, ce journal.
- SHA de la section : calculé après gel du texte, consigné dans le
  rapport de livraison au coordinateur (l'auto-référence est
  impossible dans le fichier lui-même).
- Pipeline v6.2 SHA final vérifié inchangé : f07567c4…
- Rien n'a été poussé sur GitHub, le livre blanc n'a pas été édité,
  aucun PDF régénéré par ce chantier.
