#!/usr/bin/env bash
# Append a local activity record when this helper is explicitly invoked.
# No hook or scheduler is installed by this repository. Call it manually:
# bash hooks/log-run.sh "linkedin" "workflows launch" "review-complete"
# A recorded status is self-reported; this helper does not review or publish content.

CHANNEL="${1:-unknown}"; TOPIC="${2:-untitled}"; STATUS="${3:-draft}"
LOG="$(dirname "$0")/../activity-log.md"
[ -f "$LOG" ] || printf "# Activity Log\n\n> Local records appended by an operator or an explicitly configured workflow. Review for private content before sharing.\n\n| Date | Channel | Topic | Status |\n|---|---|---|---|\n" > "$LOG"
printf "| %s | %s | %s | %s |\n" "$(date +%F)" "$CHANNEL" "$TOPIC" "$STATUS" >> "$LOG"
echo "logged: $CHANNEL · $TOPIC · $STATUS"
