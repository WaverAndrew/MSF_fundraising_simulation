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
    "MSF Italy Bilancio 2024": "https://www.medicisenzafrontiere.it/chi-siamo/bilancio/",
    "FS Group riders 2023": "https://www.quotidiano.net/economia/in-aumento-del-18-i-passeggeri-nel-2023-dc6625c3",
    "Italo riders 2023/2024": "https://www.ttgitalia.com/focus/trasporti/189187-italo-nel-2023-tagliato-il-traguardo-dei-25-milioni-di-passeggeri-KATG399377",
    "EU Consumer Rights Directive": "https://commission.europa.eu/law/law-topic/consumer-protection-law/consumer-contract-law/consumer-rights-directive_en",
    "Adyen Giving": "https://docs.adyen.com/online-payments/donations/",
    "Checkout charity coverage (NPR/AP)": "https://www.vpm.org/npr-news/npr-news/2024-03-10/that-spare-change-you-donate-at-checkout-is-adding-up-to-millions-for-charities",
    "NielsenIQ grocery stats": "https://www.alimentando.info/lo-scontrino-medio-nel-grocery-di-2512-euro-e-quasi-stabile-dice-nielseniq-il-target-over-55-gioca-la-parte-del-leone/",
    "Charm pricing prevalence": "https://mpra.ub.uni-muenchen.de/78085/",
    "Payments landscape (ECB/BoI)": "https://www.bancaditalia.it/media/notizia/la-bce-pubblica-i-risultati-dell-ultimo-studio-sulle-abitudini-di-pagamento-dei-consumatori-nell-area-dell-euro/",
    "Nexi ‘Dona Italia’": "https://www.nexigroup.com/it/media-relations/news/2025/07/dona-italia/",
}

LANGUAGE = {
    "en": {
        "title": "MSF Micro-donations Simulator",
    },
    "it": {
        "title": "Simulatore Micro-donazioni MSF",
    },
}




