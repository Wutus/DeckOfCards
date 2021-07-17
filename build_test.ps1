python -m pip uninstall deck-of-cards-api -y
python -m build
python -m pip install .\dist\deck_of_cards_api-0.0.1-py3-none-any.whl
python .\test.py