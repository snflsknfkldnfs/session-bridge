#!/usr/bin/env bash
# tools/find_shared_path.sh — v0.1.4 NEU (PB-011)
# Sucht groessten gemeinsamen mountbaren Pfad zwischen zwei Cowork-Sessions
# fuer bridge-init --shared-path-Default-Heuristik.
#
# Usage:
#   find_shared_path.sh <session-id-1> <session-id-2>
#   find_shared_path.sh --interactive  # Listet aktive Sessions + User-Question

set -e

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <session-id-1> <session-id-2>"
    echo "       $0 --interactive"
    exit 2
fi

if [ "$1" = "--interactive" ]; then
    echo "Interactive mode: list active sessions via session_info MCP."
    echo "(NOTE: dieses Helper-Tool kann nicht selbst session_info aufrufen — User muss IDs uebergeben.)"
    exit 0
fi

SESSION_1="$1"
SESSION_2="$2"

# Heuristik: groesster gemeinsamer Praefix der Working-Dirs
# (Working-Dirs sind via Cowork-Project-Setup bekannt, nicht via session_info)
# Fallback: User-Question

# Stub: in v0.1.4 ist dies Doku-Pattern, nicht voll implementiert.
# Voll-Implementation in v0.1.5 wenn session_info MCP-Pfad-Auslese-API stabil ist.

echo "Heuristik:"
echo "1. Wenn beide Sessions gleichen Cowork-Project-Working-Dir nutzen: dieser Working-Dir ist shared-path-Kandidat"
echo "2. Sonst: User muss --shared-path explizit setzen (siehe bridge-init.md Argument-Resolution-Protokoll)"
echo ""
echo "Stub-Output (v0.1.4 Doku-Pattern):"
echo "session_1=$SESSION_1"
echo "session_2=$SESSION_2"
echo "shared_path_candidate=USER-MUST-PROVIDE"
