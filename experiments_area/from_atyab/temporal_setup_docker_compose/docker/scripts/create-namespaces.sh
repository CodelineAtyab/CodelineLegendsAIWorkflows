#!/bin/sh
# Create the default namespace plus any comma/space separated extras.
# Existing namespaces are left alone, so this is safe to run on every start.
set -eu

TEMPORAL_ADDRESS="${TEMPORAL_ADDRESS:-temporal:7233}"
NAMESPACE_RETENTION="${NAMESPACE_RETENTION:-7d}"
DEFAULT_NAMESPACE="${DEFAULT_NAMESPACE:-default}"
EXTRA_NAMESPACES="${EXTRA_NAMESPACES:-}"
MAX_ATTEMPTS="${TEMPORAL_HEALTH_CHECK_MAX_ATTEMPTS:-60}"
SLEEP_SECONDS="${TEMPORAL_HEALTH_CHECK_SLEEP_SECONDS:-5}"

wait_for_server() {
  attempt=1
  while :; do
    if temporal operator cluster health --address "$TEMPORAL_ADDRESS" >/dev/null 2>&1; then
      echo "Temporal server is healthy."
      return 0
    fi
    if [ "$attempt" -ge "$MAX_ATTEMPTS" ]; then
      echo "ERROR: Temporal server not healthy after ${MAX_ATTEMPTS} attempts" >&2
      exit 1
    fi
    echo "Waiting for Temporal server (attempt ${attempt}/${MAX_ATTEMPTS})..."
    attempt=$((attempt + 1))
    sleep "$SLEEP_SECONDS"
  done
}

ensure_namespace() {
  ns="$1"
  [ -n "$ns" ] || return 0

  if temporal operator namespace describe -n "$ns" --address "$TEMPORAL_ADDRESS" >/dev/null 2>&1; then
    echo "Namespace '${ns}' already exists; leaving it unchanged."
    return 0
  fi

  attempt=1
  while :; do
    if temporal operator namespace create -n "$ns" \
        --retention "$NAMESPACE_RETENTION" \
        --address "$TEMPORAL_ADDRESS"; then
      echo "Namespace '${ns}' created with retention ${NAMESPACE_RETENTION}."
      return 0
    fi
    if [ "$attempt" -ge "$MAX_ATTEMPTS" ]; then
      echo "ERROR: failed to create namespace '${ns}'" >&2
      exit 1
    fi
    echo "Retrying namespace '${ns}' creation (attempt ${attempt}/${MAX_ATTEMPTS})..."
    attempt=$((attempt + 1))
    sleep "$SLEEP_SECONDS"
  done
}

wait_for_server
ensure_namespace "$DEFAULT_NAMESPACE"

# Split EXTRA_NAMESPACES on commas and whitespace.
for ns in $(printf '%s' "$EXTRA_NAMESPACES" | tr ',' ' '); do
  ensure_namespace "$ns"
done

echo "Namespace setup complete."
