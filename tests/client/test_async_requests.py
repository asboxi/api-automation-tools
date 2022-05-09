import os
import time

import pytest

from apiautomationtools.client.async_requests import AsyncRequests

pytestmark = pytest.mark.client

root_dir = os.path.dirname(__file__) + "/async_requests"
headers = {}
url = "https://httpbin.org/get"


def test_request(batch=None, delay=0, report=True):
    pytest.async_requests = AsyncRequests(root_dir=root_dir)
    batch = batch or {"method": "get", "headers": headers, "url": url}
    response = pytest.async_requests.request(batch, delay=delay, report=report)

    assert response.get("duration")

    responses = response.get("responses")
    assert responses

    response_fields = [
        "description",
        "code_mismatch",
        "batch_number",
        "index",
        "method",
        "expected_code",
        "actual_code",
        "json",
        "url",
        "server_headers",
        "response_seconds",
        "delay_seconds",
        "utc_time",
        "headers",
    ]
    for field in response_fields:
        assert responses[0].get(field, "missing") != "missing"

    assert responses[0].get("actual_code") == "200"
    assert responses[0].get("json")

    pytest.async_requests.logging.delete_run_info(root_dir)
    path = pytest.async_requests.logging.log_file_path
    assert not os.path.exists(path)


def test_request_multiple():
    batch = [
        {"method": "get", "headers": headers, "url": url},
        {"method": "get", "headers": headers, "url": url},
    ]
    test_request(batch)


def test_request_delay():
    start = time.perf_counter()
    test_request(delay=2)
    stop = time.perf_counter() - start
    assert stop >= 2


def test_request_report():
    test_request(report=False)
    assert not os.path.exists(pytest.async_requests.csv_path)