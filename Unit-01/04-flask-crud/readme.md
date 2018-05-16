# Flask CRUD

For this application you will be building CRUD on the resource `snacks`. Your application should:

- display all the `snacks`
- allow a user to create `snacks` 
    -  each snack should have a `name` and `kind`
- allow a user to edit a snack
- allow a user to delete a snack

You should use a list to store your snacks and make a class for a snack to create instances from.

**BONUS** Make your app look amazing with some CSS!
**BONUS** If you go to the show page for an invalid id, your application will break. Create a 404 page and redirect to it in the event that a user tries to go to the show or edit pages for a snack with an invalid id.

### Brendon's Notes
- Because we are not using a database yet, all data added to the web app that is not hard coded will be deleted when the app is shut down/restarted which happens with every file save in Flask's debug mode
