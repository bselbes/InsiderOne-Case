import pytest
from pages.HomePage import HomePage
from pages.JobsPage import JobsPage

@pytest.mark.owner("Berkay Selbes")
@pytest.mark.case_id("InsiderOneCase")

def test_insider_qa_assessment(driver, request):

    log = request.node.logger

    EXPECTED_DEPARTMENT = "Quality Assurance"
    LOCATION_OPTION_TEXT = "Istanbul, Turkiye"
    EXPECTED_LOCATION = "Istanbul, Turkiye"

    log.info("STEP 1: Open Insider home page")

    home = HomePage(driver)
    home.load()

    log.info("STEP 2: Verify that the Home page loads successfully")

    assert "insiderone.com" in home.get_current_url().lower()
    assert home.is_body_visible()
    assert home.is_header_visible()
    assert home.is_footer_visible()

    log.info("STEP 2: Go to QA careers page")

    jobs = JobsPage(driver)
    jobs.load()

    log.info("STEP 3: Click See all QA jobs")

    jobs.click_see_all_jobs()

    log.info("STEP 4: Verify that Department filter is preselected as Quality Assurance")

    jobs.wait_until_department_selected(EXPECTED_DEPARTMENT)
    dept_selected = jobs.get_selected_department()
    assert EXPECTED_DEPARTMENT in dept_selected, (
        f"Department is not preselected. Selected option: {dept_selected}"
    )

    log.info("STEP 5: Wait job cards visible")

    jobs.wait_until_job_cards_visible()
    assert len(jobs.get_jobs()) > 0, "Jobs did not load"

    log.info("STEP 6: Filter jobs by Location: Istanbul, Turkiye and Validation")

    jobs.select_location(LOCATION_OPTION_TEXT, EXPECTED_LOCATION)
    assert len(jobs.get_jobs()) > 0, "Jobs list is empty after filtering"

    log.info("STEP 7: Validate job cards")

    job_details = jobs.get_job_details()
    for i, job in enumerate(job_details, start=1):
        position = job["position"]
        department = job["department"]
        location = job["location"]

        assert (EXPECTED_DEPARTMENT in position) or ("QA" in position), (
            f"[{i}] Position mismatch: {position}"
        )

        assert EXPECTED_DEPARTMENT in department, (
            f"[{i}] Department mismatch: {department}"
        )

        assert EXPECTED_LOCATION in location, (
            f"[{i}] Location mismatch: {location}"
        )

    log.info("STEP 8: Click View Role on the first job listing")

    jobs.open_first_job()
    jobs.switch_to_lever_page()

    log.info("STEP 9: Verify redirection to the Lever application page")

    assert "lever.co" in jobs.get_current_url().lower(), "Did not redirect to Lever"

    log.info("STEP 10: Validate Lever Page Details")

    details = jobs.get_lever_job_details()
    assert "QA" in details["title"], f"Title mismatch: {details['title']}"

    assert EXPECTED_LOCATION in details["location"], \
        f"Location mismatch: {details['location']}"

    assert EXPECTED_DEPARTMENT in details["department"], \
        f"Department mismatch: {details['department']}"