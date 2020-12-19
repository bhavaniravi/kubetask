from kubetask.utils import utils
from kubetask.core.constants import State

class TestUtils:
    def test_get_obj_params(self):
        params = utils.get_object_params(State)
        assert "NOT_STARTED" in params
