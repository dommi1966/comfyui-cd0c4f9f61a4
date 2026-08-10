FROM runpod/worker-comfyui:5.8.4-base

RUN mkdir -p /comfyui/models/diffusion_models \
             /comfyui/models/text_encoders \
             /comfyui/models/vae \
             /comfyui/models/clip_vision

ARG BASE=https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files
RUN wget --progress=dot:giga -O /comfyui/models/diffusion_models/wan2.1_i2v_480p_14B_fp8_e4m3fn.safetensors \
      "$BASE/diffusion_models/wan2.1_i2v_480p_14B_fp8_e4m3fn.safetensors" \
 && wget --progress=dot:giga -O /comfyui/models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors \
      "$BASE/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors" \
 && wget --progress=dot:giga -O /comfyui/models/vae/wan_2.1_vae.safetensors \
      "$BASE/vae/wan_2.1_vae.safetensors" \
 && wget --progress=dot:giga -O /comfyui/models/clip_vision/clip_vision_h.safetensors \
      "$BASE/clip_vision/clip_vision_h.safetensors"
