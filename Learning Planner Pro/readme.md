# Learning Planner Pro
**Cloud-Based Academic Planner with Google Calendar Sync**

## Learning Planner Pro is a modern, cloud-deployed productivity web application built using Streamlit and integrated with the Google Calendar API.

It allows users to:
1. 📅 Add tasks directly to their Google Calendar
2. 📥 Track assignments with deadlines
3. 📊 Analyze academic performance
4. ⏲️ Improve focus using Pomodoro timer
5. 🌍 Access tasks from any device

**This project is deployed on a Google Cloud Platform (GCP) Virtual Machine, making it scalable and production-ready.**

**🚀 Key Features**
1. 📅 Google Calendar Integration (Core Feature)
2. OAuth2-based Google authentication
3. Secure token generation & storage
4. Automatic event creation in Google Calendar
5. Task & assignment sync across all devices
6. Real-time update support
7. Cross-device accessibility

**When a task is added →**
It is immediately created inside the user's Google Calendar.

**Accessible from:**
- Mobile
- Desktop
- Tablet

**Google Calendar Web App**
1. 📊 Dashboard (Command Center)
2. Today's tasks overview
3. Pending assignments summary
4. Deadline alerts
5. Visual metrics display
6. Quick completion actions
7. Success animations

**📋 Task Management**
Users can:
1. Add tasks with title
2. Select category
3. Set date
4. Set start & end time
5. Sync automatically with Google Calendar
6. Mark tasks complete
7. Delete tasks

**📥 Assignment Tracking**
Users can:
1. Add assignment name
2. Set deadline date & time
3. Sync with Google Calendar
4. View upcoming deadlines
5. Mark completed

**🛠️ Productivity Tools**
1. **📊 CGPA Heatmap Analytics**
   - Enter subject-wise marks
   - Generates interactive heatmap
   - Calculates average automatically
2. **🧮 Smart Calculator**
   - Evaluate mathematical expressions instantly
3. **⏲️ Pomodoro Focus Timer**
   - 25-minute focus session
   - Countdown timer
   - Break reminder
   - Productivity boost tool
4. Set deadline date & time

**Sync with Google Calendar**
Users can:
1. Sync tasks & assignments with their Google Calendar
2. View all events in their calendar

**View upcoming deadlines**
Users can:
1. See all deadlines set for the current day
2. Filter deadlines by category

**Mark completed**
Users can:
1. Mark tasks & assignments as completed
2. View completed items in the dashboard

**🛠️ Productivity Tools**
1. **📊 CGPA Heatmap Analytics**
   - Enter subject-wise marks
   - Generates interactive heatmap
   - Calculates average automatically
2. **🧮 Smart Calculator**
   - Evaluate mathematical expressions instantly
3. **⏲️ Pomodoro Focus Timer**
   - 25-minute focus session
   - Countdown timer
   - Break reminder
   - Productivity boost tool    

4. **Enter subject-wise marks**
   - Input marks for each subject
   - View interactive heatmap
   - Calculate average CGPA

5. **🧮 Smart Calculator**
   - Evaluate mathematical expressions instantly

6. **⏲️ Pomodoro Focus Timer**
   - 25-minute focus session
   - Countdown timer
   - Break reminder
   - Productivity boost tool

**🎨 UI & Design**
1. **Fully responsive layout**
2. Modern Google-style typography
3. Clean navigation menu
4. Card-based UI system
5. Smooth animations
6. Minimal & professional design

**☁️ Cloud Architecture**
1. **This application runs on:**
   - Google Cloud Platform (GCP)
   - Virtual Machine Instance
   - Google Calendar API
   - OAuth2 Authentication

**Flow Architecture**
1. User → Streamlit App (GCP VM)
        ↓
2. Google OAuth2 Authentication
        ↓
3. Access Token Generated
        ↓
4. Google Calendar API
        ↓
5. Event Created in User's Calendar

**🧑‍💻 Tech Stack**
Technology	Purpose
Streamlit	Web App Framework
Google Calendar API	Calendar Event Sync
Google Cloud Platform	Cloud Deployment
OAuth2	Secure Authentication
Pandas	Data Handling
NumPy	Calculations
Plotly	Visual Analytics
Streamlit Lottie	Animations

**📂 Project Structure**
Learning-Planner-Pro/
│
├── app.py                # Main Streamlit application
├── logic.py              # Google Calendar & task logic
├── main.py               # Google OAuth authentication flow
├── credentials.json      # Google API credentials
├── token.json            # OAuth access token
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

**⚙️ Setup & Installation**
1️⃣ Enable Google Calendar API
* Go to Google Cloud Console
* Create a new project
* Enable Google Calendar API
* Configure OAuth consent screen
* Create OAuth credentials
* Download credentials.json

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run Application
streamlit run app.py

**🔐 Authentication Process**
1. User logs in with Google account
2. OAuth consent screen appears
3. Access token generated
4. Token stored locally
5. All API calls made using authorized credentials
6. Tasks are synced directly with Google Calendar

**📌 Usage Guide**
1. Add Task
   Go to "Add Task"
2. Enter details
   Submit
3. Event automatically created in Google Calendar
   Add Assignment
4. Navigate to "Assignments"
   Set deadline
5. Save
   Deadline appears in calendar
6. View Dashboard
   Track tasks for today
7. See pending work
   Mark items completed
8. Use Tools
   Analyze marks via heatmap
9. Calculate instantly
   Start Pomodoro timer

**📈 Future Improvements**
Email notifications
SMS reminders
AI-based smart scheduling
Google Classroom integration
Multi-user system
Dark mode
Mobile app version
Performance analytics dashboard

**🎯 Ideal For**
1. Students
2. College learners
3. Competitive exam aspirants
4. Productivity-focused individuals
5. Developers learning API integration
6. Portfolio projects

**🏆 Why This Project Stands Out**
1.Real-world Google API integration
2.Cloud deployment experience
3.OAuth authentication implementation
4.SaaS-style architecture
5.Cross-device synchronization
6.Modern UI/UX design
7.Analytics + Productivity in one system
This is not just a basic Streamlit app —
**It demonstrates API integration, authentication, cloud deployment, and real-world application design.**

**🤝 Contribution**
Contributions are welcome.
Steps:
1. Fork the repository
2. Create a new branch
3. Make changes
4. Submit Pull Request  

**🐛 Reporting Issues**
If you find a bug:
1. Describe the issue clearly
2. Provide steps to reproduce
3. Include screenshots (if possible)

📜 License
This project is licensed under the MIT License.

👨‍💻 Author
By : Manan Chawla
Built with focus, productivity, and scalability in mind.