# PROVENANCE — Rotations sans doublon, §8.44 (19 novembre 2026)

Chantier 2 des 3 étapes v6.2 approuvées par Zackary le 19 nov. 2026 ~05h47 (« Lance tout cela »).
Règle permanente (27 oct. 2026) : provenance toujours nommée — source complète, nature des lignes,
comment chaque valeur a été produite, hachages des données, et ce qui manque.

## 1. Codes (jamais modifiés)

| Code | SHA-256 | Rôle |
|---|---|---|
| `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py` | `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` | Pipeline de travail, 88 runs |
| `~/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py` | `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` | CLDN18 seul (run préexistant §8.32) |
| `build_dedup_844.py` | `47447e77c031c2cbd7d9484e64696656d2e75e1dfabd455983069727c07f57d7` | Construction des 88 CSV dédoublonnés |
| `extract_ssep_844_rotations.py` | `24a07f9fd6668e6a998d08bc2eebd4c06d831db3bc6136be27dee892c66c6f02` | Extraction S_sep / MC / Delta / max_separation |
| `watch_v62_dedup_844.sh` | `f3afa779be286787f47f130d2670410c041169e4ebd67692cb410a01e124b9b9` | Surveillance du lot |
| `run_v62_lot.sh` | `7e501733d3104c1e763255544c7b56dd8af4f6579fa0ebb5581bc8c12357435b` | Lanceur reprenable (saute les sorties complètes) |

Vérification finale des SHA pipelines : revérifiés après le lot — inchangés.
Mode `fast`, graine 42 (défaut). Nul = lignes permutées, graine 42, colonne de contrôle intacte.

## 2. Entrées d'origine (vérifiées avant construction)

- 96 CSV de rotations construits par `build_rotations_v61.py` (16 nov. 2026) ; SHA-256 vérifiés un par un contre `PROVENANCE_rotations_v61.md` : **96/96 conformes**, 0 mismatch, 0 absent.
- 4 bases conformes : TCGA v4 `pdac_tcga_fluxes_v4.csv` (`e7a2adab…13a0b0`), DepMap `pdac_depmap_fluxes.csv` (`7d605fef…98e37f8`), immunitaire TCGA `pdac_immune_tcga_fluxes.csv` (`66dbb672…bbd2e`), PARP TCGA `pdac_tcga_fluxes_parp.csv` (`c9549b68…c4309`).
- Sources : TCGA-PAAD ARN Broad GDAC Firehose 2016-01-28 (RSEM) ; DepMap CRISPR 24Q2 (figshare Corsello et al.) ; GEO GSE62452/GSE71729 ; ICGC PACA-AU. Détail : PROVENANCE_tcga_v4.md, PROVENANCE_depmap.md, PROVENANCE_immune_v6.md, PROVENANCE_parp_v6.md, PROVENANCE_rotations_v61.md.
- Nature des lignes : résidus d'expression génique ou de dépendance CRISPR (mesures instrumentales — séquençage ARN, criblage CRISPR — transformées : correction de pureté, résidus) ordonnés par un flux-contrôle croissant ; les nuls sont des lignes permutées, graine 42 — des échantillons hypothétiques, pas des mesures. Aucun mot humain, aucun échantillon hypothétique dans les séries réelles.

## 3. CSV dédoublonnés construits (88) — SHA-256 complets

Méthode : retrait de la seule colonne doublon du flux contrôle (colonne k, valeurs identiques à la colonne 0 vérifiées côté réel ; multi-ensemble égal vérifié côté nul) ; contrôle, ordre et autres flux inchangés, ligne par ligne. Nul : CSV `_nul.csv` ORIGINAL moins la colonne doublon — même permutation que l'original. Colonnes 13 → 12 (contrôle + 11 flux analysés). Aucune valeur recalculée ni imputée.

Fichier `dedup_844_csv_sha.json` (SHA `9dc283c8830731fd41ab5b8e84d6707be2b4f2d86810847d0a6277e8cb5235c7`) — mêmes valeurs, lisibles en machine.

