import tmdbsimple as tmdb
tmdb.API_KEY = 'API KEY GOES HERE'
  
  
def search_movie_name(name):

    """ Searches the tmdb for a movie from a user query """ 

    search = tmdb.Search()
    search.movie(query = name)

    #Showing search results and letting you oselect a movie or tv show 
    #used a dictonary to store title as key and ID as value 
        
    search_hold = [] 

    
    for s in search.results:

        #Gathers general information about the movie 
        title = s["title"]
        title_id = s["id"]
        poster_path = s["poster_path"]
        overview = s["overview"]
        release_date = s['release_date']


        
        #gets the trailer link and creates a youtube link to trailer
        #if no trailer is found 'NaN' will be assigned to variable

        movie = tmdb.Movies(title_id)
        video_details = movie.videos()

        youtube = 'https://www.youtube.com/watch?v='

        try:
            key = video_details['results'][0]['key'] #unique youtube key for video
            youtube_key = youtube + key #creates the link 
        except:
            youtube_key = 'NaN' 



        #creates a list with movie information 
        movie = [title_id,title,release_date,poster_path,youtube_key,overview]

        #appends the movie info to the search list
        search_hold.append(movie)
        
          
        
    
    #returns a list of results 
    return search_hold
    


def get_similar(movie_id):

    """ Gets similar movies based off a movie id in tmdb """

    search = tmdb.Movies(movie_id)
    similar = search.similar_movies()

    try:
        id_numbers = []

        i = 0 
        while i <= len(similar['results']):

            id_num = similar['results'][i]['id']
            id_numbers.append(id_num)

            print(id_num)
            i += 1 
            
    except:
        pass 
        
    return id_numbers





def get_movie_info(movie_id):

    """ Searches tmdb for a movie by its id number and returns the movie info """ 


    search = tmdb.Movies(movie_id)
    similar = search.info()

    
    #gets the basic movie information 
    title_id = similar['id']
    title = similar['title']
    poster_path = similar['poster_path']
    overview = similar['overview']
    release_date = similar['release_date']


    #Gets the trailer link 
    movie = tmdb.Movies(movie_id)
    video_details = movie.videos()

    youtube = 'https://www.youtube.com/watch?v='

    try:

        key = video_details['results'][0]['key'] #unique youtube key for video
        youtube_key = youtube + key #creates the link 

    except:
        youtube_key = 'NaN' 


    
    return title_id,title,release_date,poster_path,overview,youtube_key








if __name__ == "__main__":
    print(get_movie_info(674))