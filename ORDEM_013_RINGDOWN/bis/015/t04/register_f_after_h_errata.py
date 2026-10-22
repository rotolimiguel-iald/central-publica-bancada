"""Record the stopped H attempt and reserve T04-F under the unchanged machine cap."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESK = HERE.parent
RING = DESK.parents[1]
CHATGPT = RING.parent
OUT = CHATGPT / "TUNEL" / "DO_CHATGPT"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(obj: dict) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert path.stat().st_size == len(data)


def main() -> None:
    old_path = RING / "ORCAMENTO_015_v4.json"
    order_path = CHATGPT / "TUNEL" / "PARA_CHATGPT" / "ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md"
    result_c_path = HERE / "branch_c" / "RESULT.json"
    result_h_path = HERE / "branch_h" / "RESULT.json"
    runner_path = RING / "bis" / "e2_code_v1_1_2" / "pe_runner.py"
    opening_path = OUT / "ENTREGA_016_ABERTURA_operador.md"
    assert sha(old_path) == "56da0bdff06d25db6ad7dfcd5fe5cf37b8af3155af8f6f6fc3a248d26912ccca"
    assert sha(order_path) == "c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3"
    assert sha(result_c_path) == "9663242560623d92e933bdab82ca176022f6b3606ee285aceea6c8a9eecaea36"
    assert sha(result_h_path) == "d8565e08f755262b0cdbbe5c3c1fc2a9901343d51dc8740ca16947c00ca321b3"
    assert sha(opening_path) == "216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a"
    source = runner_path.read_text(encoding="utf-8")
    assert "if count>=settings['maxcall']:status='PARTIAL_MAXCALL_NOT_ACCEPTED'" in source
    assert "if ess<settings['minimum_effective_samples']:state['status']='PARTIAL_LOW_ESS'" in source
    old = json.loads(old_path.read_bytes())
    c = json.loads(result_c_path.read_bytes())
    h = json.loads(result_h_path.read_bytes())
    assert c["controller_receipt"]["status"] == "PARTIAL_MAXCALL_NOT_ACCEPTED"
    assert h["cleanup_confirmed"] is True and h["controller_receipt"]["cleanup"]["group_absent"] is True
    assert h["fault"]["type"] == "InterruptedError"
    assert 0 < h["machine_hours"] < 8
    assert not (RING / "ORCAMENTO_015_v5.json").exists()
    budget = copy.deepcopy(old)
    now = datetime.now(timezone.utc).isoformat()
    budget["registered_utc"] = now
    budget["supersedes_sha256"] = sha(old_path)
    budget["witness_relative_to_Chatgpt"] = "TUNEL/DO_CHATGPT/ENTREGA_015_ORCAMENTO_015_v5.md"
    items = {item["item"]: item for item in budget["items"]}
    assert items["T04_branch_H"]["allocated_machine_hours"] == 8.0
    h_hours = h["machine_hours"]
    items["T04_branch_H"].update(allocated_machine_hours=h_hours,
        actual_machine_hours=h_hours, job_started=True,
        status="INTERRUPTED_ROUTE_CORRECTION_NOT_ACCEPTED_POSTERIOR",
        final_receipt_sha256=sha(result_h_path))
    f_reserve = 8.0 - h_hours
    budget["items"].append(dict(item="T04_branch_F", allocated_machine_hours=f_reserve,
        actual_machine_hours=0.0, job_started=False,
        status="RESERVED_NOT_LAUNCHED", instrument="KERR_V2_EXTENDED_DTAU220",
        estimate_statute="UPPER_BUDGET_NOT_CONVERGENCE_FORECAST"))
    assert abs(sum(item["allocated_machine_hours"] for item in budget["items"]) - budget["authorized_machine_hours"]) < 1e-9
    budget["allocated_machine_hours"] = budget["authorized_machine_hours"]
    budget["unallocated_machine_hours"] = 0.0
    budget["accounting"]["intervals"].append(dict(target="T04_branch_H_INTERRUPTED",
        receipt_relative_to_Chatgpt=result_h_path.relative_to(CHATGPT).as_posix(),
        sha256=sha(result_h_path), union_machine_hours=h_hours,
        CPU_seconds=h["children_cpu_seconds"]))
    budget["accounting"]["machine_hours_spent"] += h_hours
    budget["reallocation_reason"] = "Strict post-C tree correction: C maxcall persisted; H any-other-state did not apply; stop H and proceed to F"
    budget["reallocation_changes"] = dict(T04_branch_H=dict(old=8.0,new=h_hours),
        T04_branch_F=dict(old=0.0,new=f_reserve))
    budget["prerequisites_unpaid"] = ["T04_F_NEW_INSTRUMENT_BUILD_AND_WITNESS"]
    budget["gate_changed"] = False
    budget["H_route_errata"] = dict(
        original_interpretation="POST_C_PARTIAL_MAXCALL_AS_H_RESIDUAL",
        correction="C_STATUS_REMAINS_C_STATUS;H_ANY_OTHER_STATE_EXCLUDES_C;NEXT_F",
        H_started=True,H_interrupted_early=True,H_result_sha256=sha(result_h_path),
        H_wall_seconds=h["wall_seconds"],H_machine_hours=h_hours,
        H_accepted_posterior=False,controller_cleanup_confirmed=True,
        order_sha256=sha(order_path),status_emitter_sha256=sha(runner_path),
        independent_kimi_advisory="DECLARADO_NOT_SOURCE_REVIEWED")
    note = (
        "[REAL — T04-H interrompido; DERIVED — correção C→F]\n\n"
        f"Abertura016SHA256: {sha(opening_path)}. Ordem015SHA256: {sha(order_path)}. "
        f"RESULT C SHA256 {sha(result_c_path)}; RESULT H SHA256 {sha(result_h_path)}; "
        f"emissor pe_runner.py SHA256 {sha(runner_path)}; PROCESS.log H SHA256 {h['log_sha256']}.\n\n"
        "Erro da bancada: interpretei o status PARTIAL_MAXCALL_NOT_ACCEPTED persistente após C como "
        "'qualquer outro estado' de H. A leitura estrita da árvore T04 mantém esse status em C; "
        "H lista estados outros. O emissor escolhe MAXCALL antes de LOW_ESS/TOO_FEW, então "
        "ESS baixo material não altera o rótulo emitido. Após C sem posterior aceito, a próxima via é F.\n\n"
        f"H foi lançado uma vez, interrompido apenas no supervisor próprio após {h['wall_seconds']:.6f} s "
        f"({h_hours:.12f} h); RC={h['returncode']}; controlador={h['controller_receipt']['status']}; "
        f"limpeza confirmada={h['cleanup_confirmed']}. Nenhum posterior ou sigma aceito. "
        "A tentativa e seu custo permanecem na custódia; não será retomada. "
        f"Reserva restante para F: {f_reserve:.12f} h. Próximo: construir/testar o segundo instrumento Kerr V2 "
        "com dtau220 sem modificar os originais, registrar a configuração e medir F. Gate inalterado.\n"
    )
    budget_bytes = encoded(budget)
    budget_sha = hashlib.sha256(budget_bytes).hexdigest()
    witness = (
        "[REAL — H interrompido; INPUT — reserva F]\n\n"
        f"allocation_sha256: {budget_sha}\nregistered_utc: {now}\n\n"
        f"Abertura016SHA256: {sha(opening_path)}. Pai v4: {sha(old_path)}. "
        f"RESULT H: {sha(result_h_path)}. H real {h_hours:.12f} h; F reservado {f_reserve:.12f} h. "
        f"Total {budget['authorized_machine_hours']:.12f} h, gasto {budget['accounting']['machine_hours_spent']:.12f} h. "
        "Configuração científica não foi modificada neste registro; F ainda não foi lançado. "
        "O parecer Kimi é consultivo; a correção foi conferida na ordem e no emissor. Gate inalterado.\n"
    )
    note_path = OUT / "ENTREGA_015_MEDIDA_T04_H_INTERRUPTED_ROUTE_CORRECTION.md"
    witness_path = OUT / "ENTREGA_015_ORCAMENTO_015_v5.md"
    budget_path = RING / "ORCAMENTO_015_v5.json"
    new(note_path, note.encode("utf-8"))
    new(witness_path, witness.encode("utf-8"))
    new(budget_path, budget_bytes)
    assert sha(budget_path) == budget_sha
    print(json.dumps(dict(status="T04_H_CORRECTED_TO_F",H_cost_hours=h_hours,
        F_reserved_hours=f_reserve,budget_sha256=budget_sha,
        note_sha256=sha(note_path),witness_sha256=sha(witness_path))))


if __name__ == "__main__":
    main()
