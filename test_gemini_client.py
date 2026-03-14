import pytest
from config import AppConfig
from gemini_client import GeminiClient

def test_gemini_client_filter_duplicates():
    """
    Test Step 8: Verifies semantic duplicate detection logic using the real Gemini API.
    """
    try:
        config = AppConfig()
    except ValueError as e:
        pytest.skip(f"Skipping Gemini test due to missing environment config: {e}")

    if not config.gemini_api_key or config.gemini_api_key == "dummy":
        pytest.skip("Skipping Gemini test as .env variables contain dummy values.")

    client = GeminiClient(config.gemini_api_key)

    keep_items = ["Manzana", "tomates", "leche entera", "huevos", "champu"]
    todoist_tasks = [
        {"content": "Manzanas"}, # Plural duplicate
        {"content": "cebollas"},
        {"content": "tomate"},   # Singular duplicate
        {"content": "pan"}
    ]

    result = client.filter_duplicates(keep_items, todoist_tasks)
    
    # We expect 'Manzana' and 'tomates' to be duplicates of 'Manzanas' and 'tomate'.
    # 'leche entera', 'huevos', 'champu' should be to_insert.
    assert isinstance(result, dict)
    assert "to_insert" in result
    assert "duplicates" in result

    duplicates = [item.lower() for item in result["duplicates"]]
    to_insert = [item.lower() for item in result["to_insert"]]

    assert "manzana" in duplicates
    assert "tomates" in duplicates
    assert "leche entera" in to_insert
    assert "huevos" in to_insert
    assert "champu" in to_insert

    print("\\n[Real Endpoint] Gemini Duplicate Detection Results:")
    print(f"Duplicates: {result['duplicates']}")
    print(f"To Insert: {result['to_insert']}")

def test_gemini_client_categorize_items():
    """
    Test Step 10: Verifies semantic categorization logic using the real Gemini API.
    """
    try:
        config = AppConfig()
    except ValueError as e:
        pytest.skip(f"Skipping Gemini test due to missing environment config: {e}")

    if not config.gemini_api_key or config.gemini_api_key == "dummy":
        pytest.skip("Skipping Gemini test as .env variables contain dummy values.")

    client = GeminiClient(config.gemini_api_key)
    
    sections = ["Fruta y Verdura", "Carne y Pescado", "Lácteos", "Limpieza"]
    items_to_test = ["Manzana Golden", "Solomillo de cerdo", "Yogur natural", "Baterías AAA"]
    
    # Test valid categorizations in bulk
    cat_results = client.categorize_items(items_to_test, sections)
    
    assert cat_results["Manzana Golden"].lower() == "fruta y verdura"
    assert cat_results["Solomillo de cerdo"].lower() == "carne y pescado"
    assert cat_results["Yogur natural"].lower() == "lácteos"
    assert cat_results["Baterías AAA"] == "OTROS"
    
    print("\\n[Real Endpoint] Gemini Categorization Results:")
    for item, cat in cat_results.items():
        print(f"'{item}' -> {cat}")
