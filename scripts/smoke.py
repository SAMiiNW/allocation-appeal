import json, re, time
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
from genlayer_py.types import TransactionStatus

ROOT = Path(__file__).parents[1]
ENV = (ROOT.parents[3] / "accounts.env").read_text()
KEY = re.search(r'^ACCOUNT_1_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', ENV, re.M).group(1).strip()
DEPLOYMENT = json.loads((ROOT / "deployment.json").read_text())
ACCOUNT = create_account(account_private_key=KEY)
CLIENT = create_client(chain=studionet, account=ACCOUNT)
ADDRESS = DEPLOYMENT["contractAddress"]


def send(method, args):
    tx = CLIENT.write_contract(address=ADDRESS, function_name=method, args=args)
    print(method, tx, flush=True)
    CLIENT.wait_for_transaction_receipt(
        transaction_hash=tx, status=TransactionStatus.FINALIZED, retries=180, interval=5000
    )
    info = CLIENT.get_transaction(transaction_hash=tx)
    receipts = (info.get("consensus_data") or {}).get("leader_receipt") or []
    if info.get("status_name") != "FINALIZED" or info.get("result_name") != "MAJORITY_AGREE" or not any(
        item.get("execution_result") == "SUCCESS" for item in receipts
    ):
        raise RuntimeError({"tx": tx, "status": info.get("status_name"), "receipts": receipts})
    return tx


case_id = "AA-" + str(int(time.time()))
filed = send(
    "file_allocation",
    [
        case_id,
        ACCOUNT.address,
        "https://httpbin.org/base64/QWxsb2NhdGlvbiBydWJyaWM6IHNjb3JlIDgwLTEwMCB3aGVuIHRoZSByZXF1ZXN0IGlkZW50aWZpZXMgYSBwdWJsaWMgdGVjaG5pY2FsIHN0YW5kYXJkLCBjaXRlcyB0d28gY29ycm9ib3JhdGluZyByZWNvcmRzLCBhbmQgc3RhdGVzIGEgdXNlZnVsIHJldmlldyBvdXRjb21lOyBzY29yZSA0MC03OSBpZiBvbmx5IHR3byBjcml0ZXJpYTsgb3RoZXJ3aXNlIDAtMzku",
        "Allocate review credit for an HTTP standards analysis that identifies RFC 9110, cites two corroborating public records, and states a useful implementation-review outcome.",
        "https://httpbingo.org/base64/RXZpZGVuY2UgQTogUkZDIDkxMTAgaXMgdGhlIEhUVFAgU2VtYW50aWNzIHN0YW5kYXJkIGFuZCBpcyBpZGVudGlmaWVkIGJ5IHRoZSBSRkMgRWRpdG9yLg==",
        "https://postman-echo.com/get?record=Evidence%20B%3A%20MDN%20documents%20HTTP%20semantics%20as%20publicly%20useful%20implementation%20guidance.",
        600,
    ],
)
scored = send("score_allocation", [case_id])
after_score = CLIENT.read_contract(address=ADDRESS, function_name="get_allocation", args=[case_id])
assert after_score["state"] == "APPEAL_OPEN"
assert after_score["appeal_window"] == 600
assert after_score["appeal_deadline"] > 0
appealed = send(
    "appeal_score",
    [case_id, "Please reconsider the score using both cited evidence records and the frozen rubric."],
)
state = CLIENT.read_contract(address=ADDRESS, function_name="get_allocation", args=[case_id])
assert state["state"] == "APPEALED"
assert state["appeal_deadline"] == after_score["appeal_deadline"]
proof = {
    "caseId": case_id,
    "transactions": {"file": filed, "score": scored, "appeal": appealed},
    "afterScore": after_score,
    "state": state,
}
(ROOT / "network-run.json").write_text(json.dumps(proof, indent=2))
print(json.dumps(proof, indent=2))
