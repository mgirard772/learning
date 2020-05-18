from scripts import etl_example


def test_assignment(num_runs, num_users, num_updates):
    for _ in range(0, num_runs):
        updates = etl_example.generate_user_updates(num_users, num_updates)
        deduped_updates = etl_example.remove_outdated_duplicates(updates)
        etl_example.update_sqlite_user_without_fetching(deduped_updates)

    assert etl_example.compare_final_user_rows_without_fetching(etl_example.NEWEST_USER_DATA) is True
