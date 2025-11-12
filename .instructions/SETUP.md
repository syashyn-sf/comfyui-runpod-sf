# RunPod Setup

## 1. Add Secrets

[RunPod → Secrets](https://www.runpod.io/console/secrets)

```
HF_TOKEN = hf_xxxxxxxxxxxxxxxxxxxx
CIVITAI_API_KEY = xxxxxxxxxxxxxxxxxxxx
GOOGLE_DRIVE_SA_JSON = {"type":"service_account",...}  (optional)
COMFYUI_ADMIN_KEY = your-admin-token  (optional)
```

## 2. Create Template

[RunPod → Templates](https://www.runpod.io/console/templates)

```
Container Image: serhiiyashyn/comfyui-runpod-sf:latest
Volume Mount: /workspace
Volume Size: 100GB
Expose Ports: 7777, 8188
Secrets: Select HF_TOKEN, CIVITAI_API_KEY, and optional secrets
```

## 3. Deploy Pod

Choose GPU: RTX 4090/5090, A100, H100, or L40S

## 4. Access

**Control Panel:**
```
https://<pod-id>-7777.proxy.runpod.net
```

1. Select user (default: `serhii`)
2. Click "Launch ComfyUI"
3. Wait 2-3 minutes
4. Click "Open ComfyUI"

**ComfyUI:**
```
https://<pod-id>-8188.proxy.runpod.net
```

## Add Users

**Via Control Panel:**
- Click "+ Add User"
- Enter username and admin token
- Done

**Via SSH:**
```bash
python3 -c "
import json, os
users_file = '/workspace/user_data/users.json'
os.makedirs('/workspace/user_data', exist_ok=True)
users = json.load(open(users_file)) if os.path.exists(users_file) else []
users.append('username')
json.dump(users, open(users_file, 'w'))
for d in ['input', 'output', 'workflows']:
    os.makedirs(f'/workspace/{d}/username', exist_ok=True)
"
```

## Troubleshooting

**Pod won't start:** Check logs, verify secrets set

**502 error:** Wait 2-3 minutes for Flask to start

**ComfyUI won't launch:** Check `/workspace/comfyui.log` and `/workspace/ui.log`

**Google Drive not syncing:** Check `/tmp/rclone_sync.log`

## More Info

- [Google Drive Setup](GOOGLE_DRIVE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [GPU Support](../docs/GPU_SUPPORT.md)
