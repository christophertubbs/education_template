#!/usr/bin/env bash
#
# run-prompt.sh
#
# Feed a prompt file into the first available supported AI coding CLI.
#
# Provider priority:
#   1. Codex
#   2. Claude Code
#   3. GitHub Copilot CLI
#   4. Cursor CLI
#
#

set -uo pipefail

readonly DEFAULT_PROMPT_FILE="prompt.md"

prompt_file="${DEFAULT_PROMPT_FILE}"
requested_provider=""

usage() {
    cat <<'EOF'
Usage:
    run-prompt.sh [-f FILE] [-c PROVIDER]
    run-prompt.sh [--file FILE] [--cli PROVIDER]

Options:
    -f, --file FILE
        Prompt file to submit.
        Default: prompt.sh

    -c, --cli PROVIDER
        Explicitly select a CLI.

        Supported values:
            codex
            claude
            copilot
            cursor

        If omitted, the first available CLI is selected in this order:
            codex -> claude -> copilot -> cursor

    -h, --help
        Show this help message.

Examples:
    ./run-prompt.sh

    ./run-prompt.sh -f prompt.md

    ./run-prompt.sh -c claude

    ./run-prompt.sh -c codex -f implementation-plan.md
EOF
}


error() {
    printf 'ERROR: %s\n' "$*" >&2
}


info() {
    #
    # Informational messages deliberately go to stderr so stdout remains
    # available for the selected AI CLI's output.
    printf '%s\n' "$*" >&2
}


command_exists() {
    # Arguments:
    #   $1 - executable name
    #
    # Returns:
    #   0 if the executable exists in PATH.
    #   1 otherwise.
    command -v "$1" >/dev/null 2>&1
}


prompt_is_effectively_empty() {
    # A file containing only whitespace is considered empty.
    #
    # Arguments:
    #   $1 - prompt file path
    #
    # Returns:
    #   0 if effectively empty.
    #   1 if meaningful content exists.
    local file="$1"

    if [[ ! -s "${file}" ]]; then
        return 0
    fi

    if grep -q '[^[:space:]]' "${file}"; then
        return 1
    fi

    return 0
}


resolve_cursor_command() {
    # Cursor has used both `agent` and `cursor-agent` as CLI executable
    # names. Prefer the current `agent` executable if present.
    if command_exists "agent"; then
        printf '%s\n' "agent"
        return 0
    fi

    if command_exists "cursor-agent"; then
        printf '%s\n' "cursor-agent"
        return 0
    fi

    return 1
}


provider_available() {
    # Arguments:
    #   $1 - provider name
    local provider="$1"

    case "${provider}" in
        codex)
            command_exists "codex"
            ;;
        claude)
            command_exists "claude"
            ;;
        copilot)
            command_exists "copilot"
            ;;
        cursor)
            resolve_cursor_command >/dev/null
            ;;
        *)
            return 1
            ;;
    esac
}


select_provider() {
    # Select an explicitly requested provider, or choose the first available
    # provider according to the configured preference order.

    if [[ -n "${requested_provider}" ]]; then
        if provider_available "${requested_provider}"; then
            printf '%s\n' "${requested_provider}"
            return 0
        fi

        error "The requested CLI '${requested_provider}' is not available."
        error "It was explicitly requested, so no fallback provider will be used."

        case "${requested_provider}" in
            codex)
                error "Expected to find executable: codex"
                ;;
            claude)
                error "Expected to find executable: claude"
                ;;
            copilot)
                error "Expected to find executable: copilot"
                ;;
            cursor)
                error "Expected to find either executable: agent or cursor-agent"
                ;;
            *)
              return 1
              ;;
        esac

        return 1
    fi

    local provider

    for provider in codex claude copilot cursor; do
        if provider_available "${provider}"; then
            printf '%s\n' "${provider}"
            return 0
        fi
    done

    error "No supported AI coding CLI was found in PATH."
    error ""
    error "Searched for the following providers, in order:"
    error "  1. codex"
    error "  2. claude"
    error "  3. copilot"
    error "  4. Cursor CLI via 'agent' or 'cursor-agent'"
    error ""
    error "Current PATH:"
    error "  ${PATH}"
    error ""
    error "Install or expose at least one supported CLI before running this script."

    return 1
}


