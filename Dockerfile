# Usa una versione base stabile compatibile con tutte le GPU di RunPod
FROM runpod/worker-comfyui:5.8.4-base

# Clona ComfyUI
RUN git clone https://github.com/comfyanonymous/ComfyUI /comfyui/custom_nodes/ComfyUI

# Scarica l'immagine placeholder iniziale
RUN wget --progress=dot:giga -O '/comfyui/input/medusa_poster.png' "https://cool-anteater-319.convex.cloud/api/storage/e228e61b-991e-49a9-b0e3-0015e61fc901"

# Copia i file necessari nei percorsi corretti
COPY handler.py /handler.py
COPY api-workflow.json /comfyui/api-workflow.json

CMD [ "python", "-u", "/handler.py" ]
