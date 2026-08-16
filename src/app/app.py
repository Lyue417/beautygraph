import base64
from html import escape
from pathlib import Path
import sys

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from src.similarity.engine import (
    get_top_similar_products,
    load_similarity_inputs,
)
from src.similarity.comparison import build_product_comparison


st.set_page_config(
    page_title="BeautyGraph",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

ASSET_DIR = Path(__file__).parent / "assets"

FUNCTION_LABELS = {
    "humectant": "Humectant",
    "emollient": "Emollient",
    "occlusive": "Occlusive",
    "barrier_supporting": "Barrier supporting",
    "soothing": "Soothing",
    "antioxidant": "Antioxidant",
    "texture_viscosity": "Texture / viscosity",
    "preservative": "Preservative",
    "fragrance_related": "Fragrance related",
    "active_treatment": "Active treatment",
}


# ---------------------------------------------------------
# Data
# ---------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_products():
    return load_similarity_inputs()


def product_label(product: dict) -> str:
    return f"{product['brand']} — {product['product_name']}"


def image_data_uri(path: Path) -> str:
    data = base64.b64encode(
        path.read_bytes()
    ).decode("ascii")

    return f"data:image/png;base64,{data}"


def product_form_image(product_form: str):
    normalized = (
        product_form
        .lower()
        .strip()
        .replace("-", "_")
        .replace(" ", "_")
    )

    mapping = {
        "cream": "cream.png",
        "rich_cream": "cream.png",
        "lotion": "lotion.png",
        "gel": "gel_cream.png",
        "gel_cream": "gel_cream.png",
        "water_cream": "gel_cream.png",
        "balm": "balm.png",
        "ointment": "balm.png",
        "fluid": "fluid.png",
        "milk": "milk.png",
    }

    filename = mapping.get(normalized)

    if filename is None:
        return None

    asset = ASSET_DIR / "product_forms" / filename

    if not asset.exists():
        return None

    return image_data_uri(asset)


products = load_products()


# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------

st.html(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?'
        'family=Cormorant+Garamond:wght@400;500;600&'
        'family=Inter:wght@300;400;500;600&display=swap'
    );

    :root {
        --ivory: #FAF8F2;
        --ivory-deep: #F4F1E8;

        --sage-050: #F3F5F0;
        --sage-100: #E9EEE5;
        --sage-200: #D8E0D2;
        --sage-300: #BAC8B4;
        --sage-400: #A5B39C;
        --sage-500: #7F9278;
        --sage-600: #647963;
        --sage-700: #4F6251;

        --ink: #354038;
        --muted: #777B73;

        --blush: #E8CEC3;
        --blush-soft: #F3E4DE;

        --line: rgba(79, 98, 81, 0.13);
        --white-soft: rgba(255, 255, 255, 0.48);
    }

    html,
    body,
    [class*="css"] {
        font-family: "Inter", -apple-system, BlinkMacSystemFont,
            "Segoe UI", sans-serif;
        color: var(--ink);
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at 8% 18%,
                rgba(210, 222, 205, 0.22),
                transparent 24%
            ),
            radial-gradient(
                ellipse at 91% 41%,
                rgba(232, 206, 195, 0.13),
                transparent 20%
            ),
            var(--ivory);
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"],
    #MainMenu,
    footer {
        display: none !important;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.4rem;
        padding-bottom: 5rem;
    }

    h1,
    h2,
    h3 {
        font-family: "Cormorant Garamond", Georgia, serif !important;
        color: var(--ink);
        letter-spacing: -0.02em;
        font-weight: 500;
    }

    p {
        line-height: 1.7;
    }


    /* --------------------------------------------------
       Navigation
       -------------------------------------------------- */

    .bg-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.65rem 0 1.25rem;
        border-bottom: 1px solid var(--line);
        margin-bottom: 2.3rem;
    }

    .bg-brand {
        font-family: "Cormorant Garamond", Georgia, serif;
        font-size: 2rem;
        font-weight: 600;
        letter-spacing: -0.035em;
        color: var(--sage-700);
    }

    .bg-nav-links {
        display: flex;
        align-items: center;
        gap: 2rem;
        font-size: 0.82rem;
        color: var(--muted);
        letter-spacing: 0.02em;
    }

    .bg-nav-active {
        color: var(--sage-700);
        font-weight: 600;
        position: relative;
    }

    .bg-nav-active::after {
        content: "";
        position: absolute;
        left: 15%;
        right: 15%;
        bottom: -0.62rem;
        height: 1px;
        background: var(--sage-500);
    }


    /* --------------------------------------------------
       Hero
       -------------------------------------------------- */

    .bg-hero {
        position: relative;
        overflow: hidden;
        min-height: 360px;

        display: grid;
        grid-template-columns: 1.05fr 0.95fr;
        align-items: center;
        gap: 3rem;

        padding: 3.4rem 4rem;
        margin-bottom: 3rem;

        background:
            linear-gradient(
                135deg,
                rgba(243, 245, 240, 0.92),
                rgba(250, 248, 242, 0.72)
            );

        border: 1px solid rgba(79, 98, 81, 0.08);
        border-radius: 30px;
    }

    .bg-hero-copy {
        position: relative;
        z-index: 4;
        max-width: 600px;
    }

    .bg-eyebrow {
        margin-bottom: 1rem;

        color: var(--sage-600);

        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .bg-hero-title {
        margin: 0 0 1.25rem;

        font-family: "Cormorant Garamond", Georgia, serif;

        font-size: clamp(3.2rem, 5.2vw, 5.5rem);
        line-height: 0.94;
        font-weight: 500;
        letter-spacing: -0.045em;

        color: var(--sage-700);
    }

    .bg-hero-text {
        max-width: 510px;
        margin: 0;

        color: var(--muted);

        font-size: 1rem;
        line-height: 1.8;
    }


    /* Abstract watercolor-inspired washes only.
       No botanical or other real-object shapes. */

    .bg-wash-area {
        position: relative;
        min-height: 270px;
    }

    .bg-wash {
        position: absolute;

        filter: blur(1.5px);
        opacity: 0.72;
        transform: rotate(-8deg);
    }

    .bg-wash-one {
        width: 72%;
        height: 58%;

        right: 5%;
        top: 8%;

        background:
            radial-gradient(
                ellipse at 36% 40%,
                rgba(165, 179, 156, 0.54),
                rgba(186, 200, 180, 0.25) 54%,
                transparent 73%
            );

        border-radius:
            57% 43% 62% 38% /
            46% 61% 39% 54%;
    }

    .bg-wash-two {
        width: 49%;
        height: 44%;

        right: 29%;
        bottom: 2%;

        background:
            radial-gradient(
                ellipse at 52% 49%,
                rgba(127, 146, 120, 0.25),
                rgba(216, 224, 210, 0.14) 56%,
                transparent 77%
            );

        border-radius:
            38% 62% 41% 59% /
            62% 38% 62% 38%;

        transform: rotate(13deg);
    }

    .bg-hero-art {
        position: absolute;
        z-index: 3;

        width: min(92%, 470px);
        right: 0;
        bottom: -4%;

        object-fit: contain;

        filter:
            drop-shadow(
                0 16px 24px
                rgba(79, 98, 81, 0.08)
            );
    }

    .bg-product-layout {
        position: relative;
        z-index: 2;

        display: grid;
        grid-template-columns: minmax(0, 1fr) 260px;
        gap: 2rem;
        align-items: center;
    }

    .bg-product-copy {
        position: relative;
        z-index: 3;
    }

    .bg-product-art-wrap {
        position: relative;

        display: flex;
        align-items: center;
        justify-content: center;

        min-height: 235px;
    }

    .bg-product-art {
        position: relative;
        z-index: 3;

        display: block;

        width: auto;
        max-width: 230px;
        max-height: 235px;

        object-fit: contain;

        filter:
            drop-shadow(
                0 15px 20px
                rgba(79, 98, 81, 0.08)
            );
    }


    .bg-wash-three {
        width: 42%;
        height: 38%;

        left: 2%;
        bottom: 15%;

        background:
            radial-gradient(
                ellipse at center,
                rgba(232, 206, 195, 0.26),
                rgba(243, 228, 222, 0.10) 61%,
                transparent 78%
            );

        border-radius:
            61% 39% 52% 48% /
            47% 55% 45% 53%;

        transform: rotate(-15deg);
    }


    /* --------------------------------------------------
       Section typography
       -------------------------------------------------- */

    .bg-section-kicker {
        margin-bottom: 0.35rem;

        color: var(--sage-600);

        font-size: 0.69rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .bg-section-title {
        margin-bottom: 0.55rem;

        font-family: "Cormorant Garamond", Georgia, serif;

        color: var(--ink);

        font-size: 2.5rem;
        line-height: 1.05;
    }

    .bg-section-description {
        max-width: 710px;
        margin-bottom: 1.6rem;

        color: var(--muted);

        font-size: 0.92rem;
        line-height: 1.7;
    }


    /* --------------------------------------------------
       Selectbox
       -------------------------------------------------- */

    div[data-baseweb="select"] > div {
        min-height: 52px;

        background: rgba(255, 255, 255, 0.55) !important;

        border: 1px solid var(--line) !important;
        border-radius: 16px !important;

        box-shadow: none !important;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: rgba(79, 98, 81, 0.28) !important;
    }

    [data-testid="stSelectbox"] label {
        color: var(--sage-700) !important;

        font-size: 0.78rem !important;
        font-weight: 500 !important;
    }


    /* --------------------------------------------------
       Product card
       -------------------------------------------------- */

    .bg-product-card {
        position: relative;
        overflow: hidden;

        min-height: 300px;

        padding: 2.3rem 2.5rem;

        background:
            linear-gradient(
                125deg,
                rgba(233, 238, 229, 0.77),
                rgba(250, 248, 242, 0.86)
            );

        border: 1px solid rgba(79, 98, 81, 0.10);
        border-radius: 26px;

        margin-top: 1.4rem;
        margin-bottom: 3.1rem;
    }

    .bg-product-brand {
        color: var(--sage-600);

        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    .bg-product-name {
        max-width: 680px;
        margin: 0.45rem 0 1.3rem;

        font-family: "Cormorant Garamond", Georgia, serif;

        color: var(--ink);

        font-size: clamp(2.5rem, 4vw, 4rem);
        line-height: 0.98;
        letter-spacing: -0.035em;
    }

    .bg-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
    }

    .bg-badge {
        display: inline-flex;
        align-items: center;

        padding: 0.46rem 0.78rem;

        background: rgba(255, 255, 255, 0.55);

        border: 1px solid rgba(79, 98, 81, 0.10);
        border-radius: 999px;

        color: var(--sage-700);

        font-size: 0.69rem;
        font-weight: 600;
        letter-spacing: 0.075em;
        text-transform: uppercase;
    }

    .bg-card-wash {
        position: absolute;

        width: 310px;
        height: 210px;

        right: -35px;
        top: -25px;

        background:
            radial-gradient(
                ellipse at center,
                rgba(165, 179, 156, 0.34),
                rgba(216, 224, 210, 0.13) 56%,
                transparent 76%
            );

        border-radius:
            42% 58% 36% 64% /
            63% 39% 61% 37%;

        transform: rotate(15deg);
        opacity: 0.9;
    }


    /* --------------------------------------------------
       Formula profile
       -------------------------------------------------- */

    .bg-profile-wrap {
        padding: 1.7rem 1.8rem;

        background: rgba(255, 255, 255, 0.40);

        border: 1px solid var(--line);
        border-radius: 22px;
    }

    .bg-profile-row {
        display: grid;
        grid-template-columns: 175px 1fr 58px;
        align-items: center;
        gap: 1rem;

        margin: 0.88rem 0;
    }

    .bg-function-label {
        color: var(--ink);

        font-size: 0.82rem;
        font-weight: 500;
    }

    .bg-function-track {
        height: 8px;
        overflow: hidden;

        background: var(--sage-100);
        border-radius: 999px;
    }

    .bg-function-fill {
        height: 100%;

        background:
            linear-gradient(
                90deg,
                var(--sage-300),
                var(--sage-500)
            );

        border-radius: 999px;
    }

    .bg-function-value {
        color: var(--sage-700);

        font-size: 0.75rem;
        font-weight: 600;
        text-align: right;
    }

    .bg-method-note {
        margin-top: 1.3rem;
        padding-top: 1rem;

        border-top: 1px solid var(--line);

        color: var(--muted);

        font-size: 0.76rem;
        line-height: 1.6;
    }


    /* --------------------------------------------------
       Ingredients
       -------------------------------------------------- */

    .bg-ingredient-grid {
        display: grid;
        grid-template-columns:
            repeat(auto-fit, minmax(240px, 1fr));
        gap: 0.65rem;

        margin-top: 1.2rem;
    }

    .bg-ingredient {
        display: grid;
        grid-template-columns: 35px 1fr;
        align-items: center;
        gap: 0.8rem;

        min-height: 50px;
        padding: 0.55rem 0.8rem;

        background: rgba(255, 255, 255, 0.32);

        border-bottom: 1px solid var(--line);
    }

    .bg-ingredient-number {
        font-family: "Cormorant Garamond", Georgia, serif;

        color: var(--sage-400);

        font-size: 1.15rem;
    }

    .bg-ingredient-name {
        color: var(--ink);

        font-size: 0.79rem;
        line-height: 1.45;
    }


    /* --------------------------------------------------
       Footer note
       -------------------------------------------------- */

    .bg-footer-note {
        margin-top: 4rem;
        padding-top: 1.2rem;

        border-top: 1px solid var(--line);

        color: var(--muted);

        font-size: 0.72rem;
        line-height: 1.65;
    }


    /* --------------------------------------------------
       Mobile
       -------------------------------------------------- */

    @media (max-width: 760px) {
        .block-container {
            padding-left: 1.1rem;
            padding-right: 1.1rem;
        }

        .bg-nav-links {
            display: none;
        }

        .bg-hero {
            grid-template-columns: 1fr;

            padding: 2.4rem 1.7rem;
        }

        .bg-wash-area {
            min-height: 190px;
        }

        .bg-hero-art {
            width: min(78%, 330px);
            right: 8%;
        }

        .bg-product-layout {
            grid-template-columns: 1fr;
        }

        .bg-product-art-wrap {
            min-height: 180px;
        }

        .bg-product-art {
            max-width: 180px;
            max-height: 180px;
        }

        .bg-profile-row {
            grid-template-columns: 125px 1fr 48px;
            gap: 0.6rem;
        }

        .bg-product-card {
            padding: 1.8rem 1.5rem;
        }
    }
    </style>
    """,
)


# ---------------------------------------------------------
# Navigation
# ---------------------------------------------------------

# ---------------------------------------------------------
# Additional UI styles
# ---------------------------------------------------------

st.html(
    """
    <style>
    .bg-nav-links a {
        color: var(--muted);
        text-decoration: none;
        transition: color 0.18s ease;
    }

    .bg-nav-links a:hover {
        color: var(--sage-700);
    }

    .bg-nav-links a.bg-nav-active {
        color: var(--sage-700);
        font-weight: 600;
    }

    .bg-compare-heading {
        max-width: 760px;
        margin-bottom: 2rem;
    }

    .bg-compare-product-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1.2rem 0 2rem;
    }

    .bg-compare-card {
        position: relative;
        overflow: hidden;
        min-height: 220px;
        padding: 1.8rem;
        border-radius: 24px;
        border: 1px solid var(--line);
    }

    .bg-compare-card-a {
        background:
            linear-gradient(
                135deg,
                rgba(216, 224, 210, 0.76),
                rgba(250, 248, 242, 0.84)
            );
    }

    .bg-compare-card-b {
        background:
            linear-gradient(
                135deg,
                rgba(243, 228, 222, 0.68),
                rgba(250, 248, 242, 0.88)
            );
    }

    .bg-compare-label {
        margin-bottom: 0.65rem;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .bg-compare-card-a .bg-compare-label {
        color: var(--sage-600);
    }

    .bg-compare-card-b .bg-compare-label {
        color: #9A746A;
    }

    .bg-compare-brand {
        margin-bottom: 0.35rem;
        color: var(--muted);
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .bg-compare-name {
        max-width: 520px;
        font-family: "Cormorant Garamond", Georgia, serif;
        color: var(--ink);
        font-size: clamp(2rem, 3vw, 3.2rem);
        line-height: 1;
        letter-spacing: -0.035em;
    }

    .bg-compare-card-copy {
        position: relative;
        z-index: 3;

        max-width: calc(100% - 135px);
    }

    .bg-compare-art {
        position: absolute;

        z-index: 2;

        width: auto;
        max-width: 125px;
        max-height: 125px;

        right: 1.1rem;
        bottom: 0.9rem;

        object-fit: contain;

        opacity: 0.94;

        filter:
            drop-shadow(
                0 10px 14px
                rgba(79, 98, 81, 0.07)
            );
    }


    .bg-compare-form {
        display: inline-flex;
        margin-top: 1.2rem;
        padding: 0.42rem 0.72rem;
        border: 1px solid rgba(79, 98, 81, 0.11);
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.45);
        color: var(--sage-700);
        font-size: 0.67rem;
        font-weight: 600;
        letter-spacing: 0.07em;
        text-transform: uppercase;
    }

    .bg-score-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.85rem;
        margin: 1.2rem 0 3rem;
    }

    .bg-score-card {
        padding: 1.4rem 1.45rem;
        background: rgba(255, 255, 255, 0.40);
        border: 1px solid var(--line);
        border-radius: 20px;
    }

    .bg-score-card-primary {
        background:
            linear-gradient(
                135deg,
                rgba(216, 224, 210, 0.65),
                rgba(255, 255, 255, 0.38)
            );
    }

    .bg-score-label {
        min-height: 2.2rem;
        margin-bottom: 0.5rem;
        color: var(--muted);
        font-size: 0.71rem;
        font-weight: 500;
        line-height: 1.4;
    }

    .bg-score-value {
        font-family: "Cormorant Garamond", Georgia, serif;
        color: var(--sage-700);
        font-size: 2.6rem;
        line-height: 1;
    }

    .bg-score-track {
        height: 6px;
        margin-top: 1rem;
        overflow: hidden;
        background: var(--sage-100);
        border-radius: 999px;
    }

    .bg-score-fill {
        height: 100%;
        border-radius: 999px;
        background:
            linear-gradient(
                90deg,
                var(--sage-300),
                var(--sage-500)
            );
    }

    .bg-compare-columns {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0 3rem;
    }

    .bg-detail-card {
        padding: 1.45rem 1.5rem;
        background: rgba(255, 255, 255, 0.36);
        border: 1px solid var(--line);
        border-radius: 21px;
    }

    .bg-detail-card-a {
        border-top: 3px solid rgba(127, 146, 120, 0.50);
    }

    .bg-detail-card-b {
        border-top: 3px solid rgba(210, 166, 153, 0.42);
    }

    .bg-detail-title {
        margin-bottom: 1rem;
        font-family: "Cormorant Garamond", Georgia, serif;
        color: var(--ink);
        font-size: 1.55rem;
        line-height: 1.1;
    }

    .bg-chip-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
    }

    .bg-chip {
        display: inline-flex;
        padding: 0.38rem 0.65rem;
        background: var(--sage-050);
        border: 1px solid rgba(79, 98, 81, 0.09);
        border-radius: 999px;
        color: var(--ink);
        font-size: 0.7rem;
        line-height: 1.2;
    }

    .bg-chip-blush {
        background: var(--blush-soft);
        border-color: rgba(154, 116, 106, 0.10);
    }

    .bg-shared-card {
        padding: 1.5rem;
        margin-bottom: 3rem;
        background:
            linear-gradient(
                135deg,
                rgba(233, 238, 229, 0.62),
                rgba(255, 255, 255, 0.34)
            );
        border: 1px solid var(--line);
        border-radius: 22px;
    }

    .bg-shared-summary {
        margin-bottom: 1rem;
        color: var(--muted);
        font-size: 0.79rem;
    }

    .bg-diff-row {
        display: grid;
        grid-template-columns: 170px 1fr 1fr;
        gap: 1rem;
        align-items: center;
        padding: 0.9rem 0;
        border-bottom: 1px solid var(--line);
    }

    .bg-diff-row:last-child {
        border-bottom: none;
    }

    .bg-diff-function {
        color: var(--ink);
        font-size: 0.77rem;
        font-weight: 500;
    }

    .bg-diff-value-a,
    .bg-diff-value-b {
        font-size: 0.75rem;
        font-weight: 600;
    }

    .bg-diff-value-a {
        color: var(--sage-600);
    }

    .bg-diff-value-b {
        color: #9A746A;
    }

    .bg-explanation {
        position: relative;
        overflow: hidden;

        padding: 2.3rem 2.4rem;
        margin: 1rem 0 3rem;

        background:
            linear-gradient(
                135deg,
                rgba(216, 224, 210, 0.62),
                rgba(243, 228, 222, 0.25),
                rgba(250, 248, 242, 0.78)
            );

        border: 1px solid var(--line);
        border-radius: 26px;
    }

    .bg-explanation-lead {
        position: relative;
        z-index: 2;

        max-width: 920px;
        margin-bottom: 1.8rem;

        font-family: "Cormorant Garamond", Georgia, serif;

        color: var(--ink);

        font-size: clamp(1.55rem, 2.2vw, 2.15rem);
        line-height: 1.25;
        letter-spacing: -0.02em;
    }

    .bg-explanation-lead strong {
        color: var(--sage-700);
        font-weight: 600;
    }

    .bg-explanation-grid {
        position: relative;
        z-index: 2;

        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
    }

    .bg-explanation-point {
        padding: 1.15rem 1.2rem;

        background: rgba(255, 255, 255, 0.38);

        border: 1px solid rgba(79, 98, 81, 0.09);
        border-radius: 18px;
    }

    .bg-explanation-point-label {
        margin-bottom: 0.55rem;

        color: var(--sage-600);

        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.11em;
        text-transform: uppercase;
    }

    .bg-explanation-point-text {
        color: var(--ink);

        font-size: 0.82rem;
        line-height: 1.65;
    }

    .bg-explanation-note {
        position: relative;
        z-index: 2;

        margin-top: 1.3rem;
        padding-top: 1rem;

        border-top: 1px solid var(--line);

        color: var(--muted);

        font-size: 0.72rem;
        line-height: 1.6;
    }

    .bg-query-card {
        position: relative;
        overflow: hidden;

        padding: 1.7rem 1.9rem;
        margin: 1.3rem 0 2.6rem;

        background:
            linear-gradient(
                135deg,
                rgba(216, 224, 210, 0.67),
                rgba(250, 248, 242, 0.84)
            );

        border: 1px solid var(--line);
        border-radius: 23px;
    }

    .bg-query-brand {
        margin-bottom: 0.35rem;

        color: var(--sage-600);

        font-size: 0.67rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .bg-query-name {
        font-family: "Cormorant Garamond", Georgia, serif;

        color: var(--ink);

        font-size: 2.2rem;
        line-height: 1.05;
    }

    .bg-results {
        display: grid;
        gap: 0.85rem;

        margin-top: 1rem;
    }

    .bg-similar-card {
        display: grid;
        grid-template-columns: 55px 1fr 150px;
        gap: 1.3rem;
        align-items: start;

        padding: 1.55rem 1.65rem;

        background: rgba(255, 255, 255, 0.38);

        border: 1px solid var(--line);
        border-radius: 22px;
    }

    .bg-rank {
        padding-top: 0.15rem;

        font-family: "Cormorant Garamond", Georgia, serif;

        color: var(--sage-400);

        font-size: 1.85rem;
        line-height: 1;
    }

    .bg-result-brand {
        margin-bottom: 0.25rem;

        color: var(--sage-600);

        font-size: 0.64rem;
        font-weight: 600;
        letter-spacing: 0.11em;
        text-transform: uppercase;
    }

    .bg-result-name {
        margin-bottom: 0.65rem;

        font-family: "Cormorant Garamond", Georgia, serif;

        color: var(--ink);

        font-size: 1.65rem;
        line-height: 1.05;
    }

    .bg-result-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.42rem;

        margin-bottom: 0.85rem;
    }

    .bg-result-pill {
        display: inline-flex;

        padding: 0.33rem 0.58rem;

        background: var(--sage-050);

        border: 1px solid rgba(79, 98, 81, 0.08);
        border-radius: 999px;

        color: var(--sage-700);

        font-size: 0.63rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .bg-result-reason {
        max-width: 800px;

        color: var(--ink);

        font-size: 0.84rem;
        line-height: 1.7;
    }

    .bg-result-reason-line + .bg-result-reason-line {
        margin-top: 0.75rem;
    }

    .bg-result-score {
        text-align: right;
    }

    .bg-result-score-label {
        margin-bottom: 0.25rem;

        color: var(--muted);

        font-size: 0.61rem;
        line-height: 1.3;
    }

    .bg-result-score-value {
        font-family: "Cormorant Garamond", Georgia, serif;

        color: var(--sage-700);

        font-size: 2.3rem;
        line-height: 1;
    }

    .bg-mini-track {
        height: 5px;

        margin-top: 0.65rem;
        overflow: hidden;

        background: var(--sage-100);
        border-radius: 999px;
    }

    .bg-mini-fill {
        height: 100%;

        background:
            linear-gradient(
                90deg,
                var(--sage-300),
                var(--sage-500)
            );

        border-radius: 999px;
    }

    .bg-component-line {
        margin-top: 0.55rem;

        color: var(--muted);

        font-size: 0.62rem;
        line-height: 1.55;
    }


    .bg-placeholder {
        min-height: 360px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        text-align: center;
        background: rgba(255, 255, 255, 0.30);
        border: 1px solid var(--line);
        border-radius: 26px;
    }

    @media (max-width: 760px) {
        .bg-compare-product-grid,
        .bg-score-grid,
        .bg-compare-columns {
            grid-template-columns: 1fr;
        }

        .bg-compare-card-copy {
            max-width: calc(100% - 95px);
        }

        .bg-compare-art {
            max-width: 90px;
            max-height: 90px;
        }

        .bg-diff-row {
            grid-template-columns: 1fr;
            gap: 0.25rem;
        }

        .bg-explanation-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

VALID_PAGES = {
    "profile",
    "compare",
    "similar",
    "about",
}

page = st.query_params.get("page", "profile")

if page not in VALID_PAGES:
    page = "profile"


def nav_link(
    target: str,
    label: str,
) -> str:
    active = " bg-nav-active" if page == target else ""

    return (
        f'<a class="{active.strip()}" '
        f'href="?page={target}" target="_self">'
        f'{escape(label)}</a>'
    )


def render_navigation():
    st.html(
        f"""
        <div class="bg-nav">
            <div class="bg-brand">BeautyGraph</div>

            <div class="bg-nav-links">
                {nav_link("profile", "Product Profile")}
                {nav_link("compare", "Compare Products")}
                {nav_link("similar", "Similar Products")}
                {nav_link("about", "About")}
            </div>
        </div>
        """
    )


def render_section_header(
    kicker: str,
    title: str,
    description: str,
):
    st.html(
        f"""
        <div class="bg-section-kicker">
            {escape(kicker)}
        </div>

        <div class="bg-section-title">
            {escape(title)}
        </div>

        <div class="bg-section-description">
            {escape(description)}
        </div>
        """
    )


def format_product_form(product: dict) -> str:
    return (
        product["product_form"]
        .replace("_", " ")
        .replace("-", " ")
        .title()
    )


def render_footer():
    st.html(
        """
        <div class="bg-footer-note">
            BeautyGraph is an information-system prototype for
            explainable skincare formula comparison. Similarity and
            function profiles describe structured ingredient-list
            relationships and should not be interpreted as clinical
            efficacy or medical advice.
        </div>
        """
    )


# ---------------------------------------------------------
# Product Profile
# ---------------------------------------------------------

def render_profile():
    hero_asset = ASSET_DIR / "hero" / "hero_skincare.png"

    hero_image = (
        image_data_uri(hero_asset)
        if hero_asset.exists()
        else ""
    )

    st.html(
        f"""
        <section class="bg-hero">
            <div class="bg-hero-copy">
                <div class="bg-eyebrow">
                    Explainable skincare relationships
                </div>

                <div class="bg-hero-title">
                    Understand formulas<br>
                    beyond the label.
                </div>

                <p class="bg-hero-text">
                    Explore ingredients, formula functions,
                    and product relationships through transparent,
                    explainable comparisons.
                </p>
            </div>

            <div class="bg-wash-area">
                <div class="bg-wash bg-wash-one"></div>
                <div class="bg-wash bg-wash-two"></div>
                <div class="bg-wash bg-wash-three"></div>

                <img
                    class="bg-hero-art"
                    src="{hero_image}"
                    alt="Watercolor skincare containers"
                >
            </div>
        </section>
        """
    )

    render_section_header(
        "Explore",
        "Product Profile",
        (
            "Select a moisturizer to explore its normalized ingredient "
            "list and mapped formula-function profile."
        ),
    )

    product_ids = sorted(
        products,
        key=lambda product_id: (
            products[product_id]["brand"].lower(),
            products[product_id]["product_name"].lower(),
        ),
    )

    selected_id = st.selectbox(
        "Choose a moisturizer",
        options=product_ids,
        format_func=lambda product_id: product_label(
            products[product_id]
        ),
        key="profile_product",
    )

    product = products[selected_id]

    brand = escape(product["brand"])
    product_name = escape(product["product_name"])
    product_form = escape(format_product_form(product))

    ingredient_count = len(product["positions"])
    coverage = product["function_mapping_coverage"]

    product_image = product_form_image(
        product["product_form"]
    )

    product_art_html = ""

    if product_image:
        product_art_html = f"""
            <div class="bg-product-art-wrap">
                <img
                    class="bg-product-art"
                    src="{product_image}"
                    alt="{product_form} watercolor illustration"
                >
            </div>
        """

    st.html(
        f"""
        <section class="bg-product-card">
            <div class="bg-card-wash"></div>

            <div class="bg-product-layout">
                <div class="bg-product-copy">
                    <div class="bg-product-brand">
                        {brand}
                    </div>

                    <div class="bg-product-name">
                        {product_name}
                    </div>

                    <div class="bg-badges">
                        <span class="bg-badge">
                            {product_form}
                        </span>

                        <span class="bg-badge">
                            {ingredient_count} ingredients
                        </span>

                        <span class="bg-badge">
                            {coverage:.0%} data coverage
                        </span>
                    </div>
                </div>

                {product_art_html}
            </div>
        </section>
        """
    )

    render_section_header(
        "Formula structure",
        "Function Profile",
        (
            "A position-weighted view of the ingredient functions "
            "currently mapped by BeautyGraph."
        ),
    )

    profile_rows = sorted(
        product["formula_profile"].items(),
        key=lambda item: item[1],
        reverse=True,
    )

    profile_html = ""

    for function_name, share in profile_rows:
        if share <= 0:
            continue

        label = FUNCTION_LABELS.get(
            function_name,
            function_name.replace("_", " ").title(),
        )

        width = min(share * 100, 100)

        profile_html += f"""
            <div class="bg-profile-row">
                <div class="bg-function-label">
                    {escape(label)}
                </div>

                <div class="bg-function-track">
                    <div
                        class="bg-function-fill"
                        style="width: {width:.2f}%;">
                    </div>
                </div>

                <div class="bg-function-value">
                    {share:.1%}
                </div>
            </div>
        """

    st.html(
        f"""
        <div class="bg-profile-wrap">
            {profile_html}

            <div class="bg-method-note">
                Function profiles reflect only ingredients currently
                covered by BeautyGraph's ingredient-function mapping.
                This prototype does not infer ingredient concentration
                from the published ingredient list.
            </div>
        </div>
        """
    )

    st.html('<div style="height: 3rem;"></div>')

    render_section_header(
        "Formula detail",
        "Ingredients",
        (
            "Normalized ingredients are shown in their original "
            "published order."
        ),
    )

    ingredient_rows = sorted(
        product["positions"].items(),
        key=lambda item: item[1],
    )

    ingredients_html = ""

    for ingredient_id, position in ingredient_rows:
        ingredient_name = escape(
            product["ingredient_names"][ingredient_id]
        )

        ingredients_html += f"""
            <div class="bg-ingredient">
                <div class="bg-ingredient-number">
                    {position:02d}
                </div>

                <div class="bg-ingredient-name">
                    {ingredient_name}
                </div>
            </div>
        """

    st.html(
        f"""
        <div class="bg-ingredient-grid">
            {ingredients_html}
        </div>
        """
    )

    render_footer()


# ---------------------------------------------------------
# Compare Products
# ---------------------------------------------------------

def render_compare():
    render_section_header(
        "Formula comparison",
        "Compare Products",
        (
            "Choose two moisturizers to compare ingredient overlap, "
            "position-weighted formula structure, mapped functions, "
            "and the features that explain their relationship."
        ),
    )

    product_ids = sorted(
        products,
        key=lambda product_id: (
            products[product_id]["brand"].lower(),
            products[product_id]["product_name"].lower(),
        ),
    )

    col_a, col_b = st.columns(2)

    with col_a:
        product_a_id = st.selectbox(
            "Product A",
            options=product_ids,
            format_func=lambda product_id: product_label(
                products[product_id]
            ),
            key="compare_product_a",
        )

    with col_b:
        default_b = 1 if len(product_ids) > 1 else 0

        product_b_id = st.selectbox(
            "Product B",
            options=product_ids,
            index=default_b,
            format_func=lambda product_id: product_label(
                products[product_id]
            ),
            key="compare_product_b",
        )

    if product_a_id == product_b_id:
        st.info(
            "Choose two different products to view a comparison."
        )
        return

    comparison = build_product_comparison(
        products,
        product_a_id,
        product_b_id,
    )

    product_a = comparison["product_a"]
    product_b = comparison["product_b"]

    product_a_image = product_form_image(
        product_a["product_form"]
    )

    product_b_image = product_form_image(
        product_b["product_form"]
    )

    product_a_art = ""

    if product_a_image:
        product_a_art = f"""
            <img
                class="bg-compare-art"
                src="{product_a_image}"
                alt="{escape(format_product_form(product_a))}
                     watercolor illustration"
            >
        """

    product_b_art = ""

    if product_b_image:
        product_b_art = f"""
            <img
                class="bg-compare-art"
                src="{product_b_image}"
                alt="{escape(format_product_form(product_b))}
                     watercolor illustration"
            >
        """

    st.html(
        f"""
        <div class="bg-compare-product-grid">

            <div class="bg-compare-card bg-compare-card-a">
                <div class="bg-compare-card-copy">
                    <div class="bg-compare-label">
                        Product A
                    </div>

                    <div class="bg-compare-brand">
                        {escape(product_a["brand"])}
                    </div>

                    <div class="bg-compare-name">
                        {escape(product_a["product_name"])}
                    </div>

                    <div class="bg-compare-form">
                        {escape(format_product_form(product_a))}
                    </div>
                </div>

                {product_a_art}
            </div>

            <div class="bg-compare-card bg-compare-card-b">
                <div class="bg-compare-card-copy">
                    <div class="bg-compare-label">
                        Product B
                    </div>

                    <div class="bg-compare-brand">
                        {escape(product_b["brand"])}
                    </div>

                    <div class="bg-compare-name">
                        {escape(product_b["product_name"])}
                    </div>

                    <div class="bg-compare-form">
                        {escape(format_product_form(product_b))}
                    </div>
                </div>

                {product_b_art}
            </div>

        </div>
        """
    )

    similarity = comparison["similarity"]

    ingredient_data = comparison["ingredients"]
    function_data = comparison["functions"]

    shared = ingredient_data["shared"]
    shared_high = ingredient_data["shared_high_position"]

    if shared_high:
        high_position_text = ", ".join(
            row["name"]
            for row in shared_high[:4]
        )
    else:
        high_position_text = (
            "No ingredient appears within the first 10 "
            "positions of both formulas."
        )

    shared_function_rows = function_data["shared"][:3]

    if shared_function_rows:
        shared_function_text = ", ".join(
            FUNCTION_LABELS.get(
                row["function_name"],
                row["function_name"]
                .replace("_", " ")
                .title(),
            )
            for row in shared_function_rows
        )
    else:
        shared_function_text = (
            "No shared mapped function groups."
        )

    meaningful_differences = [
        row
        for row in function_data["differences"]
        if row["absolute_difference"] > 1e-12
    ][:2]

    if meaningful_differences:
        difference_parts = []

        for row in meaningful_differences:
            label = FUNCTION_LABELS.get(
                row["function_name"],
                row["function_name"]
                .replace("_", " ")
                .title(),
            )

            difference_parts.append(
                f"{label}: "
                f"A {row['share_a']:.1%} vs "
                f"B {row['share_b']:.1%}"
            )

        difference_text = "<br><br>".join(difference_parts) + "."
    else:
        difference_text = (
            "The mapped function profiles have the same "
            "distribution across current function groups."
        )

    st.html(
        f"""
        <div class="bg-section-kicker">
            BeautyGraph explanation
        </div>

        <div class="bg-section-title">
            Why these formulas relate
        </div>

        <div class="bg-section-description">
            Start with the relationship, then explore the
            ingredient-level evidence below.
        </div>

        <div class="bg-explanation">
            <div class="bg-explanation-lead">
                These formulas have
                <strong>
                    {similarity["ingredient_similarity"]:.0%}
                    ingredient overlap
                </strong>
                and
                <strong>
                    {similarity["formula_similarity"]:.0%}
                    position-weighted similarity
                </strong>,
                while their mapped function profiles are
                <strong>
                    {similarity["function_similarity"]:.0%}
                    similar
                </strong>.
            </div>

            <div class="bg-explanation-grid">

                <div class="bg-explanation-point">
                    <div class="bg-explanation-point-label">
                        Ingredient relationship
                    </div>

                    <div class="bg-explanation-point-text">
                        {len(shared)} normalized ingredients are shared.
                        <br><br>
                        High-position overlap:
                        {escape(high_position_text)}
                    </div>
                </div>

                <div class="bg-explanation-point">
                    <div class="bg-explanation-point-label">
                        Shared function pattern
                    </div>

                    <div class="bg-explanation-point-text">
                        Their strongest shared mapped function
                        groups are
                        {escape(shared_function_text)}.
                    </div>
                </div>

                <div class="bg-explanation-point">
                    <div class="bg-explanation-point-label">
                        Key differences
                    </div>

                    <div class="bg-explanation-point-text">
                        {difference_text}
                    </div>
                </div>

            </div>

            <div class="bg-explanation-note">
                Function comparison uses mapped ingredient
                coverage of
                {product_a["function_mapping_coverage"]:.0%}
                for Product A and
                {product_b["function_mapping_coverage"]:.0%}
                for Product B. Ingredient-list order provides
                approximate formula structure and does not reveal
                exact concentrations.
            </div>
        </div>

        <div class="bg-section-kicker">
            Similarity signals
        </div>

        <div class="bg-section-title">
            Comparison metrics
        </div>
        """
    )


    scores = [
        (
            "Position-weighted formula similarity",
            similarity["formula_similarity"],
            True,
        ),
        (
            "Normalized ingredient overlap",
            similarity["ingredient_similarity"],
            False,
        ),
        (
            "Function-profile similarity",
            similarity["function_similarity"],
            False,
        ),
    ]

    score_html = ""

    for label, value, primary in scores:
        card_class = (
            "bg-score-card bg-score-card-primary"
            if primary
            else "bg-score-card"
        )

        score_html += f"""
            <div class="{card_class}">
                <div class="bg-score-label">
                    {escape(label)}
                </div>

                <div class="bg-score-value">
                    {value:.0%}
                </div>

                <div class="bg-score-track">
                    <div
                        class="bg-score-fill"
                        style="width: {min(value * 100, 100):.2f}%;">
                    </div>
                </div>
            </div>
        """

    st.html(
        f"""
        <div class="bg-score-grid">
            {score_html}
        </div>
        """
    )

    ingredients = comparison["ingredients"]

    shared = ingredients["shared"]
    shared_high = ingredients["shared_high_position"]

    shared_chip_html = "".join(
        f'<span class="bg-chip">{escape(row["name"])}</span>'
        for row in shared
    )

    high_chip_html = "".join(
        f'<span class="bg-chip">{escape(row["name"])}</span>'
        for row in shared_high
    )

    st.html(
        f"""
        <div class="bg-section-kicker">
            Ingredient relationship
        </div>

        <div class="bg-section-title">
            What they share
        </div>

        <div class="bg-shared-card">
            <div class="bg-shared-summary">
                {len(shared)} normalized ingredients are shared.
                {len(shared_high)} appear within the first 10 positions
                of both formulas.
            </div>

            <div class="bg-detail-title">
                Shared high-position ingredients
            </div>

            <div class="bg-chip-wrap">
                {high_chip_html if high_chip_html else
                 '<span class="bg-chip">None in both top 10</span>'}
            </div>

            <div style="height: 1.4rem;"></div>

            <div class="bg-detail-title">
                All shared ingredients
            </div>

            <div class="bg-chip-wrap">
                {shared_chip_html if shared_chip_html else
                 '<span class="bg-chip">No shared ingredients</span>'}
            </div>
        </div>
        """
    )

    only_a_html = "".join(
        f'<span class="bg-chip">{escape(row["name"])}</span>'
        for row in ingredients["only_a"]
    )

    only_b_html = "".join(
        f'<span class="bg-chip bg-chip-blush">'
        f'{escape(row["name"])}</span>'
        for row in ingredients["only_b"]
    )

    st.html(
        f"""
        <div class="bg-section-kicker">
            Formula detail
        </div>

        <div class="bg-section-title">
            Where they differ
        </div>

        <div class="bg-compare-columns">
            <div class="bg-detail-card bg-detail-card-a">
                <div class="bg-detail-title">
                    Unique to {escape(product_a["product_name"])}
                </div>

                <div class="bg-chip-wrap">
                    {only_a_html if only_a_html else
                     '<span class="bg-chip">None</span>'}
                </div>
            </div>

            <div class="bg-detail-card bg-detail-card-b">
                <div class="bg-detail-title">
                    Unique to {escape(product_b["product_name"])}
                </div>

                <div class="bg-chip-wrap">
                    {only_b_html if only_b_html else
                     '<span class="bg-chip bg-chip-blush">None</span>'}
                </div>
            </div>
        </div>
        """
    )

    function_rows = comparison["functions"]["differences"][:5]

    function_html = ""

    for row in function_rows:
        label = FUNCTION_LABELS.get(
            row["function_name"],
            row["function_name"].replace("_", " ").title(),
        )

        function_html += f"""
            <div class="bg-diff-row">
                <div class="bg-diff-function">
                    {escape(label)}
                </div>

                <div class="bg-diff-value-a">
                    A · {row["share_a"]:.1%}
                </div>

                <div class="bg-diff-value-b">
                    B · {row["share_b"]:.1%}
                </div>
            </div>
        """

    st.html(
        f"""
        <div class="bg-section-kicker">
            Function structure
        </div>

        <div class="bg-section-title">
            Largest profile differences
        </div>

        <div class="bg-profile-wrap">
            {function_html}
        </div>
        """
    )

    render_footer()


# ---------------------------------------------------------
# Temporary pages
# ---------------------------------------------------------

def render_similar():
    render_section_header(
        "Product relationships",
        "Similar Products",
        (
            "Select a moisturizer to explore its five closest "
            "formula relationships in the current BeautyGraph dataset."
        ),
    )

    product_ids = sorted(
        products,
        key=lambda product_id: (
            products[product_id]["brand"].lower(),
            products[product_id]["product_name"].lower(),
        ),
    )

    selected_id = st.selectbox(
        "Choose a moisturizer",
        options=product_ids,
        format_func=lambda product_id: product_label(
            products[product_id]
        ),
        key="similar_product",
    )

    selected_product = products[selected_id]

    st.html(
        f"""
        <div class="bg-query-card">
            <div class="bg-query-brand">
                {escape(selected_product["brand"])}
            </div>

            <div class="bg-query-name">
                {escape(selected_product["product_name"])}
            </div>

            <div class="bg-result-meta">
                <span class="bg-result-pill">
                    {escape(format_product_form(selected_product))}
                </span>

                <span class="bg-result-pill">
                    {len(selected_product["positions"])}
                    ingredients
                </span>
            </div>
        </div>
        """
    )

    render_section_header(
        "Top relationships",
        "Five closest formulas",
        (
            "Results are ranked by position-weighted ingredient "
            "similarity. Ingredient overlap and mapped function "
            "similarity are shown as supporting signals. "
            "Results are relative to the current 50-product prototype "
            "dataset and do not imply equivalent clinical performance "
            "or exact formulation."
        ),
    )

    results = get_top_similar_products(
        products,
        selected_id,
        top_k=5,
    )

    cards_html = ""

    for rank, result in enumerate(results, start=1):
        comparison = build_product_comparison(
            products,
            selected_id,
            result["product_id"],
        )

        shared_high = comparison[
            "ingredients"
        ]["shared_high_position"]

        shared_functions = comparison[
            "functions"
        ]["shared"][:3]

        if shared_high:
            ingredient_text = ", ".join(
                row["name"]
                for row in shared_high[:4]
            )

            ingredient_reason = (
                "Shared high-position ingredients: "
                + ingredient_text
                + "."
            )

        else:
            shared_count = len(
                comparison["ingredients"]["shared"]
            )

            ingredient_reason = (
                f"{shared_count} normalized ingredients are "
                "shared, but none appear within the first 10 "
                "positions of both formulas."
            )

        if shared_functions:
            function_text = ", ".join(
                FUNCTION_LABELS.get(
                    row["function_name"],
                    row["function_name"]
                    .replace("_", " ")
                    .title(),
                )
                for row in shared_functions
            )

            function_reason = (
                " Strongest shared mapped function groups: "
                + function_text
                + "."
            )

        else:
            function_reason = (
                " No shared mapped function groups were found."
            )

        ingredient_reason_html = escape(
            ingredient_reason
        )

        function_reason_html = escape(
            function_reason.strip()
        )

        formula_score = result["formula_similarity"]
        ingredient_score = result["ingredient_similarity"]
        function_score = result["function_similarity"]

        cards_html += f"""
            <div class="bg-similar-card">

                <div class="bg-rank">
                    {rank:02d}
                </div>

                <div>
                    <div class="bg-result-brand">
                        {escape(result["brand"])}
                    </div>

                    <div class="bg-result-name">
                        {escape(result["product_name"])}
                    </div>

                    <div class="bg-result-meta">
                        <span class="bg-result-pill">
                            {escape(
                                result["product_form"]
                                .replace("_", " ")
                                .replace("-", " ")
                                .title()
                            )}
                        </span>
                    </div>

                    <div class="bg-result-reason">
                        <div class="bg-result-reason-line">
                            {ingredient_reason_html}
                        </div>

                        <div class="bg-result-reason-line">
                            {function_reason_html}
                        </div>
                    </div>
                </div>

                <div class="bg-result-score">                    <div class="bg-result-score-value">
                        {formula_score:.0%}
                    </div>

                    <div class="bg-mini-track">
                        <div
                            class="bg-mini-fill"
                            style="
                                width:
                                {min(formula_score * 100, 100):.2f}%;
                            ">
                        </div>
                    </div>

                    <div class="bg-component-line">
                        Ingredient overlap:
                        {ingredient_score:.0%}
                        <br>
                        Function similarity:
                        {function_score:.0%}
                    </div>
                </div>

            </div>
        """

    st.html(
        f"""
        <div class="bg-results">
            {cards_html}
        </div>
        """
    )


    render_footer()



def render_about():
    render_section_header(
        "Methodology",
        "About BeautyGraph",
        (
            "BeautyGraph is a practicum prototype for transparent, "
            "explainable skincare formula relationships."
        ),
    )

    st.html(
        """
        <div class="bg-placeholder">
            <div>
                <div class="bg-section-title">
                    Product → Ingredient → Function → Relationship
                </div>

                <div class="bg-section-description">
                    The current prototype focuses on leave-on facial
                    moisturizers and uses normalized ingredients,
                    ingredient position, and mapped function groups.
                </div>
            </div>
        </div>
        """
    )


# ---------------------------------------------------------
# Application
# ---------------------------------------------------------

render_navigation()

if page == "profile":
    render_profile()

elif page == "compare":
    render_compare()

elif page == "similar":
    render_similar()

else:
    render_about()
