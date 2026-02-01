# Agentic AI Hijacking

**Category:** Initial Access

## Technical Definition
High-level: Subverting autonomous AI agents by manipulating prompts or upstream integrations so the agent performs unauthorized data access or actions. This description is intentionally non-actionable and focused on defensive understanding.

## Advanced TTPs (descriptive)
Indirect prompt manipulation via compromised third-party integrations; attackers gain a foothold by introducing crafted inputs or policy overrides that coax agents into performing sensitive operations. Focus remains on stealth, exfiltration via legitimate agent capabilities, and minimal detectable side effects.

## 2026 Emerging Trends
- Increased use of AI orchestration platforms introduces an attack surface at the policy layer.
- Defensive controls include strict payload validation, allowlists for agent actions, and robust telemetry on agent task execution.

## The 'Unknown' Factor
Supply-chain poisoning of agent orchestration policies or weights—subtle corruptions that lead to long-duration, stealthy data leakage.

## Detection
Monitor agent API calls for anomalous endpoints or task sequences; log and review integration events and unexpected outbound destinations.

## Mitigation
Enforce least-privilege for agent tokens, restrict integrations, validate inputs, and perform regular policy audits and canary tests.
