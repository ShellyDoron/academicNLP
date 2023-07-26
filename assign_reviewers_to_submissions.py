import json
import csv

from ortools.linear_solver import pywraplp


def assign_reviewers(submissions, reviewers, score_matrix):

    solver = pywraplp.Solver.CreateSolver('CBC')

    num_reviewers = len(reviewers)
    num_submissions = len(submissions)

    # Variables
    x = {}
    for i in range(num_reviewers):
        for j in range(num_submissions):
            x[i, j] = solver.IntVar(0, 1, '')

    # Constraints for each worker
    for i in range(num_reviewers):
        solver.Add(solver.Sum([x[i, j] for j in range(num_submissions)]) <= 7)
        solver.Add(solver.Sum([x[i, j] for j in range(num_submissions)]) >= 2)

    # Constraints for each task
    for j in range(num_submissions):
        solver.Add(solver.Sum([x[i, j] for i in range(num_reviewers)]) == 2)

    # Objective
    objective_terms = []
    for i in range(num_reviewers):
        for j in range(num_submissions):
            objective_terms.append(score_matrix[j][i] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Solve the system.
    status = solver.Solve()
    assignments = {}

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        for i in range(num_reviewers):
            for j in range(num_submissions):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if submissions[j] not in assignments:
                    assignments[submissions[j]] = []
                if x[i, j].solution_value() > 0.5:
                    assignments[submissions[j]].append(reviewers[i])
    return assignments


score_matrix = []

with open('./score_matrix.json', 'r') as result:
    result_json = json.loads(result.read())
    submissions = list(result_json.keys())
    reviewers = list(result_json[submissions[0]].keys())
    i = 0
    for submission in submissions:
        score_matrix.append([])
        for reviewer_score in result_json[submission].values():
            score_matrix[i].append(-reviewer_score)
        i += 1

assignments = assign_reviewers(submissions, reviewers, score_matrix)


assigned_reviewers_len = {}

for submission, assigned_reviewers in assignments.items():
    print(f"{submission} is assigned to {', '.join(assigned_reviewers)}")
    for reviewer in assigned_reviewers:
        if reviewer not in assigned_reviewers_len:
            assigned_reviewers_len[reviewer] = 0
        assigned_reviewers_len[reviewer] += 1

with open('./assignments.json', 'w') as assignments_file:
    assignments_file.write(json.dumps(assignments))


with open('./number_of_assignments_to_reviewer.json', 'w') as num_assignments_file:
    num_assignments_file.write(json.dumps(assigned_reviewers_len))

# Prepare data for CSV
csv_data = []
for key, values in assignments.items():
    csv_data.append([key] + values)

# Write data to CSV
with open('assignments.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Paper Name", "Reviewer #1", "Reviewer #2"])  # Write header
    writer.writerows(csv_data)  # Write data
