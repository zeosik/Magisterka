# Magisterka

Całość podzielona jest na 3 moduły:
* edytor (pilk runeditor.py)
* symulator (pilk runsimulator.py)
* analizator (pilk runanalyzer.py)

Aby uruchomić moduł z terminala należy wpisać:
* python3 (nazwa pliku)

Symulator i analizator wymagaja dodatkowych parametrów które wyświetlą się po użyciu paramatru -h

Projekt należy uruchamiać z pythonem w wersji 3!

## Edytor

Aby uruchomić edytor potrzebujemy biblioteki graph-tool, jej instalacja jest skomplikowana (instrukcja dla Ubuntu):
* instalujemy Ansible http://docs.ansible.com/ansible/intro_installation.html
* $ sudo apt-get install software-properties-common
* $ sudo apt-add-repository ppa:ansible/ansible
* $ sudo apt-get update
* $ sudo apt-get install ansible
* klonujemy repo https://github.com/nlap/ansible-role-graph-tool
* ansible-playbook -i tests/inventory tests/test.yml --syntax-check //(moze być konieczne uruchomienie z sudo)
* ansible-playbook -i tests/inventory tests/test.yml --connection=local --sudo -vvvv //(moze być konieczne uruchomienie z sudo)

Oczekiwany efekt: https://travis-ci.org/nlap/ansible-role-graph-tool

Uruchomienie edytora na systemach operacyjnych innych niż Ubuntu jest teoretyczne możliwe, po udanej instalacji biblioteki graph-tool

## Symulator

Aby uruchomić symulator potrzebujesz modułu dill:
* python3 -m pip install dill

## Analizator

Aby uruchomić analizator potrzebujesz modułu dill:
* python3 -m pip install dill