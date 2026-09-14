from conftest import CONTRACT

RUBRIC = 'https://rubric.example/policy'
SOURCE_A = 'https://record-a.example/request'
SOURCE_B = 'https://record-b.example/context'
REQUEST = 'Allocate the emergency research grant using the frozen public rubric and the two independent records.'


def mocks(vm):
    vm.strict_mocks = True
    vm.check_pickling = True
    vm.mock_web(r'rubric\.example', {'status': 200, 'body': 'Rubric: award 80 points for documented urgent public benefit.'})
    vm.mock_web(r'record-a\.example', {'status': 200, 'body': 'Independent record A confirms urgent public benefit.'})
    vm.mock_web(r'record-b\.example', {'status': 200, 'body': 'Independent record B confirms the documented request.'})
    vm.mock_llm(r'.*Score the request.*', '{"score":82,"reasons":["Urgency and public benefit satisfy the frozen rubric."],"evidence_indexes":[1,2]}')


def filed(vm, deploy, subject, window=600):
    vm.warp('2030-01-01T00:00:00+00:00')
    contract = deploy(CONTRACT)
    contract.file_allocation('alloc-1', f'0x{subject.hex()}', RUBRIC, REQUEST, SOURCE_A, SOURCE_B, window)
    mocks(vm)
    return contract


def test_delayed_scoring_starts_a_fresh_full_appeal_window(direct_vm, direct_deploy, direct_alice):
    contract = filed(direct_vm, direct_deploy, direct_alice, 3600)
    assert contract.get_allocation('ALLOC-1')['appeal_deadline'] == 0
    direct_vm.warp('2030-01-21T00:00:00+00:00')
    contract.score_allocation('alloc-1')
    result = contract.get_allocation('alloc-1')
    assert result['state'] == 'APPEAL_OPEN'
    assert result['appeal_deadline'] == 1895187600
    direct_vm.sender = direct_alice
    contract.appeal_score('alloc-1', 'The score omitted a documented eligibility fact that changes the allocation result.')
    assert contract.get_allocation('alloc-1')['state'] == 'APPEALED'


def test_immediate_and_boundary_finalization_are_rejected(direct_vm, direct_deploy, direct_alice):
    contract = filed(direct_vm, direct_deploy, direct_alice)
    contract.score_allocation('alloc-1')
    with direct_vm.expect_revert('closed appeal window required'):
        contract.resolve_allocation('alloc-1')
    direct_vm.warp('2030-01-01T00:10:00+00:00')
    with direct_vm.expect_revert('closed appeal window required'):
        contract.resolve_allocation('alloc-1')
    direct_vm.warp('2030-01-01T00:10:01+00:00')
    contract.resolve_allocation('alloc-1')
    assert contract.get_allocation('alloc-1')['state'] == 'RESOLVED'


def test_unauthorized_and_late_appeals_fail(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = filed(direct_vm, direct_deploy, direct_alice)
    contract.score_allocation('alloc-1')
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert('timely subject appeal required'):
        contract.appeal_score('alloc-1', 'This unrelated wallet must not be able to lodge an appeal for the named subject.')
    direct_vm.sender = direct_alice
    direct_vm.warp('2030-01-01T00:10:01+00:00')
    with direct_vm.expect_revert('timely subject appeal required'):
        contract.appeal_score('alloc-1', 'This appeal is complete enough but was submitted after the protected window expired.')


def test_appeal_window_bounds_and_forged_score(direct_vm, direct_deploy, direct_alice):
    direct_vm.warp('2030-01-01T00:00:00+00:00')
    contract = direct_deploy(CONTRACT)
    with direct_vm.expect_revert('complete independent allocation required'):
        contract.file_allocation('short', f'0x{direct_alice.hex()}', RUBRIC, REQUEST, SOURCE_A, SOURCE_B, 599)
    with direct_vm.expect_revert('complete independent allocation required'):
        contract.file_allocation('long', f'0x{direct_alice.hex()}', RUBRIC, REQUEST, SOURCE_A, SOURCE_B, 2592001)
    contract.file_allocation('alloc-1', f'0x{direct_alice.hex()}', RUBRIC, REQUEST, SOURCE_A, SOURCE_B, 600)
    mocks(direct_vm)
    case = contract.cases['ALLOC-1']
    result = contract._score(case)
    assert direct_vm.run_validator(leader_result=result) is True
    forged = dict(result)
    forged['score'] = 81
    assert direct_vm.run_validator(leader_result=forged) is False
