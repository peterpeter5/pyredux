#! bin/bash
python3 -m venv PyEnv
./PyEnv/bin/pip install pyrsistent>=0.11.4 wheel
./PyEnv/bin/pip install -r requirements.test.txt
