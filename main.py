from skimmer import insert_new, add_tags, get_files, find_tagless, init_db
from gen_report import generate

if (input("Would you like to insert new entries and add new tags? ").lower()) == (
    "yes" or "y"
):
    init_db()
    insert_new(get_files())
    add_tags(find_tagless())

if (input("Would you like to generate reports? ").lower()) == ("yes" or "y"):
    generate()
    print("Success: Reports generated!")
else:
    print("No reports generated")
