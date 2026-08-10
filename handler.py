import runpod
import json
import urllib.request
import urllib.parse

def handler(job):
    job_input = job['input']

    # Carica il workflow JSON
    with open('/comfyui/api-workflow.json', 'r') as f:
        workflow = json.load(f)

    # Gestione Immagini di input (se inviate)
    if 'image_1' in job_input and '12' in workflow:
        workflow['12']['inputs']['image'] = job_input['image_1']
        
    if 'image_2' in job_input and '13' in workflow:
        workflow['13']['inputs']['image'] = job_input['image_2']

    # Gestione Prompt di testo (inserisce il testo nel campo text o prompt)
    if 'prompt' in job_input:
        if '15' in workflow:
            # Sostituisci 'text' o 'prompt' a seconda di dove si trova la casella di testo nel nodo 15
            if 'text' in workflow['15']['inputs']:
                workflow['15']['inputs']['text'] = job_input['prompt']
            elif 'prompt' in workflow['15']['inputs']:
                workflow['15']['inputs']['prompt'] = job_input['prompt']

    # Invia il prompt a ComfyUI locale su RunPod
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=json.dumps({"prompt": workflow}).encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(req)

    return json.loads(response.read().decode('utf-8'))

runpod.serverless.start({"handler": handler})
