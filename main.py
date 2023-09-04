#!/home/jerome/misc/projects/programming/basic_venv/bin/python3
from skimmer import insert_new, add_tags, get_files, find_tagless
from gen_report import generate

if (input("Would you like to insert new entries? ").lower()) == ("yes" or "y"):
    print("Inserting new entries...")
    insert_new(get_files())
    print("Done\n")
else:
    print("No new entries inserted")

if (input("Would you like to add new tags? ").lower()) == ("yes" or "y"):
    add_tags(find_tagless())
else:
    print("No new tags added")

if (input("Would you like to generate reports? ").lower()) == ("yes" or "y"):
    generate()
    print("Success: Reports generated!")
else:
    print("No reports generated")
