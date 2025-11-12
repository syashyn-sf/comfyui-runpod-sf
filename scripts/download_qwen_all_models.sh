#!/bin/bash

# Combined Qwen Model Download Script
# Downloads all Qwen-Image models including Edit, Generation, and ControlNet variants

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

echo "================================================"
echo "Qwen Model Download - All Variants"
echo "================================================"

# Core Models (shared across all workflows)
echo ""
echo "📦 Downloading Core Models..."
echo "------------------------------------------------"

download "https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors" \
    "/workspace/models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors"

download "https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors" \
    "/workspace/models/vae/qwen_image_vae.safetensors"

# Lightning LoRA (acceleration)
download "https://huggingface.co/lightx2v/Qwen-Image-Lightning/resolve/main/Qwen-Image-Lightning-4steps-V1.0.safetensors" \
    "/workspace/models/loras/Qwen-Image-Lightning-4steps-V1.0.safetensors"

# Diffusion Models
echo ""
echo "🎨 Downloading Diffusion Models..."
echo "------------------------------------------------"

# Standard Qwen-Image model
download "https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_fp8_e4m3fn.safetensors" \
    "/workspace/models/diffusion_models/qwen_image_fp8_e4m3fn.safetensors"

# Distilled version (faster, unofficial)
download "https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/non_official/diffusion_models/qwen_image_distill_full_fp8_e4m3fn.safetensors" \
    "/workspace/models/diffusion_models/qwen_image_distill_full_fp8_e4m3fn.safetensors"

# Qwen-Image-Edit model (2509)
download "https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_edit_2509_fp8_e4m3fn.safetensors" \
    "/workspace/models/diffusion_models/qwen_image_edit_2509_fp8_e4m3fn.safetensors"

# Edit Lightning LoRA
download "https://huggingface.co/lightx2v/Qwen-Image-Lightning/resolve/main/Qwen-Image-Edit-2509/Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors" \
    "/workspace/models/loras/Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors"

# ControlNets - InstantX Union
echo ""
echo "🎮 Downloading ControlNets - InstantX..."
echo "------------------------------------------------"

download "https://huggingface.co/Comfy-Org/Qwen-Image-InstantX-ControlNets/resolve/main/split_files/controlnet/Qwen-Image-InstantX-ControlNet-Union.safetensors" \
    "/workspace/models/controlnet/Qwen-Image-InstantX-ControlNet-Union.safetensors"

download "https://huggingface.co/Comfy-Org/Qwen-Image-InstantX-ControlNets/resolve/main/split_files/controlnet/Qwen-Image-InstantX-ControlNet-Inpainting.safetensors" \
    "/workspace/models/controlnet/Qwen-Image-InstantX-ControlNet-Inpainting.safetensors"

# ControlNets - DiffSynth (Model Patches)
echo ""
echo "🔧 Downloading ControlNets - DiffSynth..."
echo "------------------------------------------------"

download "https://huggingface.co/Comfy-Org/Qwen-Image-DiffSynth-ControlNets/resolve/main/split_files/model_patches/qwen_image_canny_diffsynth_controlnet.safetensors" \
    "/workspace/models/model_patches/qwen_image_canny_diffsynth_controlnet.safetensors"

download "https://huggingface.co/Comfy-Org/Qwen-Image-DiffSynth-ControlNets/resolve/main/split_files/model_patches/qwen_image_depth_diffsynth_controlnet.safetensors" \
    "/workspace/models/model_patches/qwen_image_depth_diffsynth_controlnet.safetensors"

download "https://huggingface.co/Comfy-Org/Qwen-Image-DiffSynth-ControlNets/resolve/main/split_files/model_patches/qwen_image_inpaint_diffsynth_controlnet.safetensors" \
    "/workspace/models/model_patches/qwen_image_inpaint_diffsynth_controlnet.safetensors"

echo ""
echo "================================================"
echo "✅ All Qwen models downloaded successfully!"
echo "================================================"
echo ""
echo "Model Summary:"
echo "  • Text Encoders: 1"
echo "  • VAE: 1"
echo "  • Diffusion Models: 3 (standard, distilled, edit)"
echo "  • LoRAs: 2 (Lightning 4-step)"
echo "  • ControlNets: 2 (InstantX Union, Inpainting)"
echo "  • Model Patches: 3 (DiffSynth Canny, Depth, Inpaint)"
echo ""
