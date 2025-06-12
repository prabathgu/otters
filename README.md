# Winston
Your personal problem solver

## Description
Winston is a small experiment in creating an AI agent designed to be your personal problem solver. It leverages the power of LLMs to understand (and execute) a wide range of tasks and questions. Given user input, Winston will create a plan to solve the problem, and then execute the plan with help from some agent friends.

## Setup
1. Git clone the repo
   ```bash
   git clone https://github.com/wandb/fc2025-space-agent-public
   ```

2. Change directory into the project folder:
   ```bash
   cd fc2025-space-agent-public
   ```

3. Install the required dependencies:
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

4. Set up your secrets:
   Create a `.env` file and add the following text with the API keys replaced with your teams' keys:
   ```
   #### CONFIGURE ME ####

   # API Key For Weave (wandb.ai/authorize)
   WANDB_API_KEY = "your-wandb-api-key" 

   # Weave Project & Team Settings
   WEAVE_TEAM= "your-team-name"
   WEAVE_PROJECT= "your-project-name"

   # API Keys for AWS (Fetch from Game Day Credentials Page)
   AWS_ACCESS_KEY_ID="XXX" 
   AWS_SECRET_ACCESS_KEY="XXX"
   AWS_SESSION_TOKEN="XXX"
   AWS_DEFAULT_REGION="us-east-1" # Leave as is

   # Your finetuned model endpopint from first Workshop (Do not worry about this if you did not participate in workshop 1)
   AWS_FINETUNED_MODEL_ENDPOINT = "huggingface-pytorch-tgi-inference-2025-06-02-21-31-48-855"
   ```

   Note: `.env` is in the `.gitignore` file to keep your secrets secure.

5. Load your secrets
   NOTE: RUN THIS AFTER ANY UPDATES TO .ENV IN THE TERMINAL FROM WHICH YOU CALL YOUR MODEL EVALUATIONS.
   
   ```
   source force_env.sh
   ```
   
   Tip: Use `python validate_aws_setup.py` to check if your credentials work (and swap the Model ID to test that too!).


6. Run an evaluation (most tasks):

   Use the following bash command from the base directory. A line with a 🍩 emoji will link to your evaluation results. 
   This URL will guide you to the input for task 1.

   ```bash
   WEAVE_PARALLELISM=1 python evaluation.py --dataset objects/datasets/eval_public.jsonl   
   ```

7. Upload a new dataset for submission (task 2.2):

   Create your new dataset, following `objects/datasets/eval_public.jsonl` formatting, and run the following:
   ```
   python upload_dataset.py --dataset_path "objects/datasets/eval_public.jsonl" --dataset_name "winston-space-agent-dataset-eval-public"
   ```

   Find the correct inputs in the "get" tab of the uploaded dataset in the Weave UI.


TIP: We provide a launch.json file containing debug commands for all tasks, compatible with VSCode, Cursor, etc.
