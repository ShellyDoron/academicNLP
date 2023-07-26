# academicNLP
a NLP project for similarity of academic researches

# How to run?
1. clone the repo to your computer using the command `git clone https://github.com/ShellyDoron/academicNLP.git`
2. create a `.env` file with the value of your `API_KEY` to `serpapi` API
   1. your file content should look like this:
      `API_KEY='put your key here'`
3. install requirements by running the command `pip install -r requirements.txt` form the code folder

# Get articles from Google Scholar 
1. create a `names.txt` file with your reviewers/professors names
   1. each name is in a new line.
2. run the command `python ./get_articles_form_google_scholar.py` from the code folder
3. you should see a printings that indicates that the code works.
4. if you see an error print like this `error on: some name` you can know that the code was not able to find at least 3 articles to this professor

# Create the score matrix
1. make sure that you have a submissions' folder name `submissions` with all your submissions
2. make sure that you have a reviewers' folder name `reviewers` with all your reviewers' folders with all the articles of the professors
3. run the command `python ./create_similarity_matrix.py`
   1. this code take some time to run, please wait
   2. at the end you should see printings of each submission name
   3. the score matrix is now in the file name `score_matix.json`

# Assign submissions to reviewers
1. make sure that you have a `score_matrix.json` file with the score of each reviewer to submission
2. the code now assign two reviewers to each submission and max 7 submission to each reviewer
   1. if you want to change this please change it in lines 22,23,27
   2. the number 7 is calculated to 192 submissions and 58 reviewers
      1. 192*2 / 58 = 6.6 so we selected 7
3. run the command `python assign_reviewers_to_submissions.py`
4. you should see some printings that indicates that the code works
5. now you have 3 new files:
   1. `assignments.json` with the assignments in a json format
   2. `assignments.csv` with the assignments in a csv format
   3. `number_of_assignments_to_reviewer.json` with the number of submissions to review for each reviewer

