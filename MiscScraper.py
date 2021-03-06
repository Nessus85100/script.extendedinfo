import sys
import os, time, datetime, re, random
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,xbmcvfs
from Utils import *
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson
    

rottentomatoes_key = 'sr9ambpra5r3ys2khtxn5bxt'
trakt_key = '7b2281f0d441ab1bf4fdc39fd6cccf15'
tvrage_key = 'VBp9BuIr5iOiBeWCFRMG'
youtube_key = 'AI39si4DkJJhM8cm7GES91cODBmRR-1uKQuVNkJtbZIVJ6tRgSvNeUh4somGAjUwGlvHFj3d0kdvJdLqD0aQKTh6ttX7t_GjpQ'
Addon_Data_Path = os.path.join( xbmc.translatePath("special://profile/addon_data/%s" % xbmcaddon.Addon().getAddonInfo('id') ).decode("utf-8") )

def GetXKCDInfo():
    settings = xbmcaddon.Addon(id='script.extendedinfo')
    items = []
    for i in range(0,10):
        try:
            url = 'http://xkcd.com/%i/info.0.json' % random.randrange(1, 1190)
            response = GetStringFromUrl(url)
            results = simplejson.loads(response)
            item = {'Image': results["img"],
                    'Title': results["title"],
                    'Description':results["alt"]  }
            items.append(item)
        except:
            log("Error when setting XKCD info")
    return items

def GetCandHInfo():
    count = 1
    images = []
    for i in range(1,30):
        try:
            url = 'http://www.explosm.net/comics/%i/' % random.randrange(1, 3128)
            response = GetStringFromUrl(url)
        except:
            log("Error when fetching CandH data from net")
        if response:
            regex = ur'src="([^"]+)"'
            matches = re.findall(regex, response)
            if matches:
                for item in matches:
                    if item.startswith('http://www.explosm.net/db/files/Comics/'):
                        dateregex = '[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9][0-9]'
                        datematches = re.findall(dateregex, response)
                        newitem = {'Image': item,
                                    'Title': datematches[0]  }
                        images.append(newitem)
                        count += 1                      
              #  wnd.setProperty('CyanideHappiness.%i.Title' % count, item["title"])
                if count > 10:
                    break
    return images
                     
def GetFlickrImages():
    images = []
    results = ""
    try:
        url = 'http://pipes.yahoo.com/pipes/pipe.run?_id=241a9dca1f655c6fa0616ad98288a5b2&_render=json'
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
    except:
        log("Error when fetching Flickr data from net")
    count = 1
    if results:
        for item in results["value"]["items"]:
            image = {'Background': item["link"]  }
            images.append(image)
            count += 1
    return images
                                   
def GetLocationNames(search_string):
    try:
        search_string = urllib.quote_plus(search_string)
        base_url='https://maps.googleapis.com/maps/api/geocode/json?&sensor=false&'
        url = base_url + 'latlng=%s' % (search_string)
        log("Google Geocodes Search:" + url)
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
        components = results["results"][0]["address_components"]
   #     for item in components:
    #        if "country" in item["type"]:
      #          log(item["short_name"])
        return (item["short_name"])
    except Exception,e:
        log(e)
        return ("","")
        
def GetRottenTomatoesMoviesInTheaters(type):
    movies = []
    results = ""
    try:
        url = 'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/in_theaters.json?apikey=%s' % (rottentomatoes_key)
        log("Json Query: " + url)
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
    except:
        log("Error when fetching RottenTomatoes data from net")
    count = 1
    if results:
        for item in results["movies"]:
            movie = {'Title': item["title"],
                     'Art(poster)': item["posters"]["original"],
                     'Runtime': item["runtime"],
                     'Year': item["year"],
                     'Premiered': item["release_dates"]["theater"],
                     'mpaa': item["mpaa_rating"],
                     'Rating': item["ratings"]["audience_score"]/10.0,
                     'Plot': item["synopsis"]  }
            movies.append(movie)
            count += 1
            if count > 20:
                break
    return movies

