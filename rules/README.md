# Rule index

Browse the current rules by ID, description, target, and impact. Follow a rule link for its rationale and evaluation criteria.

This index is generated from the rule files. After adding or editing a rule, run `python3 scripts/generate_rule_index.py` from the repository root and include the updated index in your PR.

| Rule | Description | Target | Impact |
| --- | --- | --- | --- |
| [LOG-001](./LOG-001.md) | Debug-level logs are not enabled in production environments for longer than 14 days. | Log | Important |
| [LOG-002](./LOG-002.md) | Log records have their `severityNumber` set. | Log | Important |
| [LOG-003](./LOG-003.md) | Log records do not contain sensitive data such as PII, financial identifiers, credentials, or health information. | Log | Critical |
| [MET-001](./MET-001.md) | Metric attributes have bound cardinality. | Metric | Important |
| [MET-002](./MET-002.md) | Metrics have useful metric units. | Metric | Important |
| [MET-003](./MET-003.md) | Metric names are consistently associated with the same metric unit. | Metric | Important |
| [MET-004](./MET-004.md) | Histogram metrics consistently use the same histogram buckets per metric name. | Metric | Normal |
| [MET-005](./MET-005.md) | Metric names do not contain the name of the metric unit. | Metric | Normal |
| [MET-006](./MET-006.md) | Metric names do not equal semantic convention attribute keys. | Metric | Important |
| [MET-008](./MET-008.md) | Metrics do not contain sensitive data such as PII, financial identifiers, credentials, or health information. | Metric | Critical |
| [RES-001](./RES-001.md) | `service.instance.id` is present. | Resource | Normal |
| [RES-002](./RES-002.md) | `service.instance.id` is unique across logical resources within a given `service.name`. | Resource | Important |
| [RES-003](./RES-003.md) | `k8s.pod.uid` is present in telemetry collected from applications running on a Kubernetes cluster, or from the control pane of the Kubernetes cluster itself. | Resource | Important |
| [RES-004](./RES-004.md) | Semantic conventions attributes are used at the right level. | Resource, Log, Span | Important |
| [RES-005](./RES-005.md) | `service.name` is present | Resource | Critical |
| [RES-006](./RES-006.md) | `service.criticality` uses a valid enum value | Resource | Normal |
| [RES-007](./RES-007.md) | `deployment.environment.name` is present | Resource | Important |
| [RES-010](./RES-010.md) | Resource attribute values do not contain sensitive data such as PII, financial identifiers, credentials, or health information. | Resource | Critical |
| [SDK-001](./SDK-001.md) | Dependencies (language and runtime) are supported by the SDK. | SDK | Low |
| [SPA-001](./SPA-001.md) | Traces contain a limited number of `INTERNAL` spans per service. | Span | Normal |
| [SPA-002](./SPA-002.md) | Traces do not contain orphan spans. | Span | Normal |
| [SPA-003](./SPA-003.md) | Span names have bound cardinality. | Span | Important |
| [SPA-004](./SPA-004.md) | Root spans are not `CLIENT` spans. | Span | Important |
| [SPA-005](./SPA-005.md) | Traces do not contain a high number of short duration spans. | Span | Important |
| [SPA-006](./SPA-006.md) | Spans do not contain sensitive data such as PII, financial identifiers, credentials, or health information. | Span | Critical |