| Famille | Contrôle | Col. doublon | n | CSV réel dédoublonné — SHA-256 | CSV nul dédoublonné — SHA-256 |
|---|---|---|---|---|---|
| V4ROT | CEACAM5 | 10 | 178 | `fcd615b231a98a892ad3cca620d3e9229d9cacbc76c351c0d6f7f25296594dde` | `0e3e9ca35d3ae3d87962f389d5c234a073941645506ceaad0b7e11e6978e4fc5` |
| V4ROT | CLCA1 | 11 | 178 | `e60288228b3f7df31bc6f04331a3a765b060f4d1572ecbffb17c124324cf36fc` | `2c06f3e1c9197a9364a1971c71f4b55fc4dd1a24c3b5392036f72b22a8bba204` |
| V4ROT | CR2 | 6 | 178 | `4f05322a83babccf5d48457197c2867af1299980a6c733165178dcf97f1c607d` | `529f43b3c79c3e442cec96d354a22f678488c38cd59383f8fae0a2dea8aa8162` |
| V4ROT | DPCR1 | 5 | 178 | `c754c5344927736052348118186d389ea3aa4274ac1b436c1df52140e66a20bf` | `ec9fc7f0e04bec89799573aec655ebe9f6e906c7a908af1a515b8b91e7c07cae` |
| V4ROT | GSTM1 | 9 | 178 | `07913dc409f42444e66c9f0bd9f8e742545db10c785301a03f958c244a458244` | `d3516d011fe3afb3ab6292629822263d9578132d8c90eded5c90690cad5fda7c` |
| V4ROT | KRT20 | 7 | 178 | `bfb7165ad1251338e05f13a7b0b983643c51f845d9da1f424c71b3508f240822` | `c60b418028e11cab6b85c9265b581682ddc8204a6bf8a00e19289446a38e4574` |
| V4ROT | MUC16 | 12 | 178 | `108abd88a9da3ccea747d15cf30e198472af3eea1f4611e89f7fc9c8eae2af5c` | `78a971086020576d8b2d6dbb21faf38b6679e1578fa7fd10bd0af5e90cecba2e` |
| V4ROT | MUC17 | 4 | 178 | `8df3aa80952a73725a3e6887a57cf8ce4925f34bbccc144d96e0f4c51ecc5d03` | `21a08983e5b41e316a71487b2bf8f666c304508bfa32500b82f865ba78b0bbe1` |
| V4ROT | MUC2 | 8 | 178 | `6c0626d226bbb5c1befadf8c01e4f898aaf15ddd8d0320ed3010fef01ed3e2e6` | `907d3a5e6aa72a70c843058b16dda31a7bae887e02724adb5cefa8e589beaaa2` |
| V4ROT | PGC | 1 | 178 | `e81debf83638120d02d48f8bca644ac306f3c2c4fea96bbe044ecf4f93a860ae` | `2428e077f415457722fa8bd08758609bdc4e53117c76b2d2b7c46a9a95ea7d68` |
| V4ROT | REG4 | 2 | 178 | `338753cfa633e120d1330953b93db377680ebaee9eeb2a7927fc8d4a6db574c5` | `6872e80bb76eb1c248cde1435ed2892123f22b7c26044ade123f1782244a2039` |
| DEPMAPROT | CCND1 | 3 | 45 | `64bbdae69898e5e6e4acf9d73ba920446aec7644971cbdd7abb898b523347a3d` | `d02bc8e9778c6443d1977a5784d7c3957d118643cd4546c9be09f743bfa1c0e8` |
| DEPMAPROT | CFLAR | 5 | 45 | `66448405e5802f5c9197db6fb6baca5adb0747ac2fe0d880f41170814dba5984` | `9eb3c3fdc17e0e91f4f5bdc4923ed168c4d5e68c4ccd1bc7f7b262d04b6cb950` |
| DEPMAPROT | CRKL | 10 | 45 | `388d9bb692a38557aaa7f33929815d9b5c5a432f9800bb3e5b14bbe17add6c20` | `f309b598d973aec878f5385d4fc6c646cf051777fac81df193d4b6291b5d3b88` |
| DEPMAPROT | DOCK5 | 6 | 45 | `9a768548cfc5bab5ded424d6d5a0ac68081ddffb9f3c61a49d4201701d4f5473` | `79d6e07410a8d0f597fdbae2a60fe828f41f2cec76941962d8104686e18577fd` |
| DEPMAPROT | EFR3A | 1 | 45 | `8fb49e38431dee6f24f00dcb81e883f8e9b5c5bfa062fc4ca79d43e379e865e6` | `70b7c2192e811359135664f099c33e91165063e48e9b7f1f60c61d29329f0712` |
| DEPMAPROT | MYC | 11 | 45 | `1277ee90c1853b0fd6a381f1be416abc557afc0d70198d80b5519b07c60e4809` | `7bb23c904366ee5bf881a7eedb4aae39c610120475cf21674ecbdb90901f1028` |
| DEPMAPROT | MYH9 | 7 | 45 | `58416da4ac89756c70a02a109990788f767b8000e120a9d9cce1d4c8700f811a` | `c6df992c0c56679e5b1043bf8c3205e8170e3d8ddb10475d67ad4c5809c80466` |
| DEPMAPROT | RAB10 | 2 | 45 | `958a4d70177f7d64c5d51a13e8fa059a064448dd0e3d237202379c49a2c85003` | `403c4f926d41e577cb8c74ab4d2268dbe6efa7e77a58856d0a4c42d5383cbc72` |
| DEPMAPROT | RAB6A | 9 | 45 | `1a5f2b2a5f246df1742545c705466c56a815bf434860dc58b47ee06aff5ee9fd` | `58afbecfd3c2407c5223ab81439ca395b253cc36f320fcf65e871f0eedefebd0` |
| DEPMAPROT | SCAP | 8 | 45 | `e4a7fbc6d24c2279bd341caae79b05ee26e7fa69ed42a1421b2418e4aa431150` | `113d0bc00e5cbf2e3dd572333d80fff63c8795714a2813f5b6938a349c12ef72` |
| DEPMAPROT | UROD | 4 | 45 | `01d0000c6792218baa01e5d78471d974f4239d50a103a84ff60353b58fe1559f` | `22d4f894692d55ac9fc1b37286a395875974606b4d6a4db851a15754bbb95adc` |
| IMMROT | CD163 | 6 | 178 | `d87ab5070b628e0f91a190aa24aec9a523b7428d82fbc0a384bea67de2bedd5f` | `755c12e02300f0ad89639d16dcc3c6b463027c34a02ff6bf9ae6052dd5eba5aa` |
| IMMROT | CD19 | 12 | 178 | `f751ebf9dafb022c60c743f9ec2432d728d4e63ecf0e7a3ad717b037100929e7` | `a498c63425458acd668b2014d0d37395a58d48c360138a1bcbf80471e896427f` |
| IMMROT | CD274 | 7 | 178 | `09cacf56d79b4fe1a288d5dad2628e27634a44a5b41cb6294daae6b9e4b26283` | `2f61e60b27dfa22821f146582ac720ba410522e736dd7ebfb8941b2e991e3d0b` |
| IMMROT | CD4 | 3 | 178 | `8268ed1a94e9e14149ae02c157eda2c0c3f6e5b8bff07bfc2dd60b4bf29f2ada` | `81e207ac26252fd7ff40996bcebc2f0b367ddb18d474d77acb2fcf597be3e337` |
| IMMROT | CD68 | 5 | 178 | `50b109aaef2378ae210b6b1159cfc7e4be3fb1e93e3414715e772425e31b6979` | `a8a94339a16df4c31a997fed0cb3feec0e4f04a0384023f8a33d47fca284b3f3` |
| IMMROT | CD8A | 1 | 178 | `0194f5d07b7cd3e462041c7a60c1a3d6a55aa74a47a1ed1a1094b8e8c6525634` | `adba7571b3c5ec82355b0e93b3e16ce282a8a9f5edfa895ab280e5592d9fd1de` |
| IMMROT | CD8B | 2 | 178 | `394f1cb59e6148bb4bf1713a594eb9baf89c0680fdb4fa830e3ba8d420b65442` | `cc4d2be6f6ab6afaeb9b6062963e22c60c793fff14fdf6a696becceace0bc3b3` |
| IMMROT | FOXP3 | 4 | 178 | `47802a77f20b29bbeb068046b749d1f111811fc0d4cd6d0be45b2ef7c08b7117` | `2333df46fca62b6f6c7479b99de1899c6f2cc20083486f14304121d6e653dfba` |
| IMMROT | GZMB | 10 | 178 | `27ffa33a85f84241ac9fed5eb1be386b5932ac3b654a54a405e3a1df9805ef24` | `ec25e61c5e369f991c5c99f7c04bde6d20bf53617ff904912de8da05ea08c933` |
| IMMROT | IFNG | 11 | 178 | `71d54c96786c3306c423677e33133bd5197c438dcc85d93c47d5c9a89435620c` | `954bdeca979b0859b34d54b171a57358144983b8b6871193de5927c6168bbd92` |
| IMMROT | PDCD1 | 8 | 178 | `08cf0e5c3efe005ef8514fdad48e6df3de9dd6bb7f0c0e0b42b4b345285e6bdf` | `8e00ba64348226bc26b87cc5b6a97cf94d3b90310ddf3b14caf9b6bb5461065b` |
| PARPROT | ATM | 5 | 178 | `a229275426a959d1d4d69da5adc444f5814b8265162ecac554fed42a003077bb` | `f6d7eca9cb33797aaffef450b00cdf8b1c675454f6bf033c0b4c349a3233335e` |
| PARPROT | ATR | 6 | 178 | `f3a5b17356ede4dd908716553ca1d22bc4b283774258bb5b8d2460581969e53a` | `383ba1e9745feb5f8cba7505c9abe503e0aea2e7d7d1efbd8f3941b68a3eb969` |
| PARPROT | BRCA1 | 3 | 178 | `9467754a41fe173a81da2936e0eaae4a25f840b2b5928a01b4f6f509ca828875` | `5a9859a24a1baeb16923c247782f85bec8f4400e44e994d0207a4009fba46d87` |
| PARPROT | BRCA2 | 4 | 178 | `5580dbe32230638c3847cd93d3846e933240f0ee365450c810fce511095e86ef` | `82c46ce202bb7424313cea033433de88228b0726205b1578919d209cb28a27cf` |
| PARPROT | CHEK1 | 7 | 178 | `790e0118732e344daab86ad83133d325f41063eddee78964f72d7587ab6c11f1` | `2d2519687793622167a4a27f9acc3e8f3b053cb4f79fc85ede7d7b64fb17cbad` |
| PARPROT | CHEK2 | 8 | 178 | `ec09b2cb188f7a27cfb92a908a1dc16c38136ffd9a2be3beb38dbb459a27fbb3` | `db7c73a280ee074ffdf0535e90fc2dda199a6590229314d1506626f1793bda61` |
| PARPROT | FANCD2 | 12 | 178 | `6e5ff34c4ce70b849a1da78a84476768c27bbb47919b3ae30731976246c126f7` | `4533945bc6945bb64e7a81c5b10906a713cfa0cfd7ba3fb59204aa13f84ffc4b` |
| PARPROT | PARP2 | 2 | 178 | `e98e56d37fa9dbca61c75ada9b198c61c528f2b72634040c9f740f48aee156ea` | `0dfa85d41c6b63852af7e23edd041842550d480a9869207abb1d9ff338843893` |
| PARPROT | POLQ | 11 | 178 | `7f04a1f9e8bc8c11726121637a7293ed8d1b1b4690f436ddf25b3fb569bf579a` | `19353a88617fc1098eaf33335985edf7cb3c1aadd65c3b8958b67eb28939604d` |
| PARPROT | RAD51 | 9 | 178 | `310812d04c7d0566114853339cc4011c047c213ea36dba6554eedbe8f04fb695` | `55d6586e5f09f6f84f95046685bbfcaca1d0d89488fbb0962c5f9b5fa564fe0f` |
| PARPROT | XRCC1 | 10 | 178 | `965465b95c3c55643b80297103a45051a01bf31171623f9c0e8ee41609452ad5` | `cd09923545ceed3b55554c7ee5e6581fa3b77c1a30d31f85f1438e1653539fa2` |

