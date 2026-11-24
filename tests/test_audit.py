import tempfile
import unittest
from pathlib import Path
from isin_validation_claim_audit.audit import audit, claims, evidence, main
from isin_validation_claim_audit.phrases import ISINVALIDATION, NOISINVALIDATION, GENERIC_NAMES

class AuditTests(unittest.TestCase):
    def test_phrases(self):
        self.assertEqual((len(ISINVALIDATION), len(NOISINVALIDATION), len(GENERIC_NAMES)), (50, 24, 24))
        for phrase in ISINVALIDATION:
            with self.subTest(phrase=phrase): self.assertTrue(claims(phrase)[0])
        for phrase in NOISINVALIDATION:
            with self.subTest(phrase=phrase): self.assertEqual(claims(phrase), (set(), {phrase}))
        self.assertEqual(claims('```\nvalidate isin\n```\n\n`validate isin`'), ({'validate isin'}, set()))

    def test_library_routes(self):
        cases = ['import stdnum.isin\nstdnum.isin.validate(x)', 'import stdnum.isin as si\nsi.is_valid(x)', 'from stdnum import isin\nisin.validate(x)', 'import stdnum\nstdnum.isin.is_valid(x)', 'from stdnum.isin import validate as v\nv(x)', 'from stdnum.isin import is_valid\nis_valid(x)', 'import validators\nvalidators.isin(x)', 'import validators as v\nv.isin(x)', 'from validators import finance\nfinance.isin(x)', 'import validators.finance as vf\nvf.isin(x)', 'import validators.finance\nvalidators.finance.isin(x)', 'from validators import isin as v\nv(x)', 'from validators.finance import isin\nisin(x)']
        for source in cases:
            with self.subTest(source=source): self.assertTrue(evidence(source))
        for name in GENERIC_NAMES:
            with self.subTest(name=name):
                self.assertTrue(evidence('obj.'+name+'(x)'))
                self.assertTrue(evidence('from lib import '+name+' as f\nf(x)'))
                self.assertTrue(evidence('obj = make()\nobj.'+name+'(x)'))

    def test_not_evidence(self):
        cases = ['import stdnum.isin', 'import validators', 'validate(x)', 'is_valid(x)', 'isin(x)', 'compact(x)', 'calc_check_digit(x)', 'from_natid(x)', 'validate_isin(x)', 'obj.validate(x)', 'obj.is_valid(x)', 'obj.isin(x)', 'import stdnum.isin\nstdnum.isin.compact(x)', 'import stdnum.isin\nstdnum.isin.calc_check_digit(x)', 'import stdnum.isin\nstdnum.isin.from_natid(x)', 'import stdnum.isin\nstdnum.isin.format(x)', 'import validators\nvalidators.cusip(x)', 'import validators\nvalidators.sedol(x)', 'import stdnum.cusip\nstdnum.cusip.validate(x)', 'import stdnum.sedol\nstdnum.sedol.is_valid(x)', 'import idutils\nidutils.is_isin(x)', 'lookup_isin(x)', 'import re\nre.fullmatch(pattern,x)', 'len(x)==12', 'x[:2] in countries', 'luhn.check(x)', '"validate isin"', 'from stdnum.isin import validate\nvalidate', 'def broken(:', 'import subprocess\nsubprocess.run(["isin-checker"])', 'import validators\nvalidators.email(x)', 'from stdnum.isin import validate\ndef validate(x): pass\nvalidate(x)', 'import validators\nvalidators = object()\nvalidators.isin(x)', 'import validators\nwith x as validators: pass\nvalidators.isin(x)', 'def check_isin(x): pass\nobj.check_isin(x)']
        for source in cases:
            with self.subTest(source=source): self.assertFalse(evidence(source))

    def test_findings_and_scopes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('validate isin')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            (p/'tests').mkdir(); (p/'tests'/'test_x.py').write_text('import validators\nvalidators.isin(x)')
            self.assertEqual(audit(p)[0]['severity'], 'MEDIUM')
            (p/'app.py').write_text('import validators\nvalidators.isin(x)')
            self.assertEqual(audit(p), [])
            (p/'README.md').write_text('does not validate isin')
            self.assertEqual(audit(p)[0]['id'], 'documented-no-isin-validation-claim-false')
            self.assertEqual(audit(p, ['app.py']), [])
            (p/'app.py').unlink(); self.assertEqual(audit(p), [])

    def test_cli(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('validate isin')
            self.assertEqual(main(['audit', d, '--json']), 2)
            self.assertEqual(main(['audit', d, '--ignore', 'README.md']), 0)
            self.assertEqual(main(['audit', d+'/missing']), 1)
            with self.assertRaises(SystemExit) as e: main(['audit', '--fail-on', 'HIGH'])
            self.assertEqual(e.exception.code, 1)

    def test_document_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('~~~\nvalidate isin\n~~~')
            (p/'docs').mkdir(); (p/'docs'/'guide.md').write_text('does not validate isin')
            (p/'examples').mkdir(); (p/'examples'/'x.py').write_text('import validators\nvalidators.isin(x)')
            self.assertEqual(audit(p), [])
            (p/'x.py').write_text('import validators\nvalidators.isin(x)')
            self.assertEqual(len(audit(p)), 1)

if __name__ == '__main__': unittest.main()
