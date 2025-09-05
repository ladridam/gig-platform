from gig_platform import create_app
from gig_platform.utils.helpers import find_available_port, get_debug_flag
from gig_platform.commands import cli, db
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Add models to Flask shell."""
    from gig_platform.models import Job, Worker
    return {'db': db, 'Job': Job, 'Worker': Worker}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", find_available_port()))
    debug = get_debug_flag()
    app.run(host="0.0.0.0", port=port, debug=debug)