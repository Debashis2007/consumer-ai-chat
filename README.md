# Use Case: Consumer AI Chat

**Author fingerprint:** `DBHATT-Debashis2007-SystemDesignPOC-2026` — Debashis Bhattacharjee ([@Debashis2007](https://github.com/Debashis2007))

**YouTube walkthrough:** [Consumer Ai Chat — System Design #Shorts](https://youtu.be/flQZWSZxMOc)

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [01 — LLM Inference Serving](../01-llm-inference-serving.md)

## Users & problem

Millions of consumers chat with an assistant in a web/mobile app. They expect fast first tokens, stable streaming, and fair service during peaks—without one viral spike melting the fleet.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| TTFT P99 | ≤ 500 ms (regional) |
| Inter-token P99 | ≤ 50 ms |
| Availability | 99.9% |
| Fairness | Soft quotas; free tier shed first |
| Models | Default mid/frontier; optional “fast” tier |

## Design (from parent)

Reuse the parent control plane:

```
Client → Edge → API/BFF → Router → Priority queue (interactive)
       → Continuous-batching GPU workers → Stream back
```

Apply parent patterns:

- **Continuous batching + admission control** for interactive priority.
- **Separate pools** if long-context or heavy tools would poison chat TTFT.
- **Prefix/KV cache** for system prompts and common templates.
- **Canary + rollback** on every model revision (tie to [05](../05-model-monitoring-observability.md)).

## Specializations

| vs generic inference | Consumer chat choice |
|----------------------|----------------------|
| Tenancy | User/session quotas, not org TPM first |
| Priority | Interactive always beats batch/eval |
| UX coupling | Must integrate [02 streaming](../02-streaming-token-delivery.md) |
| Safety | Always-on layered safety ([06](../06-safety-moderation-pipeline.md)) |
| Product surface | Conversations/sync live in [10](../10-global-realtime-product-surface.md) |

## Failure modes

- Peak load → raise free-tier shedding; protect paid interactive.
- GPU OOM from huge pastes → hard max prompt + dedicated long-context tier.
- Bad model deploy → auto-rollback on TTFT / thumbs-down / safety spike.




## Design walkthrough (opens on GitHub)

> **Watch on YouTube:** [Consumer Ai Chat — System Design #Shorts](https://youtu.be/flQZWSZxMOc)


![Design overview](docs/video/design-overview.gif)

Full narrated video (download): [docs/video/design-overview.mp4](docs/video/design-overview.mp4)

## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd consumer-ai-chat
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -s -X POST http://127.0.0.1:8000/chat -H 'Content-Type: application/json' -d '{"prompt":"hi","tier":"free"}' | jq

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

