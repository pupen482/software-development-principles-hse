.PHONY: task_1 task_2 task_3 task_4 task_6 install venv

venv:
	python3 -m venv .venv

install: venv
	. .venv/bin/activate && pip3 install -r task3/requirements.txt

task_1: install
	. .venv/bin/activate && python3 task1/simple_calc.py

task_2: install
	. .venv/bin/activate && python3 task2/advanced_calc.py

task_3: install
	. .venv/bin/activate && python3 task3/main.py

task_4: install
	. .venv/bin/activate && python3 task4/main.py

task_6: install
	. .venv/bin/activate && python3 task6/garden.py

task_7_server: install
	. .venv/bin/activate && python3 task7/server.py

task_7_client: install
	. .venv/bin/activate && python3 task7/client.py 