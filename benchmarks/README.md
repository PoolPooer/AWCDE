# Experimental evidence

The active plan is [EXP-001](experiments/EXP-001-load-response/protocol.md). No benchmark results are included.

Store local raw evidence under `benchmarks/runs/<run-id>/` with metadata, commands, logs and artifact hashes. Keep derived analysis separate and record its version. This directory is ignored by Git by default. Publish selected sanitized evidence deliberately with a manifest or a durable artifact location; do not commit credentials or private prompt content. Git ignores are not a security boundary.

The July RW-001 configuration is archived. Its single-concurrency configuration is insufficient to test the current offered-load question, and its referenced prompt.txt was absent from the upload.
