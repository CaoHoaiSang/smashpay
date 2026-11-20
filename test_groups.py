import os
import tempfile

os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="smashpay-groups-")

from fastapi.testclient import TestClient

from database import DATA_DIR, db_cursor, init_db
from main import app


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_groups_isolate_ledgers_and_backup():
    init_db()
    with db_cursor() as cur:
        cur.execute("INSERT INTO members (name) VALUES ('Sổ cũ')")
        cur.execute(
            "INSERT INTO sessions (title, played_at) VALUES ('Buổi cũ', '2026-01-01')"
        )
    init_db()

    with TestClient(app) as client:
        status = client.get("/api/groups/status")
        assert status.status_code == 200
        assert status.json() == {"legacy_unclaimed": True}

        blocked = client.post("/api/groups", json={"name": "Chưa được"})
        assert blocked.status_code == 409

        claim = client.post("/api/groups/claim-legacy")
        assert claim.status_code == 200
        legacy = claim.json()
        token_a = legacy["token"]
        assert legacy["group"]["role"] == "owner"
        assert legacy["group"]["name"] == "Nhóm của tôi"
        assert client.post("/api/groups/claim-legacy").status_code == 409

        members = client.get("/api/members?include_inactive=true", headers=_auth(token_a))
        assert members.status_code == 200
        old_member = next(m for m in members.json() if m["name"] == "Sổ cũ")
        sessions = client.get("/api/sessions", headers=_auth(token_a)).json()
        old_session = next(s for s in sessions if s["title"] == "Buổi cũ")
        marked = client.put(
            f"/api/sessions/{old_session['id']}/template",
            headers=_auth(token_a),
            json={"is_template": True},
        )
        assert marked.status_code == 200

        created = client.post("/api/groups", json={"name": "Nhóm B"})
        assert created.status_code == 201
        group_b = created.json()
        token_b = group_b["token"]
        assert client.get("/api/sessions", headers=_auth(token_b)).json() == []
        assert client.get("/api/members", headers=_auth(token_b)).json() == []
        assert client.get(f"/api/sessions/{old_session['id']}", headers=_auth(token_b)).status_code == 404

        member_b = client.post("/api/members", headers=_auth(token_b), json={"name": "Bình"}).json()
        session_b = client.post(
            "/api/sessions",
            headers=_auth(token_b),
            json={
                "title": "Buổi B",
                "played_at": "2026-11-20",
                "participant_ids": [member_b["id"]],
            },
        )
        assert session_b.status_code == 201
        session_b_id = session_b.json()["session"]["id"]
        assert (
            client.put(
                f"/api/sessions/{session_b_id}/template",
                headers=_auth(token_b),
                json={"is_template": True},
            ).status_code
            == 200
        )
        still_a = client.get(f"/api/sessions/{old_session['id']}", headers=_auth(token_a)).json()
        still_b = client.get(f"/api/sessions/{session_b_id}", headers=_auth(token_b)).json()
        assert still_a["session"]["is_template"] == 1
        assert still_b["session"]["is_template"] == 1

        foreign_expense = client.post(
            f"/api/sessions/{session_b_id}/expenses",
            headers=_auth(token_a),
            json={
                "category": "court",
                "title": "Sân",
                "split_type": "equal_split",
                "total_amount": 1000,
                "payer_id": old_member["id"],
                "participant_ids": [old_member["id"]],
            },
        )
        assert foreign_expense.status_code == 404

        own_session = client.post(
            "/api/sessions",
            headers=_auth(token_a),
            json={
                "title": "Buổi A",
                "played_at": "2026-11-20",
                "participant_ids": [old_member["id"]],
            },
        ).json()
        mixed = client.post(
            f"/api/sessions/{own_session['session']['id']}/expenses",
            headers=_auth(token_a),
            json={
                "category": "court",
                "title": "Sân",
                "split_type": "equal_split",
                "total_amount": 1000,
                "payer_id": member_b["id"],
                "participant_ids": [old_member["id"]],
            },
        )
        assert mixed.status_code == 400

        invite = legacy["group"]["invite_code"]
        joined = client.post("/api/groups/join", json={"code": f" {invite.lower()} "})
        assert joined.status_code == 200
        member_token = joined.json()["token"]
        assert joined.json()["group"]["role"] == "member"
        assert "owner_code" not in joined.json()["group"]
        assert client.get("/api/group", headers=_auth(member_token)).json().get("owner_code") is None
        assert client.delete(f"/api/members/{old_member['id']}", headers=_auth(member_token)).status_code == 403
        assert (
            client.put(
                f"/api/sessions/{old_session['id']}/template",
                headers=_auth(member_token),
                json={"is_template": False},
            ).status_code
            == 403
        )
        seen = client.get("/api/members", headers=_auth(member_token)).json()
        assert [m["name"] for m in seen] == ["Sổ cũ"]
        assert client.get("/api/members", headers=_auth(token_b)).json()[0]["name"] == "Bình"

        owner_again = client.post("/api/groups/join", json={"code": legacy["group"]["owner_code"]})
        assert owner_again.status_code == 200
        assert owner_again.json()["group"]["role"] == "owner"
        assert owner_again.json()["group"]["owner_code"] == legacy["group"]["owner_code"]

        assert client.get("/api/members").status_code == 401
        assert client.post("/api/groups/join", json={"code": "KHONGTONTAI"}).status_code == 404
        assert client.post("/api/voice/transcribe", content=b"\x00" * 100).status_code == 401
        assert (
            client.post(
                "/api/voice/transcribe",
                headers=_auth(token_a),
                content=b"\x00" * 100,
            ).status_code
            == 400
        )

    backups = list((DATA_DIR / "backups").glob("badminton-*.db"))
    assert backups, "daily sqlite backup was not written"