def GetRottenTomatoesMoviesOpening(type):
    movies = []
    results = ""
    try:
        url = 'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/opening.json?apikey=%s' % (rottentomatoes_key)
        log("Json Query: " + url)
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
    except:
        log("Error when fetching RottenTomatoes data from net")
    count = 1
    if results:
 #       log(results)
        for item in results["movies"]:
            movie = {'Title': item["title"],
                     'Art(poster)': item["posters"]["original"],
                     'Runtime': item["runtime"],
                     'Year': item["year"],
                     'Premiered': item["release_dates"]["theater"],
                     'mpaa': item["mpaa_rating"],
                     'Rating': item["ratings"]["audience_score"]/10.0,
                     'Plot': item["synopsis"]  }
            movies.append(movie)
            count += 1
            if count > 20:
                break
    return movies
    
def GetRottenTomatoesMoviesComingSoon(type):
    movies = []
    results = ""
    try:
        url = 'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/upcoming.json?apikey=%s' % (rottentomatoes_key)
        log("Json Query: " + url)
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
    except:
        log("Error when fetching RottenTomatoes data from net")
    count = 1
    if results:
        for item in results["movies"]:
            movie = {'Title': item["title"],
                     'Art(poster)': item["posters"]["original"],
                     'Runtime': item["runtime"],
                     'Year': item["year"],
                     'Premiered': item["release_dates"]["theater"],
                     'mpaa': item["mpaa_rating"],
                     'Rating': item["ratings"]["audience_score"]/10.0,
                     'Plot': item["synopsis"]  }
            movies.append(movie)
            count += 1
            if count > 20:
                break
    return movies

def GetRottenTomatoesMoviesBoxOffice(type):
    movies = []
    results = ""
    try:
        url = 'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/box_office.json?apikey=%s' % (rottentomatoes_key)
        log("Json Query: " + url)
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
    except:
        log("Error when fetching RottenTomatoes data from net")
    count = 1
    if results:
    #    log(results)
        for item in results["movies"]:
            movie = {'Title': item["title"],
                     'Art(poster)': item["posters"]["original"],
                     'Runtime': item["runtime"],
                     'Year': item["year"],
                     'Premiered': item["release_dates"]["theater"],
                     'mpaa': item["mpaa_rating"],
                     'Rating': item["ratings"]["audience_score"]/10.0,
                     'Plot': item["synopsis"]  }
            movies.append(movie)
            count += 1
            if count > 20:
                break
    return movies

    
def GetTraktCalendarShows(Type):
    shows = []
    results = ""
    try:
        url = 'http://api.trakt.tv/calendar/%s.json/%s/today/14' % (Type,trakt_key)
        log("Json Query: " + url)
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
    except:
        log("Error when fetching Trakt data from net")
    count = 1
    if results:
        for day in results:
            for episode in day["episodes"]:
                show = {'Title' : episode["episode"]["title"],
                        'TVShowTitle' : episode["show"]["title"],
                        'ID' : episode["show"]["tvdb_id"],
                        'Runtime' : episode["show"]["runtime"],
                        'Year' : episode["show"].get("year"),
                        'Certification' : episode["show"]["certification"],
                        'Studio' : episode["show"]["network"],
                        'Plot' : episode["show"]["overview"],
                        'Genre' : " / ".join(episode["show"]["genres"]),
                        'Thumb' : episode["episode"]["images"]["screen"],
                        'Art(poster)' : episode["show"]["images"]["poster"],
                        'Art(banner)' : episode["show"]["images"]["banner"],
                        'Art(fanart)' : episode["show"]["images"]["fanart"]  }
                shows.append(show)
                count += 1
                if count > 20:
                    break
    return shows

def HandleTraktMovieResult(results):
    count = 1
    movies = []
    for movie in results:   
        try:
            premiered = str(datetime.datetime.fromtimestamp(int(movie["released"])))[:10]
        except:
            premiered = ""
        try:         
            movie = {'Title': movie["title"],
                    'Runtime': movie["runtime"],
                    'Tagline': movie["tagline"],
                    'Trailer': ConvertYoutubeURL(movie["trailer"]),
                    'Year': movie["year"],
                    'ID': movie["tmdb_id"],
                    'mpaa': movie["certification"],
                    'Plot': movie["overview"],
                    'Premiered': premiered,
                    'Rating': movie["ratings"]["percentage"]/10.0,
                    'Votes': movie["ratings"]["votes"],
                    'Watchers': movie["watchers"],
                    'Genre': " / ".join(movie["genres"]),
                    'Art(poster)': movie["images"]["poster"],
                    'Art(fanart)': movie["images"]["fanart"]  }
            movies.append(movie)
        except Exception,e:
            log(e)          
        count += 1
        if count > 20:
            break
    return movies

