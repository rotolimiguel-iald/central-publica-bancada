# F2.3 — recibo do ligante de temperatura, ramo C

- Fonte compilada: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F2.3\LiganteLeiCampoCurvoTemperaturaStandalone.lean`; SHA-256 `3acf88c76189e69ae100fcd328cf43dc6b1767568c0857d8266baad7796fc62f`.
- Cópia do kernel: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F2.3\kernel\TGLExt\LiganteLeiCampoCurvoTemperaturaStandalone.lean`; bytes iguais à fonte entregue.
- Ramo C anterior reproduzido literalmente no corpo, após os imports: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F2.3\LiganteLeiCampoCurvoRamoC.lean`; SHA-256 `56a186a39bf5dc44f3e0e9065bbb384f558afaf61b855672a57a412dd1b4c033`. A pedra standalone não importa um módulo novo instalado no Nós.
- Comando: `lean.exe -o C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F2.3\LiganteLeiCampoCurvoTemperaturaStandalone.olean TGLExt\LiganteLeiCampoCurvoTemperaturaStandalone.lean`, cwd `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F2.3\kernel`, Lean 4.31.0; LEAN_PATH usa somente caches de leitura do Nós original e Mathlib.
- Exit code observado: 0. Erros: 0. Avisos: 0. `sorry`/`admit`/axioma novo na fonte: 0.
- `#print axioms`: propext, Classical.choice, Quot.sound apenas. Ver `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F2.3\AXIOMAS_TEMPERATURA.txt`.
- Olean: 585600 bytes.
- Limite: `rate=κ` é entrada positiva livre; a prova deriva `1/P` relativamente a essa taxa, sem fixar KMS/H3 do estado nem ligar Circle.exp à ação na rede.
- `polar_period_scale` (PeriodHeatCalibration_v3:21–27) preserva a leitura fiel sob `κ→cκ, P→P/c`; `observer_boost_eq` admite qualquer `κ>0` por parametrização. O coeficiente `1/P` é relativo ao relógio de boost escolhido, sem normalização física canônica ou KMS de estado.
- H2: `ContratoQG_v31.lean:210–244` tem `KillingNormalization N`/`ContratoH2.kappa`/`observer_unit`; este termo **não** identifica `r.rate` com esse κ. SHA-256 `2f2c6561a5a5d832b43f11f7bacccf4811eb4392f1832f78cf4a5838a72a4808`.
