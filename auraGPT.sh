#!/usr/bin/env bash
pip install  requests colorama
clear

C1="\e[38;5;33m"
C2="\e[38;5;39m"
C3="\e[38;5;45m"
C4="\e[38;5;51m"
RESET="\e[0m"
BOLD="\e[1m"


echo
echo -e "${BOLD}${C1}                          _____ _____ _______ ${RESET}"
echo -e "${BOLD}${C2}    /\                   / ____|  __ \__   __|${RESET}"
echo -e "${BOLD}${C3}   /  \  _   _ _ __ __ _| |  __| |__) | | |${RESET}"
echo -e "${BOLD}${C4}  / /\ \| | | | '__/ _\` | | |_ |  ___/  | |${RESET}"
echo -e "${BOLD}${C3} / ____ \ |_| | | | (_| | |__| | |      | |${RESET}"
echo -e "${BOLD}${C2}/_/    \_\__,_|_|  \__,_|\_____|_|      |_| ${RESET}"
echo

echo -e "${C1}ozodbekdev.uz | ${C2}@ozodbekdevv${RESET}"

python3 main.py
