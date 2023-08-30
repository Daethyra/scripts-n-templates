import sagemaker
import boto3
from sagemaker.huggingface import HuggingFace

try:
	role = sagemaker.get_execution_role()
except ValueError:
	iam = boto3.client('iam')
	role = iam.get_role(RoleName='sagemaker_execution_role')['Role']['Arn']
		
hyperparameters = {
	'model_name_or_path':'meta-llama/Llama-2-70b-chat-hf',
	'output_dir':'/opt/ml/model'
	# add your remaining hyperparameters
	# more info here https://github.com/huggingface/transformers/tree/v4.26.0/examples/pytorch/seq2seq
}

# git configuration to download our fine-tuning script
git_config = {'repo': 'https://github.com/huggingface/transformers.git','branch': 'v4.26.0'}

# creates Hugging Face estimator
huggingface_estimator = HuggingFace(
	entry_point='run_summarization.py',
	source_dir='./examples/pytorch/seq2seq',
	instance_type='ml.p3.2xlarge',
	instance_count=1,
	role=role,
	git_config=git_config,
	transformers_version='4.26.0',
	pytorch_version='1.13.1',
	py_version='py39',
	hyperparameters = hyperparameters
)

# starting the train job
huggingface_estimator.fit()