import subprocess
import os
import sys

def run_tests():
    result = subprocess.run(["pytest", "/root/AI-Hedge-Fund/tests/"], capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr

def self_heal():
    success, output = run_tests()
    if not success:
        print("Tests failed. Initiating self-healing...")
        # Placeholder for AI-driven patch logic
        print("Error log:", output)
        # Here we would invoke a model to analyze the error and patch code
        return False
    print("All tests passed.")
    return True

if __name__ == "__main__":
    self_heal()
