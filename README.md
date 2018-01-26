# Text Classification and Real-World Problems

## Code examples and presentation slides from Machine Learning ID #2 Meetup - Yogyakarta

---
Training:
1. Extract dataset directory `(dataset/bbc-fulltext.zip)`. The directory should be named `bbc`.
2. Run `compile.py` in the `/dataset` directory from your terminal to compile the text files into single dataset file.

    `$ cd dataset`

    `$ python compile.py`

3. Run `engine.py`.

    `$ python engine.py`

4. If there is no pickle files, the system will automatically train the dataset and generate pickle files. This could take some time depends on your hardware.
5. If you want to retrain your system simply delete the `pickles` directory.

---

Classification:
1. Run the `app.py` file.

    `$ python app.py`

2. Using Postman (or similar tools), send `POST` request to `http://127.0.0.1:5050/classify` with these form data:

    `post : your_article`

---
### Dataset: BBC Dataset - http://mlg.ucd.ie/datasets/bbc.html