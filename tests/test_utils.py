from kubetask.utils import utils
from kubetask.core.constants import State

class TestUtils:
    def test_get_obj_params(self):
        print ("printing ",utils.get_object_params(State))
