"""Prepare one bounded pilot; this script does not access any remote service."""
from pathlib import Path
from decimal import Decimal
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from iald_orchestrator.safe_files import save_json, utc_now

manifest = json.loads((HERE/'dataset_manifest.json').read_bytes())
audit = json.loads((HERE/'validation.json').read_bytes())
assert audit['status'] == 'LOCAL_DATA_AUDIT_PASSED'
files = {f['split']: f for f in manifest['files'] if f['format'] == 'vertex'}
proxy = Decimal(files['train']['bytes'])*2*Decimal('10')/1_000_000
campaign = {
    'schema':1, 'created_at':utc_now(), 'status':'DATA_READY_CLOUD_SETUP_IN_PROGRESS',
    'user_authorization':'Criar nossos modelos via fine-tuning em todos que admitirem; 50 dólares para o piloto; Qwen local não precisa mexer.',
    'budget':{'currency':'USD','total_limit':'50.00','training_envelope':'35.00',
              'evaluation_envelope':'5.00','storage_fees_taxes_reserve':'10.00',
              'scope':'TOTAL_PILOT_ALL_PROVIDERS_NOT_PER_PROVIDER',
              'remote_training_jobs_launched':0,'training_committed_usd':'0.00',
              'billing_invoice_verified':False},
    'candidate':{'provider':'google_vertex_ai','model':'gemini-3.5-flash',
                 'project_id':'iald-tgl-ft-20260924','region':'us-central1',
                 'epochs':2,'adapter_size':4,'learning_rate_multiplier':1,
                 'training_usd_per_million_tokens':'10.00',
                 'byte_proxy_training_usd':str(proxy),
                 'estimate_status':'UTF8_BYTE_PROXY_NOT_EXACT_TOKENS_OR_PROVIDER_QUOTE',
                 'provider_token_count':None,'remote_job_id':None,
                 'training_file':files['train'],'validation_file':files['validation'],
                 'test_file_kept_local':files['test'],
                 'pricing_source':'https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing'},
    'launch_checks':['Actual model is offered for tuning in this account/region',
                     'Provider token count/price fits total budget including evaluation and fees',
                     'Only train and validation exports uploaded; held-out test remains local',
                     'No duplicate/uncertain job; persist identity immediately after creation'],
    'evaluation':{'held_out_examples':manifest['counts']['test'],
                  'compare':'Base model versus fine-tuned model with identical held-out prompts',
                  'rubric':['Preserve equations and signs','State hypotheses and source scope',
                            'Answer the actual question','No invented compilation, hash or physical confirmation'],
                  'activation':'No automatic promotion before comparison and critical-regression review',
                  'current_status':'NOT_RUN'},
    'exclusions':['Existing local Qwen is untouched','No GPU rental or provisioned throughput',
                  'No confidential code, credential, legal archive or canonical-original edit',
                  'No claim of full TGL memorization or independent scientific validation'],
    'providers':[
       {'id':'gemini','status':'PILOT_CANDIDATE','route':'Managed supervised tuning in Google Cloud'},
       {'id':'claude','status':'DATA_FORMAT_READY_ACCOUNT_AND_FULL_COST_UNVERIFIED',
        'route':'Claude 3 Haiku on Amazon Bedrock; not the current Claude subscription model',
        'source':'https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-fine-tuning.html'},
       {'id':'kimi','status':'OPEN_WEIGHTS_TRAINING_INFRASTRUCTURE_NOT_PROVISIONED',
        'route':'Separate copy of Kimi K3; Ultra subscription is inference access',
        'source':'https://huggingface.co/moonshotai/Kimi-K3'},
       {'id':'mimo','status':'OPEN_WEIGHTS_TRAINING_INFRASTRUCTURE_NOT_PROVISIONED',
        'route':'Separate copy of MiMo V2.6 Pro RL; current inference API has no verified tuning route',
        'source':'https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL'},
       {'id':'deepseek','status':'OPEN_WEIGHTS_TRAINING_INFRASTRUCTURE_NOT_PROVISIONED',
        'route':'Separate copy of DeepSeek V4.1 Flash; current inference API has no verified tuning route',
        'source':'https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash'},
       {'id':'openai','status':'NEW_SELF_SERVICE_ACCESS_NOT_AVAILABLE',
        'route':'Deprecation/access restrictions require account eligibility; subscription models are not fine-tuned this way',
        'source':'https://developers.openai.com/api/docs/deprecations'},
       {'id':'jev','status':'NO_CUSTOMER_WEIGHT_FINE_TUNING',
        'route':'Instructions/state/criteria customization does not train Jev weights',
        'source':'https://docs.typesafe.ai/models'},
       {'id':'qwen_local','status':'EXCLUDED_BY_OPERATOR','modified':False}
    ]
}
path = HERE/'campaign.json'
if path.exists():
    raise RuntimeError('Campaign already exists; inspect and update its actual state instead of resetting it')
save_json(path,campaign)
print(json.dumps({'status':campaign['status'],'total_limit_usd':'50.00',
                  'byte_proxy_training_usd':str(proxy),'remote_jobs':0}))
