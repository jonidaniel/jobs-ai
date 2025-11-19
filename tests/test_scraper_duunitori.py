# ---------- DUUNITORI SCRAPER TEST ----------

import pytest

from unittest.mock import patch, MagicMock
from utils.scraper_duunitori import (
    fetch_search_results,
    parse_job_card,
    slugify_query
)
from bs4 import BeautifulSoup


# ------------------------------------------------------------
# Helpers for mock responses
# ------------------------------------------------------------

class MockResponse:
    def __init__(self, text="", status=200):
        self.text = text
        self.status_code = status


def load_fixture(path):
    """Load HTML fixture as text."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------
# Slugify Tests
# ------------------------------------------------------------

def test_slugify_query_basic():
    assert slugify_query("python developer") == "python-developer"


def test_slugify_query_special_chars():
    assert slugify_query("C++ developer") == "c%2B%2B-developer"


# ------------------------------------------------------------
# parse_job_card Tests
# ------------------------------------------------------------

def test_parse_job_card_basic():
    html = """
    <div class="job-box">
        <h3 class="job-box__title">
            <a href="/tyopaikat/123">Junior AI Engineer</a>
        </h3>
        <div class="job-box__employer">ACME Corp</div>
        <div class="job-box__location">Helsinki</div>
        <time datetime="2025-02-10"></time>
        <div class="job-box__teaser">We are looking for...</div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    card = soup.select_one(".job-box")

    job = parse_job_card(card)

    assert job["title"] == "Junior AI Engineer"
    assert job["company"] == "ACME Corp"
    assert job["location"] == "Helsinki"
    assert job["url"].endswith("/tyopaikat/123")
    assert job["published_date"] == "2025-02-10"
    assert "We are looking" in job["description_snippet"]


# ------------------------------------------------------------
# fetch_search_results Tests (with HTTP mocking)
# ------------------------------------------------------------

@pytest.fixture
def mock_duunitori_page(tmp_path):
    """HTML for one search page with one job card."""
    path = tmp_path / "duunitori_page.html"
    path.write_text(
        """
        <div class="job-box">
            <h3 class="job-box__title">
                <a href="/tyopaikat/abc">Python Developer</a>
            </h3>
            <div class="job-box__employer">Tech Oy</div>
            <div class="job-box__location">Espoo</div>
            <time datetime="2025-01-01"></time>
            <div class="job-box__teaser">Join our Python team...</div>
        </div>
        """,
        encoding="utf-8",
    )
    return str(path)


@pytest.fixture
def mock_duunitori_detail(tmp_path):
    """HTML for job detail page."""
    path = tmp_path / "duunitori_detail.html"
    path.write_text(
        """
        <div class="job-body">
            Full job description goes here. Lots of details.
        </div>
        """,
        encoding="utf-8",
    )
    return str(path)


@pytest.fixture
def mock_empty_page(tmp_path):
    """HTML page for pagination stop (no job cards)."""
    path = tmp_path / "duunitori_empty.html"
    path.write_text("<div>No results</div>", encoding="utf-8")
    return str(path)


@patch("utils.scraper_duunitori.safe_get")
def test_fetch_search_results_single_page(mock_safe_get, mock_duunitori_page, mock_duunitori_detail):
    """Test that one page of results is parsed correctly."""
    
    # Order of responses:
    # 1. search page
    # 2. detail page
    mock_safe_get.side_effect = [
        MockResponse(text=load_fixture(mock_duunitori_page)),   # Page 1 search
        MockResponse(text=load_fixture(mock_duunitori_detail)), # Detail
        MockResponse(text="")                                   # Page 2 empty
    ]

    results = fetch_search_results("python developer", max_pages=2, deep=True)

    assert len(results) == 1
    job = results[0]

    assert job["title"] == "Python Developer"
    assert job["company"] == "Tech Oy"
    assert job["location"] == "Espoo"
    assert "Lots of details" in job["full_description"]


@patch("utils.scraper_duunitori.safe_get")
def test_fetch_search_results_pagination_stops(mock_safe_get, mock_duunitori_page, mock_empty_page):
    """Pagination should stop when no job cards are found."""

    mock_safe_get.side_effect = [
        MockResponse(text=load_fixture(mock_duunitori_page)),  # Page 1
        MockResponse(text=load_fixture(mock_empty_page))       # Page 2 → stop
    ]

    results = fetch_search_results("python developer", max_pages=10, deep=False)

    assert len(results) == 1  # Only first page has jobs


@patch("utils.scraper_duunitori.safe_get")
def test_fetch_search_results_handles_non_200(mock_safe_get):
    """Non-200 status should stop scraping gracefully."""

    mock_safe_get.return_value = MockResponse(text="", status=500)

    results = fetch_search_results("java", max_pages=5, deep=False)
    assert results == []


@patch("utils.scraper_duunitori.fetch_job_detail")
@patch("utils.scraper_duunitori.safe_get")
def test_fetch_search_results_light_mode(mock_safe_get, mock_detail, mock_duunitori_page):
    """Light mode should not request job detail pages."""

    mock_safe_get.side_effect = [
        MockResponse(text=load_fixture(mock_duunitori_page)),  # Page 1
        MockResponse(text="")                                  # Page 2 empty
    ]

    # If light-mode works, detail fetch should NEVER be called
    results = fetch_search_results("python", deep=False, max_pages=2)

    mock_detail.assert_not_called()
    assert len(results) == 1
    assert results[0]["full_description"] == ""
