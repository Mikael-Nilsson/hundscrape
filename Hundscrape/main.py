
import logging
import azure.functions as func

from . import scraper


shelters = [
    {   "name": "hundarutanhem",
        "url": [
            "https://hundarutanhem.se/hundarna/mellanstora-hundar/",
            "https://hundarutanhem.se/hundarna/stora-hundar/"
        ],
        "element_tree": {
            "classes": "polaroid", "location": "img", "source": "src"
        },
        "outfile": "hundarutanhem.csv"
    },
    {
        "name": "hundstallet",
        "url": ["https://hundstallet.se/soker-hem/"],
        "element_tree": {
            "classes": "small-12 medium-6 large-4 cell", "location": "img", "source": "src"
        },
        "outfile": "hundstallet.csv"
    }
]


def main(OnceAWeek: func.TimerRequest) -> func.HttpResponse:
    logger = logging.getLogger('azure')
    logger.setLevel(logging.DEBUG)

    for shelter in shelters:
        logging.info('Scraping dogs')
        scraper.download_dogs_from_shelter(shelter)

    # return func.HttpResponse(
    #         "It might actually have worked!",
    #         status_code=200
    #     )


if __name__ == "__main__":
    main(None)