def HandleTraktTVShowResult(results):
    import datetime
    count = 1
    shows = []
    for tvshow in results:    
        try:
            premiered = str(datetime.datetime.fromtimestamp(int(tvshow["first_aired"])))[:10]
        except:
            premiered = ""
        show = {'Title': tvshow["title"],
                'Label': tvshow["title"],
                'TVShowTitle': tvshow["title"],
                'Runtime': tvshow["runtime"],
                'Year': tvshow["year"],
                'Status': tvshow["status"],
                'mpaa': tvshow["certification"],
                'Studio': tvshow["network"],
                'Plot': tvshow["overview"],
                'ID': tvshow["tvdb_id"],
                'AirDay': tvshow["air_day"],
                'AirShortTime': tvshow["air_time"],
                'Label2': tvshow["air_day"] + " " + tvshow["air_time"],
                'Premiered': premiered,
                'Country': tvshow["country"],
                'Rating': tvshow["ratings"]["percentage"]/10.0,
                'Votes': tvshow["ratings"]["votes"],
                'Watchers': tvshow["watchers"],
                'Genre': " / ".join(tvshow["genres"]),
                'Art(poster)': tvshow["images"]["poster"],
                'Poster': tvshow["images"]["poster"],
                'Art(banner)': tvshow["images"]["banner"],
                'Art(fanart)': tvshow["images"]["fanart"],
                'Fanart': tvshow["images"]["fanart"],
                'Thumb': tvshow["images"]["fanart"]  }
        shows.append(show)
        count += 1
        if count > 20:
            break
    return shows
    
def GetTrendingShows():
    results = ""
    filename = Addon_Data_Path + "/trendingshows.txt"
    if xbmcvfs.exists(filename) and time.time() - os.path.getmtime(filename) < 86400:
        results = read_from_file(filename)
        return HandleTraktTVShowResult(results)
    else:    
        try:
            url = 'http://api.trakt.tv/shows/trending.json/%s' % trakt_key
            response = GetStringFromUrl(url)
            results = simplejson.loads(response)
            save_to_file(results,"trendingshows",Addon_Data_Path)
        except Exception, e:
            log("Error when fetching  trending data from Trakt.tv")
            log(e)
        if results:
            return HandleTraktTVShowResult(results)
            
def GetTVShowInfo(id):
    results = ""
    filename = Addon_Data_Path + "/tvshow" + id + ".txt"
    if xbmcvfs.exists(filename) and time.time() - os.path.getmtime(filename) < 86400:
        results = read_from_file(filename)
        return HandleTraktTVShowResult([results])
    else:    
        try:
            url = 'http://api.trakt.tv/show/summary.json/%s/%s' % (trakt_key,id)
            response = GetStringFromUrl(url)
            results = simplejson.loads(response)
            save_to_file(results,"tvshow" + id,Addon_Data_Path)
        except Exception, e:
            log("Error when fetching  trending data from Trakt.tv")
            log(e)
        if results:
            return HandleTraktTVShowResult([results])
                       
    
def GetTrendingMovies():
    results = ""
    filename = Addon_Data_Path + "/trendingmovies.txt"
    if xbmcvfs.exists(filename) and time.time() - os.path.getmtime(filename) < 86400:
        results = read_from_file(filename)
   #     log(results)
        return HandleTraktMovieResult(results)
    else:  
        try:
            url = 'http://api.trakt.tv/movies/trending.json/%s' % trakt_key
            response = GetStringFromUrl(url)
            results = simplejson.loads(response)
        except Exception, e:
            log("Error when fetching  trending data from Trakt.tv")
            log(e)
        count = 1
        if results:
            return HandleTraktMovieResult(results)
       
