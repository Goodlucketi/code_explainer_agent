#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

from code_explainer_agent.crew import CodeExplainerAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    print("=== Code Explainer Agent ===")
    print("Would you like to (1) paste code or (2) upload a file?")
    choice = input("Enter 1 or 2: ").strip()

    user_code = ""

    if choice == "1":
        print("\nPaste your code snippet below (end with ENTER + Ctrl+D on Mac/Linux or Ctrl+Z on Windows):\n")
        user_code = sys.stdin.read().strip()

    elif choice == "2":
        file_path = input("\nEnter path to your code file: ").strip()
        if not os.path.exists(file_path):
            print("❌ File not found. Exiting...")
            return
        with open(file_path, "r", encoding="utf-8") as f:
            user_code = f.read()

    else:
        print("❌ Invalid choice. Exiting...")
        return

    if not user_code:
        print("⚠️ No code provided. Exiting...")
        return
    
    inputs = {
        "code_snippet": user_code,
        "current_year": str(datetime.now().year)
    }

    try:
        CodeExplainerAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        CodeExplainerAgent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CodeExplainerAgent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        CodeExplainerAgent().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
