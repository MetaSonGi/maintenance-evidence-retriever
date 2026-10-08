import unittest,json
from pathlib import Path
from main import *
class Tests(unittest.TestCase):
    def sample(self):return json.loads(Path(__file__).with_name('sample-input.json').read_text(encoding='utf-8'))

    def test_asset_revision_date_and_citation(self):
        o=run(self.sample());self.assertEqual(len(o['hits']),1);self.assertEqual(o['hits'][0]['citation'],'manual@2#heat');self.assertIsNone(o['generated_answer'])
    def test_no_match(self):
        d=self.sample();d['query']='불일치단어';self.assertEqual(run(d)['status'],'no_evidence')
    def test_historical_revision(self):
        d=self.sample();d['as_of']='2026-02-01';self.assertEqual(run(d)['hits'][0]['citation'],'manual@1#heat')
    def test_duplicate_and_topk(self):
        d=self.sample();d['documents'].append(d['documents'][0].copy())
        with self.assertRaises(ValueError):run(d)
        d=self.sample();d['top_k']=0
        with self.assertRaises(ValueError):run(d)

if __name__=="__main__":unittest.main()
