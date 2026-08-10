import runpod
import json
import urllib.request
import urllib.parse

def handler(job):
    job_input = job['input']
    
    # Carica il workflow JSON
    with open('/comfyui/api-workflow.json', 'r') as f:
        workflow = json.load(f)
    
    # Sostituisce l'immagine di input se fornita nella chiamata API
    if 'image_name' in job_input:
        workflow['12']['inputs']['image'] = job_input['image_name']
        
    # Sostituisce il prompt di testo se fornito
    if 'prompt' in job_input:
        workflow['15']['inputs']['seed'] = job_input['prompt']
    
    # Invia il prompt a ComfyUI locale su RunPod
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=json.dumps({"prompt": workflow}).encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(req)
    
    return json.loads(response.read().decode('utf-8'))

runpod.serverless.start({"handler": handler})
