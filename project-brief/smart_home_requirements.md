# Smart Home Requirements

## Standard Requirements

### House

| #   | Requirement                                                                              |
| --- | ---------------------------------------------------------------------------------------- |
| 1   | LED lights up between 8pm to 7am                                                         |
| 2   | If PIR movement detected light up RGB in orange                                          |
| 3   | If steam sensor detects moisture (water droplet), close window, flash RGB blue           |
| 4   | If gas sensor detects gas/flame, turn on fan until sensor stops detecting, solid RGB red |
| 5   | RGB flashes red and buzzer buzzes when unknown RFID card is scanned                      |

### Web App

| #   | Requirement                                                                                         |
| --- | --------------------------------------------------------------------------------------------------- |
| 1   | Current temperature in celsius                                                                      |
| 2   | Current humidity as a percentage                                                                    |
| 3   | Show asthma alert on LCD if humidity is greater than 50% and temperature is over 27 degrees celsius |
| 4   | Display number of PIR detections in the last hour                                                   |
| 5   | Alert when gas sensor detects                                                                       |
| 6   | Show a list of all RFID scans, allow filter for successful and failed                               |
| 7   | Show status (open/closed) of door and window                                                        |
| 8   | Show status of fan (on/off)                                                                         |
| 9   | Open window and door via web app                                                                    |
| 10  | Turn on fan via web app                                                                             |

### Database

| #   | Requirement                                                |
| --- | ---------------------------------------------------------- |
| 1   | Logs temperature and humidity every 30min                  |
| 2   | If PIR movement detected log into database – time and date |
| 3   | Log every gas sensor detection - time, date, value         |
| 4   | RFID logs in user against users in database                |
| 5   | Logs ALL RFID scans - success or fail, time                |

---

## Extra - Bonus Requirements

### House

- PIR can be armed by 2 clicks lhs button, 3 clicks on rhs button, 1 click on lhs button. Disarm is the same combo
- If both buttons are held down while RFID is scanned, register the card
- If PIR is armed and senses, make buzzer sound like alarm and RGB flash blue and red
- Alarm can be disarmed using same button combo as arming/disarming the PIR
- Automatically disable PIR if valid RFID card

### Web App

- Show average temperature per day
- Show historical list of temperature and humidity - allow to filter by date
- Card number can be associated with a user - create new user interface if required
- PIR can be armed and disarmed
- Alert if alarm is triggered
- Alarm state can be disarmed

### Database

- User roles - Parent can control doors and windows, Child can only view house status

---

## Technical Requirements

### House

1. Micropython or Arduino C

### Web App

1. Javascript framework must be used
2. Allow users to log in via web app. This is counted as equivalent to RFID login

### API

1. C# API must be used if API layer is created separately to Web App
2. _C# API required for extra/bonus implementation_

### Database

1. ERD must be created
2. Relational database required

### Project Management

1. User stories/requirements must be logged/tracked in a project management tool
2. Tasks must show date started and completed as a bare minimum
3. All code is to be version controlled via GitHub
4. Must be deployed to an online environment with CI/CD capabilities
5. MQTT must be used for communication with the house (SSL/TLS not required)
6. Mock-ups/Wireframes need to be attached
