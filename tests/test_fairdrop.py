import json
import pytest

BODY = 'Intelligent Contracts use AI to interpret text. Validators independently check results. Consensus is not a guarantee of truth.'
REFERENCE = 'GenLayer uses Python contracts, LLM calls and independent validators. Source quality matters.'

def review(scores=(45,27,18), needs_review=False):
    return {'scores':list(scores),'needs_review':needs_review,'reasons':['Grounded facts.','Example and limits.','Clear prose.'],'evidence':['Validators independently check results.']}

@pytest.fixture
def campaign(direct_deploy):
    return direct_deploy('contracts/fairdrop.py','FairDrop test','Explain the concept, an example and limits.',REFERENCE,1000)

def submit(c,vm,account):
    with vm.prank(account):
        c.submit('Article',BODY)
    return str(account)

def grade(c,vm,key,result=None):
    vm.clear_mocks()
    vm.mock_llm(r'.*',json.dumps(review() if result is None else result))
    c.evaluate(key)

def state(c):
    return json.loads(c.get_campaign())

def test_happy_path(campaign,direct_vm,direct_alice,direct_bob,direct_charlie):
    c=campaign; vm=direct_vm
    ids=[submit(c,vm,a) for a in [direct_alice,direct_bob,direct_charlie]]
    c.close_submissions()
    for key,scores in zip(ids,[(45,27,18),(40,23,17),(5,10,15)]):
        grade(c,vm,key,review(scores))
        assert vm.run_validator() is True
    assert json.loads(c.proposal())=={ids[0]:529,ids[1]:471}
    c.approve()
    assert state(c)['phase']=='approved'
    assert sum(state(c)['allocations'].values())==1000
    assert json.loads(c.proposal())==state(c)['allocations']

@pytest.mark.parametrize('method,args',[('close_submissions',()),('evaluate',('missing',)),('approve',()),('cancel',('cancel test',))])
def test_owner_permissions(campaign,direct_vm,direct_alice,method,args):
    before=state(campaign)
    with direct_vm.prank(direct_alice),direct_vm.expect_revert('Owner only'):
        getattr(campaign,method)(*args)
    assert state(campaign)==before

def test_duplicate_and_closed_submission(campaign,direct_vm,direct_alice,direct_bob):
    submit(campaign,direct_vm,direct_alice)
    with direct_vm.prank(direct_alice),direct_vm.expect_revert('One submission per address'):
        campaign.submit('Again',BODY)
    campaign.close_submissions()
    with direct_vm.prank(direct_bob),direct_vm.expect_revert('Submissions closed'):
        campaign.submit('Late',BODY)

@pytest.mark.parametrize('method,args',[('approve',()),('evaluate',('missing',)),('proposal',()),('withdraw_unresolved',('why',))])
def test_phase_guards(campaign,direct_vm,method,args):
    with direct_vm.expect_revert('Not in review phase'):
        getattr(campaign,method)(*args)

def test_empty_close(campaign,direct_vm):
    with direct_vm.expect_revert('Campaign must have submissions'):
        campaign.close_submissions()

def test_missing_and_unevaluated(campaign,direct_vm,direct_alice):
    submit(campaign,direct_vm,direct_alice);campaign.close_submissions()
    with direct_vm.expect_revert('Submission not found'):
        campaign.evaluate('missing')
    with direct_vm.expect_revert('Unresolved reviews remain'):
        campaign.approve()

def test_no_score_shopping(campaign,direct_vm,direct_alice):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions();grade(campaign,direct_vm,key)
    with direct_vm.expect_revert('Already evaluated'):
        campaign.evaluate(key)

def test_unresolved_author_withdrawal(campaign,direct_vm,direct_alice,direct_bob):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions();grade(campaign,direct_vm,key,review(needs_review=True))
    with direct_vm.expect_revert('Unresolved reviews remain'):
        campaign.approve()
    with direct_vm.prank(direct_bob),direct_vm.expect_revert('Submission not found'):
        campaign.withdraw_unresolved('Not my article')
    with direct_vm.prank(direct_alice):
        campaign.withdraw_unresolved('Reference is insufficient; I opt out.')
    assert state(campaign)['entries'][0]['review']['needs_review'] is True
    assert state(campaign)['entries'][0]['withdrawn'] is True
    assert json.loads(campaign.proposal())=={}
    campaign.approve()
    assert state(campaign)['allocations']=={}

def test_cannot_withdraw_qualified(campaign,direct_vm,direct_alice):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions();grade(campaign,direct_vm,key)
    with direct_vm.prank(direct_alice),direct_vm.expect_revert('Only unresolved'):
        campaign.withdraw_unresolved('Cannot discard a valid score')

def test_cancel_terminal(campaign,direct_vm,direct_alice):
    campaign.cancel('Insufficient reference material')
    assert state(campaign)['phase']=='cancelled'
    assert state(campaign)['allocations']=={}
    with direct_vm.expect_revert('Campaign is terminal'):
        campaign.cancel('Again')
    with direct_vm.prank(direct_alice),direct_vm.expect_revert('Submissions closed'):
        campaign.submit('Late',BODY)

