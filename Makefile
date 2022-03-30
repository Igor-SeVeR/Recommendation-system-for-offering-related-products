add_user:
	python server/users_operations_db.py $(USER_NAME) $(PASSWORD) $(FULL_NAME) $(EMAIL)

del_user:
	python server/users_operations_db.py $(USER_NAME) delete_user

devel:
	@if ! which pipenv &> /dev/null; then \
		pip install -U pipenv; \
	fi
	pipenv install -d

kill:
	fuser -k 8090/tcp

load_after_parallel_train:
	python server/load_after_parallel_train.py

run:
	python server/server_launcher.py

run-prod:
	nohup python server/server_launcher.py > log.txt &

train:
	python server/train_recommendation_system.py $(PATH_TO_DATA) False

train_parallel:
	python server/train_recommendation_system.py $(PATH_TO_DATA) True
