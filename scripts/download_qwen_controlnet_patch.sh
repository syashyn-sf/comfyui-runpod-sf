#!/bin/bash

cd "$(dirname "$0")"

download() {
    url="$1"
    dest="$2"
    
    mkdir -p "$(dirname "$dest")"
    
    if [ -f "$dest" ]; then
        echo "Skip: $(basename "$dest") exists"
        return
    fi
    
    echo "Downloading $(basename "$dest")..."
    wget --show-progress -q -O "$dest" "$url" || curl -L --progress-bar -o "$dest" "$url"
}

download "https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_fp8_e4m3fn.safetensors" \
    "ComfyUI/models/diffusion_models/qwen_image_fp8_e4m3fn.safetensors"

download "https://huggingface.co/Comfy-Org/Qwen-Image-DiffSynth-ControlNets/resolve/main/split_files/model_patches/qwen_image_canny_diffsynth_controlnet.safetensors" \
    "ComfyUI/models/model_patches/qwen_image_canny_diffsynth_controlnet.safetensors"

download "https://huggingface.co/Comfy-Org/Qwen-Image-DiffSynth-ControlNets/resolve/main/split_files/model_patches/qwen_image_depth_diffsynth_controlnet.safetensors" \
    "ComfyUI/models/model_patches/qwen_image_depth_diffsynth_controlnet.safetensors"

download "https://huggingface.co/Comfy-Org/Qwen-Image-DiffSynth-ControlNets/resolve/main/split_files/model_patches/qwen_image_inpaint_diffsynth_controlnet.safetensors" \
    "ComfyUI/models/model_patches/qwen_image_inpaint_diffsynth_controlnet.safetensors"

download "https://huggingface.co/lightx2v/Qwen-Image-Lightning/resolve/main/Qwen-Image-Lightning-4steps-V1.0.safetensors" \
    "ComfyUI/models/loras/Qwen-Image-Lightning-4steps-V1.0.safetensors"

download "https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors" \
    "ComfyUI/models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors"

download "https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors" \
    "ComfyUI/models/vae/qwen_image_vae.safetensors"

echo "Done"
