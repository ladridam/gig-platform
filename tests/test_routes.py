def test_home_page(client):
    """Test home page route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Gig Platform" in response.data


def test_jobs_page(client):
    """Test jobs page route."""
    response = client.get("/jobs/")
    assert response.status_code == 200
    assert b"Available Jobs" in response.data


def test_workers_page(client):
    """Test workers page route."""
    response = client.get("/workers/")
    assert response.status_code == 200
    assert b"Available Workers" in response.data


def test_map_page(client):
    """Test map page route."""
    response = client.get("/map/")
    assert response.status_code == 200
    assert b"Jobs & Workers Nearby" in response.data