import json

from scipy.optimize import linear_sum_assignment
import numpy as np


def assign_reviewers(submissions, reviewers, score_matrix):
    assert len(submissions) == score_matrix.shape[0]
    assert len(reviewers) == score_matrix.shape[1]

    negative_score_matrix = -score_matrix

    assignments = {}
    # Calculate the number of times each reviewer needs to be cloned.
    # This is twice the number of submissions divided by the number of reviewers, rounded up.
    num_clones = -(-2 * score_matrix.shape[0] // score_matrix.shape[
        1])  # equivalent to ceil(2*n_submissions/n_reviewers)

    # Clone the reviewers to create a new cost matrix
    cost_matrix = np.repeat(negative_score_matrix, num_clones, axis=1)

    # Get the first and second optimal assignments using linear_sum_assignment
    row_ind1, col_ind1 = linear_sum_assignment(cost_matrix)
    for r, c in zip(row_ind1, col_ind1):
        cost_matrix[r, c] = np.inf
    row_ind2, col_ind2 = linear_sum_assignment(cost_matrix)

    for r1, c1, r2, c2 in zip(row_ind1, col_ind1, row_ind2, col_ind2):
        assignments[submissions[r1]] = [reviewers[c1 % negative_score_matrix.shape[1]],
                                        reviewers[c2 % negative_score_matrix.shape[1]]]

    return assignments


score_matrix = None
array = []

with open('./score_matrix.json', 'r') as result:
    result_json = json.loads(result.read())
    submissions = list(result_json.keys())
    reviewers = list(result_json[submissions[0]].keys())
    i = 0
    for submission in submissions:
        array.append([])
        for reviewer_score in result_json[submission].values():
            array[i].append(reviewer_score)
        i += 1
score_matrix = np.array(array)

assignments = assign_reviewers(submissions, reviewers, score_matrix)

assigned_reviewers_len = {}
for submission, assigned_reviewers in assignments.items():
    print(f"{submission} is assigned to {', '.join(assigned_reviewers)}")
    for reviewer in assigned_reviewers:
        if reviewer not in assigned_reviewers_len:
            assigned_reviewers_len[reviewer] = 0
        assigned_reviewers_len[reviewer] += 1

with open('./assignments_new.json', 'w') as assignments_file:
    assignments_file.write(json.dumps(assignments))


with open('./number_of_assignments_to_reviewer_new.json', 'w') as num_assignments_file:
    num_assignments_file.write(json.dumps(assigned_reviewers_len))