# ComfyUI RunPod - Stillfront

Production ComfyUI for RunPod with multi-user support and Google Drive sync.

## Quick Start

**Docker Image:**
```
serhiiyashyn/comfyui-runpod-sf:latest
```

**Required RunPod Secrets:**
- `HF_TOKEN` - Hugging Face token
- `CIVITAI_API_KEY` - CivitAI API key

**Optional Secrets:**
- `GOOGLE_DRIVE_SA_JSON` - Google Drive service account
- `COMFYUI_ADMIN_KEY` - Admin token for user management

**Access:**
- Control Panel: `https://<pod-id>-7777.proxy.runpod.net`
- ComfyUI: `https://<pod-id>-8188.proxy.runpod.net`

## Setup

See [.instructions/SETUP.md](.instructions/SETUP.md)

## Build

```bash
./build.sh
docker push yourusername/comfyui-runpod-sf:latest
```

## License

Based on [wolfgrimmm/comfyui-runpod-installer](https://github.com/wolfgrimmm/comfyui-runpod-installer)
© 2025 Stillfront
