#!/bin/bash
_multipjson_completions()
{
    COMPREPLY=($(compgen -W "--number --fields --values --output --help" "${COMP_WORDS[1]}"))
}
complete -F _multipjson_completions multipjson
