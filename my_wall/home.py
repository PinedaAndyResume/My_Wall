import tkinter as tk
import sync_data as pa
import pandas as pd 
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import urllib.request
from io import BytesIO
import webbrowser
import time
import tmdbsimple as tmdb



class home():

    """ Body """

    def __init__(self):

        """ Holds the database for the user """ 

        self.database = pd.read_csv('movies.csv')
        self.history_database = pd.read_csv('history.csv')
        self.rec_history = pd.read_csv('rec_history.csv')
      
        
        self.intended_list = self.database['title_id']
        self.movies_csv = 'movies.csv'
        self.history_csv = 'history.csv'
        self.rec_h = 'rec_history.csv'
        
        #holds load count 
        self.load_count = 0
        self.main_image_url =  'http://image.tmdb.org/t/p/w185///'

        """ Creates the main window""" 

        #Creating the main body 
        self.root = tk.Tk() 
        self.root.geometry('448x378')


        #Creates title
        self.root.title('MyWall')



        #font used for canvas 
        self.main_font = "Adorn condensed sans"



        #Crates MyWall Label 
        self.main_mywall_label = tk.Label(self.root,text = 'My Wall', font =(self.main_font,40))
        self.main_mywall_label.place(x=154, y=68)


        #Creats the find button 
        self.find_button = tk.Button(self.root, text ="Find", command = self.load_a_recommendation, width = 20, height =2)
        self.find_button.place(x =140, y =138)


        #Creates the watchlist button 
        self.watch_list_button = tk.Button(self.root,text = 'Watchlist', command = self.watched_list_frame, width = 20, height = 2)
        self.watch_list_button.place(x = 140, y= 188)


        #Creates the watched button 
        self.watched_list_button = tk.Button(self.root,text = 'Watched', command = self.watched_movie, width = 20, height = 2)
        self.watched_list_button.place(x = 140, y= 238)


        #Creates the search button 
        self.search = tk.Button(self.root,text = 'Search', command = self.search_a_movie, width = 20, height = 2)
        self.search.place(x = 140, y= 288)


        self.root.mainloop()

    


    def load_a_recommendation(self):

        """ Loads a reccomendation of a movie from your history list """

        # Searches your movie id's and finds similar movies 
        movie_ids = [] 

        for movie in self.database['title_id'].unique():
            movie_ids.append(movie)

        self.rec_id_nums = [] # holds recommmendation movie id numbs 

        #Adds recommended numbers to new list if movie

        for i in movie_ids:
            if i not in self.rec_history['title_id']:          
                numbers = pa.get_similar(i)
                self.rec_id_nums.append(numbers)
                

                title_id,title,release_date,poster_path,overview,youtube_key = pa.get_movie_info(i)
                line = [title_id,title,release_date,poster_path,overview,youtube_key]
                series = pd.Series(line, index = self.rec_history.columns)
                self.rec_history = self.rec_history.append(series, ignore_index=True)
                self.rec_history.to_csv(self.rec_h, mode='a', header=False, index = False)




            else: 
                pass 



        
        #current movie 
      
        movie_num = self.rec_id_nums[0][self.load_count]
        title_id,title,release_date,poster_path,overview,youtube_key = pa.get_movie_info(movie_num)
            
        self.find_frame(title_id,title,release_date,poster_path,overview,youtube_key)
        self.find_screen




    def find_frame(self,title_id,title,release_date,poster_path,overview,youtube_key):


        """ Find Frame to swipe through movies """ 
            #Need to work on closing windows when switching frames 

        try:
            #destroys previous window 
            self.root.destroy()

        except:
            pass 

         
        #creates a new window 
        self.find_screen = tk.Tk()   
        self.find_screen.geometry('475x478')

        #Creates title for screen
        self.find_screen.title('MyWall')

        #frame to hold all the widgets in order to be able to delete and repopulate 
        self.dummy_frame = tk.Frame(self.find_screen, width = 475, height = 478)
        self.dummy_frame.pack(fill ='both', expand = True)



        #Create the backbutton to the main screen
        self.backbutton = tk.Button(self.dummy_frame,text = "<--", command = home)
        self.backbutton.place(x =10, y =11)
        

        #creates ttile of movie
        title_of_movie = tk.Label(self.dummy_frame, text = title,font =(self.main_font,12) )
        title_of_movie.place(x =50, y=11)


        #Creates canvas to hold poster for movie 
        self.poster_frame = tk.Frame(self.dummy_frame, bg ='black', width =164, height =134)
        self.poster_frame.place(x=15, y=42)




        #loads poster onto canvas by retrieving the imaage from the the database 

        try:
            image_url = self.main_image_url + poster_path

            data = urllib.request.urlopen(image_url)
            raw_data = data.read()
            data.close()

            im = Image.open(BytesIO(raw_data))
            image = ImageTk.PhotoImage(im)


            self.poster_image = tk.Label(self.poster_frame, image = image )
            self.poster_image.pack(fill ='both', expand = True)

        except:
            self.no_image = tk.Label(self.poster_frame, text = "NO IMAGE")
            self.no_image.pack(fill ='both', expand = True)




        #Overview textbox
        self.overview_textbox = tk.Text(self.dummy_frame, width = 34, height = 20)# state = 'disabled'
        self.overview_textbox.insert('end',overview) # adds the overview to the box 
        self.overview_textbox.config(state = 'disabled')
        self.overview_textbox.place(x= 220, y=43)


     


        #play button for trailer 
        self.play_button = tk.Button(self.dummy_frame, text = 'Play', width = 10, height = 3, command = lambda: self.open_trailer_link(youtube_key))
        self.play_button.place(x=167, y=350)



        #add to watch list button 
        add_watch_list = tk.Button(self.dummy_frame, text = 'Watch', height =2, width = 10, command = lambda: self.add_movie(title_id,title,release_date,poster_path,overview,youtube_key))
        add_watch_list.place(x=122 , y=433)

        #Watched button for movies 
        already_watched_button = tk.Button(self.dummy_frame, text = 'Watched', height =2, width = 10, command = lambda: self.add_movie_to_seen(title_id,title,release_date,poster_path,overview,youtube_key))
        already_watched_button.place(x=222 , y=433)



        self.find_screen.mainloop()

 

    def open_trailer_link(self,trailer_path):
        """Opens youtube and players trailer """ 
        
        webbrowser.open(trailer_path,new=1)
    

    def add_movie(self,title_id,title,release_date,poster_path,overview,youtube_key):

        """ Adds movie to the database of movies you intend to watch located in the movies csv file """ 

        self.load_count += 1 

        line = [title_id,title,release_date,poster_path,overview,youtube_key]
        series = pd.Series(line, index = self.database.columns)
        self.database = self.database.append(series, ignore_index=True)
        self.database.to_csv(self.movies_csv, mode='a', header=False, index = False)
        messagebox.showinfo('Success',"Movie successfully added") #message box to display success of movie added
        
        #Destroys old screen 
        self.dummy_frame.destroy()
        self.dummy_frame = None 

        #creates a new one with a new reccomendation 
        movie_num = self.rec_id_nums[0][self.load_count]
        title_id,title,release_date,poster,overview,youtube_key = pa.get_movie_info(movie_num)
        
        self.find_frame(title_id,title,release_date,poster,overview,youtube_key)
        self.find_screen


    def add_movie_to_seen(self,title_id,title,release_date,poster_path,overview,youtube_key):

        """ Adds movies you already seen into a history csv file  """ 

        self.load_count += 1 

        line = [title_id,title,release_date,poster_path,overview,youtube_key]
        series = pd.Series(line, index = self.database.columns)
        self.history_database = self.history_database.append(series, ignore_index=True)
        self.history_database.to_csv(self.history_csv, mode='a', header=False, index = False)
        messagebox.showinfo('Success',"Movie successfully added") #message box to display success of movie added
        
        #Destroys old screen 
        self.dummy_frame.destroy()
        self.dummy_frame = None 

        #creates a new one with a new reccomendation 
        movie_num = self.rec_id_nums[0][self.load_count]
        title_id,title,release_date,poster,overview,youtube_key = pa.get_movie_info(movie_num)
        
       
        self.find_frame(title_id,title,release_date,poster,overview,youtube_key)
        self.find_screen
 
    
    def watched_list_frame(self):

        """Shows your watch list of movies """

        self.root.destroy()

        #Creates window 
        watch_list = tk.Tk()
        watch_list.geometry('448x378')
        watch_list.title('MyWall')



        #Creates the backbutton 
        backbutton = tk.Button(watch_list, text = "<--", command = home)
        backbutton.place(x =10, y =11)


        #creates my wall label 
        my_wall_label = tk.Label(watch_list, text ='My Wall',font =(self.main_font,12) )
        my_wall_label.place(x =195, y=11)



        #Listbox to display results 
        self.watched_listbox = tk.Listbox(watch_list, height =16 , width = 46)
        self.watched_listbox.bind('<<ListboxSelect>>',self.remove_from_watched)
        self.watched_listbox.place(x=14, y = 66)

        
        "Loads the results onto canvas"

        titles = self.database['title'].unique()

        for name in titles:
            self.watched_listbox.insert('end',name)



        

        

        watch_list.mainloop()


    def remove_from_watched(self, *args):
        #removes movie from watch list 

        #gets selection from listbox
        selected = self.watched_listbox.get(self.watched_listbox.curselection())

        #finds the location in the database and then removes it from the database and updates csv file
        location = self.database[self.database['title']== selected].index.values
        self.database.drop(location)
        self.database.to_csv(self.movies_csv, mode='a', header=False, index = False)

        #removes from listbox 
        value = self.watched_listbox.curselection()
        self.watched_listbox.delete(value)


    def watched_movie(self):

        """Shows your watch list of movies """

        self.root.destroy()

        #Creates window 
        watched_movies = tk.Tk()
        watched_movies.geometry('448x378')
        watched_movies.title('MyWall')



        #Creates the backbutton 
        backbutton = tk.Button(watched_movies, text = "<--", command = home)
        backbutton.place(x =10, y =11)


        #creates my wall label 
        my_wall_label = tk.Label(watched_movies, text ='My Wall',font =(self.main_font,12) )
        my_wall_label.place(x =195, y=11)



        #Listbox to display results 
        self.watched_movie_listbox = tk.Listbox(watched_movies, height =16 , width = 46)
        self.watched_movie_listbox.place(x=14, y = 66)

        
        "Loads the results onto canvas"

        titles = self.history_database['title'].unique()

        for name in titles:
            self.watched_movie_listbox.insert('end',name)


        

        

        watched_movies.mainloop()   



    def search_a_movie(self):

        """Lets you search for any movie in the movie database and add it to your watchlist"""


        self.root.destroy()

        #Creates window 
        search = tk.Tk()
        search.geometry('448x378')
        search.title('MyWall')



        #Creates the backbutton 
        backbutton = tk.Button(search, text = "<--", command = home)
        backbutton.place(x =10, y =11)


        #creates search entry bar 
        self.search_bar = tk.Entry(search, width =30)
        self.search_bar.place(x =63, y = 10)

        search_button = tk.Button(search,width = 8, text = 'Search', command = self.searching)
        search_button.place(x = 345, y =13)



        #Listbox to display results 
        self.search_listbox = tk.Listbox(search, height =16 , width = 46)
        self.search_listbox.place(x=14, y = 66)
        self.search_listbox.bind('<<ListboxSelect>>',self.selected_movie)

       



        #Add Button 
        add_button = tk.Button(search, text = 'Add', height =1 , width = 10, command = self.add_movie_to_watch)
        add_button.place(x=171, y=343)


        

        

        search.mainloop()
  









    """ REQUESTS """

    def searching(self):
        """ Searches for a movie in the movie database and uploads it to the listbox"""

        #clears the previous searches 
        self.search_listbox.delete(0,tk.END)

        #movie name 
        search_name = str(self.search_bar.get())

        #movie search results 
        self.results = pa.search_movie_name(search_name)

        #appends results to listbox
        for movie in self.results:
            self.search_listbox.insert('end',movie[1])
        
        


    def selected_movie(self, *args):
        """Gets the selected movie from the list box""" 
        self.selected = self.search_listbox.get(self.search_listbox.curselection())
        
    
    
    def add_movie_to_watch(self, *args):

        """ Add a movie to your watchlist located in the movies csv file """ 
        
        try:
            if self.selected is not None: #makes sure the user selected a movie 
                for line in self.results: #goes through each line in the result 

                    name_of_movie = line[1] #name of the movie in results 
                    id_num = line[0]

                    if name_of_movie == self.selected: # matches the selected movie in the results 
                        
                        
                        if self.intended_list.empty: #makes sure the movie was not already added to list 
                            
                            series = pd.Series(line, index = self.database.columns)
                            self.database = self.database.append(series, ignore_index=True)
                            self.database.to_csv(self.movies_csv, mode='a', header=False, index = False)

                            messagebox.showinfo('Success',"Movie successfully added") #message box to display success of movie added
                            

                        elif id_num not in self.intended_list: #checks to see if you have any movies in your database

                            series = pd.Series(line, index = self.database.columns)
                            self.database = self.database.append(series, ignore_index=True)
                            self.database.to_csv(self.movies_csv, mode='a', header=False, index = False) #saves to movies csv

                            messagebox.showinfo('Success',"Movie successfully added") #message box to display success of movie added 
                          


                        else: 
                            messagebox.showinfo('Duplicate',"Movie is already added in your list") #message box to display duplicate of movie added

           

        except:
            print('Couldnt Add')


    



    """
    def clean_csv(self):
        new = pd.read_csv(self.movies_csv,usecols=['title_id']).drop_duplicates(keep='first').reset_index() 
        new.to_csv(self.movies_csv,index = False)
    """


if __name__ == "__main__":
    h = home() 
    h 