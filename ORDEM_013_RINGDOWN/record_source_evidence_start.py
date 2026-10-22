"""Record the live registered computation and its actual, limited validation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parent
RUN = ROOT/"cache/source_evidence"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def safe(p, raw):
    old = p.read_bytes() if p.exists() else None
    if old is not None:
        backup = p.with_name(p.name+".bak_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        backup.write_bytes(old)
        if backup.read_bytes() != old:
            raise ValueError("Byte backup differs")
    temporary = p.with_name(p.name+".tmp")
    temporary.write_bytes(raw)
    if temporary.stat().st_size != len(raw):
        raise ValueError("Short write")
    if old is not None and p.read_bytes() != old:
        raise ValueError("Concurrent memory change")
    temporary.replace(p)
    if p.read_bytes() != raw:
        raise ValueError("Replacement differs")


def main():
    handoff = ROOT.parent/"TUNEL/DO_CHATGPT/ENTREGA_013_C5_integracao_fonte_em_execucao.md"
    if handoff.exists():
        raise FileExistsError("Create-once recorder")
    reg = json.loads((RUN/"REGISTRATION.json").read_bytes())
    for name, expected in reg["hashes"].items():
        if sha(RUN/name) != expected:
            raise ValueError("Registration changed: "+name)
    if sha(ROOT/"REGISTRO_C6.json") != sha(RUN/"REGISTRO_C6.json"):
        raise ValueError("C6 changed")
    validation = json.loads((RUN/"VALIDATION.json").read_bytes())
    oracle = json.loads((RUN/"NESTED_ORACLE.json").read_bytes())
    progress = json.loads((RUN/"runs/IMRPhenomXPHM_seed130522_nlive256/PROGRESS.json").read_bytes())
    now = datetime.now(timezone.utc).isoformat()
    paths = ["prepare_source_evidence.py", Path(__file__).name]
    paths += ["cache/source_evidence/"+n for n in ("source_evidence.py", "validate_source_evidence.py", "validate_nested_mixture.py",
              "analyze_source_evidence.py", "REGISTRATION.json", "PROVENANCE.json", "INJECTIONS.json", "INJECTIONS.npz",
              "VALIDATION.json", "NESTED_ORACLE.json", "vendor/MANIFEST.json")]
    hashes = {n:sha(ROOT/n) for n in paths}
    audit = dict(status="RUNNING_NOT_A_SCIENTIFIC_RESULT", date_utc=now,
                 dataset_count=1200, likelihood_components_per_waveform=2400, independent_noise_intervals_per_detector=50,
                 source_dimensions_integrated=7, common_distance_polarization_dimensions_integrated=2,
                 adapter_error=max(r["adapter_error"] for r in validation["checks"]),
                 independent_quadrature_error=validation["component_integral_max_error"],
                 oracle_caution="The analytic 7D oracle passes a loose stochastic consistency check, but its low-weight component has ESS19-22 and logZ errors0.62-0.76. It FAILS the intended component precision. PASS in NESTED_ORACLE is not scientific acceptance.",
                 oracle_small_component_ESS=[r["ESS"][0] for r in oracle["runs"]],
                 oracle_small_component_errors=[r["errors"][0] for r in oracle["runs"]],
                 live_process=dict(tool="write_stdin", session_id=79591, linux_pid=progress["pid"],
                                   observation="Tool poll returned a live session and advancing samples immediately before this record; revalidate next turn",
                                   last_progress=progress,
                                   checkpoint="cache/source_evidence/runs/IMRPhenomXPHM_seed130522_nlive256/checkpoint.pkl"),
                 no_target_strain_read=True, no_C6_change=True, hashes=hashes)
    safe(ROOT/"C5_SOURCE_EVIDENCE_START.json", (json.dumps(audit, indent=2, ensure_ascii=False)+"\n").encode())
    text = f"""[REAL — implementação verificada e processo iniciado; OPEN — evidência científica ainda não concluída]

# ORDEM 013 — Integração não linear da fonte

Registro: {now}.

**PAGO:** a likelihood direta das formas de onda agora integra sete coordenadas físicas
(massa total, razão de massas, dois spins, inclinação, fase orbital e deslocamento do pico),
com distância/polarização comuns integradas analiticamente. O pico usa a correção intrínseca
22 previamente demonstrada. Priors uniformes declarados, sem reutilizar o posterior do
próprio evento. O prior de distância continua inverso-Rayleigh, não uniforme em volume.

**PAGO:** entradas congeladas: três fontes × duas famílias de injeção × a=0/1 × O4/O5 ×
50 intervalos = 1200 conjuntos simulados. São os mesmos 50 intervalos reutilizados e
pareados; não são 1200 eventos independentes. Cada conjunto recebe duas hipóteses:
2400 componentes de likelihood, reconstruídas SEPARADAMENTE. A média usada pelo
integrador é um recurso de cálculo, nunca o produto dessas simulações.

