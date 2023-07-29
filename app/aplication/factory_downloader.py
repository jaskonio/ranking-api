from app.aplication.Sportmaniacs import Sportmaniacs


class FactoryDownloader:
    def factory_method(self, url_race):
        print("FactoryDownloader. factory_method. url_race: " + url_race)
        downloader = None

        if 'sportmaniacs' in url_race:
            print("Platform: Sportmaniacs")
            downloader = Sportmaniacs(url_race)

        elif 'valenciaciudaddelrunning' in url_race:
            print("Platform: valenciaciudaddelrunning")
            #downloader = Valenciaciudaddelrunning(url_race)

        elif 'toprun' in url_race:
            print("Platform: toprun")
            #downloader = TopRun(url_race)
        else:
            print("Platform not compatible")

        return downloader
