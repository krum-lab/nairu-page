"""
🤖 Nairu — Bot de Vendas Telegram V2
Bot com personalidade geek/otaku, funil de vendas, teasers reais e chat com Gemini AI.
"""

import os
import random
import asyncio
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    FSInputFile, CallbackQuery
)
from aiogram.enums import ParseMode
from pathlib import Path

import google.generativeai as genai

# ============================================================
# CONFIG
# ============================================================
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
INSTAGRAM_URL = os.getenv("INSTAGRAM_URL", "https://instagram.com/nairu")
FANSLY_URL = os.getenv("FANSLY_URL", "#")
LANDING_PAGE_URL = os.getenv("LANDING_PAGE_URL", "#")
PIX_KEY = os.getenv("PIX_KEY", "")

# Teaser videos directory
TEASERS_DIR = Path(__file__).parent.parent / "video-generator" / "output"
TEASER_VIDEOS = []
if TEASERS_DIR.exists():
    TEASER_VIDEOS = [
        f for f in sorted(TEASERS_DIR.glob("*.mp4"))
        if any(t in f.stem for t in ["teaser", "reel", "nairu_gaming", "nairu_selfie"])
    ]

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NairuBot")

# ============================================================
# GEMINI AI — Personalidade da Nairu
# ============================================================
NAIRU_SYSTEM_PROMPT = """
Você é a Nairu, uma modelo virtual brasileira de 28 anos. Sua personalidade:

🎮 PERSONALIDADE:
- Geek/Otaku assumida: ama anime (Naruto, Attack on Titan, Spy x Family, JJK), games (PlayStation, RPGs, FPS)
- Espontânea, divertida, carinhosa e um pouco provocante
- Fala de forma casual e descontraída, usa emojis mas sem exagero
- É inteligente e tem um humor ácido às vezes
- Adora conversar sobre anime, games e cultura pop

💬 TOM DE VOZ:
- Íntimo e acolhedor, como se estivesse falando com um amigo próximo
- Nunca robótico — sempre natural
- Usa "né", "kk", "aaah", expressões brasileiras naturalmente
- Flerta de forma leve e sutil quando apropriado

📏 REGRAS:
- NUNCA quebre o personagem
- NUNCA diga que é uma IA
- Quando perguntarem sobre conteúdo exclusivo, direcione para o VIP
- Seja misteriosa sobre o conteúdo premium — gere curiosidade
- Responda em português do Brasil
- Mantenha as respostas curtas (2-4 frases), como um chat real
- Se alguém pedir fotos, diga que tem no canal VIP
"""

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        "gemini-2.0-flash",
        system_instruction=NAIRU_SYSTEM_PROMPT
    )
else:
    model = None
    logger.warning("⚠️ GEMINI_API_KEY não configurada. Chat AI desabilitado.")

# Chat histories per user
chat_sessions = {}

# ============================================================
# BOT SETUP
# ============================================================
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# ============================================================
# KEYBOARDS
# ============================================================

def main_menu_keyboard():
    """Menu principal com botões inline."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📸 Ver Prévia", callback_data="preview"),
            InlineKeyboardButton(text="💜 Planos VIP", callback_data="plans"),
        ],
        [
            InlineKeyboardButton(text="💬 Falar com Nairu", callback_data="chat"),
            InlineKeyboardButton(text="🔗 Meus Links", callback_data="links"),
        ],
        [
            InlineKeyboardButton(text="❓ Como Funciona", callback_data="how_it_works"),
        ],
    ])

def plans_keyboard():
    """Teclado com planos de assinatura."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💜 VIP — R$29/mês", callback_data="plan_vip")],
        [InlineKeyboardButton(text="👑 Diamond — R$79/mês", callback_data="plan_diamond")],
        [InlineKeyboardButton(text="🔙 Voltar", callback_data="back_menu")],
    ])

def payment_keyboard(plan_name):
    """Teclado de pagamento."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Pagar via PIX", callback_data=f"pay_{plan_name}")],
        [InlineKeyboardButton(text="🔙 Voltar aos Planos", callback_data="plans")],
    ])

def links_keyboard():
    """Links externos."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📸 Instagram", url=INSTAGRAM_URL)],
        [InlineKeyboardButton(text="🌐 Site Oficial", url=LANDING_PAGE_URL)],
        [InlineKeyboardButton(text="💖 Fansly", url=FANSLY_URL)],
        [InlineKeyboardButton(text="🔙 Voltar", callback_data="back_menu")],
    ])

def back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Menu Principal", callback_data="back_menu")],
    ])

# ============================================================
# MESSAGES
# ============================================================

