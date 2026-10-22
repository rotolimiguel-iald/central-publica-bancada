# -*- coding: utf-8 -*-
"""regua.py -- a RÉGUA dentro da máquina (a mesma da casa): estatuto em toda saída, palavra proibida recusada, o LIVRO DE TENTATIVAS.

Buscar evidência com um motor sempre ligado e várias IAs consultando é o cenário clássico de «achar sinal por insistência». Por isso:
  * toda operação que produz estatística de teste (ajustar, comparar, amostrar) é registrada no livro, por FAMÍLIA (operação + conjuntos +
    modelo + parâmetros livres). Šidák é apenas ilustração, não calibração da busca adaptativa.
    p_global/z_global ficam indisponíveis até existir contrato e calibração próprios;
  * nenhuma saída diz CONFIRMED / PROVED_BY / confirmado: a Bancada produz DIAGNÓSTICO com estatuto;
  * NOT_FALSIFIED ≠ CONFIRMED; PROVADA ≠ CONFIRMADA.
"""
from contextlib import contextmanager
import hashlib
import json
import math
import re
import sqlite3
import threading
import time

PROIBIDO = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED|CONSCIOUSNESS_PROVED|\bconfirmad[oa]s?\b", re.I)

ESTATUTOS = {
    "DIAGNOSTICO_DE_AVALIACAO": "avaliação de um ponto do modelo contra os dados: não é ajuste nem inferência",
    "AJUSTE_DE_MAXIMA_VEROSSIMILHANCA": "melhor ajuste por mínimos quadrados; σ pela matriz JᵀJ (aproximação gaussiana local)",
    "COMPARACAO_DE_MODELOS_DELTA_CHI2": "diferenças de chi2; conversão local TGL fixa versus beta livre condicional a Wilks; global indisponível",
    "DIAGNOSTICO_INVALIDO_SEM_SIGNIFICANCIA": "ajuste ou comparação inválidos; nenhuma significância calculada",
    "POSTERIOR_CONDICIONAL_AO_MODELO_E_AOS_DADOS": "amostras do posterior sob priors uniformes nos limites do pipeline; não é confirmação",
}


def guarda(obj):
    """Recusa (exceção) qualquer saída que contenha palavra proibida pela régua."""
    s = json.dumps(obj, ensure_ascii=False, default=str)
    m = PROIBIDO.search(s)
    if m:
        raise ValueError("REGUA: saída recusada por palavra proibida: %r" % m.group(0))
    return obj


def z_de_p(p):
    """z bilateral de um p (p pequeno: expansão assintótica estável)."""
    if p <= 0:
        return float("inf")
    if p >= 1:
        return 0.0
    from scipy.stats import norm
    return float(norm.isf(p / 2.0))


def p_de_z(z):
    from scipy.stats import norm
    return float(2.0 * norm.sf(abs(z)))


class Livro:
    """O livro de consultas: SQLite só de acréscimo em estado/livro.sqlite3."""

    def __init__(self, caminho):
        self.caminho = caminho
        self.lock = threading.Lock()
        with self._con() as c:
            c.execute("CREATE TABLE IF NOT EXISTS consultas (id INTEGER PRIMARY KEY, ts TEXT, cliente TEXT, operacao TEXT, familia TEXT, "
                      "conjuntos TEXT, modelo TEXT, pedido TEXT, resultado_sha TEXT, estatuto TEXT, estatistica REAL, p_local REAL)")

    @contextmanager
    def _con(self):
        connection = sqlite3.connect(self.caminho, timeout=30)
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    @staticmethod
    def familia(operacao, conjuntos, modelo):
        chave = json.dumps([operacao, sorted(conjuntos), modelo], sort_keys=True)
        return hashlib.sha256(chave.encode()).hexdigest()[:16]

    def registra(self, cliente, operacao, conjuntos, modelo, pedido, resultado, estatuto, estatistica=None, p_local=None):
        sha = hashlib.sha256(json.dumps(resultado, sort_keys=True, default=str).encode()).hexdigest()
        with self.lock, self._con() as c:
            c.execute("INSERT INTO consultas (ts, cliente, operacao, familia, conjuntos, modelo, pedido, resultado_sha, estatuto, estatistica, p_local) "
                      "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (time.strftime("%Y-%m-%dT%H:%M:%S"), cliente, operacao, self.familia(operacao, conjuntos, modelo), json.dumps(sorted(conjuntos)),
                       json.dumps(modelo, sort_keys=True), json.dumps(pedido, sort_keys=True, default=str), sha, estatuto, estatistica, p_local))
        return sha

    def n_familias_de_teste(self, incluir=None):
        """Famílias distintas de teste no livro; `incluir` soma a família do teste corrente se ela ainda não estiver lá."""
        with self._con() as c:
            fams = {r[0] for r in c.execute("SELECT DISTINCT familia FROM consultas WHERE p_local IS NOT NULL")}
        if incluir:
            fams.add(incluir)
        return len(fams)

    def corrige(self, p_local, familia=None):
        """Return a typed Sidak illustration, never a calibrated global claim."""
        if isinstance(p_local, bool):
            raise ValueError("tail probability must be numeric, not boolean")
        p_local = float(p_local)
        if not math.isfinite(p_local) or not 0.0 <= p_local <= 1.0:
            raise ValueError("tail probability must be finite and in [0, 1]")
        n = max(1, self.n_familias_de_teste(incluir=familia))
        pg = -math.expm1(n * math.log1p(-p_local)) if p_local < 1.0 else 1.0
        zl = z_de_p(p_local) if p_local > 0.0 else None
        zs = z_de_p(pg) if pg > 0.0 else None
        zl = zl if zl is not None and math.isfinite(zl) else None
        zs = zs if zs is not None and math.isfinite(zs) else None
        return dict(schema="evidence-tail-diagnostic-v1", p_local=p_local, z_local=zl, n_familias=n,
                    p_global=None, z_global=None, global_calibrated=False,
                    global_status="UNAVAILABLE_NOT_CALIBRATED",
                    local_status="TAIL_EQUIVALENT_NOT_CALIBRATION" if zl is not None else "NUMERICAL_LIMIT_NO_FINITE_Z",
                    sidak_ilustrativo=dict(p=pg, z=zs, n_familias=n,
                                          status="ILLUSTRATION_ONLY_NOT_GLOBAL_EVIDENCE"),
                    metodo="Šidák ilustrativo; validade local e busca global exigem calibração própria")

    def resumo(self, n=30):
        with self._con() as c:
            tot = c.execute("SELECT COUNT(*) FROM consultas").fetchone()[0]
            ult = c.execute("SELECT ts, cliente, operacao, conjuntos, modelo, estatuto, estatistica, p_local, resultado_sha FROM consultas "
                            "ORDER BY id DESC LIMIT ?", (n,)).fetchall()
        return dict(total=int(tot), familias_de_teste=self.n_familias_de_teste(),
                    ultimas=[dict(ts=a, cliente=b, operacao=o, conjuntos=json.loads(cj), modelo=json.loads(mo), estatuto=e, estatistica=s,
                                  p_local=p, resultado_sha=h[:16]) for a, b, o, cj, mo, e, s, p, h in ult])
