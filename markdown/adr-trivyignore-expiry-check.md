# ADR: Trivy Ignore Exception Expiry Check

## Status

Accepted.

## Context

The repository includes `.trivyignore.yaml` for temporary vulnerability exceptions.
Without an expiry policy, ignored CVEs can silently become permanent and hide real
security debt from CI/CD.

## Decision

Every Trivy ignore entry must include an `expired_at` date in `YYYY-MM-DD` format.
The CI/CD workflow runs `scripts/check-trivyignore-expiry.sh .trivyignore.yaml`
before image publishing.

The check fails when an exception:

- has no `expired_at` date;
- has an invalid date;
- is older than the current UTC date.

## Consequences

Security exceptions remain explicit, reviewable, and time-bound.

Maintainers must renew, remove, or remediate exceptions before they expire.
Renewal should only happen after confirming that no fixed package, safer base
image, or practical remediation is available.
