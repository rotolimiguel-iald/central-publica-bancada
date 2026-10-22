"""Prepare one bounded request; never submit or invoke a provider here."""
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
base = root.parent / "IALD_ORQUESTRACAO_20260923"
dest = root / "A2" / "delegation_a23_core.json"
if dest.exists():
    print(json.dumps({k: v for k, v in json.loads(dest.read_bytes()).items()
                      if k in ("request_id", "status", "job_id")}))
    raise SystemExit(0)

source = root.parent / "TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS/A2_A3_RETA_DE_LUZ/JULGAMENTO_FORMA_INSCRITA.md"
lines = source.read_text(encoding="utf-8").splitlines()
start = next(i for i, s in enumerate(lines, 1) if s.startswith("### A-2 —"))
end = next(i for i, s in enumerate(lines, 1) if i > start and s.startswith("### A-3 —")) - 1
digest = hashlib.sha256(source.read_bytes()).hexdigest()
prompt = f"""ORDEM 016, A-2.3.a, rascunho MiMo, UMA pergunta matemática. Não executar sem executor MiMo fixado e reserva de custo dentro de US$0,50 no ramo e US$10 na missão. Máximo uma chamada neste pedido, sem substituição automática. Coordenação Física apenas prepara/transmite, sem aprovar prova. NÃO reenviar A1b1, já encerrado. Não executar código nem alterar arquivos. Nenhuma credencial ou acervo jurídico incluído.

PERGUNTA: qual demonstração completa (ou contraexemplo) estabelece que o span REAL das funções f_r(z)=exp(-b*(z-r-i*pi/2)^2), r real, b>0 fixo, é denso no subespaço real K={{f em L2(R): Ff pertence a Fix(S_c)}}, c=2*pi^2, e que o multiplicador m_a(z)=exp(i*a*exp(z)), a>=0, preserva o fecho K? Justifique especialmente o passo do core ao domínio fechado, sem pressupor a isotonia que se busca demonstrar. Se a família for insuficiente, dê precisamente a hipótese/etapa que falha. Essa é uma única unidade: a rota por core denso de A2.3.a.

Dados disponíveis: Fourier usa exp(-2*pi*i*x*omega). T_c é multiplicação não limitada por exp(-c*omega), com domínio ponderado L2 explicitamente provado; J h(omega)=conj(h(-omega)); S_c=J*T_c; K_c=Fix(S_c) é padrão, Delta_c=T_c^2, domínio e grafo iguais ao multiplicador exp(-2*c*omega). Já compilei a ponte F(D(s)f)=exp(-2*pi*i*s*omega)Ff, D(s)f(x)=f(x-s). c=2*pi^2 identifica D(2*pi*t) com exp(i*t*log(deltaSymbol)); isto ainda NÃO prova meia-inclusão nem força 2*pi.

Receita a auditar: f_r(x+i*pi)=conj(f_r(x)); |m_a(x+i*y)|=exp(-a*exp(x)*sin(y))<=1 no strip 0<=y<=pi. Não basta citar estas igualdades para afirmar densidade, Hardy ou pertença ao domínio. Precisamos da ligação efetiva ao K_c acima, com sinais e normalização explícitos. Preserve a separação entre c0 por Fourier e 2*pi forçado. Resposta em português, até 2500 palavras; provas à mão marcadas DERIVED, nenhum resultado declarado compilado. Pode indicar lemas Lean necessários, sem inventar que existem. Não pesquisar fora das fontes nomeadas da ordem.

Proveniência: {source.name}, linhas {start}-{end}, SHA256 {digest}. Conteúdo relevante reexpresso acima; o provedor não deve presumir acesso ao caminho local. A base documental comum da TGL será acrescida pelo transporte com recibo; mantenha a projeção total <=20000 caracteres e bloqueie se não couber.
"""
rid = str(uuid.uuid4())
record = dict(request_id=rid, origin_thread_id="01a070fc-9484-7e13-a654-c6b5f61093a4",
              origin_house="Central de Patentes / Chatgpt / ORDEM_016_QG",
              created_at=datetime.now(timezone.utc).isoformat(), target="A-2.3.a",
              requested_provider="mimo", max_cost_usd=0.50, max_calls=1,
              prompt=prompt, prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
              status="prepared_awaiting_enforced_controls", job_id=None)
for path in [dest, base / "state/session_requests" / f"{rid}.json"]:
    assert not path.exists()
    data = json.dumps(record, ensure_ascii=False, indent=2).encode("utf-8")
    tmp = path.with_suffix(".tmp")
    with tmp.open("xb") as f:
        f.write(data)
    assert tmp.stat().st_size == len(data)
    os.replace(tmp, path)
print(json.dumps({"request_id": rid, "prompt_chars": len(prompt), "status": record["status"]}))