@pytest.mark.parametrize('scores,flag,expected',[
 ((44,26,18),False,True),((39,27,18),False,False),((45,23,18),False,False),((45,27,15),False,False),((45,27,18),True,False)])
def test_independent_validator(campaign,direct_vm,direct_alice,scores,flag,expected):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions();grade(campaign,direct_vm,key)
    direct_vm.clear_mocks();direct_vm.mock_llm(r'.*',json.dumps(review(scores,flag)))
    assert direct_vm.run_validator() is expected

def test_threshold_disagreement(campaign,direct_vm,direct_alice):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions();grade(campaign,direct_vm,key,review((30,20,10)))
    direct_vm.clear_mocks();direct_vm.mock_llm(r'.*',json.dumps(review((29,20,10))))
    assert direct_vm.run_validator() is False

@pytest.mark.parametrize('bad',[
 {'scores':[51,27,18]}, {'scores':[True,27,18]}, {'scores':[45.5,27,18]}, {'scores':[45,27]},
 {'needs_review':'false'}, {'reasons':[]}, {'evidence':['An invented quote']}, {'evidence':['']},
])
def test_invalid_llm_output(campaign,direct_vm,direct_alice,bad):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions()
    invalid=review();invalid.update(bad)
    direct_vm.mock_llm(r'.*',json.dumps(invalid))
    with pytest.raises(Exception):
        campaign.evaluate(key)
    assert state(campaign)['entries'][0]['review'] is None

@pytest.mark.parametrize('pool',[0,-1,1000001])
def test_invalid_pool(direct_deploy,direct_vm,pool):
    with direct_vm.expect_revert('Invalid campaign'):
        direct_deploy('contracts/fairdrop.py','Title','Brief',REFERENCE,pool)

@pytest.mark.parametrize('body',['tiny',' '*12000+BODY],ids=['too-short','padded-overlimit'])
def test_body_limits(campaign,direct_vm,direct_alice,body):
    with direct_vm.prank(direct_alice),direct_vm.expect_revert('Invalid submission'):
        campaign.submit('Article',body)

def test_no_eligible_submissions(campaign,direct_vm,direct_alice):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions();grade(campaign,direct_vm,key,review((20,20,19)))
    assert json.loads(campaign.proposal())=={}
    campaign.approve();assert state(campaign)['allocations']=={}

def test_tie_break(campaign,direct_vm,direct_alice,direct_bob,direct_charlie):
    ids=[submit(campaign,direct_vm,a) for a in [direct_charlie,direct_bob,direct_alice]]
    campaign.close_submissions()
    for key in ids:grade(campaign,direct_vm,key,review((30,20,10)))
    allocation=json.loads(campaign.proposal())
    assert allocation[min(ids)]==334
    assert sorted(allocation.values())==[333,333,334]

def test_terminal_approval(campaign,direct_vm,direct_alice,direct_bob):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions();grade(campaign,direct_vm,key);campaign.approve()
    saved=state(campaign)
    for method,args in [('approve',()),('evaluate',(key,)),('cancel',('Too late',)),('close_submissions',())]:
        with pytest.raises(Exception):getattr(campaign,method)(*args)
    assert state(campaign)==saved

def test_invalid_json_leaves_entry_unreviewed(campaign,direct_vm,direct_alice):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions()
    direct_vm.mock_llm(r'.*','```json not actually json')
    with pytest.raises(Exception):campaign.evaluate(key)
    assert state(campaign)['entries'][0]['review'] is None

def test_withdrawal_audit_and_repeat(campaign,direct_vm,direct_alice):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions();grade(campaign,direct_vm,key,review(needs_review=True))
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert('Withdrawal reason required'):campaign.withdraw_unresolved(' ')
        campaign.withdraw_unresolved('Insufficient reference')
        with direct_vm.expect_revert('Only unresolved'):campaign.withdraw_unresolved('Again')
    with direct_vm.expect_revert('Submission withdrawn'):campaign.evaluate(key)
    assert state(campaign)['entries'][0]['withdrawal_reason']=='Insufficient reference'
    assert state(campaign)['audit'][-1].startswith('Author withdrew')

def test_invalid_validator_output_disagrees(campaign,direct_vm,direct_alice):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions();grade(campaign,direct_vm,key)
    direct_vm.clear_mocks();direct_vm.mock_llm(r'.*','invalid json')
    assert direct_vm.run_validator() is False

def test_forged_leader_output_rejected(campaign,direct_vm,direct_alice):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions();grade(campaign,direct_vm,key,review((30,20,10)))
    assert direct_vm.run_validator(leader_result=review((50,30,20))) is False

def test_leader_error_rejected(campaign,direct_vm,direct_alice):
    key=submit(campaign,direct_vm,direct_alice);campaign.close_submissions();grade(campaign,direct_vm,key)
    import genlayer as gl
    assert direct_vm.run_validator(leader_error=gl.vm.UserError('Simulated leader failure')) is False

def test_nondeterministic_closure_serialization(campaign,direct_vm,direct_alice):
    direct_vm.check_pickling=True
    key=submit(campaign,direct_vm,direct_alice)
    campaign.close_submissions()
    grade(campaign,direct_vm,key)
    assert direct_vm.run_validator() is True
