#!/bin/zsh
# measure_propagation_halflife.sh — contradiction-census instrument, landed 2026-08-06
# Decay curve of a retired form through git history: carriers at sampled commits
# from the retirement commit to HEAD, split internal-live vs public-site.
# First instance: '⊙ = • × ○' (retired ill-typed 2026-08-01, commit 1c270dbd;
# site sweep 2828be05 took public display count 476 -> 0).
#
# Provenance: written by the L1 propagation agent 2026-08-06 (unbound-variable
# bug at the HEAD-index line fixed at landing: revs has indices 0..n-1, and
# step must be >= 1). The verdict it established: 725 carriers at retirement;
# every reduction since was a dedicated repair wave — the spontaneous
# propagation half-life is effectively infinite; decay required two waves and
# a sweep. Re-run recomputes; do not re-quote the figure without re-running.
#
# READ-ONLY: git grep over commit objects only. No checkouts, no edits.
# Run: zsh measure_propagation_halflife.sh   (cwd = 01_EMERGENTISM repo root)
set -u
FORM=${1:-'⊙ = • × ○'}
RETIRE=${2:-1c270dbd}
SWEEP=${3:-2828be05}

count_at() { # $1=commit  -> prints: total internal_live public_site
  local c=$1
  local files
  files=$(git grep -l "$FORM" "$c" -- '*.md' '*.html' 2>/dev/null | sed "s/^$c://")
  local total internal public
  total=$(printf '%s\n' "$files" | grep -c . || true)
  public=$(printf '%s\n' "$files" | grep -c '^12_PUBLIC_SITE/' || true)
  internal=$(printf '%s\n' "$files" | grep -v '90_ARCHIVE\|91_COMPATIBILITY\|^12_PUBLIC_SITE/' | grep -c . || true)
  echo "$total $internal $public"
}

echo "form: $FORM"
echo "commit     date                    total internal_live public_site"
# t-1 baseline (parent of retirement) and t0 (retirement commit)
for c in ${RETIRE}~1 $RETIRE; do
  d=$(git show -s --date=iso --pretty='%ad' $c | cut -c1-19)
  read t i p <<< "$(count_at $c)"
  echo "$c $d  $t  $i  $p"
done
# ~12 evenly spaced commits between retirement and HEAD, sweep forced in
revs=($(git rev-list --reverse ${RETIRE}..HEAD))
n=${#revs[@]}
step=$(( n / 12 ))
(( step < 1 )) && step=1
sample=()
for ((k=step; k<n; k+=step)); do sample+=(${revs[$k]}); done
sample+=($SWEEP ${revs[$((n-1))]})   # sweep + HEAD (dedupe below)
typeset -U sample
for c in $sample; do
  d=$(git show -s --date=iso --pretty='%ad' $c | cut -c1-19)
  read t i p <<< "$(count_at $c)"
  echo "$c $d  $t  $i  $p"
done
