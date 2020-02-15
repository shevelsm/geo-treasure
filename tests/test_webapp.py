import os
import tempfile

import pytest

from geotreasure import create_app


geotreasure = create_app()


@pytest.fixture
def client():
    db_fd, geotreasure.app.config["DATABASE"] = tempfile.mkstemp()
    geotreasure.app.config["TESTING"] = True

    with geotreasure.app.test_client() as client:
        with geotreasure.app.app_conext():
            geotreasure.init_db()
        yield client

    os.close(db_fd)
    os.unlink(geotreasure.app.config["DATABASE"])
