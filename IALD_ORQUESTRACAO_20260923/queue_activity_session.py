"""Local-session adapter to the existing queue CLI; exact entity IDs only.

Deployment places this beside the queue transport_cli.py. A new process loads
current code. This does not refresh, stop or impersonate an existing MCP process.
OS-local access is the trust boundary, not possession of a ticket.
"""
import json
import sys
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.activity_bridge import invoke

def main():
    request=json.load(sys.stdin)
    result=invoke(Runtime(recover=False),request)
    print(json.dumps(result,ensure_ascii=False,allow_nan=False))

if __name__=='__main__':main()