Les 4 paires déjà refaites au §8.41 (non reconstruites ici) — SHA vérifiés contre §8.41.6, conformes :

| Paire | CSV réel — SHA-256 | CSV nul — SHA-256 |
|---|---|---|
| CLDN18 (V4ROT, v6.1) | `b1071f84e7228b9946562c04fb43d5d48603b4924afa04cf0f417bb86fc4d4f8` | `33d5f3177484cd40ffb92920a4bb22a23635e5c4ea2a32dd04c4df3de164f3d7` |
| CTLA4 (IMMROT) | `36bce1335a2d23f94f0a71dbfdc28c19a0d0df5e455f84466e2f61c2ada3a389` | `ac1b3c5d51f5bd5929d1fb3153169374de262a1ed290de40179130a59aa6c369` (nouvelle permutation) |
| ACO2 (DEPMAPROT) | `ef398777f292b7702b74029ccfba435d0f55b1b3f5e76434db4c9e456b61541c` | `33d13387b612a1a2b5ca877197a4e1ddba369e2cff97121037a8001eb9adca09` (même permutation ; nul nouvelle permutation : `3700d844d2033a4903a62c14f26da7501ee45fb3b4eaf6af0bbfcee3bd4cbb1c`) |
| PARP1 (PARPROT) | `95750c870fb6e6ac94da3d928e89a136e1d8a2edab2579e3494cad3f77cd8cd5` | `591f88ec34e839044fae0a890cb58d2e658f74c6e9833309eef1cc9911b2e4f9` (même permutation = nouvelle permutation, même fichier) |