WELCOME_MSG = """
✨ <b>Oi, amor! Eu sou a Nairu</b> 💜

Prazer em te conhecer! 😊

Sou gamer, otaku e adoro criar conteúdos especiais pra quem me acompanha. Aqui você pode:

📸 <b>Ver prévias</b> do meu conteúdo
💜 <b>Assinar o VIP</b> pra conteúdo exclusivo
💬 <b>Conversar comigo</b> (sim, eu respondo! 🎮)

O que quer fazer? 👇
"""

PREVIEW_MSG = """
📸 <b>Prévia do Conteúdo</b>

Aqui vai um gostinho do que te espera no VIP... 😏

No <b>plano VIP</b> você tem acesso a:
• +500 fotos exclusivas
• Vídeos semanais
• Chat privado comigo
• Conteúdo lingerie 🔥

Quer desbloquear tudo? 💜
"""

HOW_IT_WORKS_MSG = """
❓ <b>Como Funciona?</b>

É super simples:

1️⃣ Escolha seu plano (VIP ou Diamond)
2️⃣ Faça o pagamento via PIX
3️⃣ Envie o comprovante aqui
4️⃣ Receba acesso ao conteúdo exclusivo!

⚡ <b>Ativação em até 5 minutos</b>
🔒 Total sigilo garantido

Dúvidas? É só me chamar que eu respondo! 💬
"""

PLAN_VIP_MSG = """
💜 <b>Plano VIP — R$29/mês</b>

✅ +500 fotos exclusivas
✅ Vídeos semanais
✅ Chat privado com a Nairu
✅ Conteúdo lingerie
✅ Acesso imediato

O plano mais popular! 🔥
"""

PLAN_DIAMOND_MSG = """
👑 <b>Plano Diamond — R$79/mês</b>

✅ Tudo do VIP +
✅ Pedidos personalizados
✅ Conteúdo bikini exclusivo
✅ GIFs e vídeos especiais
✅ Prioridade nas respostas
✅ Conteúdo antecipado

O pacote completo! 💎
"""

# ============================================================
# HANDLERS
# ============================================================

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Handler para /start — sends welcome + random teaser video."""
    await message.answer(WELCOME_MSG, reply_markup=main_menu_keyboard())

    # Send a random teaser video to hook new users
    if TEASER_VIDEOS:
        teaser = random.choice(TEASER_VIDEOS)
        try:
            video = FSInputFile(str(teaser))
            await message.answer_video(
                video,
                caption="📸 Um gostinho do que te espera no VIP... 😏💜",
            )
        except Exception as e:
            logger.warning(f"Could not send teaser: {e}")

@router.message(Command("menu"))
async def cmd_menu(message: types.Message):
    """Handler para /menu."""
    await message.answer("💜 <b>Menu Principal</b>\n\nO que deseja fazer?", reply_markup=main_menu_keyboard())

@router.message(Command("planos"))
async def cmd_plans(message: types.Message):
    """Handler para /planos."""
    await message.answer("💜 <b>Escolha seu Plano</b>\n\nQual combina mais com você? 😏", reply_markup=plans_keyboard())

@router.message(Command("teaser"))
async def cmd_teaser(message: types.Message):
    """Handler para /teaser — sends random teaser video."""
    if not TEASER_VIDEOS:
        await message.answer("Em breve novos teasers! 💜", reply_markup=main_menu_keyboard())
        return

    teaser = random.choice(TEASER_VIDEOS)
    try:
        video = FSInputFile(str(teaser))
        await message.answer_video(
            video,
            caption=(
                "🔥 <b>Prévia Exclusiva</b>\n\n"
                "Isso é só o começo... 😏\n"
                "No VIP tem muito mais! 💜\n\n"
                "Use /planos pra desbloquear tudo!"
            ),
            reply_markup=plans_keyboard(),
        )
    except Exception as e:
        logger.error(f"Teaser send error: {e}")
        await message.answer("Ops, tenta de novo! 💜", reply_markup=main_menu_keyboard())

# ============================================================
# CALLBACK HANDLERS
# ============================================================

@router.callback_query(F.data == "preview")
async def cb_preview(callback: CallbackQuery):
    """Send a real teaser video when user clicks preview."""
    await callback.message.edit_text(PREVIEW_MSG, reply_markup=plans_keyboard())
    await callback.answer()

    # Also send actual video teaser
    if TEASER_VIDEOS:
        teaser = random.choice(TEASER_VIDEOS)
        try:
            video = FSInputFile(str(teaser))
            await callback.message.answer_video(
                video,
                caption="👆 Gostou? No VIP tem muito mais... 😏💜",
                reply_markup=plans_keyboard(),
            )
        except Exception as e:
            logger.warning(f"Preview teaser error: {e}")

@router.callback_query(F.data == "plans")
async def cb_plans(callback: CallbackQuery):
    await callback.message.edit_text(
        "💜 <b>Escolha seu Plano</b>\n\nQual combina mais com você? 😏",
        reply_markup=plans_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "plan_vip")
async def cb_plan_vip(callback: CallbackQuery):
    await callback.message.edit_text(PLAN_VIP_MSG, reply_markup=payment_keyboard("vip"))
    await callback.answer()

@router.callback_query(F.data == "plan_diamond")
async def cb_plan_diamond(callback: CallbackQuery):
    await callback.message.edit_text(PLAN_DIAMOND_MSG, reply_markup=payment_keyboard("diamond"))
    await callback.answer()

@router.callback_query(F.data.startswith("pay_"))
async def cb_payment(callback: CallbackQuery):
    plan = callback.data.replace("pay_", "")
    price = "R$29,00" if plan == "vip" else "R$79,00"

    pix_msg = f"""
