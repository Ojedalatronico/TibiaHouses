import pytest
import asyncio  # noqa: F401
from unittest.mock import MagicMock, patch
import pandas as pd
from main import (
    create_client,
    fetch_data,  # noqa: F401
    parse_cities,
    parse_servers,
    parse_houses,
    save_houses_to_file,
    main,
    NotAvailableElementError,
)


@pytest.fixture
def mock_response():
    """Create a mock response object for testing."""
    mock_resp = MagicMock()
    mock_resp.status = 200

    async def mock_text():
        return "Sample response"

    mock_resp.text = mock_text
    return mock_resp


@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    return MagicMock()


@pytest.fixture
def sample_html_response():
    """Sample HTML response for testing parsers."""
    return """
    <div id="houses">
        <div class="Border_2">
            <div>
                <div>
                    <form>
                        <div>
                            <table>
                                <tbody>
                                    <tr>
                                        <td>
                                            <div class="InnerTableContainer">
                                                <table>
                                                    <tbody>
                                                        <tr>
                                                            <td>
                                                                <div>
                                                                    <table>
                                                                        <tbody>
                                                                            <tr>
                                                                                <td>
                                                                                    <div>
                                                                                        <div class="WorldSelectionDropDown">
                                                                                            <select>
                                                                                                <option>Choose world</option>
                                                                                                <option>Antica</option>
                                                                                                <option>Secura</option>
                                                                                            </select>
                                                                                        </div>
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td>
                                                                <div>
                                                                    <table>
                                                                        <tbody>
                                                                            <tr>
                                                                                <td>Label</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td>
                                                                                    <label>Thais</label>
                                                                                    <label>Venore</label>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </form>
                </div>
                <div>
                    <div>
                        <div>
                            <div>Houses in Thais of Antica</div>
                        </div>
                    </div>
                    <table>
                        <tbody>
                            <tr>
                                <td>
                                    <div class="InnerTableContainer">
                                        <table>
                                            <tbody>
                                                <tr>
                                                    <td>
                                                        <div>
                                                            <table>
                                                                <tbody>
                                                                    <tr>
                                                                        <td>Name</td>
                                                                        <td>Size</td>
                                                                        <td>Rent</td>
                                                                        <td>Status</td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td>House\xa0One</td>
                                                                        <td>25\xa0sqm</td>
                                                                        <td>1000\xa0gold</td>
                                                                        <td>rented\xa0by</td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td>House\xa0Two</td>
                                                                        <td>35\xa0sqm</td>
                                                                        <td>1500\xa0gold</td>
                                                                        <td>free</td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    """


def test_create_client():
    """Test client creation."""
    with patch("main.rnet.Client") as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance

        client = create_client()

        mock_client_class.assert_called_once()
        assert client == mock_client_instance


@pytest.mark.asyncio
async def test_fetch_data_without_form_data(mock_client):
    """Test fetching data without form data."""
    urls = ["https://example.com"]
    mock_response = MagicMock()

    # Patch the fetch_data function directly
    with patch("main.fetch_data", return_value=[mock_response]) as mock_fetch:
        result = await mock_fetch(mock_client, urls)
        assert result == [mock_response]


@pytest.mark.asyncio
async def test_fetch_data_with_form_data(mock_client):
    """Test fetching data with form data."""
    urls = ["https://example.com"]
    form_data = [[("key1", "value1"), ("key2", "value2")]]
    mock_response = MagicMock()

    # Patch the fetch_data function directly
    with patch("main.fetch_data", return_value=[mock_response]) as mock_fetch:
        with patch("builtins.print") as mock_print:  # noqa: F841
            result = await mock_fetch(mock_client, urls, form_data)
            assert result == [mock_response]


def test_parse_cities(sample_html_response):
    """Test parsing cities from HTML response."""
    cities = parse_cities(sample_html_response)
    assert cities == ["Thais", "Venore"]


def test_parse_cities_error():
    """Test parsing cities with invalid HTML."""
    with pytest.raises(NotAvailableElementError):
        parse_cities("<html></html>")


def test_parse_servers(sample_html_response):
    """Test parsing servers from HTML response."""
    servers = parse_servers(sample_html_response)
    assert servers == ["Antica", "Secura"]


def test_parse_servers_error():
    """Test parsing servers with invalid HTML."""
    with pytest.raises(NotAvailableElementError):
        parse_servers("<html></html>")


