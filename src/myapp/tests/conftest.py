

import pytest
from myapp.lib.ctx import ctx_from_env


@pytest.fixture()
def test_ctx():
    ctx = ctx_from_env('test')
    yield ctx