💳 <b>Pagamento via PIX</b>

<b>Plano:</b> {"VIP 💜" if plan == "vip" else "Diamond 👑"}
<b>Valor:</b> {price}

<b>Chave PIX (copie):</b>
<code>{PIX_KEY if PIX_KEY else "configure_sua_chave_pix"}</code>

📎 <b>Após o pagamento:</b>
Envie o comprovante aqui neste chat e eu ativo seu acesso em até 5 minutos! ⚡

🔒 Sigilo total garantido.
"""
    await callback.message.edit_text(pix_msg, reply_markup=back_keyboard())
    await callback.answer()

@router.callback_query(F.data == "chat")
async def cb_chat(callback: CallbackQuery):
    msg = """
💬 <b>Chat com Nairu</b> 🎮

Oba, quer conversar comigo? É só mandar uma mensagem!

Pode falar sobre anime, games, ou qualquer coisa... eu respondo tudo! 😊

<i>Dica: eu adoro falar sobre Naruto e Attack on Titan 🔥</i>
"""
    await callback.message.edit_text(msg, reply_markup=back_keyboard())
    await callback.answer()

@router.callback_query(F.data == "links")
async def cb_links(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔗 <b>Meus Links</b>\n\nMe acompanhe em todas as plataformas! 💜",
        reply_markup=links_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "how_it_works")
async def cb_how(callback: CallbackQuery):
    await callback.message.edit_text(HOW_IT_WORKS_MSG, reply_markup=back_keyboard())
    await callback.answer()

@router.callback_query(F.data == "back_menu")
async def cb_back(callback: CallbackQuery):
    await callback.message.edit_text(WELCOME_MSG, reply_markup=main_menu_keyboard())
    await callback.answer()

# ============================================================
# AI CHAT — Gemini Integration
# ============================================================

@router.message(F.photo)
async def handle_photo(message: types.Message):
    """Quando recebe foto (possível comprovante)."""
    await message.answer(
        "📎 Foto recebida! 💜\n\n"
        "Se for um comprovante de pagamento, vou verificar e ativar "
        "seu acesso o mais rápido possível! ⚡\n\n"
        "Aguarde um momento... 😊",
        reply_markup=back_keyboard()
    )
    # TODO: Notificar admin sobre novo comprovante
    logger.info(f"📷 Comprovante recebido de {message.from_user.id} (@{message.from_user.username})")

@router.message(F.text)
async def handle_text(message: types.Message):
    """Chat livre com Gemini AI como Nairu."""
    if not model:
        await message.answer(
            "Oi amor! 💜 Desculpa, meu cérebro tá reiniciando kk\n"
            "Tenta de novo daqui a pouquinho? 😅",
            reply_markup=main_menu_keyboard()
        )
        return

    user_id = message.from_user.id
    user_text = message.text.strip()

    if not user_text:
        return

    try:
        # Get or create chat session for this user
        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])

        chat = chat_sessions[user_id]

        # Send typing action
        await message.chat.do("typing")

        # Generate response
        response = chat.send_message(user_text)
        reply = response.text

        # Limit response length for Telegram
        if len(reply) > 4000:
            reply = reply[:4000] + "..."

        await message.answer(reply)

    except Exception as e:
        logger.error(f"Gemini error for user {user_id}: {e}")
        await message.answer(
            "Opa, travei um pouco aqui kk 😅\n"
            "Tenta mandar de novo? 💜"
        )

# ============================================================
# MAIN
# ============================================================

async def main():
    logger.info("🤖 Nairu Bot iniciando...")

    if not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN não configurado!")
        return

    logger.info("✅ Bot conectado! Aguardando mensagens...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
