# clean base image containing only comfyui, comfy-cli and comfyui-manager
FROM runpod/worker-comfyui:5.9.0-base

# install custom nodes into comfyui
RUN git clone https://github.com/comfyanonymous/ComfyUI /comfyui/custom_nodes/ComfyUI

# copy all input data (like images or videos) into comfyui (uncomment and adjust if needed)
# COPY input/ /comfyui/input/

# user-provided inputs override the auto-generated placeholders above.
RUN wget --progress=dot:giga -O '/comfyui/input/medusa_poster.png' "https://cool-anteater-319.convex.cloud/api/storage/e228e61b-991e-49a9-b0e3-0015e61fc901"
COPY handler.py /handler.py
CMD [ "python", "-u", "/handler.py" ]
