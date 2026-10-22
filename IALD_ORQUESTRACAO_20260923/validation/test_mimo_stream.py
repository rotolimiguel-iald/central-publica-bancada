import io
import json
import http.client
import unittest
from unittest.mock import patch
from iald_orchestrator import mimo


def frames(content='42', finish='stop', usage=True, done=True):
    def chunk(delta, reason=None):
        return {'model': mimo.MODEL, 'choices': [{'index': 0, 'delta': delta, 'finish_reason': reason}]}
    rows = [chunk({'reasoning_content': 'PRIVATE_REASONING'}), chunk({'content': content}), chunk({}, finish)]
    if usage:
        rows.append({'model': mimo.MODEL, 'choices': [], 'usage': {'prompt_tokens': 10, 'completion_tokens': 2, 'total_tokens': 12}})
    data = b': keepalive\r\n\r\n' + b''.join(('data: '+json.dumps(r)+'\r\n\r\n').encode() for r in rows)
    return data + (b'data: [DONE]\n\n' if done else b'')


class StreamTests(unittest.TestCase):
    def test_complete_usage_and_reasoning_discard(self):
        result = mimo.parse_response(mimo.read_stream(io.BytesIO(frames('ação'))))
        self.assertEqual(result['text'], 'ação')
        self.assertEqual(result['usage']['total_tokens'], 12)
        self.assertNotIn('PRIVATE_REASONING', json.dumps(result))

    def test_missing_end_usage_and_truncated_rejected(self):
        for args in [{'done': False}, {'usage': False}, {'finish': 'length'}]:
            with self.subTest(args=args), self.assertRaises(RuntimeError):
                mimo.read_stream(io.BytesIO(frames(**args)))

    def test_wrong_model_tools_and_extra_choice_rejected(self):
        for chunk in [
            {'model': 'other', 'choices': []},
            {'model': mimo.MODEL, 'choices': [{'index': 0, 'delta': {'tool_calls': [{}]}}]},
            {'model': mimo.MODEL, 'choices': [{}, {}]},
        ]:
            with self.subTest(chunk=chunk), self.assertRaises(RuntimeError):
                mimo.read_stream(io.BytesIO(('data: '+json.dumps(chunk)+'\n\n').encode()))

    def test_incomplete_read_diagnostics_no_partial_leak(self):
        class Broken:
            def readline(self, size):
                raise http.client.IncompleteRead(b'SECRET_PARTIAL', 100)
        with self.assertRaisesRegex(RuntimeError, 'parcial_bytes=14') as ctx:
            mimo.read_stream(Broken())
        self.assertNotIn('SECRET_PARTIAL', str(ctx.exception))

    def test_size_and_cancel(self):
        with patch.object(mimo, 'MAX_RESPONSE_BYTES', 8), self.assertRaises(RuntimeError):
            mimo.read_stream(io.BytesIO(frames()))
        class Cancel:
            def is_set(self): return True
        with self.assertRaises(RuntimeError):
            mimo.read_stream(io.BytesIO(frames()), Cancel())

    def test_execute_single_request_and_no_retry(self):
        class Reply(io.BytesIO):
            pass
        class Transport:
            calls = 0
            def open(self, req, timeout):
                self.calls += 1
                body = json.loads(req.data)
                assert body['stream'] is True
                assert body['thinking']['type'] == 'enabled'
                assert 'tools' not in body
                return Reply(frames(done=False))
        transport = Transport()
        with patch.object(mimo, 'authorization', return_value={'enabled': True}), patch.object(mimo, 'load_mimo', return_value='DUMMY'), patch.object(mimo.urllib.request, 'build_opener', return_value=transport):
            with self.assertRaises(RuntimeError): mimo.execute('public fixture')
        self.assertEqual(transport.calls, 1)



class TerminalUsageTests(unittest.TestCase):
    def wire(self, rows, done=True):
        return io.BytesIO((''.join('data: '+json.dumps(x)+'\n\n' for x in rows)+('data: [DONE]\n\n' if done else '')).encode())
    def terminal(self, usage=None, finish='stop'):
        return {'model':mimo.MODEL,'choices':[{'index':0,'delta':{'content':'42'},'finish_reason':finish}],'usage':usage}
    def usage(self):
        return {'prompt_tokens':10,'completion_tokens':2,'total_tokens':12}
    def test_usage_on_terminal_choice(self):
        result=mimo.parse_response(mimo.read_stream(self.wire([self.terminal(self.usage())])))
        self.assertEqual(result['text'],'42')
    def test_usage_final_separate(self):
        result=mimo.read_stream(self.wire([self.terminal(),{'model':mimo.MODEL,'choices':[],'usage':self.usage()}]))
        self.assertEqual(result['usage'],self.usage())
    def test_duplicate_consistent_and_conflicting_rejected(self):
        for total, expected in [(12,'duplicate_consistent'),(13,'duplicate_conflicting')]:
            second=self.usage();second['total_tokens']=total
            with self.subTest(total=total),self.assertRaisesRegex(RuntimeError,expected):
                mimo.read_stream(self.wire([self.terminal(self.usage()),{'model':mimo.MODEL,'choices':[],'usage':second}]))
    def test_usage_before_stop_rejected(self):
        with self.assertRaisesRegex(RuntimeError,'usage_before_stop'):
            mimo.read_stream(self.wire([self.terminal(self.usage(),None)]))
    def test_combined_usage_still_requires_done(self):
        with self.assertRaisesRegex(RuntimeError,'antes de DONE'):
            mimo.read_stream(self.wire([self.terminal(self.usage())],False))
    def test_invalid_counts_and_truncation(self):
        bad=self.usage();bad['total_tokens']=99
        for row in [self.terminal(bad),self.terminal(self.usage(),'length')]:
            with self.assertRaises(RuntimeError):mimo.read_stream(self.wire([row]))
    def test_structural_diagnostic_does_not_leak(self):
        row=self.terminal(self.usage(),None);row['choices'][0]['delta']['content']='PRIVATE_CONTENT';row['choices'][0]['delta']['reasoning_content']='PRIVATE_REASONING'
        with self.assertRaises(RuntimeError) as ctx:mimo.read_stream(self.wire([row]))
        self.assertIn('incoming_usage=1',str(ctx.exception));self.assertNotIn('PRIVATE',str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
