# GoTime Project ToDo List
Here is a small non-exhaustive list of future improvements.
___
- [ ] Addition of a system allowing the user to record times (for example those that he uses regularly), in
addition to the initial system with the `spinbox` entries. This would consist of a `combobox` type drop-down menu, which
would only be displayed if at least one time is already recorded, otherwise a button to create a new predefined time.
If one or more times have already been recorded, the selector is displayed, next to it a button to launch the predefined time
on the timer and another to add a new time to the list.

- [ ] Addition of an extension system to the application, such as a secure password generator, a stopwatch, or a random class plan generator, for example. The extensions would be stored on a GitHub separate from that of the application, and the latter
would download and integrate the one that the user wants in a specific tab of the settings.

- [ ] Choice of ringtone. In future versions of the application, it will be possible to choose the ringtone via a selector in the
settings, of the `combobox` type. This selector will be managed dynamically via the `tkinter` variable of the switch allowing to activate the
ringtone. Concretely, if the ringtone is deactivated then the selector will be grayed out, unusable.

- [x] Change of GUI module. Basically the project should have used a cross-platform library like wxWidget (use of the wxPython adaptation), see use the base library for better performances by recreating the application in `C++`. In the end, use of [customtkinter](https://github.com/tomschimansky/customtkinter), a module adding an overlay to the Tcl/Tk wrapper integrated into python3 with more modern widgets.

- [x] Finish the "About" section of the "Source" menu