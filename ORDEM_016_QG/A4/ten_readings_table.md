[DERIVED — álgebra exata; relógio físico OPEN; números históricos de planejamento]

# Dez leituras sob H_tauStar_eq_KMS_period

Hipótese: tauStar=2pi/kappa_H, no MESMO horizonte e referencial. Ela não é demonstrada pelo círculo.
Beta permanece simbólico. C_N designa a esperança Poisson; J_z a integral de propagação.

| Leitura | Lei original | Razão à taxa KMS (R-PROP: ao expoente Gamma*T) | Comparação |
|---|---|---|---|
| R-A | `beta*(1+z)*t_P*omega^2/2` | `kappa*tP*(z + 1)/(2*pi)` | Não por H_tauStar_eq_KMS_period sozinho: requer (1+z)tP=2pi/kappa no mesmo referencial. |
| R-B | `beta*w(chi)^2/(2*tM)` | `kappa*tM/(2*pi)` | Não: requer tM=2pi/kappa. No Schwarzschild o período é 8pi*tM; as taxas diferem por 8pi. |
| R-MOD | `pi*beta*(omega-m*Omega_H)^2/kappa` | `(Omega*m - omega)**2/omega**2` | Sim sob Omega_H=0; em rotação requer substituir a frequência por omega-m*Omega_H e justificar fisicamente o gerador/coerência. |
| R-RAIZ-0 | `beta*omega/2` | `kappa/(2*pi*omega)` | Não como função universal: coincidência pontual exige omega=kappa/(2pi), para beta,omega,kappa>0. |
| R-RAIZ-EP4 | `beta*omega^2/[2*(sqrt(omega0+omega)+sqrt(omega0))^2]` | `2*kappa*tP*(z + 1)/(pi*(sqrt(4*omega*tP*(z + 1) + 1) + 1)**2)` | Não: relógio efetivo depende de omega0 e omega; exige 1/(sqrt(omega0+omega)+sqrt(omega0))^2=2pi/kappa. |
| R-RAIZ-REST | `beta*omega^2/[2*(sqrt(omega0+omega)+sqrt(omega0))^2]` | `hbar*kappa*(z + 1)/(2*pi*(sqrt(M)*c + sqrt(M*c**2 + hbar*omega*(z + 1)))**2)` | Não: mesma condição do offset, agora omega0=Msrc*c^2/(hbar*(1+z)); identificação de massa é hipótese adicional. |
| R-RAIZ-COHERENT | `Gamma_initial=(beta*omega/2)*E_Poisson[1/(sqrt(n+1)+sqrt(n))^2] ~ beta*omega/(8*Nbar)` | `C_N*kappa/(2*pi*omega)` | Não: C_N é esperança Poisson dependente da ocupação; exige C_N=2pi*omega/kappa. É inclinação inicial, não lei exponencial geral. |
| R-LIN | `beta*omega` | `kappa/(pi*omega)` | Não como função universal: coincidência pontual exige omega=kappa/pi. |
| R-GLOBAL | `Gamma_relative=0` | `0` | Não para beta,omega,kappa>0: a taxa relativa é zero sob a partição relacional declarada. |
| R-PROP | `Xi=(beta*t_P*omega_obs^2/2)*integral_0^z (1+zprime)/H(zprime) dzprime` | `J_z*kappa*tP/(2*pi*T)` | Objetos diferentes: Xi é expoente integrado, Gamma é taxa. Se comparados Xi e Gamma*T, seria preciso tP*J_z=(2pi/kappa)*T, além do modelo de propagação. |

| Leitura | Estatuto do relógio | Excluída se universal | I90 | N90 (teto) | 887/I90 |
|---|---|---|---:|---:|---:|
| R-A | INPUT_PRINCIPLED_IDENTIFICATION | não informado agregado; ver partição | — | — | — |
| R-B | INPUT_SOURCE_MASS_CLOCK | não informado agregado; ver partição | 95215.975144 | 3327.148181 (3328) | 0.931566% |
| R-MOD | CONJECTURE_KMS_OSCILLATOR_IDENTIFICATION | True | 30209.424853 | 1055.613124 (1056) | 2.936170% |
| R-RAIZ-0 | INPUT_POSITIVE_GENERATOR_AND_VACUUM_COHERENCE | True | 27907.150915 | 975.164370 (976) | 3.178397% |
| R-RAIZ-EP4 | INPUT_BACKGROUND_E_P_OVER_4 | não informado agregado; ver partição | — | — | — |
| R-RAIZ-REST | CONJECTURE_REMNANT_REST_OFFSET | True | — | — | — |
| R-RAIZ-COHERENT | CONJECTURE_OCCUPATION_AND_READOUT | não informado agregado; ver partição | — | — | — |
| R-LIN | CONJECTURE_LINEAR_GAP_PHYSICAL_BRIDGE | True | 7513.267067 | 262.537382 (263) | 11.805783% |
| R-GLOBAL | INPUT_RELATIONAL_PARTITION | não informado agregado; ver partição | — | — | — |
| R-PROP | CONJECTURE_PROPAGATION_MODEL | não informado agregado; ver partição | — | — | — |

Bonferroni: z(p5/4)=5.260933604821; fator N90=1.084804892706.
Os N90 são o planejamento ilustrativo registrado, com sistemáticas ainda não liberadas; as frações não são sigmas nem probabilidade de confirmação. Nenhuma leitura foi escolhida.

## Proveniência

- `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_016_INSUMOS\ESTADO_RINGDOWN_LEITURAS.json` — `b1d32e3a78af96be1c9a72ed6f6dfd793d87066e65a63ea793f49dafa18a8729`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C1_LEITURAS_v4.json` — `126270a896d8589870954b209155f26a8b08295839b31e0e9a6e28e512621980`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\RINGDOWN_5SIGMA_V1.json` — `e1be6b0409720c6883af5281458922fb03c5329bc0b08df7efe129d65e487416`
