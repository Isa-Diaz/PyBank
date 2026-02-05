import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Ajusta o path para permitir imports do MS2
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)


# ============================
# CLIENT DO MS2
# ============================
@pytest.fixture
def client_ms2():
    try:
        from client_access_service.controller.controller_access import app as flask_app
    except Exception:
        pytest.skip("MS2 não disponível para este teste")

    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ============================
# CLIENT DO MS1
# ============================
@pytest.fixture
def client_ms1():
    try:
        from investment_data_service.app import app
    except Exception:
        pytest.skip("MS1 não disponível para este teste")

    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ============================
# MOCK AUTOMÁTICO DO MS2
# ============================
@pytest.fixture(autouse=True)
def mock_requests_ms2():
    try:
        import client_access_service
    except Exception:
        yield
        return

    with patch("client_access_service.client.client_access.requests.get") as get1, \
         patch("client_access_service.client.client_access.requests.post") as post1, \
         patch("client_access_service.client.client_access.requests.patch") as patch1, \
         patch("client_access_service.client.client_access.requests.delete") as delete1, \
         patch("client_access_service.client.adm_access.requests.get") as get2, \
         patch("client_access_service.client.adm_access.requests.post") as post2, \
         patch("client_access_service.client.adm_access.requests.patch") as patch2, \
         patch("client_access_service.client.adm_access.requests.delete") as delete2:

        get1.return_value = MagicMock()
        post1.return_value = MagicMock()
        patch1.return_value = MagicMock()
        delete1.return_value = MagicMock()

        get2.return_value = MagicMock()
        post2.return_value = MagicMock()
        patch2.return_value = MagicMock()
        delete2.return_value = MagicMock()

        yield

# ============================================================
# Alias para compatibilidade com testes antigos
# ============================================================

@pytest.fixture
def client(client_ms2):
    return client_ms2
