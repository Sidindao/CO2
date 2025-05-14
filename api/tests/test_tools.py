import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pytest

from api import tools


def test_co2_to_trees():
    assert tools.co2_to_trees(9.9) == 1
    assert tools.co2_to_trees(20) == 2

def test_get_all_distances(monkeypatch):
    def mock_osrm(lat1, lon1, lat2, lon2):
        return {'car': 100, 'bike': 50, 'foot': 10}
    monkeypatch.setattr(tools, "osrm", mock_osrm)

    result = tools.get_all_distances(45.75, 4.85, 48.8566, 2.3522)
    assert result['plane'] > 0
    assert result['car'] == 100
    assert result['bike'] == 50
    assert result['foot'] == 10

def test_get_lat_long(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return [{'lat': '45.75', 'lon': '4.85'}]

    monkeypatch.setattr(tools.requests, "get", lambda *args, **kwargs: MockResponse())
    lat, lon = tools.get_lat_long("Lyon")
    assert lat == '45.75'
    assert lon == '4.85'

def test_fetch_distance_osrm(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {'routes': [{'distance': 10000}]}

    monkeypatch.setattr(tools.requests, "get", lambda *args, **kwargs: MockResponse())
    result = tools.fetch_distance_osrm("car", 45.75, 4.85, 48.8566, 2.3522)
    assert result == {"car": 10.0}

def test_osrm(monkeypatch):
    def mock_fetch_distance_osrm(transport, lat1, lon1, lat2, lon2):
        return {transport: 42.0}

    monkeypatch.setattr(tools, "fetch_distance_osrm", mock_fetch_distance_osrm)

    result = tools.osrm(45.75, 4.85, 48.8566, 2.3522)
    assert result == {
        "car": 42.0,
        "bike": 42.0,
        "foot": 42.0
    }
def test_fetch_distance_osrm_no_routes(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {'routes': []}
    monkeypatch.setattr(tools.requests, "get", lambda *args, **kwargs: MockResponse())
    result = tools.fetch_distance_osrm("car", 1, 1, 2, 2)
    assert result is None

def test_fetch_distance_osrm_error(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 500
        def json(self):
            return {}
    monkeypatch.setattr(tools.requests, "get", lambda *args, **kwargs: MockResponse())
    result = tools.fetch_distance_osrm("car", 1, 1, 2, 2)
    assert result is None
    
def test_get_lat_long_not_found(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return []
    monkeypatch.setattr(tools.requests, "get", lambda *args, **kwargs: MockResponse())
    lat, lon = tools.get_lat_long("Nowhere")
    assert lat is None
    assert lon is None
