# 🎨 Nairu — Biblioteca de Prompts

> Prompts otimizados para gerar imagens consistentes da Nairu.
> Use com: Stable Diffusion, ComfyUI, SeaArt, LeonardoAI (ferramentas grátis).
> Futuramente: RenderNet AI (FaceLock ativado).

---

## Base Prompt (sempre incluir)

```
photorealistic photo of a 28-year-old Brazilian woman, long straight black 
shiny hair, green-hazel eyes with visible iris details, warm golden tan skin, 
clear smooth skin without freckles, well-defined natural dark eyebrows, 
subtle natural makeup with lip gloss, delicate layered gold necklaces, 
ultra realistic skin texture with visible pores, 8K DSLR professional photography
```

## Negative Prompt (sempre incluir)

```
freckles, spots, blemishes, unrealistic skin, plastic skin, cartoon, 
illustration, painting, drawing, anime style, 3d render, deformed, 
bad anatomy, extra fingers, bad hands, blurry, low quality, watermark, 
text, logo, oversaturated
```

---

## 🎮 Gaming Setup

```
[BASE PROMPT], wearing a white casual t-shirt, sitting in a red and black 
gaming chair, holding a PlayStation controller, gaming setup room with RGB LED 
lights in purple and blue, dual monitors showing a game, gaming PC with RGB, 
anime posters and action figures on shelves in background, warm smile, 
natural expression, soft ambient lighting
```

## 📸 Selfie Casual (Quarto)

```
[BASE PROMPT], selfie perspective from slightly above, wearing a blue crop top, 
laying on a bed with beige and cream pillows, warm natural window lighting, 
charming flirty smile, relaxed natural pose, cozy bedroom atmosphere, 
wooden headboard visible, iPhone selfie angle
```

## 🌸 Lifestyle Otaku

```
[BASE PROMPT], wearing a cute oversized anime t-shirt and comfortable shorts, 
sitting cross-legged on a bean bag, reading a manga volume, surrounded by 
manga bookshelves, soft warm desk lamp lighting, cozy room with anime 
decorations, natural relaxed expression, comfortable at-home atmosphere
```

## 🖤 Cyberpunk / Dark Mood (Hero)

```
[BASE PROMPT], wearing a stylish black crop top with subtle details, 
dramatic cinematic lighting with purple and blue neon glow from behind, 
dark moody cyberpunk atmosphere, confident seductive gaze looking at camera, 
gold layered necklaces catching light, dark background with bokeh neon lights, 
high fashion editorial photography style
```

## 👙 Bikini / Praia

```
[BASE PROMPT], wearing a trendy black bikini, standing on a tropical beach 
at golden hour, ocean waves in background, warm sunset lighting, natural 
wind-blown hair, confident relaxed pose, sun-kissed skin with natural glow, 
beach lifestyle photography
```

## 🩱 Lingerie (VIP)

```
[BASE PROMPT], wearing elegant black lace lingerie, sitting on a bed with 
white satin sheets, soft warm bedroom lighting, candles in background creating 
bokeh, tasteful and artistic composition, elegant feminine pose, 
confident expression, boudoir photography style
```

## 🎭 Cosplay Casual

```
[BASE PROMPT], wearing a casual cosplay inspired by [PERSONAGEM], in a 
bedroom with anime decorations, LED strip lights, playful pose, fun 
expression, convention-ready look, natural lighting mixed with colored 
LED accent lights
```

## 🪞 Espelho / Mirror Selfie

```
[BASE PROMPT], mirror selfie in a stylish bedroom, wearing a fitted casual 
outfit, phone visible in reflection, full body visible, bedroom with modern 
decor, natural daylight from window, candid authentic style, Instagram-ready 
composition
```

## 🎥 Close-up (Olhos)

```
extreme macro close-up of a 28-year-old Brazilian woman's face, focusing on 
stunning green-hazel eyes with detailed iris patterns and natural light 
reflections, long dark eyelashes with natural mascara, perfectly groomed 
dark eyebrows, clear warm golden tan skin showing realistic pores and skin 
texture, straight black hair strands framing face, soft natural diffused 
lighting, indistinguishable from real photograph, 8K ultra detailed 
macro photography
```

---

## 📐 Configurações Recomendadas (Stable Diffusion)

| Parâmetro | Valor |
|---|---|
| **Modelo** | Epic Realism Natural Sin ou CyberRealistic |
| **Sampler** | DPM++ 2M Karras |
| **Steps** | 30-40 |
| **CFG Scale** | 7 |
| **Resolução** | 768x1024 (portrait) ou 1024x1024 (square) |
| **Upscaler** | 4x-UltraSharp ou ESRGAN_4x |

---

## 💡 Dicas de Consistência

1. **Sempre use o Base Prompt** como início
2. **Sempre use o Negative Prompt** completo
3. **Seed fixa**: após achar um rosto bom, anote o seed e reutilize
4. **LoRA**: se usar ComfyUI, treine um LoRA com 10-15 imagens boas
5. **FaceLock**: no RenderNet AI (futuro), ative para manter a identidade
6. **Inpainting**: use para corrigir detalhes sem refazer a imagem toda
