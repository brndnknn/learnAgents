#!/bin/bash
# Mobile-friendly confirmation prompt with timeout fallback.
# Usage: ask.sh "question?" "what Claude is trying to do" "why"
# Exit codes: 0=yes, 1=no, 2=no response after both attempts

QUESTION="${1:-Proceed?}"
ACTION="${2:-}"
WHY="${3:-}"

echo ""
echo "┌─────────────────────────────────┐"
echo "│   CLAUDE NEEDS YOUR APPROVAL    │"
echo "└─────────────────────────────────┘"
echo ""
printf "  %s\n" "$QUESTION"
[ -n "$ACTION" ] && printf "  Doing: %s\n" "$ACTION"
[ -n "$WHY"    ] && printf "  Why:   %s\n" "$WHY"
echo ""
echo "  y = yes   n = no   (20s timeout)"
echo ""

read -t 20 -p "  > " response 2>/dev/null
TIMED_OUT=$?

if [ $TIMED_OUT -ne 0 ] || [ -z "$response" ]; then
    echo ""
    echo "  (no response — trying once more)"
    echo ""
    printf "  %s  [y/n, 20s]\n" "$QUESTION"
    echo ""
    read -t 20 -p "  > " response 2>/dev/null
    TIMED_OUT=$?

    if [ $TIMED_OUT -ne 0 ] || [ -z "$response" ]; then
        echo ""
        echo "┌─────────────────────────────────┐"
        echo "│   NO RESPONSE — TASK STOPPED    │"
        echo "└─────────────────────────────────┘"
        echo ""
        printf "  Question:  %s\n" "$QUESTION"
        printf "  Action:    %s\n" "$ACTION"
        printf "  Reason:    %s\n" "$WHY"
        echo ""
        echo "  Claude has stopped and taken no action."
        echo "  Reply here if you'd like to continue."
        echo ""
        exit 2
    fi
fi

case "${response,,}" in
    y|yes) exit 0 ;;
    n|no)  exit 1 ;;
    *)
        echo "  Unrecognised input — treating as No"
        exit 1
        ;;
esac
