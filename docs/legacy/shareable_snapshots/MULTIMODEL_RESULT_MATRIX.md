# MULTIMODEL RESULT MATRIX

- Scope: qwen25 / llama32_3b / mistral7b logical result matrix
- Rows show canonical baseline (`k=0`) and stored-history follow-ups by relation/pool/k.

## qwen25

### gpqa
- baseline: run `run-20260317T072913Z-673904be`, accuracy `0.203125`, format-failure `0.22321428571428573`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | 0.2857142857142857 | 0.29017857142857145 | 0.2700892857142857 | 0.27232142857142855 |
| same_domain | incorrect | 0.29910714285714285 | 0.3080357142857143 | 0.28348214285714285 | 0.2924107142857143 |
| same_domain_other_dataset | correct | 0.265625 | 0.265625 | 0.27901785714285715 | 0.29464285714285715 |
| same_domain_other_dataset | incorrect | 0.27901785714285715 | 0.2767857142857143 | 0.2700892857142857 | 0.26339285714285715 |
| cross_domain | correct | 0.28348214285714285 | 0.26339285714285715 | 0.28125 | 0.25 |
| cross_domain | incorrect | 0.26785714285714285 | 0.25 | 0.2700892857142857 | 0.24776785714285715 |

### gsm8k
- baseline: run `run-20260317T075659Z-c4421795`, accuracy `0.5299469294920395`, format-failure `0.052312357846853674`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | 0.09476876421531463 | 0.09021986353297953 | 0.0932524639878696 | 0.10159211523881728 |
| same_domain | incorrect | 0.10614101592115238 | 0.09628506444275967 | 0.08946171341925702 | 0.09855951478392722 |
| same_domain_other_dataset | correct | — | — | — | — |
| same_domain_other_dataset | incorrect | 0.07657316148597422 | 0.08718726307808947 | 0.0887035633055345 | 0.07960576194086429 |
| cross_domain | correct | 0.10614101592115238 | 0.09628506444275967 | 0.09855951478392722 | 0.10841546626231995 |
| cross_domain | incorrect | 0.10007581501137225 | 0.09476876421531463 | 0.10614101592115238 | 0.09931766489764973 |

### aime
- baseline: run `run-20260317T070536Z-db599493`, accuracy `0.03333333333333333`, format-failure `0.3`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | — | — | — | — |
| same_domain | incorrect | 0.0 | 0.0 | 0.03333333333333333 | 0.0 |
| same_domain_other_dataset | correct | 0.0 | 0.03333333333333333 | 0.0 | 0.0 |
| same_domain_other_dataset | incorrect | 0.03333333333333333 | 0.0 | 0.0 | 0.0 |
| cross_domain | correct | 0.03333333333333333 | 0.0 | 0.0 | 0.06666666666666667 |
| cross_domain | incorrect | 0.06666666666666667 | 0.03333333333333333 | 0.0 | 0.03333333333333333 |

### mmlu
- baseline: run `run-20260317T161519Z-73645a5e`, accuracy `0.45826805298390544`, format-failure `0.14428144139011537`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | 0.5841048283720268 | 0.5903005269904572 | 0.5897308075772681 | 0.5923657598632673 |
| same_domain | incorrect | 0.5858139866115938 | 0.5890186583107819 | 0.5905141717704031 | 0.5917248255234298 |
| same_domain_other_dataset | correct | — | — | — | — |
| same_domain_other_dataset | incorrect | — | — | — | — |
| cross_domain | correct | 0.5614584816977638 | 0.5654465175900869 | 0.568651189289275 | 0.5714285714285714 |
| cross_domain | incorrect | 0.5677253952428429 | 0.5687936191425723 | 0.5742771684945165 | 0.5750605326876513 |

## llama

### gpqa
- baseline: run `run-20260324T051316Z-a0f54d2b`, accuracy `0.23660714285714285`, format-failure `0.12053571428571429`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | 0.2611607142857143 | 0.2924107142857143 | 0.27455357142857145 | 0.2700892857142857 |
| same_domain | incorrect | 0.28125 | 0.28125 | 0.234375 | 0.25892857142857145 |
| same_domain_other_dataset | correct | 0.2611607142857143 | 0.3080357142857143 | 0.2700892857142857 | 0.25223214285714285 |
| same_domain_other_dataset | incorrect | 0.25669642857142855 | 0.27232142857142855 | 0.24553571428571427 | 0.2611607142857143 |
| cross_domain | correct | 0.22991071428571427 | 0.28125 | 0.25892857142857145 | 0.26339285714285715 |
| cross_domain | incorrect | 0.25223214285714285 | 0.25669642857142855 | 0.2544642857142857 | 0.2924107142857143 |

### gsm8k
- baseline: run `run-20260317T084627Z-f13f3ce2`, accuracy `0.14935557240333586`, format-failure `0.17210007581501138`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | 0.2357846853677028 | 0.18043972706595907 | 0.1068991660348749 | 0.09476876421531463 |
| same_domain | incorrect | 0.21076573161485973 | 0.1470811220621683 | 0.10614101592115238 | 0.09173616376042457 |
| same_domain_other_dataset | correct | — | — | — | — |
| same_domain_other_dataset | incorrect | — | — | — | — |
| cross_domain | correct | 0.14556482183472327 | 0.10614101592115238 | 0.09401061410159212 | 0.08946171341925702 |
| cross_domain | incorrect | 0.1425322213798332 | 0.1023502653525398 | 0.10538286580742987 | 0.09249431387414708 |

