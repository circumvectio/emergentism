import os
import urllib.request

BASE_URL = "https://unpkg.com/three@0.160.0/"
VENDOR_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(VENDOR_DIR, "three-0.160.0")

FILES = [
    ("build/three.module.js", "three.module.js"),
    ("examples/jsm/controls/OrbitControls.js", "controls/OrbitControls.js"),
    ("examples/jsm/postprocessing/EffectComposer.js", "postprocessing/EffectComposer.js"),
    ("examples/jsm/postprocessing/RenderPass.js", "postprocessing/RenderPass.js"),
    ("examples/jsm/postprocessing/UnrealBloomPass.js", "postprocessing/UnrealBloomPass.js"),
    ("examples/jsm/postprocessing/ShaderPass.js", "postprocessing/ShaderPass.js"),
    ("examples/jsm/shaders/CopyShader.js", "shaders/CopyShader.js"),
    ("examples/jsm/shaders/LuminosityHighPassShader.js", "shaders/LuminosityHighPassShader.js"),
]

def download_files():
    print(f"Downloading Three.js modules to: {TARGET_DIR}")
    for source_path, dest_rel_path in FILES:
        url = BASE_URL + source_path
        dest_path = os.path.join(TARGET_DIR, dest_rel_path)

        # Ensure directory exists
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        print(f"Fetching: {url} ...")
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read()

            # Write to file
            with open(dest_path, "wb") as f:
                f.write(content)
            print(f"Saved: {dest_path}")
        except Exception as e:
            print(f"FAILED to download {url}: {e}")
            raise e

if __name__ == "__main__":
    download_files()
