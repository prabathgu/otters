# Winston
Your personal problem solver

## Description
Winston is a small experiment in creating an AI agent designed to be your personal problem solver. It leverages the power of LLMs to understand (and execute) a wide range of tasks and questions. Given user input, Winston will create a plan to solve the problem, and then execute the plan with help from some agent friends.

## Setup
1. Git clone the repo
   ```bash
   git clone XYZ TODO XYZ
   ```

2. Install the required dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   or 
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

3. Set up your secrets:
   Create a `.streamlit/secrets.toml` file and add the following text with the API keys replaced with your teams' keys:
   ```toml
   #### CONFIGURE ME ####
   AWS_ACCESS_KEY_ID = "XXXX" 
   AWS_SECRET_ACCESS_KEY = "XXX"
   AWS_SESSION_TOKEN = "XXXX"

   WEAVE_API_KEY = "XXXX"
   WEAVE_ENTITY= "your-team-here"
   WEAVE_PROJECT= "your-weave-project-here"

   #### DO NOT CHANGE ####
   AWS_REGION_NAME = "us-east-1"
   ```

   Note: `.streamlit/secrets.toml` is in the `.gitignore` file to keep your secrets secure.
   Tip: Use `python validate_aws_setup.py` to check if your credentials work (and swap the Model ID to test that too!).

4. Run an evaluation (most tasks):

   Use the following bash command from the base directory. A line with a 🍩 emoji will link to your evaluation results. 
   This URL will guide you to the input for task 1.

   ```bash
   WEAVE_PARALLELISM=5 python evaluation.py --dataset objects/datasets/eval_public.jsonl   
   ```

5. Upload a new dataset for submission (task 2.2):

   Create your new dataset, following `objects/datasets/eval_public.jsonl` formatting, and run the following:
   ```
   python upload_dataset.py --dataset_path "objects/datasets/eval_public.jsonl" --dataset_name "winston-space-agent-dataset-eval-public"
   ```

   Find the correct inputs in the "get" tab of the uploaded dataset in the Weave UI.

