import sys
from repositories.MovieRepository import Movie_Repository
from services.MovieService import Movie_Service
import datetime

class Movie():


    def __init__(self, movie_name: str, publish_year: str):
        self.movie_name = movie_name
        self.publish_year = publish_year
        self.votes = 0


    # This is for testing only
    '''
    test_movie_1 = Movie("The Shawshank Redemption", "1994")
    MovieRepository.list_of_movies_to_be_voted.append(test_movie_1)
    test_movie_2 = Movie("The Godfather", "1972")
    MovieRepository.list_of_movies_to_be_voted.append(test_movie_2)
    test_movie_3 = Movie("The Dark Knight", "2008")
    MovieRepository.list_of_movies_to_be_voted.append(test_movie_3)
    test_movie_4 = Movie("The Godfather: Part II", "1974")
    MovieRepository.list_of_movies_to_be_voted.append(test_movie_4)
    '''


    # Movie basic functionalities for user
    def welcome_to_movieapp():

        voting_status = Movie_Repository.check_voting_status()


        if voting_status == "open":
            print("This weeks movie vote is open!\n")
        else:
            print("Unfortunately there is no ongoing movie voting right now.")


        while True:

            print("What would you like to do?")

            if voting_status == "open":
                print("  [S]ee movie voting list")
                print("  [V]ote for a movie ")
                print("  [P]ropose a movie for nex weeks vote")
                print("  [E]xit app \n")

            answer = input("Answer by giving a letter: ")

            if answer in ("E", "e"):
                print("Bye!")
                sys.exit()
            elif answer in ("S", "s"):
                Movie_Service.print_voting_list()
            elif answer in ("V", "v"):
                Movie.suggest_a_movie()
            elif answer in ("P","p"):
                Movie.suggest_a_movie()
            else:
                print("Please choose from the list. ")

    def get_movie_name(self, movie):
        return movie.movie_name


    def movie_to_string(self, movie):
        return "{movie.movie_name} (published in {movie.publish_year}"


    # User can vote for a movie by giving number 1-4.
    def vote_for_movie():

        print("")
        print("This weeks candidates: ")
        Movie_Service.print_voting_list()
        print("")

        while True:
            vote = input("My vote (write number): ")

            if vote.isnumeric and int(vote) >= 1 and int(vote) <= 4:
                the_movie = Movie_Repository.list_of_movies_to_be_voted[vote - 1].get_movie_name()

                Movie_Repository.save_movie_vote(the_movie)
                print("Thank you for voting! \n")
                break

            print("Please answer by giving number 1, 2, 3 or 4. ")
            continue


    def suggest_a_movie():

        print("You can suggest one movie for next weeks voting.")    
        print("App admin(s) will decide, if this movie is worthy.\n")

        while True:
            movie_name = input("Please give movie name: ")

            if len(movie_name) < 1:
                print("Movie name is too short. Please give correct movie name. \n")
                continue
            break

        while True:
            publish_year = input("Please give movie publish year: ")
            current_date = datetime.date.today()
            current_year = current_date.year


            if int(publish_year) < 1878:
                print("Please check the year.")
                print("As a true movie fan, you do must now that the first movie was published 1878.\n")
                continue
            if int(publish_year) > current_year + 1:
                print("Please check the year.")
                print("It can't be bigger than current year. (We are no going back to the future.)")
                continue
            break

        new_movie = Movie(movie_name, publish_year)
        Movie_Repository.list_of_movie_suggestions.append(new_movie)

        Movie_Repository.save_movie_suggestion(movie_name, publish_year)

        print("Thank you for your suggestion!\n")


# For admin: set up a list of 4 movies for next vote. Admin can add movies of their choice
    # or pick max 4 suggestions from movie suggestion list.
    def set_voting_list():

        max_amount_of_movies_to_be_added = 4
        setting_successfull = False

        if len(Movie_Repository.list_of_movies_to_be_voted) > 0:
            print("Empty the current list before creating new")
            choice = input("Do you want to empty old list? [Y]es or [N]o: ")

            if choice in ("Y", "y"):
                Movie_Repository.empty_voting_list
            elif choice in ("N", "n"):
                print("Can't add any more movies right now.")
                return setting_successfull

        movies_added = 0

        print("Would you like to add something from the suggestions list?\n")
        choice1 = input("Choose below: ")
        print("  [Y]es, show me the list")
        print("  [N]o \n")

        while True:
            if choice1 in ("Y", "y"):
                Movie_Repository.print_movie_suggestion_list()
                print()
                choice2 = print("If you want to add any of these, type the movie number. If not, press [X].\n")

                if len(Movie_Repository.print_movie_suggestion_list) <= choice2 > 0:
                    add_this_movie_to_be_voted = Movie_Repository.list_of_movie_suggestions[int(choice2) - 1]
                    Movie_Repository.list_of_movies_to_be_voted.append(add_this_movie_to_be_voted)
                    movies_added += 1
                elif choice2 in ("X", "x"):
                    break

        while movies_added < max_amount_of_movies_to_be_added:
            movie_name = input(f"Write movie no {movies_added + 1} name: ")
            publish_year = input("Publish year: ")
            print()
            new_movie = Movie(movie_name, publish_year)
            Movie_Repository.list_of_movies_to_be_voted.append(new_movie)
            movies_added += 1

        Movie_Repository.save_voting_list_to_file()

        setting_successfull = True
        print("\ņSetting movie list succesfull.\n")
        return setting_successfull
