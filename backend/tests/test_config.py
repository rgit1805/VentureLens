from app.core.config import settings


def test_embedding_configuration():
    assert settings.embedding_provider == "gemini"
    assert settings.embedding_model == "gemini-embedding-2"
    assert settings.embedding_dimension == 768
    