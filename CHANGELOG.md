# CHANGELOG

Change log for GoTime application project, create at the 2.0.0 version

## Semantic versioning
base : x.y.z
with :
- x : major changes
- y : minor changes
- z : patch changes
___
## [2.0.0] - 2024-12-28

⚙️ _alpha test version._

## Fixed
- application windows are now modal (only one icon in the taskbar)
- the ringtone doesn't work when the stop timer button is clicked, but it works when the timer stops by itself

## Changed
- the application now uses a more modern `tkinter` overlay for the graphical interface (`customtkinter`)
- translation of code and documentation into English

## Added
- ability to enable or disable the <kbd>ctrl+Q</kbd> keyboard shortcut to quit the application
- creation of this `changelog.md` file

## [1.1.0] - 2024-9-10

⚙️ _alpha test version._

### Fixed
- the application no longer needs to restart because of the redesign of the operation of the settings
- About window with checking for update

## [1.0.2] - 2024-8-30

🔄 _beta test version._

### Added
- installer file for Linux
- icon on all application windows

### Bug
- reboot still doesn't work
- the application is flagged by antivirus (tested on Avast)

## [1.0.1] - 2024-7-1

🔄 _beta test version._

### Fixed
- working ringtone on Microsoft Windows

### Bug
- reboot not working

## [1.0.0] - 2024-6-26
🌱 _Initial release. beta version_

[2.0.0]: https://www.github.com/pandaroux007/RepulsTime/releases/tag/v2.0.0
[1.1.0]: https://www.github.com/pandaroux007/RepulsTime/releases/tag/v1.1.0-beta
[1.0.2]: https://www.github.com/pandaroux007/RepulsTime/releases/tag/v1.0.1-stable
[1.0.1]: https://www.github.com/pandaroux007/RepulsTime/releases/tag/v1.0.1-stable
[1.0.0]: https://www.github.com/pandaroux007/RepulsTime/releases/tag/v1.0.1-beta