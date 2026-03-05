import pytest
import logging
from datetime import datetime
from utils.driver import create_driver


def pytest_configure(config):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


@pytest.fixture
def driver():
    driver = create_driver()
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def test_setup_teardown(request, driver):
    logger = logging.getLogger(request.node.name)
    request.node.logger = logger

    logger.info("===== TEST SETUP START =====")

    markers = [
        m.name + (f"={m.args[0]}" if m.args else "")
        for m in request.node.iter_markers()
    ]
    logger.info(f"Markers: {markers}")


    main_window = driver.current_window_handle

    yield

    logger.info("===== TEST TEARDOWN START =====")


    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"artifacts/{request.node.name}_{timestamp}.png"
        try:
            driver.save_screenshot(screenshot_name)
            logger.error(f"Test failed. Screenshot saved: {screenshot_name}")
        except Exception as e:
            logger.error(f"Could not capture screenshot: {e}")


    try:
        handles = driver.window_handles


        for h in handles:
            if h != main_window:
                driver.switch_to.window(h)
                driver.close()


        driver.switch_to.window(main_window)

        logger.info("Tab cleanup completed (extra tabs closed).")

    except Exception as e:
        logger.warning(f"Tab cleanup skipped/failed: {e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        item.rep_call = rep