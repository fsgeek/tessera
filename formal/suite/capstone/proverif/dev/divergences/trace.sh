#!/bin/bash
# usage: trace.sh file.out RESULTLINE  -- prints the goal and the process-trace steps (events, stage/env messages, front-end input)
f=$1; e=$2
s=$(awk -v e=$e 'NR<e && /^-- Query/ {l=NR} END{print l}' $f)
echo "=== $f query@$s result@$e"
awk -v s=$s -v e=$e 'NR>=s && NR<=e' $f | grep -v "rules inserted" \
 | grep -E "^(event |out\((stageCh|envMat|stdMat|standCore|sStageCh)|in\(c, \(framed|goal reachable|A trace has been found|RESULT)" \
 | cut -c1-${3:-900}
