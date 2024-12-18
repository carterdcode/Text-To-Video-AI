import json
from video_search_query_generator import getImagePromptsTimed, call_OpenAI

def test_getImagePromptsTimed():
    # Mock data
    script = "This is a sample video script describing various scenes and actions."
    captions_timed = [
        {"s": "0.1", "e": "6.1", "p": "A misty morning in a dense forest."},
        {"s": "6.1", "e": "12.1", "p": "A busy street in a metropolitan city."},
        {"s": "12.1", "e": "18.1", "p": "A serene beach with gentle waves."},
        {"s": "18.1", "e": "24.1", "p": "A starry night sky over a mountain range."},
        {"s": "24.1", "e": "30.1", "p": "A futuristic cityscape with neon lights."},
        {"s": "30.1", "e": "36.1", "p": "A cozy cabin in a snowy forest."}
    ]

    # Mock OpenAI function (to replace actual call_OpenAI for testing)
    def mock_call_OpenAI(script, captions_timed):
        # Simulated response from OpenAI
        return json.dumps([
            {"s": "0.1", "e": "6.1", "p": "A misty morning in a dense forest."},
            {"s": "6.1", "e": "12.1", "p": "A busy street in a metropolitan city."},
            {"s": "12.1", "e": "18.1", "p": "A serene beach with gentle waves."},
            {"s": "18.1", "e": "24.1", "p": "A starry night sky over a mountain range."},
            {"s": "24.1", "e": "30.1", "p": "A futuristic cityscape with neon lights."},
            {"s": "30.1", "e": "36.1", "p": "A cozy cabin in a snowy forest."},
        ])
    # Replace the actual function with the mock
    global call_OpenAI
    call_OpenAI = mock_call_OpenAI

    # Call the function
    result = getImagePromptsTimed(script, captions_timed)

    # Print the result
    print("\nTest result for getImagePromptsTimed:")
    print(result)

if __name__ == "__main__":
    test_getImagePromptsTimed()