### aime
- baseline: run `run-20260324T050441Z-a02c523e`, accuracy `0.06666666666666667`, format-failure `0.3333333333333333`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | — | — | — | — |
| same_domain | incorrect | — | — | — | — |
| same_domain_other_dataset | correct | 0.06666666666666667 | 0.03333333333333333 | 0.03333333333333333 | 0.03333333333333333 |
| same_domain_other_dataset | incorrect | 0.0 | 0.03333333333333333 | 0.06666666666666667 | 0.03333333333333333 |
| cross_domain | correct | 0.03333333333333333 | 0.03333333333333333 | 0.03333333333333333 | 0.03333333333333333 |
| cross_domain | incorrect | 0.03333333333333333 | 0.03333333333333333 | 0.03333333333333333 | 0.03333333333333333 |

### mmlu
- baseline: run `run-20260317T104305Z-c30e6268`, accuracy `0.5228599914542088`, format-failure `0.057897735365332575`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | 0.523572140720695 | 0.5281298960262071 | 0.5245691496937758 | 0.5185158809286426 |
| same_domain | incorrect | 0.5190143854151831 | 0.5239282153539382 | 0.5291269049992878 | 0.5171627973223187 |
| same_domain_other_dataset | correct | — | — | — | — |
| same_domain_other_dataset | incorrect | — | — | — | — |
| cross_domain | correct | 0.49601196410767695 | 0.49494374020794757 | 0.4883207520296254 | 0.4880358923230309 |
| cross_domain | incorrect | 0.498860561173622 | 0.49230878792194843 | 0.4905284147557328 | 0.4915254237288136 |

## mistral

### gpqa
- baseline: run `run-20260317T105040Z-7f11db30`, accuracy `0.10491071428571429`, format-failure `0.65625`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | — | — | — | — |
| same_domain | incorrect | 0.27455357142857145 | 0.2924107142857143 | 0.2544642857142857 | 0.2700892857142857 |
| same_domain_other_dataset | correct | 0.26785714285714285 | 0.26339285714285715 | 0.27232142857142855 | 0.2857142857142857 |
| same_domain_other_dataset | incorrect | 0.25669642857142855 | 0.2857142857142857 | 0.24330357142857142 | 0.2544642857142857 |
| cross_domain | correct | 0.2700892857142857 | 0.26339285714285715 | 0.28125 | 0.31026785714285715 |
| cross_domain | incorrect | 0.27232142857142855 | 0.28125 | 0.2611607142857143 | 0.27232142857142855 |

### gsm8k
- baseline: run `run-20260317T112419Z-d063ba2b`, accuracy `0.017437452615617893`, format-failure `0.8711144806671721`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | 0.08112206216830932 | 0.07354056103108415 | 0.07278241091736164 | 0.06747536012130402 |
| same_domain | incorrect | 0.06444275966641395 | 0.07960576194086429 | 0.0667172100075815 | 0.07354056103108415 |
| same_domain_other_dataset | correct | — | — | — | — |
| same_domain_other_dataset | incorrect | — | — | — | — |
| cross_domain | correct | 0.06823351023502654 | 0.0758150113722517 | 0.07354056103108415 | 0.0712661106899166 |
| cross_domain | incorrect | 0.05913570887035633 | 0.06141015921152388 | 0.0758150113722517 | 0.07050796057619409 |

### aime
- baseline: run `run-20260324T051159Z-3a804857`, accuracy `0.0`, format-failure `0.8`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | — | — | — | — |
| same_domain | incorrect | — | — | — | — |
| same_domain_other_dataset | correct | 0.0 | 0.03333333333333333 | 0.03333333333333333 | 0.03333333333333333 |
| same_domain_other_dataset | incorrect | 0.0 | 0.0 | 0.0 | 0.0 |
| cross_domain | correct | 0.0 | 0.0 | 0.0 | 0.0 |
| cross_domain | incorrect | 0.0 | 0.0 | 0.0 | 0.03333333333333333 |

### mmlu
- baseline: run `run-20260317T125046Z-5efa7f4e`, accuracy `0.21770403076484832`, format-failure `0.5266343825665859`

| relation | pool | k2 | k4 | k8 | k16 |
| --- | --- | --- | --- | --- | --- |
| same_domain | correct | — | — | — | — |
| same_domain | incorrect | — | — | — | — |
| same_domain_other_dataset | correct | — | — | — | — |
| same_domain_other_dataset | incorrect | — | — | — | — |
| cross_domain | correct | 0.48753738783649053 | 0.49736504771400086 | 0.5023500925794047 | 0.5010682238997294 |
| cross_domain | incorrect | 0.49309215211508334 | 0.49935906566016236 | 0.5012818686796753 | 0.4983620566870816 |

