import torch

from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import create_pan_cameras, decode_latent_images, gif_widget
from shap_e.util.notebooks import decode_latent_mesh

def generate_local_model(prompt_string, stream_id):
    torch.cuda.is_available()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    xm = load_model('transmitter', device = device)
    model = load_model('text300M', device = device)
    diffusion = diffusion_from_config(load_config('diffusion'))

    batch_size = 1
    guidance_scale = 15.0
    prompt = prompt_string

    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(texts=[prompt] * batch_size),
        progress=True,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=256,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0,
    )

    for i, latent in enumerate(latents):
        t = decode_latent_mesh(xm, latent).tri_mesh()

        with open(str(stream_id)+".obj",'w') as f:
            t.write_obj(f)

    return str(stream_id)+'.obj'
