import pytest
from httpx import AsyncClient, ASGITransport

from main import main_app


@pytest.mark.asyncio
async def test_frontend_is_not_cached_by_browser():
    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url="http://test",
    ) as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "no-store" in response.headers.get("Cache-Control", "").lower()

        asset_response = await client.get("/static/app.js")
        assert asset_response.status_code == 200
        assert "no-store" in asset_response.headers.get("Cache-Control", "").lower()
