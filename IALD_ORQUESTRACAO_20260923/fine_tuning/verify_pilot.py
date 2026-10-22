"""Audit the actual exports, source custody and disjoint evaluation groups."""
from pathlib import Path
from collections import Counter, defaultdict
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_pilot import EXTRA_PRIVATE, FORBIDDEN, digest
from iald_orchestrator.safe_files import save_json, utc_now


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    manifest = json.loads((HERE/'dataset_manifest.json').read_bytes())
    examples = json.loads((HERE/'provenance.json').read_bytes())
    source_text = {}
    for source in manifest['sources']:
        raw = Path(source['path']).read_bytes()
        require(digest(raw) == source['sha256'], 'Scientific source changed')
        source_text[source['name']] = raw.decode('utf-8-sig').replace('\r\n', '\n')
    assignments = defaultdict(set)
    ids = set()
    for example in examples:
        require(example['id'] not in ids, 'Duplicate example')
        ids.add(example['id'])
        assignments[example['group_id']].add(example['split'])
        exported = example['user'] + example['assistant']
        require(not EXTRA_PRIVATE.search(exported), 'Private content detected')
        require(not FORBIDDEN.search(exported), 'Forbidden content detected')
        cited = example['user'].split('<documento>\n', 1)[1].rsplit('\n</documento>', 1)[0]
        require(cited.replace('\r\n','\n') in source_text[example['source']['file']], 'Evidence is not an exact source excerpt')
        if example['target_kind'].startswith('EXACT_'):
            require(cited in example['assistant'], 'Extractive answer changed evidence')
    require(all(len(splits) == 1 for splits in assignments.values()), 'Section leakage across splits')
    require(len(assignments) == manifest['groups'], 'Incorrect distinct-group count')
    checked = []
    for file in manifest['files']:
        raw = (HERE/file['file']).read_bytes()
        require(digest(raw) == file['sha256'], 'Export checksum mismatch')
        rows = [json.loads(line) for line in raw.splitlines()]
        expected = [e for e in examples if e['split'] == file['split']]
        require(len(rows) == len(expected) == file['records'], 'Record count mismatch')
        for row, example in zip(rows, expected):
            if file['format'] == 'vertex':
                require([r['role'] for r in row['contents']] == ['user','model'], 'Invalid Vertex roles')
                actual = [r['parts'][0]['text'] for r in row['contents']]
            else:
                messages = row['messages'][-2:]
                require([r['role'] for r in messages] == ['user','assistant'], 'Invalid chat roles')
                actual = [r['content'] for r in messages]
            require(actual == [example['user'], example['assistant']], 'Export lost or changed content')
        checked.append(file['file'])
    report = {'at':utc_now(), 'status':'LOCAL_DATA_AUDIT_PASSED',
              'examples':len(examples), 'counts':dict(Counter(e['split'] for e in examples)),
              'distinct_section_groups':len(assignments),
              'target_kinds':dict(Counter(e['target_kind'] for e in examples)),
              'checked_exports':checked, 'current_source_hashes_verified':True,
              'train_validation_test_section_overlap':False,
              'privacy_scan':'PASSED_PATTERN_SCAN_NOT_A_GENERAL_DLP_GUARANTEE',
              'model_quality_evaluated':False, 'qwen_local_modified':False}
    save_json(HERE/'validation.json', report)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
