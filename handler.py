import runpod
import json
import urllib.request
import urllib.parse
import time
import os
import base64
import uuid

def download_image(url):
    """Scarica l'immagine dal link pubblico e la salva nella cartella di input di ComfyUI"""
    if not url.startswith('http'):
        return url
    
    filename = str(uuid.uuid4()) + ".png"
    filepath = os.path.join('/comfyui/input', filename)
    try:
        urllib.request.urlretrieve(url, filepath)
        return filename
    except Exception as e:
        print(f"Errore download immagine: {e}")
        return url

def get_latest_output(prompt_id):
    # Interroga l'API di ComfyUI ogni 2 secondi per sapere se ha finito
    while True:
        try:
            req = urllib.request.Request("http://127.0.0.1:8188/history/" + prompt_id)
            with urllib.request.urlopen(req) as response:
                history = json.loads(response.read())
                if prompt_id in history:
                    # Il lavoro è finito! Cerchiamo l'immagine o il video finale
                    outputs = history[prompt_id].get('outputs', {})
                    for node_id, node_output in outputs.items():
                        # Cerca output di tipo immagine (PNG/JPEG)
                        if 'images' in node_output:
                            for image in node_output['images']:
                                return image.get('filename')
                        # Cerca output di tipo video o gif
                        if 'gifs' in node_output:
                            for gif in node_output['gifs']:
                                return gif.get('filename')
                    return None
        except Exception as e:
            pass
        time.sleep(2)

def handler(job):
    job_input = job['input']

    # Carica il workflow JSON dal container
    with open('/comfyui/api-workflow.json', 'r') as f:
        workflow = json.load(f)

    # Inietta l'immagine principale se presente (per Product Placement)
    if 'image_1' in job_input and '12' in workflow:
        # Scarichiamo fisicamente l'immagine prima di darla a ComfyUI
        local_filename = download_image(job_input['image_1'])
        workflow['12']['inputs']['image'] = local_filename
        
    # Inietta il testo se presente
    if 'prompt' in job_input:
        if '15' in workflow:
            if 'text' in workflow['15']['inputs']:
                workflow['15']['inputs']['text'] = job_input['prompt']
            elif 'prompt' in workflow['15']['inputs']:
                workflow['15']['inputs']['prompt'] = job_input['prompt']

    # 1. Invia il workflow a ComfyUI locale
    req = urllib.request.Request(
        "http://127.0.0.1:8188/prompt", 
        data=json.dumps({"prompt": workflow}).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            prompt_id = result.get('prompt_id')
    except Exception as e:
        return {"error": f"Errore durante l'avvio di ComfyUI: {str(e)}"}

    if not prompt_id:
        return {"error": "Nessun prompt_id restituito da ComfyUI"}

    # 2. Aspetta che ComfyUI finisca il rendering e trova il nome del file
    filename = get_latest_output(prompt_id)
    
    if not filename:
        return {"error": "Lavoro completato ma nessun file trovato nell'output."}

    # 3. Leggi il file dal disco del pod e convertilo in Base64 per inviarlo al sito
    file_path = os.path.join('/comfyui/output', filename)
    try:
        with open(file_path, "rb") as media_file:
            encoded_string = base64.b64encode(media_file.read()).decode('utf-8')
            
        return {
            "file_name": filename,
            "file_base64": encoded_string
        }
    except Exception as e:
        return {"error": f"Errore nella lettura del file finale: {str(e)}"}

runpod.serverless.start({"handler": handler})
