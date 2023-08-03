from api.idm.deprovisioning import Deprovisioner


class TestClassAttributes:
    instance = Deprovisioner()

    # Test for existing Attributes
    def test_has_model(self):
        assert hasattr(self.instance, "model")

    def test_has_req_obj_count(self):
        assert hasattr(self.instance, "REQUEST_OBJ_COUNT")

    def test_has_idm_api_url(self):
        assert hasattr(self.instance, "idm_api_url")

    def test_has_api_key(self):
        assert hasattr(self.instance, "API_KEY")

    def test_has_secret_key(self):
        assert hasattr(self.instance, "SECRET_KEY")
        
    def test_has_queryset(self):
        assert hasattr(self.instance,"queryset")

    def test_has_request_bodies(self):
        assert hasattr(self.instance, "request_bodies")
        
    def test_has_time(self):
        assert hasattr(self.instance, "time")

    # Test for existing methods
    def test_has_get_model(self):
        assert hasattr(self.instance, "get_model")
        assert callable(getattr(self.instance, "get_model"))

    def test_has_get_queryset(self):
        assert hasattr(self.instance, "get_queryset")
        assert callable(getattr(self.instance, "get_queryset"))

    def test_has_create_hmac(self):
        assert hasattr(self.instance, "create_hmac")
        assert callable(getattr(self.instance, "create_hmac"))

    def test_has_create_headers(self):
        assert hasattr(self.instance, "create_headers")
        assert callable(getattr(self.instance, "create_headers"))

    def test_has_prepare_request_bodies(self):
        assert hasattr(self.instance, "prepare_request_bodies")
        assert callable(getattr(self.instance, "prepare_request_bodies"))

    def test_has_prepare_obj_json_rpc(self):
        assert hasattr(self.instance, "prepare_obj_json_rpc")
        assert callable(getattr(self.instance, "prepare_obj_json_rpc"))

    def test_has_deprovison(self):
        assert hasattr(self.instance, "deprovison")
        assert callable(getattr(self.instance, "deprovison"))

    def test_has_handle_response(self):
        assert hasattr(self.instance, "handle_response")
        assert callable(getattr(self.instance, "handle_response"))
