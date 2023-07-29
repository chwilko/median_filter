fill() {
    local text="$1"
    local fill_char="$2"
    local columns=$(tput cols)
    local stars=$(( (columns - ${#text}) / 2  - 1))
    printf '%.s*' $(seq 1 $stars) 
    printf " "
    printf $text
    printf " "
    printf '%.s*' $(seq 1 $stars)
    printf "\n"
}


fill "BLACK" "*"
poetry run black .
fill "ISORT" "*"
poetry run isort .
fill "MYPY" "*"
poetry run mypy .
fill "FLAKE8" "*"
poetry run flake8 .
fill "PYLINT" "*"
poetry run pylint median_filter
poetry run pylint tests
