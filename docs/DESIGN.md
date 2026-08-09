# Design: Consumer AI Chat

**Project:** `consumer-ai-chat`  
**Parent system design:** `01-llm-inference-serving.md`

## 1. What this POC demonstrates

Interactive chat for mass-market users with tiered fairness so free traffic cannot starve paid interactive sessions.

## 2. Architecture (POC)

```text
Client → POST /chat → tier quota (TokenBucket)
                    → SafetyPlane (input)
                    → MockLLM complete
                    → JSON response
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Priority / tiered admission | Protects paid interactive SLO when free tier spikes. | `TokenBucket` per tier; 429 sheds free first. |
| Fail-closed safety gate | Blocks disallowed prompts before spending model time. | `SafetyPlane.check_input`. |
| MockLLM | Demonstrates latency/token behavior without cloud keys. | `poc_core.MockLLM`. |

## 4. Key endpoints

`GET /health`, `POST /chat`

## 5. Tradeoffs / POC limits

In-memory quotas reset on process restart — fine for POC, not for multi-instance prod.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

Narrated with **ElevenLabs Debpro voice** and Debpro still image (via [GitaProject](/Users/deb/Development/GenAI/GitaProject)):

- Video: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Script: [`video/narration.txt`](./video/narration.txt)

