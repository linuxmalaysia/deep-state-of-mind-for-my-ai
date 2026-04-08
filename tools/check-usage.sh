#!/bin/bash
# ==============================================================================
# 📜 Antigravity Token & Quota Monitor (v8.6 Bash Port)
#
# Description:
#   Real-time monitor for Gemini Pro / Antigravity conversation context files (.pb).
#   Shows size, estimated tokens, velocity, age, and status for each session.
#   Marks the most recently active session with [>>].
#
#   Token estimate: 1 MB ~ 62,500 tokens (4 chars/token avg, 1MB = 250k chars).
#
# DSOM For My AI Protocol v6.1 - Harisfazillah Jamel
# ==============================================================================

# Default parameters
LOOP=0
INTERVAL=60
THRESHOLD_MB=20
CRITICAL_MB=50
DORMANT_HOURS=4
TOP=0
NO_PULSE=0

VERSION="v8.6"
CONVERSATION_PATH="$HOME/.gemini/antigravity/conversations/"
TOKENS_PER_MB=62500

# ANSI Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
DARKGRAY='\033[1;30m'
GRAY='\033[0;37m'
WHITE='\033[1;37m'
DARKCYAN='\033[0;36m'
NC='\033[0m' # No Color

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -l|--loop) LOOP=1 ;;
        -i|--interval) INTERVAL="$2"; shift ;;
        -w|--threshold) THRESHOLD_MB="$2"; shift ;;
        -c|--critical) CRITICAL_MB="$2"; shift ;;
        -d|--dormant) DORMANT_HOURS="$2"; shift ;;
        -n|--top) TOP="$2"; shift ;;
        --no-pulse) NO_PULSE=1 ;;
        -h|--help)
            echo -e "\n  ${CYAN}[DSOM] check-usage.sh $VERSION  --  Antigravity Session Monitor${NC}"
            echo -e "  ${DARKGRAY}----------------------------------------------------------------------${NC}"
            echo -e "  ${WHITE}USAGE:${NC}"
            echo -e "    ./check-usage.sh  [options]\n"
            echo -e "  ${WHITE}OPTIONS:${NC}"
            echo -e "    -l, --loop              Live monitor mode (repeats every interval)"
            echo -e "    -i, --interval SECS     Refresh interval in seconds     [default: 60]"
            echo -e "    -w, --threshold MB      MB size to trigger WARNING       [default: 20]"
            echo -e "    -c, --critical MB       MB size to trigger LIMIT RISK    [default: 50]"
            echo -e "    -d, --dormant HOURS     Hours idle before DORMANT status [default: 4]"
            echo -e "    -n, --top N             Show only top N sessions         [default: all]"
            echo -e "    --no-pulse              Suppress countdown bar in loop mode"
            echo -e "    -h, --help              Show this help screen\n"
            exit 0
            ;;
        *)
            echo -e "\n  ${RED}[ERROR] Unknown parameter: $1${NC}"
            echo -e "\n  ${YELLOW}Did you mean one of these?${NC}"
            echo -e "    --loop (-l)"
            echo -e "    --interval (-i)"
            echo -e "    --threshold (-w)"
            echo -e "    --critical (-c)"
            echo -e "    --top (-n)"
            echo -e "    --help (-h)\n"
            exit 1
            ;;
    esac
    shift
done

declare -A PREVIOUS_STATE

get_age_label() {
    local age_sec=$1
    if (( age_sec < 60 )); then
        echo "just now"
    elif (( age_sec < 3600 )); then
        echo "$(( age_sec / 60 ))m ago"
    elif (( age_sec < 86400 )); then
        echo "$(( age_sec / 3600 ))h ago"
    elif (( age_sec < 604800 )); then
        echo "$(( age_sec / 86400 ))d ago"
    else
        echo "$(( age_sec / 604800 ))w ago"
    fi
}

