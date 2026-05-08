DEMO_SCENARIOS = [
    {
        "id": 1,
        "title": "Yapay Zeka Destekli Mobil Uygulama",
        "description": "3 kişilik ekiple yapay zeka destekli mobil uygulama geliştirme projesi.",
        "project_name": "Yapay zeka destekli mobil uygulama"
    },
    {
        "id": 2,
        "title": "E-Ticaret Sitesi Geliştirme",
        "description": "Küçük bir ekip ile ürün listeleme, sepet ve ödeme özellikleri olan e-ticaret sitesi geliştirme.",
        "project_name": "E-ticaret sitesi geliştirme projesi"
    },
    {
        "id": 3,
        "title": "Üniversite Bitirme Projesi",
        "description": "Teslim tarihi yaklaşan akademik bitirme projesi için görev planlama.",
        "project_name": "Üniversite bitirme projesi"
    }
]


def get_demo_scenarios() -> list:
    """
    Demo ve test için hazır proje senaryolarını döndürür.
    """

    return DEMO_SCENARIOS


def get_demo_scenario_by_id(scenario_id: int) -> dict:
    """
    Verilen id değerine göre demo senaryosunu döndürür.
    """

    for scenario in DEMO_SCENARIOS:
        if scenario["id"] == scenario_id:
            return {
                "success": True,
                "scenario": scenario
            }

    return {
        "success": False,
        "error": "Belirtilen id değerine ait demo senaryosu bulunamadı."
    }