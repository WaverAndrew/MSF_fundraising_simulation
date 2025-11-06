DEFAULTS = {
    "msf_italy": {
        "fundraising_2024_eur": 79_900_000.0,
    },
    "rail": {
        "trenitalia_riders": 470_000_000,
        "italo_riders": 22_000_000,  # base scenario Italo-only
        "digital_share_pct": 65,
        "eligible_share_pct": 90,
        "ask_type": "€1 fixed",
        "choice_share_eur1_pct": 70,
        "optin_web_1_pct": 4,
        "optin_web_2_pct": 2,
        "optin_pos_pct": 2,
        "seasonality": [1.0]*12,
    },
    "retail": {
        "istat_monthly_spend_2023": 2738.0,
        "istat_monthly_spend_2024": 2755.0,
        "grocery_share_pct": 18,
        "avg_receipt_eur": 25.12,
        "households": 1_000_000,  # placeholder for top-down
        "optin_pct": 5,
        "charm_prevalence_pct": 80,
        "payment_card_share_pct": 70,
        "daily_receipts": 500,
        "stores": 100,
        "active_days": 360,
    },
    "fees": {
        "processor": "Adyen Giving",
        "rate_pct": 1.4,
        "fixed_eur": 0.10,
    },
}

SOURCES = {
    "MSF Italy Bilancio 2024": "https://www.medicisenzafrontiere.it/",
    "FS Group riders 2023": "https://www.fsitaliane.it/",
    "Italo riders 2023/2024": "https://www.italotreno.it/",
    "EU Consumer Rights Directive": "https://eur-lex.europa.eu/",
    "Adyen Giving": "https://www.adyen.com/",
    "Checkout charity coverage (NPR/AP)": "https://apnews.com/",
    "NielsenIQ grocery stats": "https://nielseniq.com/",
    "Charm pricing prevalence": "https://en.wikipedia.org/wiki/Psychological_pricing",
    "Payments landscape (ECB/BoI)": "https://www.ecb.europa.eu/",
    "Nexi ‘Dona Italia’": "https://www.nexi.it/",
}

LANGUAGE = {
    "en": {
        "title": "MSF Micro-donations Simulator",
    },
    "it": {
        "title": "Simulatore Micro-donazioni MSF",
    },
}