run_codex() {
    #
    # `codex exec -` explicitly tells Codex to read the prompt from stdin.
    #
    # This avoids placing a potentially very large prompt into argv and lets
    # Codex retain its normal exec-mode stdout/stderr behavior.
    local file="$1"

    info "Using Codex CLI."

    codex exec - < "${file}"
}


run_claude() {
    #
    # Claude's print mode supports piped input. We deliberately do not capture
    # stdout so Claude can write directly to the caller's terminal or pipe.
    #
    # `--output-format text` produces human-readable output. Claude may buffer
    # portions of the response internally in print mode, so this does not
    # necessarily reproduce every interactive TUI progress update.
    local file="$1"

    info "Using Claude Code CLI."

    claude \
        --print \
        --output-format text \
        < "${file}"
}


run_copilot() {
    # GitHub Copilot CLI explicitly supports receiving a complete prompt from
    # stdin. Unlike `copilot -p`, this avoids argv size limits for large files.
    local file="$1"

    info "Using GitHub Copilot CLI."

    copilot < "${file}"
}


run_cursor() {
    # Cursor print mode supports scripting/headless operation. Cursor's CLI
    # executable has appeared as both `agent` and `cursor-agent`, so resolve
    # whichever one is available.
    #
    # Text output is selected instead of JSON/stream-json because this wrapper
    # is intended primarily for humans watching a terminal.
    local file="$1"
    local cursor_command

    if ! cursor_command="$(resolve_cursor_command)"; then
        error "Cursor was selected but neither 'agent' nor 'cursor-agent' exists."
        return 1
    fi

    info "Using Cursor CLI via '${cursor_command}'."

    "${cursor_command}" \
        --print \
        --output-format text \
        < "${file}"
}


run_provider() {
    # Arguments:
    #   $1 - provider name
    #   $2 - prompt file
    local provider="$1"
    local file="$2"

    case "${provider}" in
        codex)
            run_codex "${file}"
            ;;
        claude)
            run_claude "${file}"
            ;;
        copilot)
            run_copilot "${file}"
            ;;
        cursor)
            run_cursor "${file}"
            ;;
        *)
            error "Internal error: unsupported provider '${provider}'."
            return 1
            ;;
    esac
}


while (( $# > 0 )); do
    case "$1" in
        -f|--file)
            if (( $# < 2 )); then
                error "Option '$1' requires a file path."
                usage >&2
                exit 2
            fi

            prompt_file="$2"
            shift 2
            ;;

        -c|--cli)
            if (( $# < 2 )); then
                error "Option '$1' requires a provider name."
                usage >&2
                exit 2
            fi

            requested_provider="${2,,}"

            case "${requested_provider}" in
                codex|claude|copilot|cursor)
                    ;;
                *)
                    error "Unsupported CLI provider: '${requested_provider}'."
                    error "Valid values are: codex, claude, copilot, cursor."
                    exit 2
                    ;;
            esac

            shift 2
            ;;

        -h|--help)
            usage
            exit 0
            ;;

        *)
            error "Unknown argument: '$1'"
            usage >&2
            exit 2
            ;;
    esac
done


if [[ ! -e "${prompt_file}" ]]; then
    error "Prompt file does not exist: '${prompt_file}'"
    error "The default prompt file is '${DEFAULT_PROMPT_FILE}'."
    error "Specify another file with: -f FILE"
    exit 2
fi

if [[ ! -f "${prompt_file}" ]]; then
    error "Prompt path is not a regular file: '${prompt_file}'"
    exit 2
fi

if [[ ! -r "${prompt_file}" ]]; then
    error "Prompt file is not readable: '${prompt_file}'"
    exit 2
fi

#
# Silently exit successfully for an empty or whitespace-only prompt.
# There is nothing useful to submit and spinning up an AI agent to ponder
# whitespace would be an impressive new frontier in wasted compute.
#
if prompt_is_effectively_empty "${prompt_file}"; then
    exit 0
fi


if ! provider="$(select_provider)"; then
    exit 127
fi


if [[ -t 1 ]]; then
    info "Prompt: ${prompt_file}"
fi


if ! run_provider "${provider}" "${prompt_file}"; then
    status=$?

    error ""
    error "The '${provider}' CLI failed."
    error "Prompt file: '${prompt_file}'"
    error "Exit status: ${status}"
    error ""
    error "The wrapper does not suppress stderr from the underlying CLI."
    error "Any authentication, permission, network, model, or configuration"
    error "errors printed above came directly from '${provider}'."

    exit "${status}"
fi
