from html import escape
from pathlib import Path
import sys

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from src.similarity.engine import load_similarity_inputs


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
            min-height: 150px;
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

st.html(
    """
    <div class="bg-nav">
        <div class="bg-brand">BeautyGraph</div>

        <div class="bg-nav-links">
            <span class="bg-nav-active">Product Profile</span>
            <span>Compare Products</span>
            <span>Similar Products</span>
            <span>About</span>
        </div>
    </div>
    """,
)


# ---------------------------------------------------------
# Hero
# ---------------------------------------------------------

st.html(
    """
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
        </div>
    </section>
    """,
)


# ---------------------------------------------------------
# Product selector
# ---------------------------------------------------------

st.html(
    """
    <div class="bg-section-kicker">Explore</div>
    <div class="bg-section-title">Product Profile</div>
    <div class="bg-section-description">
        Select a moisturizer to explore its normalized ingredient
        list and mapped formula-function profile.
    </div>
    """,
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
)

product = products[selected_id]


# ---------------------------------------------------------
# Product summary
# ---------------------------------------------------------

brand = escape(product["brand"])
product_name = escape(product["product_name"])
product_form = escape(
    product["product_form"]
    .replace("_", " ")
    .replace("-", " ")
    .title()
)

ingredient_count = len(product["positions"])
coverage = product["function_mapping_coverage"]

st.html(
    f"""
    <section class="bg-product-card">
        <div class="bg-card-wash"></div>

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
    </section>
    """,
)


# ---------------------------------------------------------
# Formula profile
# ---------------------------------------------------------

st.html(
    """
    <div class="bg-section-kicker">Formula structure</div>
    <div class="bg-section-title">Function Profile</div>
    <div class="bg-section-description">
        A position-weighted view of the ingredient functions
        currently mapped by BeautyGraph.
    </div>
    """,
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
    """,
)


# ---------------------------------------------------------
# Ingredients
# ---------------------------------------------------------

st.html(
    """
    <div style="height: 3rem;"></div>

    <div class="bg-section-kicker">Formula detail</div>
    <div class="bg-section-title">Ingredients</div>
    <div class="bg-section-description">
        Normalized ingredients are shown in their original
        published order.
    </div>
    """,
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
    """,
)


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.html(
    """
    <div class="bg-footer-note">
        BeautyGraph is an information-system prototype for
        explainable skincare formula comparison. Similarity and
        function profiles describe structured ingredient-list
        relationships and should not be interpreted as clinical
        efficacy or medical advice.
    </div>
    """,
)
