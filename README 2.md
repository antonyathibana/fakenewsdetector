# Fake-News-Detector-School-Project
A reposatory holding the use of three data sets, used in conjunction with 3 models in an attempt to make fake news detector

How to use
First their is the library requirements
pandas, re, pytorch, transformers, tensorflow, sklearn, matplotlib, tqdm

Also, to run the Kaggle files (They are the ones without a tag like, Liar or News sample)
then you can either go here
https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset?select=True.csv
to get the real files or remove the words truncated from the true.csv and false.csv
Sorry for the difficulty, but the files where to gig for discord.

after that make sure that these files are in the same directory

The data folder has to be in the same folder as all the exactuables

fake_news_CNN.py and Fake_news_BiLSTM.py need to be in the same folder as shared_preprocessing.py
fake_news_text_CNN_lair.py and Fake_news_BiLSTM_liar.py need to be in the same folder as liar_preprocessing.py
fake_news_news_samples_CNN.py and Fake_news_BiLSTM_news_sample.py need to be in the same folder as shared_preprocessing_news_samples.py

After that, you should be able to just run the program through a code editor, or terminal

terminal instructions:
navigate to where it is in terminal that run the python command and the file name,

ex python file_name.py
