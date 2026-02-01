# Deepfake Identity-Forge

**Category:** Social Engineering

## Technical Definition
High-level: Real-time synthesis of audio/video biometric evidence to bypass liveness checks and social engineering defenses. This description focuses on detection and mitigation rather than exploitation.

## Advanced TTPs (descriptive)
Real-time man-in-the-middle on video conferencing feeds to substitute a high-fidelity AI-generated avatar during verification calls; attackers aim to bypass human-based verification and liveness checks.

## 2026 Emerging Trends
- Generative models produce highly convincing biometric forgeries; defenders rely on multi-modal attestation, hardware-backed device attestation, and active challenge-response checks.

## The 'Unknown' Factor
Firmware-level compromise of camera or biometric sensors that report forged attestations to verification servers.

## Detection
Cross-verify biometric streams with device telemetry, watch for replay/timing artifacts, and correlate session metadata for inconsistencies.

## Mitigation
Adopt multi-factor, multi-modal verification (e.g., biometrics + device-bound attestations), implement liveness-challenges, and use hardware attestation where available.