## 4. Runs et sorties

- Lot v6.2 : unité systemd `v62-dedup-844-watch` (surveillance `watch_v62_dedup_844.sh`), 13h52:48–20h11:52 UTC le 19 nov. 2026 (6 h 19) ; **88/88 exit 0** (86 dans `runs_v62_dedup_844.log` + 2 du pilote CEACAM5 dans `runs_v62_dedup_844_pilot.log`, 13h18:48–13h52:35 UTC, 2/2 exit 0). Manifeste `manifest_v62_dedup_844.txt` (SHA `1831e0d00c403169d1910816f2184e9a15899001f034cf9c8889b44222cfdcd7`) ; log `runs_v62_dedup_844.log` (SHA `3951ff677b21ee4163f8e3e7f8416a0dab8bcf845af0a6af8d1de8592485a4cd`).
- Dossiers de sortie : `results_fast_v62_<famille>_<contrôle>_dedup[_nul]` (88), chacun avec `master_results.json`.
- Deux redémarrages machine pendant le lot (~17h43 et ~19h51 UTC) : l'unité de surveillance est morte avec la machine à chaque fois (aucune entrée dans `journalctl`, cause non établie) ; relance reprenable à 17h44:22 et 19h52:26 UTC ; sorties complètes intactes (41/88 puis 82/88), non touchées ; reprise au run interrompu (SCAP_NUL puis POLQ) ; aucun run perdu, aucun dossier partiel à nettoyer.
- Extraction : `extract_ssep_844_rotations.py` → `ssep_844_rotations.json` (SHA `06f41b6592291114f8404ea8b3dc69d122e0db2f5d4db474c6a76d0cea59b362`, 72 130 octets) et `ssep_844_rotations.csv` (SHA `d1abc0aba2e480e611b87dea2861ef5bd96a83a196e1b8736b596506653fc999`). Contrôles : 88/88 runs lus (+8/8 existants), 48/48 paires, versions conformes, 88/88 SHA CSV conformes, 0 écart vs les 4 écarts du §8.41 (tolérance 10⁻⁴).
- Section : `section_8.44_rotations_dedup.md` (ce chantier). Tableaux générés depuis `ssep_844_rotations.json` par `write_section_844.py` — aucune valeur recopiée à la main.

## 5. Ce qui manque

- S_sep par flux analysé (hors contrôle) : non extrait — S_sep est global ; lecture par flux du §8.32 (`v61_rotations_flux_reading.md`, doublon exclu) reste la référence.
- Nul dédoublonné de CTLA4 à nouvelle permutation (pas à permutation identique) : verdict indépendant de ce choix (+0,8986, large marge), mais la comparaison stricte « un seul effet change » ne vaut que pour les 47 autres paires.
- MUC16 passe (A) de 0,0012 : verdict fragile par construction (v6.2 déterministe, gigue 0 — un re-run ne changerait rien).
- Livre blanc : modifié entre la remise du chantier (SHA `de3aa316…`, 2 750 lignes) et la fin du lot (SHA `c5537270…`, 2 752 lignes, modifié 13h17 UTC par un autre processus — ce chantier ne l'a jamais touché) ; il s'arrête toujours au §8.42. Cette section n'y est pas insérée (fichier séparé, publication par le coordinateur).
- PDF non régénéré, rien poussé sur GitHub dans ce chantier (hors périmètre, publication sur go séparé).