**PAGO:** equivalência da implementação com a API anterior: erro máximo
{audit['adapter_error']:.17g}; identidade de reconstrução de evidência conferida por
quadratura independente: {audit['independent_quadrature_error']:.17g}.

**NÃO PAGO:** convergência astrofísica, distribuição final de ln B, posterior contínuo de a,
viés/cobertura, demais SNR e leituras. A primeira família de recuperação, IMRPhenomXPHM,
está em execução. SEOBNRv4HM continua na matriz, mas sua integração ainda não foi iniciada.
256 pontos vivos, orçamento piloto de 24000 avaliações, semente 130522 e checkpoints.
Não executar outra cópia enquanto a sessão 79591 continuar viva.

## O alerta que o controle produziu

O controle analítico usa gaussianas em sete dimensões. A componente com menor evidência
ficou com ESS de {audit['oracle_small_component_ESS']} e erros em ln Z de
{audit['oracle_small_component_errors']}. Portanto, a etiqueta PASS do teste de consistência
ampla **não satisfaz a precisão pretendida**. A auditoria astrofísica exigirá ESS≥100,
peso máximo≤0,05, estabilidade ao dobrar a amostragem temporal e repetição independente
com mais pontos vivos; a convergência global sozinha não basta. Se necessário, a rodada
piloto poderá orientar balanceamento computacional, preservando os priors e reconstruindo
as integrais por componente. O erro medido não será escondido por médias.

## Comandos

No WSL, diretório `cache/source_evidence`:

```text
/opt/pycbc_env/bin/python -B source_evidence.py run
/opt/pycbc_env/bin/python -B analyze_source_evidence.py IMRPhenomXPHM_seed130522_nlive256
```

O primeiro comando já está rodando: NÃO duplicar. A auditoria só pode rodar quando existir
RESULT.json. `--resume` é reservado a processo comprovadamente interrompido e checkpoint
existente; um timeout de observação não demonstra interrupção.

O pacote dynesty3.1.0 e sua licença foram COPIADOS de instalação existente para `vendor`;
nenhuma instalação de /opt foi alterada. A interface foi conferida na documentação primária
<https://dynesty.readthedocs.io/en/latest/quickstart.html> e no código local. A documentação
adverte que poucos pontos vivos podem perder modos; isso é uma limitação relevante aqui.

Não houve leitura nova da janela do evento, alteração de C6, seleção física de relógio,
partição ou desenrolamento, alteração do um.py, kernel, Atlas ou gate. C6 preserva
INCONCLUSIVE_SYSTEMATICS. Axiomas: N/A — sem Lean.

## Custódia dos insumos e scripts

| arquivo relativo à bancada | SHA256 medido |
|---|---|
"""
    text += "".join(f"| `{n}` | `{h}` |\n" for n, h in hashes.items())
    safe(handoff, text.encode())
    status_path = ROOT/"STATUS_ORDEM_013.json"
    status = json.loads(status_path.read_bytes())
    status["previous_goal_turn"] = "PROGRESS: controles não lineares, pico intrínseco corrigido, integral comum e reprodução"
    status["previous_visible_nonresearch_turn"] = "NO_GOAL_PROGRESS: forneceu prompt curto solicitado; retomada auditada nesta rodada"
    status["this_goal_turn"] = "PROGRESS: inferência direta de sete parâmetros registrada, injeções e controles concluídos, sampler real em execução"
    status["date_utc"] = now
    status["active_processes"] = [audit["live_process"]]
    status["verified"]["C5_nonlinear_source_integration_start"] = {k:v for k, v in audit.items() if k not in ("hashes", "live_process")}
    status["next_action"] = ("Revalidar write_stdin session79591 (Phenom, sete dimensões, 2400 componentes); não reiniciar por timeout. "
       "Ao terminar, ler RESULT e executar analyze_source_evidence.py. Auditar ESS/pesos/erro de Monte Carlo/rate e "
       "planejar repetição com mais pontos vivos ou balanceamento se necessário. Oráculo analítico mostrou erro de componente "
       "apesar da convergência global; não chamar o piloto de evidência validada. Depois integrar SEOB, completar distribuições "
       "O4/O5 e calibração contínua de a, sem alterar C6.")
    status["requirements_remaining"][0] = status["next_action"]
    status["hashes"].update(hashes)
    safe(status_path, (json.dumps(status, indent=2, ensure_ascii=False)+"\n").encode())
    progress_path = ROOT/"PROGRESSO.md"
    addition = "\n\n---\n"+text
    safe(progress_path, progress_path.read_bytes()+addition.encode())
    print(json.dumps(dict(status="PROGRESS_NOT_COMPLETE", handoff=str(handoff), active_session=79591,
                          posterior_results_available=False, last_ncall=progress["ncall"])))


if __name__ == "__main__":
    main()