def GetSimilarTrakt(type,imdb_id):
    movies = []
    shows = []
    results = ""
    if type == "tvshow":
        type = "show"
    filename = Addon_Data_Path + "/similar" + type + imdb_id + ".txt"
    if xbmcvfs.exists(filename) and time.time() - os.path.getmtime(filename) < 1:
        results = read_from_file(filename)
        if type == "show":
            return HandleTraktTVShowResult(results)
        elif type =="movie":
            return HandleTraktMovieResult(results)
    else:         
        try:
            url = 'http://api.trakt.tv/%s/related.json/%s/%s/' % (type, trakt_key, imdb_id)
            log(url)
            response = GetStringFromUrl(url)
            results = simplejson.loads(response)
            save_to_file(results,"similar" + type + imdb_id,Addon_Data_Path)
        except:
            log("Error when fetching  trending data from Trakt.tv")
        if results:
            if type == "show":
                return HandleTraktTVShowResult(results)
            elif type =="movie":
                return HandleTraktMovieResult(results)
    return[]
            
def GetYoutubeVideos(jsonurl,prefix = ""):
    results = []
    try:
        response = GetStringFromUrl(jsonurl)
        results = simplejson.loads(response)
    except:
        log("Error when fetching JSON data from net")
    count = 1
    log("found youtube vids: " + jsonurl)
    videos=[]
    if results:
        try:
            for item in results["value"]["items"]:
                video = {'Thumb': item["media:thumbnail"][0]["url"],
                         'Media': ConvertYoutubeURL(item["link"]),
                         'Play': "PlayMedia(" + ConvertYoutubeURL(item["link"]) + ")",
                         'Title':item["title"],
                         'Description':item["content"]["content"],
                         'Date':item["pubDate"]  }
                videos.append(video)
                count += 1
        except:
            for item in results["feed"]["entry"]:
                for entry in item["link"]:
                    if entry.get('href','').startswith('http://www.youtube.com/watch'):
                        video = {'Thumb': "http://i.ytimg.com/vi/" + ExtractYoutubeID(entry.get('href','')) + "/0.jpg",
                                 'Media': ConvertYoutubeURL(entry.get('href','')),
                                 'Play':"PlayMedia(" + ConvertYoutubeURL(entry.get('href','')) + ")",
                                 'Title':item["title"]["$t"],
                                 'Description':"To Come",
                                 'Date':"To Come"  }
                        videos.append(video)
                        count += 1
    return videos
    
def GetYoutubeSearchVideos(search_string = "" ,hd = "", orderby = "relevance", time = "all_time"):
    results = []
    if hd and not hd == "false":
        hd_string = "&hd=true"
    else:
        hd_string = ""
    search_string = urllib.quote(search_string.replace('"',''))
    try:
        url = 'http://gdata.youtube.com/feeds/api/videos?v=2&alt=json&q=%s&time=%s&orderby=%s&key=%s%s' % (search_string, time, orderby, youtube_key,hd_string)
        log(url)
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
    except:
        log("Error when fetching JSON data from net")
    count = 1
    videos = []
    if results:
            for item in results["feed"]["entry"]:
                video = {'Thumb': item["media$group"]["media$thumbnail"][2]["url"],
                         'Play': ConvertYoutubeURL(item["media$group"]["media$player"]["url"]),
                         'Description': item["media$group"]["media$description"]["$t"],
                         'Title': item["title"]["$t"],
                         'Author': item["author"][0]["name"]["$t"],
                         'Date': item["published"]["$t"].replace("T"," ").replace(".000Z","")  }
                videos.append(video)
                count += 1
    return videos
    
    
def GetYoutubeUserVideos(userid = ""):
    results = []
    userid = urllib.quote(userid.replace('"',''))
    try:
        url = 'https://gdata.youtube.com/feeds/api/users/%s/uploads?v=2&alt=json' % (userid)
        log(url)
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
    except:
        log("Error when fetching JSON data from net")
    count = 1
    videos = []
    if results:
        for item in results["feed"]["entry"]:
            video = {'Thumb': item["media$group"]["media$thumbnail"][2]["url"],
                     'Play': ConvertYoutubeURL(item["media$group"]["media$player"]["url"]),
                     'Description': item["media$group"]["media$description"]["$t"],
                     'Title': item["title"]["$t"],
                     'Author': item["author"][0]["name"]["$t"],
                     'Date': item["published"]["$t"].replace("T"," ").replace(".000Z","")  }
            videos.append(video)
            count += 1
    return videos
    