from gig_platform.models import Job, Worker


def test_job_creation(app):
    """Test job model creation."""
    with app.app_context():
        job = Job(
            title="Test Job",
            lat=40.7128,
            lng=-74.0060,
            pay="$100"
        )
        
        assert job.title == "Test Job"
        assert job.lat == 40.7128
        assert job.lng == -74.0060
        assert job.pay == "$100"


def test_job_to_dict(app):
    """Test job to_dict method."""
    with app.app_context():
        job = Job(
            title="Test Job",
            lat=40.7128,
            lng=-74.0060,
            pay="$100"
        )
        
        job_dict = job.to_dict()
        assert job_dict["title"] == "Test Job"
        assert job_dict["location"] == [40.7128, -74.0060]
        assert job_dict["pay"] == "$100"


def test_worker_creation(app):
    """Test worker model creation."""
    with app.app_context():
        worker = Worker(
            name="John Doe",
            skill="Plumbing",
            experience="5 years",
            lat=40.7128,
            lng=-74.0060
        )
        
        assert worker.name == "John Doe"
        assert worker.skill == "Plumbing"
        assert worker.experience == "5 years"
        assert worker.lat == 40.7128
        assert worker.lng == -74.0060