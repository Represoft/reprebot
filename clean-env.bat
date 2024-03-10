:: execute this only if the env is activated
:: it will remove re-install the direct dependencies
:: to their latest versions and remove any non-used
:: dependency
@echo off
pip freeze > current-requirements.txt
pip uninstall -r current-requirements.txt -y
pip install -r direct-requirements.txt
del current-requirements.txt
pip freeze > requirements.txt
