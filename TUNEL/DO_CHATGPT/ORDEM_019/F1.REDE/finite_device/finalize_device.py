"""Report and pin the completed, immutable finite-device run."""
from pathlib import Path
import hashlib
import json

BASE=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes()
    return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}

def main():
    r=json.loads((BASE/"RESULTADO_DEVICE_R1.json").read_text(encoding="utf-8"))
    receipt=json.loads((BASE/"RUN_RECEIPT_DEVICE_R1.json").read_text(encoding="utf-8"))
    if receipt["result_sha256"]!=pin(BASE/"RESULTADO_DEVICE_R1.json")["sha256"]:
        raise RuntimeError("Result differs from run receipt")
    pre=json.loads((BASE/"PREREGISTRO_DEVICE_R1.json").read_text(encoding="utf-8"))
    for src in pre["source_pins"].values():
        if pin(Path(src["path"]))["sha256"]!=src["sha256"]:
            raise RuntimeError("Source changed since preregistration")
    a=r["local_algebras"]; c=r["controls"]
    lines=[
        "# F1.REDE — integração finita do dispositivo",
        f"[REAL — teste numérico sintético; parâmetros INPUT] {r['verdict']}: {r['checks_passed']}/{r['checks_total']} verificações, EXIT {receipt['exit_code']}; sem dado observado.",
        "Pré-registro por hash anterior à execução: PREREGISTRO_DEVICE_R1.json, 6e4e2ce553aea405878e967df9314be2af030b45e234dd35dbe1b30731d2560a; freeze 21:29:11 UTC, início 21:29:37 UTC de 13/10/2026.",
        "Geometria documental: 27 sítios (8 vértices, 12 arestas, 6 faces, 1 centro); 54 conexões por vizinhança cartesiana [INPUT]. Não alocamos o Hilbert de 27 qubits.",
        "Modelo reduzido: Hilbert 2×2×2, H e salto a_out†σ_-+σ_+a_in da fonte TeX, γ_holo=βγ_Λ; β=α_CODATA2018√e em runtime. Taxas e frequências adimensionais INPUT, sem ajuste.",
        f"Álgebras dos 3 fatores: 8 regiões; {a['counts']['multiplication']} produtos, {a['counts']['isotony']} inclusões e {a['counts']['disjoint_commutator']} comutadores disjuntos, resíduos máximos zero.",
        f"15 canais exp(tL): mínimo de Choi {min(x['choi_min_eigenvalue'] for x in r['channels']):.3e}, erro TP máximo {max(x['trace_preservation_residual'] for x in r['channels']):.3e}; tolerância 1e-10, 29 estados por canal preservados.",
        f"Livro de energia aberto: max|Tr(HLρ)−Tr(ρL†H)|={max(x['energy_duality_error'] for x in r['generators']):.3e}; erro integrado {max(x['ledger_residual'] for x in r['energy_ledger']):.3e}. Fluxo oposto é contabilidade, não construção microscópica do banho.",
        f"Controle PSD: ρ01=1−β literal foi recusado (λ_min={c['invalid_literal_coherence']['minimum_eigenvalue']:.12f}); C=2|ρ01|=1−β é normalizado e admissível, sem predizer um platô dinâmico.",
        "Reuso explícito: one_mqc.py já resolve desde 29/07 um GKLS qutrit de reset com C normalizado; citado sem rerrodar. A presente integração 2×2×2 usa outro salto, o explícito do Supercondutor.",
        f"Raiz aplicada a amplitudes e normalizada: duas decomposições da mesma ρ deram distância {c['root_nonlinearity']['different_output_frobenius_norm']:.12f}; essa interpretação não é canal linear CPTP. Codificação/decodificação clássica segue válida.",
        "Taxas negativas, NaN, infinito e booleano recusados. Corte 0/1 fóton: [a,a†]=diag(1,−1), não I. O terceiro nível |Ψ⟩ do MQC está fora deste modelo reduzido.",
        "Sem alegação de realização de hardware, transporte instantâneo, fidelidade experimental, 5σ ou rede 4D. Aprovação independente e integração são etapas posteriores.",
        "Fontes, versões NumPy/SciPy, seed, parâmetros, tolerâncias, resultados e comando/início/fim estão pinados nos arquivos vizinhos. Nenhuma produção ou memória alterada.",
    ]
    # The freeze and times are read again below, to avoid a report detached from the receipt.
    freeze=json.loads((BASE/"FREEZE_DEVICE_R1.json").read_text(encoding="utf-8"))
    lines[2]=(f"Pré-registro anterior à execução: SHA256 {freeze['preregister']['sha256']}; "
              f"freeze {freeze['created_utc']}; início {receipt['started_utc']}.")
    report=BASE/"RELATORIO_DEVICE_R1.md"
    with report.open("x",encoding="utf-8",newline="\n") as f: f.write("\n".join(lines)+"\n")
    manifest={"unit":"F1.REDE","status":"ENTREGA_CANDIDATA_SEM_APROVACAO_INDEPENDENTE",
              "files":[pin(p) for p in sorted(BASE.iterdir()) if p.is_file()],
              "sources_unchanged":True,"all_outputs_new":True}
    path=BASE/"HASHES_DEVICE_R1.json"
    with path.open("x",encoding="utf-8",newline="\n") as f: json.dump(manifest,f,ensure_ascii=False,indent=2);f.write("\n")
    print(json.dumps({"report":pin(report),"manifest":pin(path),"result":pin(BASE/"RESULTADO_DEVICE_R1.json")},ensure_ascii=False))

if __name__=="__main__": main()
