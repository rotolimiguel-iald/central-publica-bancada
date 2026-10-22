"""Offline check of the campaign's Claude Opus selection and receipt."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from iald_orchestrator import canonical_memory, providers


class FakeProcess:
    def __init__(self, args, **kwargs):
        self.args = args
        self.returncode = 0

    def communicate(self, prompt, timeout):
        assert timeout == 900
        assert "Desenvolva a resposta na extensão necessária" in prompt
        return json.dumps({
            "is_error": False, "subtype": "success", "result": "ok",
            "usage": {}, "modelUsage": {"claude-opus-5-5[1m]": {}},
        }), ""


def main():
    prompt = "ORDEM_018 route smoke"
    generation = "a" * 64
    packet = {
        "prompt": prompt,
        "receipt": {"packet_sha256": canonical_memory.digest(prompt.encode()),
                    "generation": generation, "sources": []},
    }
    constraints = {
        "mission_id": "TGL_BANCADA_OFICIAL",
        "branch_id": "ORDEM_018_SENSITIVITY",
        "lemma_id": "claude_opus_final_order_v375",
        "role": "skeptic", "required_provider": "claude",
        "max_calls": 1, "memory_generation": generation,
        "allowed_sources": ["um.py"],
    }
    created = []

    def fake_popen(args, **kwargs):
        process = FakeProcess(args, **kwargs)
        created.append(process)
        return process

    with patch.object(providers, "client_command", return_value=["mock-claude"]), \
         patch.object(providers.subprocess, "Popen", side_effect=fake_popen):
        result = providers.execute("claude", prompt, BASE,
                                   memory_packet=packet,
                                   execution_constraints=constraints)
    assert created and created[0].args[-2:] == ["--model", "opus"]
    assert result["model_identifiers"] == ["claude-opus-5-5[1m]"]
    assert result["opus_model_verified"] is True
    print("claude_opus_route_offline_passed")


if __name__ == "__main__":
    main()
