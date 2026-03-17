-- QA Verification Queries
-- Run these against qa.db after seeding data to verify the API stored everything correctly.
-- Usage: sqlite3 qa.db < sql/verify.sql

-- How many test cases exist per suite?
SELECT ts.name AS suite, COUNT(tc.id) AS total_cases
FROM test_suites ts
LEFT JOIN test_cases tc ON tc.suite_id = ts.id
GROUP BY ts.id, ts.name;

-- List all failed test results with the test case title
SELECT tr.id, tc.title AS test_case, tr.status, tr.notes
FROM test_results tr
JOIN test_cases tc ON tc.id = tr.test_case_id
WHERE tr.status = 'failed';

-- Find all high or critical priority test cases
SELECT id, title, priority, severity, status
FROM test_cases
WHERE priority IN ('high', 'critical')
ORDER BY priority;

-- Check which test suites belong to a specific user (replace 1 with actual user id)
SELECT id, name, description
FROM test_suites
WHERE owner_id = 1;

-- Show all results for a specific test run, with status summary
SELECT tr.status, COUNT(*) AS count
FROM test_results tr
WHERE tr.run_id = 1
GROUP BY tr.status;

-- Verify a test result is correctly linked to its run and test case
SELECT
    tr.id        AS result_id,
    tr.status,
    run.name     AS run_name,
    tc.title     AS test_case_title
FROM test_results tr
JOIN test_runs run ON run.id = tr.run_id
JOIN test_cases tc  ON tc.id  = tr.test_case_id
WHERE tr.id = 1;

-- List all test runs and how many results each has
SELECT run.id, run.name, run.status, COUNT(tr.id) AS result_count
FROM test_runs run
LEFT JOIN test_results tr ON tr.run_id = run.id
GROUP BY run.id, run.name, run.status;
