import pytest
from src import etl_assignment

def test_assignment(num_runs, num_users, num_updates):
    for _ in range(0, num_runs):
        updates = etl_assignment.generate_user_updates(num_users, num_updates)
        deduped_updates = etl_assignment.remove_outdated_duplicates(updates)
        etl_assignment.update_sqlite_user_without_fetching(deduped_updates)

    assert etl_assignment.compare_final_user_rows_without_fetching(etl_assignment.NEWEST_USER_DATA) is True
