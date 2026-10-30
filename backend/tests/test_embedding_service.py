from unittest.mock import Mock

import pytest

from app.ai.embeddings.service import EmbeddingService


def make_service(vector=None, dimension=3):
    provider = Mock()
    provider.embed_text.return_value = vector or [0.1, 0.2, 0.3]
    return EmbeddingService(provider, expected_dimension=dimension), provider


def test_embedding_service_embeds_multiple_texts_in_order():
    service, provider = make_service()

    result = service.embed_texts(["first document chunk", "second document chunk"])

    assert result == [[0.1, 0.2, 0.3], [0.1, 0.2, 0.3]]
    assert provider.embed_text.call_count == 2
    provider.embed_text.assert_any_call("first document chunk")
    provider.embed_text.assert_any_call("second document chunk")


def test_embedding_service_rejects_empty_batch():
    service, provider = make_service()

    with pytest.raises(ValueError, match="At least one text"):
        service.embed_texts([])

    provider.embed_text.assert_not_called()


@pytest.mark.parametrize("texts", [["   "], ["valid text", ""]])
def test_embedding_service_rejects_blank_text(texts):
    service, provider = make_service()

    with pytest.raises(ValueError, match="cannot be empty"):
        service.embed_texts(texts)


def test_embedding_service_rejects_non_string_input():
    service, provider = make_service()

    with pytest.raises(TypeError, match="must be a string"):
        service.embed_texts(["valid text", 123])


def test_embedding_service_rejects_wrong_dimension():
    service, provider = make_service(vector=[0.1, 0.2])

    with pytest.raises(ValueError, match="expected 3"):
        service.embed_texts(["startup overview"])


@pytest.mark.parametrize("vector", [[0.1, float("nan"), 0.3], [0.1, float("inf"), 0.3]])
def test_embedding_service_rejects_non_finite_values(vector):
    service, provider = make_service(vector=vector)

    with pytest.raises(ValueError, match="must be finite"):
        service.embed_texts(["startup overview"])


def test_embedding_service_rejects_non_numeric_values():
    service, provider = make_service(vector=[0.1, "bad", 0.3])

    with pytest.raises(ValueError, match="must be numeric"):
        service.embed_texts(["startup overview"])


def test_embedding_service_propagates_provider_errors():
    service, provider = make_service()
    provider.embed_text.side_effect = RuntimeError("provider unavailable")

    with pytest.raises(RuntimeError, match="provider unavailable"):
        service.embed_texts(["startup overview"])


def test_embedding_service_rejects_invalid_dimension_configuration():
    _, provider = make_service()

    with pytest.raises(ValueError, match="greater than zero"):
        EmbeddingService(provider, expected_dimension=0)
