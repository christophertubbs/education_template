#!/usr/bin/env bash

set -u

HOST="0.0.0.0"
PORT="8000"
CERT_PATH="${SERVER_CERT_PATH:-}"
KEY_PATH="${SERVER_KEY_PATH:-}"

usage() {
    cat <<'EOF'
Usage:
  ./launch.sh [OPTIONS]

Launch the Django application using the first available server:

  1. uvicorn
  2. gunicorn
  3. python manage.py runserver

Options:
  -h, --help
      Show this help message.

  --host HOST
      Address to bind to.
      Default: 0.0.0.0

  --port PORT
      Port to bind to.
      Default: 8000

  --cert PATH
      Path to the TLS certificate.
      Default: $SERVER_CERT_PATH

  --key PATH
      Path to the TLS private key.
      Default: $SERVER_KEY_PATH

TLS:
  TLS options are only used when both the certificate and private key
  exist and are readable.

Examples:
  ./launch.sh

  ./launch.sh --host 127.0.0.1 --port 8080

  ./launch.sh \
      --cert ~/.certs/server.pem \
      --key ~/.certs/server-key.pem

Environment:
  SERVER_CERT_PATH
      Default TLS certificate path.

  SERVER_KEY_PATH
      Default TLS private-key path.
EOF
}


error() {
    printf 'ERROR: %s\n' "$*" >&2
}


validate_port() {
    local port="$1"

    if ! [[ "${port}" =~ ^[0-9]+$ ]]
    then
        error "Port must be numeric: ${port}"
        return 1
    fi

    if (( port < 1 || port > 65535 ))
    then
        error "Port must be between 1 and 65535: ${port}"
        return 1
    fi
}


tls_available() {
    [[ -n "${CERT_PATH}" ]] &&
        [[ -n "${KEY_PATH}" ]] &&
        [[ -f "${CERT_PATH}" ]] &&
        [[ -r "${CERT_PATH}" ]] &&
        [[ -f "${KEY_PATH}" ]] &&
        [[ -r "${KEY_PATH}" ]]
}


while (( $# > 0 ))
do
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;

        --host)
            if (( $# < 2 ))
            then
                error "--host requires a value"
                exit 2
            fi

            HOST="$2"
            shift 2
            ;;

        --port)
            if (( $# < 2 ))
            then
                error "--port requires a value"
                exit 2
            fi

            PORT="$2"
            shift 2
            ;;

        --cert)
            if (( $# < 2 ))
            then
                error "--cert requires a value"
                exit 2
            fi

            CERT_PATH="$2"
            shift 2
            ;;

        --key)
            if (( $# < 2 ))
            then
                error "--key requires a value"
                exit 2
            fi

            KEY_PATH="$2"
            shift 2
            ;;

        *)
            error "Unknown option: $1"
            printf '\n' >&2
            usage >&2
            exit 2
            ;;
    esac
done


if ! validate_port "${PORT}"
then
    exit 2
fi


if command -v uvicorn >/dev/null 2>&1
then
    declare -a command_args=(
        uvicorn
        "standalone.asgi:application"
        --host "${HOST}"
        --port "${PORT}"
        --reload
    )

    if tls_available
    then
        command_args+=(
            --ssl-certfile "${CERT_PATH}"
            --ssl-keyfile "${KEY_PATH}"
        )
    fi

    exec "${command_args[@]}"
fi


if command -v gunicorn >/dev/null 2>&1
then
    declare -a command_args=(
        gunicorn
        "standalone.wsgi:application"
        --bind "${HOST}:${PORT}"
    )

    if tls_available
    then
        command_args+=(
            --certfile "${CERT_PATH}"
            --keyfile "${KEY_PATH}"
        )
    fi

    exec "${command_args[@]}"
fi


if [[ ! -f "manage.py" ]]
then
    error "manage.py was not found in the current directory"
    exit 1
fi

exec python manage.py runserver "${HOST}:${PORT}"
