import weave
from weave import Dataset
import evaluation
import argparse
from dotenv import load_dotenv
import os

load_dotenv()


# Parse command line arguments
parser = argparse.ArgumentParser(description='Upload a dataset to Weave')
parser.add_argument('--dataset_path', help='Path to the dataset file')
parser.add_argument('--dataset_name', help='Name of the dataset')
args = parser.parse_args()

# Initialize Weave
weave.init(f"{os.getenv('WEAVE_TEAM')}/{os.getenv('WEAVE_PROJECT')}")

# Create a dataset
data = evaluation.load_dataset(args.dataset_path)
dataset = Dataset(
    name=args.dataset_name,
    rows=data
)

# Publish the dataset
weave.publish(dataset)

# Retrieve the dataset
dataset_ref = weave.ref(args.dataset_name+":latest").get()

print(f"Dataset uploaded successfully! You can access it in the Weave UI datasets tab under the name: {args.dataset_name}")