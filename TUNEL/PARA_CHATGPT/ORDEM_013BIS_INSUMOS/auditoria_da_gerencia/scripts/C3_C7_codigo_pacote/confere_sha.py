import hashlib, os, sys
B = r'C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/'
claims = {
 'C3_UNRAVELING_API.json':'e280b73ccbdeece3ee051e2ffa32fd963e85ff81717a9df8881a04f5f5c6ed24',
 'C6_GUARD_TEST.json':'46aa5d66b7db186b19c4148149b6ebe9a3ec8ffeb75c78530641a1fbc46a5c4e',
 'C7_PACKAGE_VALIDATION.json':'9b333c7859c1c5b9ea60076e84fc173c88b7cbe96c6cdff50bf0a307511989c1',
 'tgl_ringdown_unravelings.py':'2858efdbf0e1f8ba2b8419e9f2a987c340ae02e2e5825495f0d3381b2d26e830',
 'verify_unravelings.py':'e696a6f768dd9a4eae1c09a7d6d9ff7664ccf531b44d8d9c69c5dbe5b5f0a965',
 'build_independent_package.py':'a0cb6e21326128e39a7af3ea0cc389053aafff8067f9afe089a7e677255a39d5',
 'package_demo.py':'63d299e5be9bd659f5c140c4a8216f04b10ecd930e7858a8274b67cd12e09c2b',
 'package_reproduce_c6.py':'916b812ed3b359c42a5929ca7355083ed8229fc563b715ac8b7827753204cc72',
 'verify_package_release.py':'ca1dcbdccc7b411ff51887fceb4c2de064f8943fdcd92a1582b5df9617b58c30',
 'C7_INDEPENDENT/MANIFEST.json':'29d36d2e921344ee2a2d3ea69f95c962b538c5f042b7c70a16942414f096279c',
 'C7_INDEPENDENT/README.md':'4b8f73158cae5c7231725ec2d4c8dd12a62db3720e26b4b189d3ae898468272b',
 'C7_INDEPENDENT/C6_REPRODUCTION_RESULT.json':'0ed044f5db8d47cc845fc2de0b78da9e70250f6f4cfcbe3a1ac282b32b2e61a4',
 'cache/TGL_RINGDOWN_INDEPENDENT_v1.zip':'c03563c8ecc1b0efb76ffa20ea3a1615e2e12965058121204dac4e166d2ed436',
 'C2_TEMPLATE_CHECKS.json':'b43fa517a37f9b41b8aa2d4f699571a4e24c7da5f6027266e55a86b6ffbe579a',
 'C0_C3_checks.json':'0592189981243c503a36967cd9285666e5120c804cca41bb23e233a6bd5230b0',
}
ok=0
for p,h in claims.items():
    try:
        got = hashlib.sha256(open(B+p,'rb').read()).hexdigest()
    except Exception as e:
        print('ERRO',p,e); continue
    st = 'OK' if got==h else 'DIVERGE'
    ok += st=='OK'
    print(st, p, got[:16], 'alegado', h[:16])
print('conferidos', ok, 'de', len(claims))