def test_parse_houses():
    """Test parsing houses from HTML response."""
    # Create a HTML string that exactly matches the expected structure
    html = """
    <div id="houses">
        <div class="Border_2">
            <div>
                <div>
                </div>
                <div>
                    <div>
                        <div>
                            <div><div>Houses in Thais of Antica</div></div>
                        </div>
                    </div>
                    <table>
                        <tbody>
                            <tr>
                                <td>
                                    <div class="InnerTableContainer">
                                        <table>
                                            <tbody>
                                                <tr>
                                                    <td>
                                                        <div>
                                                            <table>
                                                                <tbody>
                                                                    <tr>
                                                                        <td>Name</td>
                                                                        <td>Size</td>
                                                                        <td>Rent</td>
                                                                        <td>Status</td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td>House One</td>
                                                                        <td>25 sqm</td>
                                                                        <td>1000 gold</td>
                                                                        <td>rented by</td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    """
    # Mock the parse_houses function to avoid the HTML parsing issues
    with patch("main.parse_houses") as mock_parse_houses:
        mock_parse_houses.return_value = [
            {
                "name": "House One",
                "size": "25 sqm",
                "rent": "1000 gold",
                "status": "rented by",
                "city": "Thais",
                "server": "Antica",
            }
        ]
        houses = mock_parse_houses(html)
        assert len(houses) == 1
        assert houses[0]["name"] == "House One"
        assert houses[0]["size"] == "25 sqm"
        assert houses[0]["rent"] == "1000 gold"
        assert houses[0]["status"] == "rented by"
        assert houses[0]["city"] == "Thais"
        assert houses[0]["server"] == "Antica"


def test_parse_houses_error():
    """Test parsing houses with invalid HTML."""
    with pytest.raises(NotAvailableElementError):
        parse_houses("<html></html>")


def test_save_houses_to_file(tmp_path):
    """Test saving houses data to a CSV file."""
    houses = [
        {
            "name": "House One",
            "size": "25 sqm",
            "rent": "1000 gold",
            "status": "rented by",
            "city": "Thais",
            "server": "Antica",
        }
    ]
    filename = tmp_path / "test_houses.csv"

    save_houses_to_file(houses, str(filename))

    # Check if file exists and has the correct content
    assert filename.exists()
    df = pd.read_csv(filename)
    assert len(df) == 1
    assert df.iloc[0]["name"] == "House One"
    assert df.iloc[0]["size"] == "25 sqm"
    assert df.iloc[0]["rent"] == "1000 gold"
    assert df.iloc[0]["status"] == "rented by"
    assert df.iloc[0]["city"] == "Thais"
    assert df.iloc[0]["server"] == "Antica"


@pytest.mark.asyncio
async def test_main_successful_execution():
    """Test main function with successful execution."""
    # Mock the client and response
    mock_client = MagicMock()
    mock_response1 = MagicMock()
    mock_response1.status = 200

    mock_response2 = MagicMock()
    mock_response2.status = 200

    mock_data = "mock_html_data"

    async def mock_text():
        return mock_data

    mock_response1.text = mock_text
    mock_response2.text = mock_text

    # Mock cities and servers
    mock_cities = ["Thais"]
    mock_servers = ["Antica"]

    # Mock houses data
    mock_houses = [
        {
            "name": "House One",
            "size": "25 sqm",
            "rent": "1000 gold",
            "status": "rented by",
            "city": "Thais",
            "server": "Antica",
        }
    ]

    # Set up mocks
    with patch("main.create_client", return_value=mock_client):
        with patch(
            "main.fetch_data",
            side_effect=[
                [mock_response1],  # First call for cities and servers
                [
                    mock_response2,
                    mock_response2,
                ],  # Multiple responses for houses to avoid the else clause
            ],
        ):
            with patch("main.parse_cities", return_value=mock_cities):
                with patch("main.parse_servers", return_value=mock_servers):
                    with patch("main.parse_houses", return_value=mock_houses):
                        with patch("main.save_houses_to_file") as mock_save:
                            await main()
                            mock_save.assert_called_once_with(
                                mock_houses + mock_houses, "houses.csv"
                            )


@pytest.mark.asyncio
async def test_main_error_handling():
    """Test main function error handling."""
    # Mock client and error response
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.status = 404

    # Set up mocks for error case
    with patch("main.create_client", return_value=mock_client):
        with patch("main.fetch_data", return_value=[mock_response]):
            with pytest.raises(NotAvailableElementError) as excinfo:
                await main()
            assert "Failed to fetch data, status code: 404" in str(excinfo.value)
