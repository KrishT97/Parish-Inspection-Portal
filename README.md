### Update V2
- Views.py is now modified to be class based instead of function based.
- Improved register and login page UI
- For each Parish creation, a profile pic default or user uploaded will be shown.
- In Parish details page, the UI is better now and Number of inspections as well as reference is shown (starting from oldest to newest).
- Admin has control over all parishes and inspections (CRUD)
- Questions UI is better, fixed where certain answers where not appearing.
- Edit inspection UI now shows the questions as well (not just the topics as before).
- Delete option confirmation page is made.
- Options for question responses are now "yes", "no", and "other", can make general comments at the end
- Pagination on homepage
#### Things to consider for next update
- UI can be better for all pages.
- Signals is incorporated, however questions does not get populated in "Questions" section in admin page yet due to the current logic. Basically right now questions can be     added for each inspection created but the idea is to pre-load all the questions and have the changes take effect on all new inspections.  Have to look into this**
- Should also have an option to remove parishes, only admin can delete for now.
- Be able to modify profile pic in parish detail page anytime.
- Improve the ID of parishes parish/paris_id , it somehow shows random numbers and could not be considering deleted parishes or inspections to restart the numbering
- A return to button in parish and inspection page, to go back to previous page.
### Example UI
<img src="https://github.com/KrishT97/parish_inspection/blob/main/extras/home.jpg" width="800"/>
<img src="https://github.com/KrishT97/parish_inspection/blob/main/extras/fancyparish.jpg" width="800"/>