show_monitor() {
    clear
    local now_str=$(date +"%Y-%m-%d %H:%M:%S")
    local now_ts=$(date +%s)
    
    echo -e "\n  ${CYAN}[DSOM Sovereign Monitor $VERSION]  $now_str${NC}"
    echo -e "  ${DARKGRAY}Path: $CONVERSATION_PATH${NC}"
    echo -e "  ${DARKGRAY}Thresholds: WARN=${THRESHOLD_MB}MB  CRIT=${CRITICAL_MB}MB  DORMANT=${DORMANT_HOURS}h${NC}\n"

    if [[ ! -d "$CONVERSATION_PATH" ]]; then
        echo -e "  ${RED}[ERROR] Path not found: $CONVERSATION_PATH${NC}"
        return
    fi
    
    # Check for files
    # shopt nullglob ensures empty array if no matches
    shopt -s nullglob
    local files=("$CONVERSATION_PATH"*.pb)
    shopt -u nullglob

    if [ ${#files[@]} -eq 0 ]; then
        echo -e "  ${YELLOW}No .pb conversation files found.${NC}"
        return
    fi
    
    # Gather data
    local -a rows
    local latest_id=""
    local latest_mtime=0
    
    # Using a temporary file to sort correctly
    local tmp_file=$(mktemp)
    
    for f in "${files[@]}"; do
        if [[ ! -f "$f" ]]; then continue; fi
        local baseid=$(basename "$f" .pb)
        local fsize=$(stat -c%s "$f")
        local mtime=$(stat -c%Y "$f")
        
        # update latest
        if (( mtime > latest_mtime )); then
            latest_mtime=$mtime
            latest_id="$baseid"
        fi
        
        # calculate sizes
        local size_mb=$(bc <<< "scale=2; $fsize / 1048576")
        
        local prev_size=${PREVIOUS_STATE[$baseid]:-$size_mb}
        local delta=$(bc <<< "scale=2; $size_mb - $prev_size")
        PREVIOUS_STATE[$baseid]=$size_mb
        
        local short_id="$baseid"
        if (( ${#baseid} >= 8 )); then
            short_id="${baseid:0:8}..."
        fi
        
        local age_sec=$(( now_ts - mtime ))
        local age_hours=$(bc <<< "scale=2; $age_sec / 3600")
        local age_label=$(get_age_label $age_sec)
        local last_str=$(date -d "@$mtime" +"%m-%d %H:%M")
        
        local tokens=$(bc <<< "scale=0; $size_mb * $TOKENS_PER_MB / 1")
        
        echo "$size_mb|$baseid|$short_id|$tokens|$age_label|$age_hours|$last_str|$delta" >> "$tmp_file"
    done
    
    local sep="--------------------------------------------------------------------------------------------------------------"
    echo -e "  ${DARKGRAY}$sep${NC}"
    printf "  ${GRAY}%-16s %10s %13s %11s %-10s %-16s %s${NC}\n" "Session" "Size(MB)" "Tokens(Est)" "Velocity" "Age" "Last Active" "Status"
    echo -e "  ${DARKGRAY}$sep${NC}"
    
    local total_mb=0
    local total_tokens=0
    local warn_count=0
    local crit_count=0
    local row_count=0
    
    # Read sorted by sizeMB descending
    while IFS='|' read -r size_mb baseid short_id tokens age_label age_hours last_str delta; do
        total_mb=$(bc <<< "scale=2; $total_mb + $size_mb")
        total_tokens=$(bc <<< "scale=0; $total_tokens + $tokens")
        
        local vel_str="         -"
        local delta_cmp=$(bc <<< "$delta > 0")
        local delta_lt0=$(bc <<< "$delta < 0")
        local delta_burst=$(bc <<< "$delta > 2.0")
        
        if (( delta_cmp == 1 )); then
            vel_str="+$(printf "%.2f" $delta) MB"
        elif (( delta_lt0 == 1 )); then
            vel_str="$(printf "%.2f" $delta) MB"
        fi
        vel_str=$(printf "%11s" "$vel_str")
        
        local marker="    "
        local is_current=0
        if [[ "$baseid" == "$latest_id" ]]; then
            marker="[>>]"
            is_current=1
        fi
        
        local status="[OK ] Nominal"
        local color=$GREEN
        
        local hr_cmp=$(bc <<< "$age_hours > $DORMANT_HOURS")
        local crit_cmp=$(bc <<< "$size_mb > $CRITICAL_MB")
        local warn_cmp=$(bc <<< "$size_mb > $THRESHOLD_MB")
        
        if (( delta_burst == 1 )); then
            status="[RPM] RISK - High Burst"
            color=$MAGENTA
            ((warn_count++))
        elif (( delta_cmp == 1 )); then
            status="[ACT] Active +$(printf "%.2f" $delta)MB"
            color=$CYAN
        elif (( crit_cmp == 1 )); then
            status="[CRT] LIMIT RISK - Pause"
            color=$RED
            ((crit_count++))
        elif (( warn_cmp == 1 )); then
            status="[WRN] Warning >${THRESHOLD_MB}MB"
            color=$YELLOW
            ((warn_count++))
        elif (( hr_cmp == 1 )) && (( is_current == 0 )); then
            status="[ZZZ] Dormant"
            color=$DARKGRAY
        fi
        
        local display_id="$marker $short_id"
        printf "  ${color}%-16s %10.2f %13.0f %s %-10s %-16s %s${NC}\n" "$display_id" "$size_mb" "$tokens" "$vel_str" "$age_label" "$last_str" "$status"
        
        ((row_count++))
        if (( TOP > 0 && row_count >= TOP )); then
            break
        fi
    done < <(sort -t'|' -k1,1nr "$tmp_file")
    
    rm -f "$tmp_file"
    
    # footer
    echo -e "  ${DARKGRAY}$sep${NC}"
    local total_files=${#files[@]}
    local shown_note=" ($row_count total)"
    if (( TOP > 0 && TOP < total_files )); then
        shown_note=" (top $TOP of $total_files)"
    fi
    
    echo -e "  ${DARKGRAY}Sessions$shown_note  |  Total: $(printf "%.2f" $total_mb) MB  |  Est Tokens: $(printf "%.0f" $total_tokens)  |  WARN: $warn_count  |  CRIT: $crit_count${NC}"
    echo -e "  ${DARKGRAY}Token basis: 1 MB ~ $(printf "%.0f" $TOKENS_PER_MB) tokens (4 chars/token avg)${NC}\n"

}

if (( LOOP == 1 )); then
    # trap ctrl-c
    trap 'echo -e "\n  ${GRAY}Monitor stopped.${NC}"; exit 0' INT
    while true; do
        show_monitor
        if (( NO_PULSE == 0 )); then
            echo -e "  ${DARKGRAY}--- Next refresh in ${INTERVAL}s (Ctrl+C to stop) ---${NC}"
            for (( i=$INTERVAL; i>0; i-- )); do
                filled=$(( (i * 20) / INTERVAL ))
                empty=$(( 20 - filled ))
                bar=$(printf "%0.s#" $(seq 1 $filled))$(printf "%0.s." $(seq 1 $empty))
                pct=$(( (i * 100) / INTERVAL ))
                printf "\r  ${DARKCYAN}[%s] %3d%%  %3ds remaining  ${NC}" "$bar" "$pct" "$i"
                sleep 1
            done
            printf "\r%55s\r" " "
        else
            sleep "$INTERVAL"
        fi
    done
else
    show_monitor
    echo -e "  ${DARKGRAY}Tip: run with --help (-h) for all options, or --loop (-l) to monitor live.${NC}\n"
fi
