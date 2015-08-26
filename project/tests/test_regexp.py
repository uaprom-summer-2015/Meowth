from project.tests.utils import ProjectTestCase
from project.utils import contacts_map_coordinates

map_url_links = {
    "https://www.google.com.ua/maps/place/UAPROM/@50.4049258,30.6798472,17z/"
    "data=!3m1!4b1!4m2!3m1!1s0x40d4c4f328925f07:0xa47f647a2cdf1661?hl=en":
        ("50.4049258", "30.6798472", "17"),
    "https://www.google.com.ua/maps/place/UAPROM/@50.4048801,30.6798378,21z/"
    "data=!4m6!1m3!3m2!1s0x40d4c4f328925f07:0xa47f647a2cdf1661!2s"
    "UAPROM!3m1!1s0x40d4c4f328925f07:0xa47f647a2cdf1661?hl=en":
        ("50.4048801", "30.6798378", "21"),
    "https://www.google.com.ua/maps/place/UAPROM/@6.3471491,-7.6466703,4.08z/"
    "data=!4m6!1m3!3m2!1s0x40d4c4f328925f07:0xa47f647a2cdf1661!2s"
    "UAPROM!3m1!1s0x40d4c4f328925f07:0xa47f647a2cdf1661?hl=en":
        ("6.3471491", "-7.6466703", "4.08"),
    "https://www.google.com.ua/maps/place/UAPROM/@0.0039854,7.6737268,4.83z/"
    "data=!4m6!1m3!3m2!1s0x40d4c4f328925f07:0xa47f647a2cdf1661!2sUAPROM"
    "!3m1!1s0x40d4c4f328925f07:0xa47f647a2cdf1661?hl=en":
        ("0.0039854", "7.6737268", "4.83"),
    "https://www.google.com.ua/maps/place/UAPROM/@41.0722665,-127.5186222,3z/"
    "data=!4m6!1m3!3m2!1s0x40d4c4f328925f07:0xa47f647a2cdf1661!2s"
    "UAPROM!3m1!1s0x40d4c4f328925f07:0xa47f647a2cdf1661?hl=en":
        ("41.0722665", "-127.5186222", "3"),
    "https://www.google.com.ua/maps/place/UAPROM/"
    "@82.4121861,169.6055086,4.25z/"
    "data=!4m6!1m3!3m2!1s0x40d4c4f328925f07:0xa47f647a2cdf1661!2s"
    "UAPROM!3m1!1s0x40d4c4f328925f07:0xa47f647a2cdf1661?hl=en":
        ("82.4121861", "169.6055086", "4.25"),
    "https://www.google.com.ua/maps/place/"
    "82%C2%B024'43.9%22N+169%C2%B036'19.8%22E/@82.4121861,169.6055086,17z/"
    "data=!3m1!4b1!4m2!3m1!1s0x0:0x0?hl=en":
        ("82.4121861", "169.6055086", "17"),
    "https://www.google.com.ua/maps/search/82.4121861,169.6055086+@/"
    "@82.4121861,169.6055086,17z/data=!3m1!4b1?hl=en":
        ("82.4121861", "169.6055086", "17"),
    "https://www.google.com.ua/maps/search/'@83.4121861,169.6055086'/"
    "@82.4121861,169.6055086,17z?hl=en": ("82.4121861", "169.6055086", "17")
}


class MapUrlParserTest(ProjectTestCase):
    def test_map_url_parses_gmaps(self):
        for regex, expected in map_url_links.items():
            actual = contacts_map_coordinates.search(regex)
            self.assertEqual(expected, actual.groups())
