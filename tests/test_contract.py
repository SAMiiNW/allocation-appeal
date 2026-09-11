from pathlib import Path
import ast
s=(Path(__file__).parents[1]/'contracts/contract.py').read_text()
def test_parse():ast.parse(s)
def test_appeal_lifecycle():assert all(('def '+x) in s for x in ('file_allocation','score_allocation','appeal_score','resolve_allocation','get_allocation'))
def test_appeal_survives_scoring():assert "c.state='APPEAL_OPEN'" in s and 'now()<=c.appeal_deadline' in s
