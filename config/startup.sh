#!/bin/bash

echo "Hello isolated World !"
# instaling jupyter if not exist 
pip install jupyter

# start jupyter
jupyter lab ~ --ip=0.0.0.0 --port=8888 --no-browser --allow-root &