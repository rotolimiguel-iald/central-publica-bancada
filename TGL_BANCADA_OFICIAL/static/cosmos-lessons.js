/* Short, source-linked lessons. Educational text is not an observation or a fit. */
(function (root, factory) {
  "use strict";
  var lessons = factory();
  if (typeof module === "object" && module.exports) module.exports = lessons;
  root.CosmosLessons = lessons;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";
  return {
    sources: [
      { id: "nasa-components", title: "NASA — The Universe's Building Blocks", url: "https://science.nasa.gov/universe/overview/building-blocks/" },
      { id: "planck-background", title: "ESA — Planck and the cosmic microwave background", url: "https://www.esa.int/Science_Exploration/Space_Science/Planck/Planck_and_the_cosmic_microwave_background" },
      { id: "planck-maps", title: "ESA Planck Legacy Archive — CMB and astrophysical component maps", url: "https://wiki.cosmos.esa.int/planckpla/index.php?title=CMB_and_astrophysical_component_maps" },
      { id: "flrw-wmap", title: "NASA/WMAP — Five-Year Cosmological Interpretation, equações 7 e 9", url: "https://lambda.gsfc.nasa.gov/product/wmap/dr3/pub_papers/fiveyear/cosmology/wmap_5yr_cosmo_reprint.pdf" },
      { id: "nasa-redshift", title: "NASA Hubble — Cosmological Redshift", url: "https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/hubble-cosmological-redshift/" },
      { id: "nasa-web", title: "NASA Hubble — Mapping the Cosmic Web", url: "https://science.nasa.gov/mission/hubble/science/science-highlights/mapping-the-cosmic-web/" },
      { id: "desi-ruler", title: "DESI — What do DESI's 5000 eyes see?", url: "https://www.desi.lbl.gov/2021/06/01/what-do-desis-5000-eyes-see/" },
      { id: "desi-dr2", title: "DESI — DR2 Results: March 19 Guide", url: "https://www.desi.lbl.gov/2025/03/19/desi-dr2-results-march-19-guide/" },
      { id: "ligo-waves", title: "LIGO — What are Gravitational Waves?", url: "https://www.ligo.caltech.edu/page/what-are-gw" },
      { id: "ligo-detector", title: "LIGO — What is LIGO?", url: "https://www.ligo.caltech.edu/page/what-is-ligo" }
    ],
    topics: [
      {
        id: "baryons", title: "Matéria bariônica", group: "Ingredientes", eyebrow: "Átomos e luz",
        summary: "Bárions formam estrelas, gás e pessoas. O conhecido ‘cerca de 5%’ é uma fração inferida dentro de um modelo cosmológico, não matéria contada diretamente num mapa.",
        question: "Como distinguir a matéria que emite luz da matéria total inferida pela gravidade?",
        observe: "No diagrama didático, veja a fração bariônica em cada redshift; a fração cósmica real exige observações e hipóteses de modelo.",
        experiment: "No diagrama de composição, mova o redshift, escolha uma época ou altere Ωb. O anel e a curva histórica mostram as frações calculadas.",
        tgl: "O Fundo V3 desta bancada recebe Ωm agregada; não resolve uma fração bariônica separada. β não é fração de matéria.",
        capability: "Aula interativa: Ωb ajustável no FLRW didático; o Fundo V3 continua com Ωm agregada.",
        lab: { label: "Explorar frações", url: "/explore" }, sourceIds: ["nasa-components", "flrw-wmap"]
      },
      {
        id: "dark-matter", title: "Matéria escura", group: "Ingredientes", eyebrow: "Gravidade sem brilho",
        summary: "Matéria escura é inferida por seus efeitos gravitacionais; sua natureza física permanece aberta. O ‘cerca de 27%’ depende do modelo cosmológico usado no ajuste.",
        question: "Que observação sugere massa além da matéria luminosa?",
        observe: "Movimentos em galáxias e lentes gravitacionais ajudam a mapear massa que não vemos emitindo luz.",
        experiment: "Varie Ωc e o redshift no diagrama de composição; compare a participação da matéria escura no anel e na curva histórica.",
        tgl: "V3 usa Ωm total, sem decompor matéria escura e bárions; mudar β não equivale a mudar a fração escura.",
        capability: "Aula interativa: frações FLRW disponíveis; lentes e mapas 3D de massa não integrados.",
        lab: { label: "Explorar frações", url: "/explore" }, sourceIds: ["nasa-components", "nasa-web", "flrw-wmap"]
      },
      {
        id: "dark-energy", title: "Energia escura", group: "Ingredientes", eyebrow: "Expansão acelerada",
        summary: "‘Energia escura’ nomeia a explicação usual para a aceleração cósmica; sua natureza é desconhecida. O ‘cerca de 68%’ é uma estimativa dependente do modelo.",
        question: "O que muda nas distâncias quando muda a história de expansão?",
        observe: "No Cosmos, compare distâncias em z≤3; H(z) pode ser inferido de D_H=c/H. As 13 medidas BAO ajudam a confrontar curvas com dados.",
        experiment: "Varie w₀ e wₐ apenas no fundo FLRW/CPL; no V3 compare β fixo e β=0 com w₀=−1, wₐ=0.",
        tgl: "β altera o fundo condicional V3; não é uma fração de energia escura nem uma previsão de perturbações CMB.",
        capability: "Dados: curvas de fundo e BAO disponíveis; comparação visual, sem ajuste global ou significância.",
        lab: { label: "Explorar Cosmos", url: "http://127.0.0.1:18766/cosmos" },
        sourceIds: ["nasa-components", "desi-dr2"]
      },
      {
        id: "cmb", title: "Fundo cósmico · CMB", group: "Luz antiga", eyebrow: "Uma imagem do Universo jovem",
        summary: "O CMB é luz liberada quando o Universo esfriou o suficiente para os fótons viajarem livremente. Pequenas variações no mapa guardam informação sobre condições antigas.",
        question: "Por que manchas pequenas no CMB informam sobre estrutura futura?",
        observe: "Planck publica mapas e espectros angulares; parâmetros cosmológicos vêm da análise desses dados sob hipóteses de modelo.",
        experiment: "Selecione a época CMB (z≈1100) e mova o redshift: veja quanto matéria e radiação contribuem para a densidade nesse cenário.",
        tgl: "A rota V3 local calcula somente H(z) e distâncias tardias; não fornece perturbações nem Cℓ TGL.",
        capability: "Aula interativa: frações na época aproximada do CMB; mapa, Cℓ e likelihood Planck não integrados.",
        lab: { label: "Explorar épocas", url: "/explore" }, sourceIds: ["planck-background", "planck-maps", "flrw-wmap"]
      },
      {
        id: "expansion", title: "Expansão", group: "Geometria", eyebrow: "Distância e redshift",
        summary: "A expansão alonga a luz de galáxias distantes. Redshift é observável; converter redshift em distância requer um modelo de expansão.",
        question: "Se H(z) muda, como mudam as distâncias radial e transversal?",
        observe: "No Cosmos, acompanhe D_M, D_H=c/H(z) e D_V em 0≤z≤3; H(z) é inferível de D_H, mas não há curva H traçada.",
        experiment: "Mova o cursor de redshift e compare o fundo FLRW/CPL com V3 β fixo e β=0, preservando as hipóteses próprias de cada rota.",
        tgl: "V3 é um fundo plano condicional com matéria total, radiação e Λ; a curva FLRW/CPL didática é uma rota separada.",
        capability: "Dados: curvas calculadas para z≤3; mover controles explora modelos, não mede H(z) diretamente.",
        lab: { label: "Explorar expansão", url: "http://127.0.0.1:18766/cosmos" },
        sourceIds: ["nasa-redshift", "desi-dr2", "flrw-wmap"]
      },
      {
        id: "structure", title: "Formação de estruturas", group: "Geometria", eyebrow: "Da flutuação à teia",
        summary: "Pequenas diferenças iniciais de densidade cresceram pela gravidade e participam da formação de galáxias, aglomerados e filamentos.",
        question: "Por que uma curva de expansão não mostra sozinha como galáxias se agrupam?",
        observe: "Mapas de galáxias e reconstruções por lentes mostram aspectos distintos da teia cósmica.",
        experiment: "Percorra as épocas e observe quando radiação, matéria e Λ dominam a densidade. Esse é o pano de fundo da pergunta sobre crescimento; a aglomeração exige outro cálculo.",
        tgl: "O fundo V3 local não calcula crescimento de perturbações, lentes ou uma simulação de formação de estruturas.",
        capability: "Aula interativa: história de frações FLRW; catálogos 3D, lentes e formação de estruturas não integrados.",
        lab: { label: "Explorar épocas", url: "/explore" }, sourceIds: ["planck-background", "nasa-web", "flrw-wmap"]
      },
      {
        id: "bao", title: "Régua acústica · BAO", group: "Réguas cósmicas", eyebrow: "Uma escala no agrupamento",
        summary: "As BAO deixam uma escala característica na distribuição estatística de galáxias e outros traçadores. DESI usa essa régua para estudar distâncias cósmicas.",
        question: "O mesmo modelo descreve a distância transversal e a radial em cada redshift?",
        observe: "A bancada usa 13 medidas locais DESI DR2 e sua covariância completa para visualizar resíduos e χ²; r_d é entrada fornecida.",
        experiment: "Compare D_M/r_d, D_H/r_d e D_V/r_d nos redshifts observados. Observe covariâncias; não leia χ² isolado como significância.",
        tgl: "V3 fornece distâncias de fundo; não deriva r_d nem prevê CMB. A comparação BAO aqui não confirma ou refuta TGL sozinha.",
        capability: "Dados: 13 entradas BAO com covariância; diagnóstico visual, sem ajuste ou sigma global.",
        lab: { label: "Explorar BAO", url: "http://127.0.0.1:18766/cosmos" },
        sourceIds: ["desi-ruler", "desi-dr2"]
      },
      {
        id: "gravitational-waves", title: "Ondas gravitacionais", group: "Mensageiros", eyebrow: "O espaço-tempo oscila",
        summary: "Ondas gravitacionais são perturbações do espaço-tempo. Interferômetros como LIGO medem variações relativas de comprimento chamadas strain.",
        question: "Por que comparar detectores e tempos importa ao interpretar um sinal?",
        observe: "O painel residente permite inspecionar strain de 180 arquivos da rodada verificada anteriormente; arquivo disponível não significa evento independente.",
        experiment: "Explore uma janela temporal e compare canais e hipóteses condicionais, mantendo unidades, tempos e máscaras explícitos.",
        tgl: "Uma curva teórica condicional de ringdown não equivale à confirmação física da TGL nem a um ajuste global.",
        capability: "Dados: painel GW residente local; disponibilidade atual depende do estado do serviço, sem inferência de eventos independentes.",
        lab: { label: "Explorar ondas gravitacionais", url: "http://127.0.0.1:18765/universe" },
        sourceIds: ["ligo-waves", "ligo-detector"]
      }
    ]
  };
});
