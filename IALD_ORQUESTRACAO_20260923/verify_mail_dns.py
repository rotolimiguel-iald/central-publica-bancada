"""Record public DNS evidence, with atomic local receipts."""
import json
import subprocess
from pathlib import Path
from iald_orchestrator.safe_files import save_json, utc_now

base = Path(__file__).resolve().parent
script = r'''
$ErrorActionPreference='Stop'
$rows=@()
foreach($domain in @('rmiguel.adv.br','convim.com.br')) {
  foreach($kind in @('MX','TXT')) {
    try {
      $items=@(Resolve-DnsName -Name $domain -Type $kind -Server 1.1.1.1 -DnsOnly | Select-Object Name,Type,NameExchange,Preference,Strings)
      $rows += [pscustomobject]@{name=$domain;kind=$kind;ok=$true;records=$items}
    } catch { $rows += [pscustomobject]@{name=$domain;kind=$kind;ok=$false;error='DNS_QUERY_FAILED'} }
  }
  try {
    $items=@(Resolve-DnsName -Name "_dmarc.$domain" -Type TXT -Server 1.1.1.1 -DnsOnly | Select-Object Name,Strings)
    $rows += [pscustomobject]@{name="_dmarc.$domain";kind='TXT';ok=$true;records=$items}
  } catch { $rows += [pscustomobject]@{name="_dmarc.$domain";kind='TXT';ok=$false;error='DNS_QUERY_FAILED'} }
}
foreach($alias in @('imap','pop','pop3','smtp','mail','mobile','pda','autodiscover')) {
  $name="$alias.rmiguel.adv.br"
  try {
    $items=@(Resolve-DnsName -Name $name -Type CNAME -Server 1.1.1.1 -DnsOnly | Select-Object Name,NameHost)
    $rows += [pscustomobject]@{name=$name;kind='CNAME';ok=$true;records=$items}
  } catch { $rows += [pscustomobject]@{name=$name;kind='CNAME';ok=$false;error='DNS_QUERY_FAILED'} }
}
ConvertTo-Json -InputObject $rows -Depth 8 -Compress
'''
run = subprocess.run(['powershell.exe', '-NoProfile', '-Command', script],
                     capture_output=True, text=True, timeout=90)
if run.returncode:
    raise RuntimeError('DNS verification command failed')
rows = json.loads(run.stdout)
expected = {'mx.core.locaweb.com.br': 10, 'mx.b.locaweb.com.br': 10,
            'mx.a.locaweb.com.br': 20, 'mx.jk.locaweb.com.br': 20}
for row in rows:
    if row['kind'] == 'MX':
        row['expected_match'] = {x['NameExchange'].rstrip('.'): x['Preference'] for x in row.get('records', [])} == expected
receipt = dict(checked_at=utc_now(), resolver='1.1.1.1', queries=rows,
               provider_source='https://www.locaweb.com.br/ajuda/wiki/como-configurar-o-mx-e-mail-locaweb/',
               mail_aliases_dns_only_verified_in_cloudflare=True,
               sites_and_tunnels_modified=False, delivery_tested=False, dkim_validated=False)
save_json(base/'validation/mail_dns_after.json', receipt)
print(json.dumps({'queries': len(rows), 'query_failures': sum(not x['ok'] for x in rows),
                  'mx_domains_match': sum(x.get('expected_match', False) for x in rows)}))
