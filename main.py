#!/home/jerome/misc/projects/programming/basic_venv/bin/python3
if (input("Would you like to insert new entries? ").lower()) == "yes" or "y":
    import skimmer

    print("Inserting new entries...")
    skimmer.insert_new(skimmer.get_files())
    print("Done\n")
else:
    print("No new entries inserted")

if (input("Would you like to add new tags? ").lower()) == "yes" or "y":
    import skimmer

    skimmer.add_tags(skimmer.find_tagless())
else:
    print("No new tags added")

if (input("Would you like to generate reports? ").lower()) == "yes" or "y":
    import gen_report

    gen_report.generate()
    print("Success: Reports generated!")
else:
    print("No reports generated")
