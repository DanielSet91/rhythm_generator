    # Rhythm Generator App
    #### Video Demo:  https://www.youtube.com/watch?v=ht1-7mKoQs0
    #### Description: Rhythmic generator app for musicians practice.
    

    ### For musicians rhythm is everything.
    So when we come to practice on rhythmic exercises its important it will be always something new and offer a challenging exprience.
    I wanted to build an app that will replace the old books and generate for you, upon your choices, a new exercise.

    I've started with an array that stores dictinories of all common rhythmic notes, their image, their value and name.
    I've created a class that will reprsent the generator app and interface.
    within the init function I've set up all the dictinories, config files, logging and the paths.  
    the gui function handles all the interface - buttons, configurations and the fields.
    the toggle pattern function should handle the add or remove from the list of all the user rhythmic notes.

    ### The most important function in the app is the generate_oneBar.
    This function is handling the given length of the bar(time signature),
    and ensures the production of a random bar.
    The function handles most of the exceptional states to make sure the bar won't get funky such as:
    choosing rhythms that won't work(for example: quarter(1, 4) and dotted-eighth note(3, 16) in case a 4/4 time signature is chosen)
    producing triplets in rhythmic places that will exceed the time signature of the bar.
    making sure the chosen rhythmic notes list isnt empty.

    ### After sending the app for friend to check, I was needed to add some files to track down bugs.
    In order to keep track on bugs and configuration problems I've added the logging and configuration options.
    the logging makes sure that to make a file rhythm_generator.log that will capture all the loggings in order to send them back to me.
    The configuration options were meant for those who have other programs than the one I was working with, such as Finale and Sibelius.
    making sure after the first configuration a file called config.ini will be created and store the configurations.
    added the options to configure each program and a radio switcher to choose from which program to launch the musicxml file.
    Either way, a musicxml suppose to be created.
    I've added an option to let the user choose where to save the file and an option to let the user choose the type of file that will be saved(musicxml/midi)

    I've built functions that will handle triplets, for they are tricky and can cause some problems.
    the valid custom signature making sure the time signature is legit within the laws of music!
    The valid custom signature checks for the standart type of time signature writing, checks if the base is legit
    and for reducing bugs, I've made sure the numerator won't excceed the number 60.
    the generatre rhythms yields the chosen number of bars one by one, thus making sure it will run faster.
    the generate and show music handles espically on producing the musicxml, streaming it into the chosen music program(Finale, Sibelius or MuseScore)
    The show music function also randomly choosing between a note(80%) and the same note duration silence(20%)

    the app.py contains the module rhythm_generator and makes an isntance of the class.