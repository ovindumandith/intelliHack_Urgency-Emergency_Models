from model_loader import DisasterModelLoader

def test_models():
    loader = DisasterModelLoader()
    if not loader.load_models():
        print("Failed to load models")
        return False
    
    test_text = "Building collapsed, people trapped inside"
    result = loader.analyze_request(test_text)
    print("Test result:", result)
    return True

if __name__ == "__main__":
    test_models()
