# Shadow-SaaS Exfiltration

**Category:** Exfiltration

## Technical Definition
High-level: Abuse of long-lived OAuth tokens or forgotten third-party integrations to move sensitive data through legitimate API flows (defensive summary only).

## Advanced TTPs (descriptive)
Chaining compromised SaaS app tokens across services to pivot and exfiltrate data via authorized API calls while minimizing network anomalies.

## 2026 Emerging Trends
- Centralized token inventories, short-lived tokens, and fine-grained OAuth scopes to reduce risk.

## The 'Unknown' Factor
Speculative: token-delegation chains that cross organizational boundaries enabling stealthy data aggregation.

## Detection
Track anomalous API requests and unusual cross-service access patterns; maintain an integration inventory.

## Mitigation
Rotate tokens, enforce least-privilege scopes, and routinely revoke unused third-party app tokens.
