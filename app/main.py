# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""Consumer AI Chat — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload, AUTHOR_NAME, AUTHOR_FINGERPRINT, AUTHOR_GITHUB
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Consumer AI Chat"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(
        USE_CASE,
        {
            "author": AUTHOR_NAME,
            "author_github": AUTHOR_GITHUB,
            "fingerprint": AUTHOR_FINGERPRINT,
        },
    )

@app.get("/author")
def author():
    return {
        "author": AUTHOR_NAME,
        "github": AUTHOR_GITHUB,
        "fingerprint": AUTHOR_FINGERPRINT,
        "notice": "Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.",
    }


quotas = {"free": TokenBucket(5, 0.5), "paid": TokenBucket(50, 5)}

class ChatIn(BaseModel):
    prompt: str
    tier: str = "free"

@app.post("/chat")
async def chat(body: ChatIn):
    q = quotas.get(body.tier) or quotas["free"]
    if not q.allow():
        raise HTTPException(429, detail="shed: free tier quota exceeded")
    decision = safety.check_input(body.prompt)
    if decision.action != "allow":
        return {"action": decision.action, "reason_code": decision.reason_code}
    text = await llm.complete(body.prompt)
    return {"tier": body.tier, "model": llm.model, "text": text, "quota_remaining": q.remaining()}
