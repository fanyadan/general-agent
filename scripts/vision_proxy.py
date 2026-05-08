import sys
import os
from hermes_tools import terminal

def analyze_image(image_path):
    """
    Acts as a bridge between Codex CLI and the Hermes Vision System.
    Calls the host's vision analysis capability using the full model identifier.
    """
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} not found.")
        sys.exit(1)

    # Corrected full model identifier for gemini-3-pro-preview via CLI
    model_id = "google-gemini-cli/gemini-3-pro-preview"
    
    # The prompt to be sent to the vision model
    prompt = f"Analyze this image in detail: {image_path}. Use model {model_id}. Return a comprehensive technical description of all text and visual elements."
    
    try:
        # We trigger the vision analysis via the hermes CLI tool embedded in the environment
        result = terminal(command=f"hermes vision-analyze --image \"{image_path}\" --model \"{model_id}\" --prompt \"{prompt}\"")
        return result['output']
    except Exception as e:
        return f"Vision Analysis Failed: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 vision_proxy.py <image_path>")
        sys.exit(1)
    
    path = sys.argv[1]
    print(analyze_image(path))
