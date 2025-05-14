_multipjson_completions()
{
    COMPREPLY=($(compgen -W "--help --fields --values --prefix --suffix -t --total -o --output" -- "${COMP_WORDS[1]}"))
}
complete -F _multipjson_completions multipjson
