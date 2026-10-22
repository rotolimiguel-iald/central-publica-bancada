# Renderização e primeiro domínio cosmológico

Entrega de 28/09/2026. Este arquivo descreve a implementação da bancada, não um novo resultado físico.

## Abrir

O atalho **TGL** usa o launcher da bancada em TETELESTAI. Há acesso no Desktop local e no Desktop sincronizado pelo OneDrive do usuário. O launcher verifica separadamente os dois serviços, inicia apenas os ausentes e abre **Universo residente**. O cartão **Cosmologia · domínio acústico** leva ao novo painel. O retorno **Ondas gravitacionais** mantém a mesma carga científica em memória.

## O que é carregado

O perfil BAO desta etapa contém o vetor comprimido DESI DR2 com 13 medidas em sete redshifts e sua covariância completa 13×13. Não é o catálogo individual de galáxias, nem mapas ou espectros CMB. A origem e os hashes das cópias estão em `data/cosmology/ORIGINS.md`. A custódia local foi conferida; o commit remoto da distribuição não foi verificado nesta entrega.

Os dois arquivos são lidos uma vez e convertidos em tuplas numéricas imutáveis, incluindo a fatoração de Cholesky. A resposta informa identificador de carga, bytes das fontes e contador de leituras. Os bytes equivalentes da matriz não são anunciados como RSS total do Python.

## Interação disponível

- Variação de H₀, Ωm, rd, w₀ e wₐ; cálculo de DM/rd, DH/rd e DV/rd.
- Cursor de redshift e fator de escala a=1/(1+z), pontos observados, resíduos e covariância.
- χ² calculado por solução triangular de Cholesky: rᵀC⁻¹r. Não é ajuste automático, significância ou descoberta.
- Curvas de fundo FLRW plano com matéria e energia escura CPL, restritas a z≤3; radiação e curvatura não entram nesta primeira visualização. rd é uma entrada independente, não um horizonte acústico calculado por um solver de recombinação.
- Representação gráfica da expansão distinguida da observação: não há posições de galáxias nesses 13 pontos e não se fabrica um mapa 3D observado a partir deles.

Estatuto do modelo: `EXPLORATORY_BACKGROUND_NOT_TGL_PREDICTION`. Ele prepara e verifica a camada de dados e o rival cosmológico de referência. A previsão acústica canônica completa da TGL, espectros CMB, inferência e calibração global por simulações continuam no contrato D10/CMB–BAO. Os quatro relatórios previstos e a proibição de contar dados reutilizados duas vezes permanecem.

## Escolha do renderizador

**WebGL2 na aplicação** é o caminho implementado para visualização interativa. Os dados e cálculos científicos ficam nos processos residentes; a GPU recebe as coordenadas necessárias à vista. Isso evita copiar todos os bancos para VRAM ou fazer um render de vídeo para cada mudança de parâmetro. A identificação fornecida pelo navegador e a telemetria do dispositivo são evidências distintas: existir um contexto WebGL não basta para afirmar renderização pela RTX.

**Blender** pode ser acrescentado como ferramenta de produção de modelos, cenas e animações exportáveis. Não é dependência desta entrega. Sua disponibilidade de renderizadores interativos e de produção não fornece, por si, uma ligação com as matrizes científicas da bancada. Fontes: [WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API), [renderização Blender](https://www.blender.org/features/rendering/).

## Isolamento operacional

O servidor e worker GW atuais permanecem em `127.0.0.1:18765`; o worker GW ainda depende dos pipes de seu servidor. Reiniciar esse servidor encerraria a carga, portanto isso não é feito para instalar o novo domínio. O serviço cosmológico independente usa `127.0.0.1:18766`, sem importar ou instanciar `resident_bridge.Worker`. A interface navega por links; não abre CORS nem expõe serviços à rede externa.

O launcher serializa cliques simultâneos com um mutex Windows. Se o serviço cosmológico falhar, o GW já saudável continua acessível e a falha parcial é exibida. Isso não substitui os testes do domínio: `/health` apenas identifica o serviço; `/status` lê e verifica a fonte.

## Validação

Testes focados cobrem quadratura refinada, solução analítica de controle, χ² com correlação, custódia adulterada, parâmetros inválidos, carga residente após remoção de fixtures temporárias, HTTP e abertura concorrente/serviço parcial. Os recibos `state/validation_cosmology_*.json` contêm cenários HTTP, tempos medidos e a comparação da carga GW antes/depois. São medições de poucas consultas locais, não benchmark de carga ampla.

Próximos incrementos científicos: ligar o motor cosmológico canônico já derivado às mesmas entradas, verificar background e perturbações contra os referentes, integrar as likelihoods CMB/BAO e seus nuisance/correlações, depois congelar e simular a estatística global. Nenhum resultado visual move o gate matemático.
