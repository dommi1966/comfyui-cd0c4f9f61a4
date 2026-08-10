FROM runpod/worker-comfyui:5.8.4-base

# --- Custom node: WanVideoWrapper (kijai) ---
RUN git clone https://github.com/kijai/ComfyUI-WanVideoWrapper \
      /comfyui/custom_nodes/ComfyUI-WanVideoWrapper \
 && pip install --no-cache-dir -r \
      /comfyui/custom_nodes/ComfyUI-WanVideoWrapper/requirements.txt

# --- Cartelle modelli ---
RUN mkdir -p /comfyui/models/diffusion_models \
             /comfyui/models/text_encoders \
             /comfyui/models/vae \
             /comfyui/models/clip_vision

# --- Modelli Wan 2.1 I2V (480p, fp8) da Kijai/WanVideo_comfy ---
ARG HF=https://huggingface.co/Kijai/WanVideo_comfy/resolve/main
RUN wget --progress=dot:giga -O /comfyui/models/diffusion_models/Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors \
      "$HF/Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors" \
 && wget --progress=dot:giga -O /comfyui/models/text_encoders/umt5-xxl-enc-fp8_e4m3fn.safetensors \
      "$HF/umt5-xxl-enc-fp8_e4m3fn.safetensors" \
 && wget --progress=dot:giga -O /comfyui/models/vae/Wan2_1_VAE_bf16.safetensors \
      "$HF/Wan2_1_VAE_bf16.safetensors" \
 && wget --progress=dot:giga -O /comfyui/models/clip_vision/open-clip-xlm-roberta-large-vit-huge-14_visual_fp16.safetensors \
      "$HF/open-clip-xlm-roberta-large-vit-huge-14_visual_fp16.safetensors"

# NIENTE handler custom, NIENTE CMD: ci pensa il base image
