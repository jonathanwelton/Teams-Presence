print("Please select which presence indicator to wish to use...")
print("Press 1 to run the Teams Presence Indicator")
print("Press 2 to run the Zoom Presence Indicator")
choice = input("Indicator: ")

if choice == '1':
    print("Starting the Teams Presence Indicator...")
    import teamsPresence
    teamsPresence.run()

if choice == '2':
    print("Starting the Zoom Presence Indicator...")
    import zoomPresence
    zoomPresence.run()
