from flask import Flask, request, jsonify, render_template_string, send_from_directory
import json, os
from datetime import datetime

DATA_FILE = "data.json"
app = Flask(__name__)


def load_data():
    if not os.path.exists(DATA_FILE):
        data = {"users": [], "quizzes": [], "encouragements": []}
        save_data(data)
        return data
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {"users": [], "quizzes": [], "encouragements": []}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def gen_id():
    return datetime.utcnow().strftime("%Y%m%d%H%M%S%f")


@app.route("/api/data", methods=["GET"])
def api_get_data():
    data = load_data()
    # Return flattened list of objects for compatibility with original script which filtered by keys
    combined = []
    for u in data["users"]:
        combined.append(u)
    for q in data["quizzes"]:
        combined.append(q)
    for e in data["encouragements"]:
        combined.append(e)
    return jsonify(combined)


@app.route("/api/create", methods=["POST"])
def api_create():
    payload = request.json
    if not payload:
        return jsonify({"isOk": False, "message": "No JSON body"}), 400
    data = load_data()

    # Detect object type by presence of keys
    if payload.get("user_id") or (payload.get("username") and payload.get("role")):
        # user
        data["users"].append(payload)
        save_data(data)
        return jsonify({"isOk": True, "created": payload})
    if payload.get("quiz_id") and payload.get("user_id"):
        data["quizzes"].append(payload)
        save_data(data)
        return jsonify({"isOk": True, "created": payload})
    if payload.get("encouragement_id") and payload.get("educator_id"):
        data["encouragements"].append(payload)
        save_data(data)
        return jsonify({"isOk": True, "created": payload})

    # fallback heuristics
    if "role" in payload:
        data["users"].append(payload)
    elif "quiz_id" in payload:
        data["quizzes"].append(payload)
    elif "encouragement_id" in payload:
        data["encouragements"].append(payload)
    else:
        data["users"].append(payload)
    save_data(data)
    return jsonify({"isOk": True, "created": payload})


@app.route("/api/sync_google", methods=["POST"])
def api_sync_google():
    mock_courses = [
        {"id": "1", "name": "Advanced Mathematics", "section": "Grade 10"},
        {"id": "2", "name": "Physics Fundamentals", "section": "Grade 10"},
        {"id": "3", "name": "World History", "section": "Grade 10"},
        {"id": "4", "name": "English Literature", "section": "Grade 10"},
    ]
    return jsonify({"isOk": True, "courses": mock_courses})


@app.route("/")
def index():
    # The full HTML (CSS + JS embedded). Kept as one template so this single-file app works.
    html = r'''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>EduTutor AI - Personalized Learning Platform</title>
  <style>
        /* == THEME UPDATED: light pink + light blue glassy UI + lively bubbles == */

        :root{
          --pink-100: #ffe8ef;
          --pink-200: #ffd9e6;
          --blue-100: #e6f4ff;
          --blue-200: #d0ecff;
          --glass-bg: rgba(255,255,255,0.35);
          --glass-border: rgba(255,255,255,0.6);
          --accent-pink: #ff9fc1;
          --accent-blue: #a6d8ff;
          --text-dark: #2b2b2b;
        }

        *{box-sizing:border-box}

        html,body{
          height:100%;
          margin:0;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          -webkit-font-smoothing:antialiased;
          -moz-osx-font-smoothing:grayscale;
          color:var(--text-dark);
        }

        /* lively gradient background */
        body {
            background: linear-gradient(135deg, var(--pink-200) 0%, var(--blue-200) 100%);
            overflow: auto;
        }

        /* === BUBBLES === */
        .bubble {
          position: absolute;
          bottom: -160px;
          border-radius: 50%;
          background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.95), rgba(255,255,255,0.08));
          box-shadow: inset -8px -12px 24px rgba(255,255,255,0.45), 0 10px 30px rgba(0,0,0,0.06);
          opacity: 0.9;
          filter: blur(0.2px);
          animation: rise 12s linear infinite;
          mix-blend-mode: screen;
        }

        @keyframes rise {
          0% { transform: translateX(0) translateY(0) scale(1); opacity: 0.8; }
          40% { opacity: 1; }
          100% { transform: translateX(-120px) translateY(-1200px) scale(0.8); opacity: 0; }
        }

        /* many different sizes/positions/delays for lively look */
        .bubble.n1 { width: 160px; height:160px; left: 8%; animation-duration: 18s; animation-delay: 0s; }
        .bubble.n2 { width: 100px; height:100px; left: 22%; animation-duration: 14s; animation-delay: 1.2s; }
        .bubble.n3 { width: 220px; height:220px; left: 36%; animation-duration: 20s; animation-delay: 2s; }
        .bubble.n4 { width: 80px; height:80px; left: 50%; animation-duration: 12s; animation-delay: 0.6s; }
        .bubble.n5 { width: 130px; height:130px; left: 64%; animation-duration: 16s; animation-delay: 3.2s; }
        .bubble.n6 { width: 180px; height:180px; left: 78%; animation-duration: 22s; animation-delay: 4s; }
        .bubble.n7 { width: 70px; height:70px; left: 12%; animation-duration: 13s; animation-delay: 5.5s; }
        .bubble.n8 { width: 110px; height:110px; left: 44%; animation-duration: 17s; animation-delay: 6.1s; }
        .bubble.n9 { width: 150px; height:150px; left: 86%; animation-duration: 19s; animation-delay: 7.3s; }
        .bubble.n10{ width: 95px; height:95px; left: 30%; animation-duration: 15s; animation-delay: 8.6s; }
        .bubble.n11{ width: 210px; height:210px; left: 60%; animation-duration: 21s; animation-delay: 2.8s; }
        .bubble.n12{ width: 55px; height:55px; left: 72%; animation-duration: 11s; animation-delay: 9.8s; }

        /* main container sits over bubbles */
        .container {
            position: relative;
            z-index: 5;
            max-width: 1400px;
            margin: 28px auto;
            padding: 20px;
            min-height: calc(100vh - 56px);
        }

        .header {
            text-align: center;
            color: var(--text-dark);
            margin-bottom: 32px;
            position: relative;
            z-index: 6;
        }
        .header h1 { font-size: 2.8rem; margin: 0; letter-spacing: -0.5px; }
        .header p { font-size: 1.2rem; margin: 12px 0; opacity: 0.95; }

        /* LARGER glassy panels - increased size */
        .auth-container, .dashboard-container {
            background: linear-gradient(180deg, rgba(255,255,255,0.45), rgba(255,255,255,0.25));
            border-radius: 20px;
            padding: 32px;
            box-shadow: 0 12px 30px rgba(39, 35, 77, 0.06);
            margin-bottom: 20px;
            border: 1px solid var(--glass-border);
            backdrop-filter: blur(10px) saturate(140%);
            -webkit-backdrop-filter: blur(10px) saturate(140%);
            min-height: 500px;
        }

        .tabs { display:flex; gap:12px; margin-bottom: 24px; position: relative; z-index: 6; }
        .tab { padding:14px 20px; cursor:pointer; border-radius:12px; background:transparent; border:1px solid transparent; font-weight:600; font-size: 1.1rem; }
        .tab.active { background: linear-gradient(90deg, rgba(255,159,193,0.25), rgba(166,216,255,0.25)); border-color: rgba(255,255,255,0.6); color:var(--text-dark); box-shadow: 0 6px 18px rgba(102,102,150,0.06); }

        .tab-content { display:none; }
        .tab-content.active { display:block; }

        .form-group { margin-bottom: 20px; }
        .form-group label { display:block; margin-bottom:8px; font-weight:600; color:var(--text-dark); font-size: 1.1rem; }
        .form-group input, .form-group select, .form-group textarea {
            width:100%; padding:14px; border-radius:12px; border:1px solid rgba(0,0,0,0.06); font-size:16px;
            background: rgba(255,255,255,0.7);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
        }

        .btn { padding:14px 18px; border-radius:12px; font-weight:700; cursor:pointer; border:none; font-size: 1.1rem; }
        .btn-primary { background: linear-gradient(90deg, var(--accent-pink), var(--accent-blue)); color:white; box-shadow: 0 8px 20px rgba(102,105,230,0.08); }
        .btn-secondary { background: rgba(255,255,255,0.7); color:var(--text-dark); border:1px solid rgba(0,0,0,0.06); }

        .btn-google { background: linear-gradient(90deg,#63a7ff,#2b8cff); color:white; display:inline-flex; gap:12px; align-items:center; justify-content:center; border-radius:12px; padding:14px 16px; font-size: 1.1rem; }

        .info-message, .error-message, .success-message {
            padding:16px; border-radius:12px; margin-bottom:16px; font-weight:600; font-size: 1.1rem;
        }
        .info-message { background: rgba(215,245,255,0.6); color:#0c5460; border:1px solid rgba(178,235,255,0.6); }
        .success-message { background: rgba(220,255,234,0.6); color:#155724; border:1px solid rgba(200,245,220,0.6); }
        .error-message { background: rgba(255,230,230,0.6); color:#721c24; border:1px solid rgba(255,200,200,0.6); }

        .dashboard-nav { display:flex; gap:10px; margin-bottom:18px; flex-wrap:wrap; }
        .nav-btn { padding:8px 12px; border-radius:10px; background: rgba(255,255,255,0.7); border:1px solid rgba(0,0,0,0.04); cursor:pointer; font-weight:700; }
        .nav-btn.active { background: linear-gradient(90deg, rgba(255,159,193,0.25), rgba(166,216,255,0.25)); color:var(--text-dark); box-shadow: 0 8px 20px rgba(100,100,160,0.05); }

        .stats-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; margin-bottom:16px; }
        .stat-card { padding:16px; border-radius:12px; color:var(--text-dark); background: linear-gradient(180deg, rgba(255,255,255,0.85), rgba(255,255,255,0.65)); text-align:center; border:1px solid rgba(0,0,0,0.03); box-shadow: 0 6px 18px rgba(73,72,114,0.02); }
        .quiz-card { background: rgba(255,255,255,0.82); padding:14px; border-radius:10px; border-left:4px solid rgba(166,216,255,0.6); margin-bottom:10px; box-shadow: 0 6px 18px rgba(80,80,120,0.02); }

        .quiz-question { background: rgba(255,255,255,0.9); padding:12px; border-radius:10px; border:1px solid rgba(0,0,0,0.04); margin-bottom:10px; }
        .quiz-options { margin-top:8px; }
        .quiz-option { padding:8px; border-radius:8px; background: rgba(250,250,250,0.9); margin:6px 0; cursor:pointer; display:flex; gap:8px; align-items:center; border:1px solid rgba(0,0,0,0.03); }
        .progress-bar { width:100%; height:8px; background:rgba(0,0,0,0.05); border-radius:6px; overflow:hidden; margin-top:8px; }
        .progress-fill { height:100%; background: linear-gradient(90deg, var(--accent-pink), var(--accent-blue)); width:0%; transition:width .25s ease; }
        .hidden { display:none !important; }

        .google-sync-status { padding:10px; border-radius:8px; background: rgba(220,255,234,0.6); color:#155724; margin-bottom:12px; }

        /* Quiz interface scrolling */
        #quiz-interface {
            max-height: 70vh;
            overflow-y: auto;
            padding-right: 10px;
        }
        
        #quiz-questions-container {
            max-height: 60vh;
            overflow-y: auto;
            padding-right: 5px;
        }
        
        /* Scrollbar styling */
        #quiz-interface::-webkit-scrollbar,
        #quiz-questions-container::-webkit-scrollbar {
            width: 8px;
        }
        
        #quiz-interface::-webkit-scrollbar-track,
        #quiz-questions-container::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.3);
            border-radius: 10px;
        }
        
        #quiz-interface::-webkit-scrollbar-thumb,
        #quiz-questions-container::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--accent-pink), var(--accent-blue));
            border-radius: 10px;
        }
        
        #quiz-interface::-webkit-scrollbar-thumb:hover,
        #quiz-questions-container::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #ff7bad, #8cc9ff);
        }

        /* Larger login card specific styles */
        .login-grid {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 30px;
            align-items: start;
        }
        
        .login-section, .google-section {
            padding: 20px;
        }
        
        .login-section h3, .google-section h3 {
            font-size: 1.5rem;
            margin-bottom: 20px;
            color: var(--text-dark);
        }

        @media (max-width:720px) {
            .container { padding:12px; margin:8px; }
            .header h1 { font-size:1.6rem; }
            .login-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            .auth-container {
                padding: 20px;
            }
            #quiz-interface {
                max-height: 80vh;
            }
        }

  </style>
</head>
<body>
  <!-- animated bubbles (lively) -->
  <div class="bubble n1"></div>
  <div class="bubble n2"></div>
  <div class="bubble n3"></div>
  <div class="bubble n4"></div>
  <div class="bubble n5"></div>
  <div class="bubble n6"></div>
  <div class="bubble n7"></div>
  <div class="bubble n8"></div>
  <div class="bubble n9"></div>
  <div class="bubble n10"></div>
  <div class="bubble n11"></div>
  <div class="bubble n12"></div>

  <div class="container">
    <div class="header">
      <h1 id="app-title">🎓 EduTutor AI</h1>
      <p id="welcome-message">Personalized Learning with Generative AI and LMS Integration</p>
    </div>

    <div id="auth-section" class="auth-container">
      <div class="tabs">
        <button class="tab active" data-tab="login">Login</button>
        <button class="tab" data-tab="register">Register</button>
      </div>

      <div id="login-tab" class="tab-content active">
        <div class="login-grid">
          <div class="login-section">
            <h3>Manual Login</h3>
            <form id="login-form">
              <div class="form-group"><label>Username</label><input id="login-username" required /></div>
              <div class="form-group"><label>Password</label><input id="login-password" type="password" required /></div>
              <button class="btn btn-primary" style="width:100%;">Login</button>
            </form>
          </div>
          <div class="google-section">
            <h3>Google Login</h3>
            <div class="info-message">🔐 Quick access with Google</div>
            <button id="google-login-btn" class="btn btn-google" style="width:100%; margin-top: 20px;">🔗 Login with Google Classroom</button>
            <div class="info-message" style="margin-top: 20px;">
              <strong>Benefits:</strong><br>
              • Sync with Google Classroom<br>
              • Access your courses<br>
              • Quick setup<br>
              • Secure authentication
            </div>
          </div>
        </div>
      </div>

      <div id="register-tab" class="tab-content">
        <h3 style="font-size: 1.5rem; margin-bottom: 20px;">Create New Account</h3>
        <form id="register-form">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="form-group"><label>Username</label><input id="reg-username" required /></div>
            <div class="form-group"><label>Email</label><input id="reg-email" type="email" required /></div>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="form-group"><label>Password</label><input id="reg-password" type="password" required /></div>
            <div class="form-group"><label>Confirm Password</label><input id="reg-confirm" type="password" required /></div>
          </div>
          <div class="form-group"><label>I am a:</label>
            <select id="reg-role" required style="padding: 14px; font-size: 16px;">
              <option value="">Select Role</option>
              <option value="student">Student</option>
              <option value="educator">Educator</option>
            </select>
          </div>
          <button class="btn btn-primary" style="width:100%; padding: 16px; font-size: 1.2rem;">Register</button>
        </form>
      </div>
    </div>

    <div id="dashboard-section" class="dashboard-container hidden">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
        <h2 id="dashboard-title">Welcome!</h2>
        <button id="logout-btn" class="btn btn-secondary">Logout</button>
      </div>

      <!-- Student dashboard -->
      <div id="student-dashboard" class="hidden">
        <div class="dashboard-nav">
          <button class="nav-btn active" data-section="home">Dashboard</button>
          <button class="nav-btn" data-section="quiz">Take Quiz</button>
          <button class="nav-btn" data-section="history">Quiz History</button>
          <button class="nav-btn" data-section="sync">Google Classroom</button>
        </div>

        <div id="student-home" class="dashboard-content">
          <div class="stats-grid">
            <div class="stat-card"><h3 id="total-quizzes">0</h3><p>Total Quizzes</p></div>
            <div class="stat-card"><h3 id="avg-score">0%</h3><p>Average Score</p></div>
            <div class="stat-card"><h3 id="last-topic">N/A</h3><p>Last Topic</p></div>
          </div>

          <div id="google-sync-indicator" class="hidden">
            <div class="google-sync-status">✅ Google Classroom synced successfully! <span id="synced-courses-count"></span></div>
          </div>

          <h3>Recent Quiz Performance</h3>
          <div id="recent-quizzes"></div>
        </div>

        <div id="student-quiz" class="dashboard-content hidden">
          <div id="quiz-setup">
            <h3>Generate New Quiz</h3>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
              <div class="form-group"><label>Select Topic</label>
                <select id="quiz-topic"><option value="">Choose Topic</option><option>Mathematics</option><option>Science</option><option>History</option><option>English</option><option>Physics</option><option>Biology</option><option>Chemistry</option><option>Geography</option><option>Computer Science</option></select>
              </div>
              <div class="form-group"><label>Select Difficulty</label>
                <select id="quiz-difficulty"><option value="">Choose Difficulty</option><option>Easy</option><option>Medium</option><option>Hard</option></select>
              </div>
            </div>

            <div class="form-group">
              <label>Number of Questions: <span id="questions-count">5</span></label>
              <input id="quiz-questions" type="range" min="3" max="15" value="5" />
            </div>
            <button id="generate-quiz-btn" class="btn btn-primary" style="width:100%;">Generate Quiz</button>
          </div>

          <div id="quiz-interface" class="hidden">
            <div id="quiz-header">
              <h3 id="quiz-title"></h3>
              <div class="progress-bar"><div id="quiz-progress" class="progress-fill"></div></div>
            </div>
            <div id="quiz-questions-container"></div>
            <div style="display:flex;gap:8px;margin-top:12px;">
              <button id="cancel-quiz-btn" class="btn btn-secondary" style="flex:1;">Cancel Quiz</button>
              <button id="submit-quiz-btn" class="btn btn-primary" style="flex:1;">Submit Quiz</button>
            </div>
          </div>

          <div id="quiz-results" class="hidden" style="margin-top:12px;">
            <div class="quiz-card">
              <div class="score-display" style="background:linear-gradient(135deg,#28a745,#20c997);color:white;padding:16px;border-radius:8px;">
                <h2 id="final-score">0%</h2>
                <p id="score-feedback">Great job!</p>
                <p id="score-details">You got 0 out of 0 questions correct!</p>
              </div>
              <button id="new-quiz-btn" class="btn btn-primary" style="width:100%;margin-top:10px;">Take Another Quiz</button>
            </div>
          </div>
        </div>

        <div id="student-history" class="dashboard-content hidden">
          <h3>Quiz History</h3>
          <div id="quiz-history-list"></div>
        </div>

        <div id="student-sync" class="dashboard-content hidden">
          <h3>🔗 Google Classroom Integration</h3>
          <div id="sync-disconnected">
            <div class="info-message">Connect your Google Classroom account to sync courses and generate quizzes from your class topics.</div>
            <button id="sync-google-btn" class="btn btn-google" style="width:100%;">🔗 Sync with Google Classroom</button>
          </div>
          <div id="sync-connected" class="hidden">
            <div class="google-sync-status">✅ Google Classroom is connected</div>
            <h4>Your Courses</h4>
            <div id="synced-courses-list"></div>
            <button id="disconnect-google-btn" class="btn btn-secondary">Disconnect Google Classroom</button>
          </div>
        </div>
      </div>

      <!-- Educator -->
      <div id="educator-dashboard" class="hidden">
        <div class="dashboard-nav">
          <button class="nav-btn active" data-edu="analytics">Analytics</button>
          <button class="nav-btn" data-edu="students">Students</button>
          <button class="nav-btn" data-edu="leaderboard">Leaderboard</button>
          <button class="nav-btn" data-edu="encourage">Encourage</button>
        </div>

        <div id="educator-analytics" class="dashboard-content">
          <h3>👨‍🏫 Student Performance Analytics</h3>
          <div class="stats-grid">
            <div class="stat-card"><h3 id="total-students">0</h3><p>Total Students</p></div>
            <div class="stat-card"><h3 id="total-class-quizzes">0</h3><p>Total Quizzes</p></div>
            <div class="stat-card"><h3 id="class-average">0%</h3><p>Class Average</p></div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;">
            <div><h4>📊 Subject Performance</h4><div id="subject-performance"></div></div>
            <div><h4>📈 Difficulty Analysis</h4><div id="difficulty-analysis"></div></div>
          </div>
        </div>

        <div id="educator-students" class="dashboard-content hidden">
          <h3>👥 Student Details</h3>
          <div id="students-list"></div>
        </div>

        <div id="educator-leaderboard" class="dashboard-content hidden">
          <h3>🏆 Student Leaderboard</h3>
          <div style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:12px;margin-top:12px;">
            <div><h4>🥇 Top Performers</h4><div id="leaderboard-list"></div></div>
            <div><h4>📚 Most Active</h4><div id="most-active-list"></div></div>
            <div><h4>🎯 Subject Champions</h4><div id="subject-champions"></div></div>
          </div>
        </div>

        <div id="educator-encourage" class="dashboard-content hidden">
          <h3>💪 Student Encouragement</h3>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div>
              <h4>⚠ Students Needing Support</h4>
              <div id="low-performers-list"></div>
              <h4 style="margin-top:12px;">📝 Send Encouragement</h4>
              <div class="form-group"><label>Select Student</label><select id="encourage-student"><option value="">Choose a student</option></select></div>
              <div class="form-group"><label>Encouragement Message</label><textarea id="encourage-message" rows="4">Keep up the great work! I believe in your potential. Practice makes perfect, and every quiz is a step toward improvement. You've got this! 🌟</textarea></div>
              <button id="send-encouragement-btn" class="btn btn-primary" style="width:100%;">Send Encouragement</button>
            </div>
            <div>
              <h4>📬 Recent Encouragements</h4>
              <div id="encouragement-history"></div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <div id="message-container"></div>
  </div>

<script>
/* == JS: cleaned + adapted to use the Flask endpoints == */

const defaultConfig = {
  app_title: "🎓 EduTutor AI",
  welcome_message: "Personalized Learning with Generative AI and LMS Integration"
};

let currentUser = null;
let currentQuiz = null;
let quizAnswers = [];
let googleSynced = false;
let syncedCourses = [];
let allUsers = [];
let allQuizzes = [];
let allEncouragements = [];

async function fetchData() {
  try {
    const res = await fetch('/api/data');
    const combined = await res.json();
    // original code expected arrays filtered by keys; mimic that:
    allUsers = combined.filter(it => it.role);
    allQuizzes = combined.filter(it => it.quiz_id);
    allEncouragements = combined.filter(it => it.encouragement_id);
  } catch (e) {
    console.error(e);
    allUsers = []; allQuizzes = []; allEncouragements = [];
  }
}

/* small helper: POST create */
async function createItem(obj) {
  const res = await fetch('/api/create', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(obj)
  });
  return res.json();
}

/* UI message helper */
function showMessage(msg, type='info') {
  const container = document.getElementById('message-container');
  const div = document.createElement('div');
  div.className = type==='error' ? 'error-message' : type==='success' ? 'success-message' : 'info-message';
  div.textContent = msg;
  container.appendChild(div);
  setTimeout(() => { if (div.parentNode) div.parentNode.removeChild(div); }, 4000);
}

/* basic util */
function formatDate() {
  const d = new Date();
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString();
}

/* initialize */
async function initializeApp() {
  await fetchData();
  // apply default config
  document.getElementById('app-title').textContent = defaultConfig.app_title;
  document.getElementById('welcome-message').textContent = defaultConfig.welcome_message;
}

/* Tab switching (auth) */
document.querySelectorAll('.tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
    btn.classList.add('active');
    const tab = btn.dataset.tab;
    document.getElementById(tab + '-tab').classList.add('active');
  });
});

/* Nav (student) */
document.querySelectorAll('#student-dashboard .nav-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    document.querySelectorAll('#student-dashboard .nav-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    const sec = btn.dataset.section;
    document.querySelectorAll('#student-dashboard .dashboard-content').forEach(c=>c.classList.add('hidden'));
    const el = document.getElementById('student-' + sec);
    if (el) el.classList.remove('hidden');
    if (sec === 'history') updateQuizHistory();
  });
});

/* Nav (educator) */
document.querySelectorAll('#educator-dashboard .nav-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    document.querySelectorAll('#educator-dashboard .nav-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    const sec = btn.dataset.edu;
    document.querySelectorAll('#educator-dashboard .dashboard-content').forEach(c=>c.classList.add('hidden'));
    const el = document.getElementById('educator-' + sec);
    if (el) el.classList.remove('hidden');
    if (sec === 'students') updateStudentsList();
    if (sec === 'analytics') updateEducatorAnalytics();
    if (sec === 'leaderboard') updateLeaderboard();
    if (sec === 'encourage') updateEncouragementSection();
  });
});

/* Auth handlers */
document.getElementById('register-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('reg-username').value.trim();
  const email = document.getElementById('reg-email').value.trim();
  const pw = document.getElementById('reg-password').value;
  const cpw = document.getElementById('reg-confirm').value;
  const role = document.getElementById('reg-role').value;
  if (!username || !email || !pw || !cpw || !role) { showMessage('Please fill all fields','error'); return; }
  if (pw !== cpw) { showMessage('Passwords do not match','error'); return; }
  await fetchData();
  if (allUsers.find(u => u.username === username)) { showMessage('Username already exists','error'); return; }
  const user = { user_id: gen_id_js(), username, email, password: pw, role };
  const resp = await createItem(user);
  if (resp.isOk) {
    showMessage('Registration successful! You can login now','success');
    document.getElementById('register-form').reset();
    // switch to login tab
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
    document.querySelector('.tab[data-tab="login"]').classList.add('active');
    document.getElementById('login-tab').classList.add('active');
    await fetchData();
  } else {
    showMessage('Registration failed','error');
  }
});

document.getElementById('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('login-username').value.trim();
  const pw = document.getElementById('login-password').value;
  await fetchData();
  const user = allUsers.find(u => u.username === username && u.password === pw);
  if (!user) { showMessage('Invalid username or password','error'); return; }
  currentUser = user;
  showDashboard();
  showMessage('Login successful!','success');
});

/* Google login simulator */
document.getElementById('google-login-btn').addEventListener('click', async () => {
  showMessage('Connecting to Google Classroom...','info');
  setTimeout(async () => {
    // create or reuse a dummy google user
    await fetchData();
    let g = allUsers.find(u => u.username === 'google_user_demo');
    if (!g) {
      g = { user_id: gen_id_js(), username: 'google_user_demo', email:'student@google.com', role:'student', password:'google_auth' };
      await createItem(g);
      await fetchData();
    }
    currentUser = g;
    // sync courses
    const res = await fetch('/api/sync_google', { method:'POST' });
    const data = await res.json();
    if (data.isOk) {
      googleSynced = true;
      syncedCourses = data.courses;
      updateGoogleSyncUI();
      showDashboard();
      showMessage('Google login successful! Courses synced automatically.','success');
      await fetchData();
    } else {
      showMessage('Google sync failed','error');
    }
  }, 1200);
});

/* logout */
document.getElementById('logout-btn').addEventListener('click', () => {
  currentUser = null;
  currentQuiz = null;
  quizAnswers = [];
  googleSynced = false;
  syncedCourses = [];
  document.getElementById('auth-section').classList.remove('hidden');
  document.getElementById('dashboard-section').classList.add('hidden');
  document.getElementById('login-form').reset();
  document.getElementById('register-form').reset();
  showMessage('Logged out','success');
});

/* EXPANDED quiz templates with MANY questions for each topic */
const quizTemplates = {
  'Mathematics': {
    'Easy': [
      {question:'What is 5 + 3?', options:['7','8','9','6'], correct:1},
      {question:'What is 10 - 4?', options:['6','7','5','8'], correct:0},
      {question:'What is 2 × 3?', options:['5','6','7','8'], correct:1},
      {question:'What is 12 ÷ 4?', options:['2','3','4','5'], correct:1},
      {question:'What is 7 + 8?', options:['14','15','16','13'], correct:1},
      {question:'What is 20 - 5?', options:['15','14','16','13'], correct:0},
      {question:'What is 9 × 2?', options:['16','18','20','22'], correct:1},
      {question:'What is 25 ÷ 5?', options:['4','5','6','7'], correct:1},
      {question:'What is 6 + 9?', options:['14','15','16','17'], correct:1},
      {question:'What is 18 - 7?', options:['10','11','12','13'], correct:1},
      {question:'What is 4 × 7?', options:['26','28','30','32'], correct:1},
      {question:'What is 36 ÷ 6?', options:['5','6','7','8'], correct:1},
      {question:'What is 11 + 14?', options:['24','25','26','27'], correct:1},
      {question:'What is 30 - 12?', options:['16','17','18','19'], correct:2},
      {question:'What is 8 × 8?', options:['62','64','66','68'], correct:1}
    ],
    'Medium': [
      {question:'What is 15 + 27?', options:['42','41','43','40'], correct:0},
      {question:'Solve: 8 × 7 = ?', options:['54','56','58','52'], correct:1},
      {question:'What is 144 ÷ 12?', options:['11','12','13','14'], correct:1},
      {question:'Calculate: 3² + 4² = ?', options:['25','24','16','9'], correct:0},
      {question:'What is 25% of 80?', options:['20','25','30','15'], correct:0},
      {question:'Solve: 15 × 6 = ?', options:['80','90','100','110'], correct:1},
      {question:'What is 125 ÷ 5?', options:['20','25','30','35'], correct:1},
      {question:'Calculate: 7² - 3² = ?', options:['40','38','36','34'], correct:0},
      {question:'What is 33% of 150?', options:['45','49.5','50','55'], correct:1},
      {question:'Solve: 45 + 67 = ?', options:['110','112','114','116'], correct:1},
      {question:'What is 256 ÷ 16?', options:['14','15','16','17'], correct:2},
      {question:'Calculate: 5³ = ?', options:['100','115','125','135'], correct:2},
      {question:'What is 18 × 5?', options:['80','85','90','95'], correct:2},
      {question:'Solve: 144 - 89 = ?', options:['55','56','57','58'], correct:0},
      {question:'What is 75% of 200?', options:['140','150','160','170'], correct:1}
    ],
    'Hard': [
      {question:'Solve: ∫(2x + 3)dx', options:['x² + 3x + C','2x² + 3x + C','x² + 6x + C','4x + 3 + C'], correct:0},
      {question:'What is the derivative of sin(x)?', options:['cos(x)','-cos(x)','-sin(x)','tan(x)'], correct:0},
      {question:'Solve: 2x + 5 = 15', options:['x = 5','x = 10','x = 7.5','x = 6'], correct:0},
      {question:'What is the area of circle with radius 7?', options:['49π','14π','28π','154π'], correct:0},
      {question:'Solve: log₁₀100 = ?', options:['1','2','10','100'], correct:1},
      {question:'What is the value of i²?', options:['1','-1','0','i'], correct:1},
      {question:'Solve: 3x - 7 = 14', options:['x = 6','x = 7','x = 8','x = 9'], correct:1},
      {question:'What is the derivative of e^x?', options:['xe^x','e^x','ln(x)','1/x'], correct:1},
      {question:'Solve: x² - 5x + 6 = 0', options:['x=2,3','x=1,6','x=-2,-3','x=-1,-6'], correct:0},
      {question:'What is the limit of (1/x) as x→∞?', options:['0','1','∞','-∞'], correct:0},
      {question:'Solve: 2³ × 2² = ?', options:['2⁵','2⁶','4⁵','4⁶'], correct:0},
      {question:'What is the integral of 3x²?', options:['x³ + C','3x³ + C','x² + C','6x + C'], correct:0},
      {question:'Solve: |x-3| = 7', options:['x=10,-4','x=4,-10','x=7,-7','x=3,-3'], correct:0},
      {question:'What is the value of sin(π/2)?', options:['0','1','-1','0.5'], correct:1},
      {question:'Solve: 4x² - 16 = 0', options:['x=2,-2','x=4,-4','x=8,-8','x=1,-1'], correct:0}
    ]
  },
  'Science': {
    'Easy': [
      {question:'What do plants need to make food?', options:['Water only','Sunlight only','Sunlight and water','Soil only'], correct:2},
      {question:'How many legs does a spider have?', options:['6','8','10','4'], correct:1},
      {question:'Which planet is known as the Red Planet?', options:['Venus','Mars','Jupiter','Saturn'], correct:1},
      {question:'What is H₂O?', options:['Oxygen','Hydrogen','Water','Carbon dioxide'], correct:2},
      {question:'Which animal can fly?', options:['Penguin','Ostrich','Eagle','Kangaroo'], correct:2},
      {question:'What gas do humans breathe in?', options:['Carbon dioxide','Oxygen','Nitrogen','Helium'], correct:1},
      {question:'Which is the largest mammal?', options:['Elephant','Giraffe','Blue whale','Polar bear'], correct:2},
      {question:'What is the boiling point of water?', options:['50°C','100°C','150°C','200°C'], correct:1},
      {question:'Which organ pumps blood?', options:['Liver','Heart','Lungs','Brain'], correct:1},
      {question:'What is the closest star to Earth?', options:['Sirius','Sun','Alpha Centauri','Betelgeuse'], correct:1},
      {question:'Which metal is liquid at room temperature?', options:['Iron','Gold','Mercury','Silver'], correct:2},
      {question:'What is the main gas in the atmosphere?', options:['Oxygen','Carbon dioxide','Nitrogen','Hydrogen'], correct:2},
      {question:'Which planet has rings?', options:['Mars','Venus','Saturn','Mercury'], correct:2},
      {question:'What is the chemical symbol for gold?', options:['Go','Gd','Au','Ag'], correct:2},
      {question:'Which is NOT a state of matter?', options:['Solid','Liquid','Gas','Energy'], correct:3}
    ],
    'Medium': [
      {question:'What is the chemical symbol for water?', options:['H2O','CO2','O2','N2'], correct:0},
      {question:'What is the boiling point of water?', options:['90°C','100°C','110°C','120°C'], correct:1},
      {question:'Which gas do plants absorb?', options:['Oxygen','Carbon Dioxide','Nitrogen','Hydrogen'], correct:1},
      {question:'What is the speed of light?', options:['300,000 km/s','150,000 km/s','500,000 km/s','1,000,000 km/s'], correct:0},
      {question:'Which law states F=ma?', options:['Newton\'s 1st','Newton\'s 2nd','Newton\'s 3rd','Ohm\'s Law'], correct:1},
      {question:'What is photosynthesis?', options:['Plant breathing','Plant eating','Food making process','Water absorption'], correct:2},
      {question:'Which planet is known for its great red spot?', options:['Mars','Jupiter','Saturn','Venus'], correct:1},
      {question:'What is the atomic number of carbon?', options:['6','12','14','8'], correct:0},
      {question:'Which element is the most abundant in universe?', options:['Oxygen','Carbon','Hydrogen','Helium'], correct:2},
      {question:'What is the unit of electric current?', options:['Volt','Ampere','Ohm','Watt'], correct:1},
      {question:'Which blood cells fight infection?', options:['Red blood cells','White blood cells','Platelets','Plasma'], correct:1},
      {question:'What is the main component of natural gas?', options:['Propane','Butane','Methane','Ethane'], correct:2},
      {question:'Which planet has the most moons?', options:['Jupiter','Saturn','Uranus','Neptune'], correct:1},
      {question:'What is the pH of pure water?', options:['5','6','7','8'], correct:2},
      {question:'Which scientist developed theory of relativity?', options:['Newton','Einstein','Galileo','Hawking'], correct:1}
    ],
    'Hard': [
      {question:'What is the molecular formula for glucose?', options:['C6H12O6','C12H22O11','C2H6O','C6H6'], correct:0},
      {question:'What is Newton\'s First Law?', options:['F=ma','Every action has equal reaction','Object at rest stays at rest','Energy cannot be created'], correct:2},
      {question:'What is DNA?', options:['Deoxyribonucleic Acid','Ribonucleic Acid','Protein','Enzyme'], correct:0},
      {question:'Which subatomic particle has negative charge?', options:['Proton','Neutron','Electron','Positron'], correct:2},
      {question:'What is the Heisenberg Uncertainty Principle?', options:['Energy conservation','Position-momentum uncertainty','Wave-particle duality','Relativity'], correct:1},
      {question:'Which planet has the strongest magnetic field?', options:['Earth','Jupiter','Saturn','Neptune'], correct:1},
      {question:'What is the half-life of Carbon-14?', options:['5730 years','11460 years','2865 years','10000 years'], correct:0},
      {question:'Which theory explains the origin of universe?', options:['String Theory','Big Bang Theory','Steady State Theory','Multiverse Theory'], correct:1},
      {question:'What is the chemical formula for ozone?', options:['O2','O3','CO2','H2O'], correct:1},
      {question:'Which element has the highest melting point?', options:['Tungsten','Carbon','Osmium','Iridium'], correct:0},
      {question:'What is the speed of sound in air?', options:['331 m/s','343 m/s','299 m/s','400 m/s'], correct:1},
      {question:'Which quantum number describes electron spin?', options:['Principal','Azimuthal','Magnetic','Spin'], correct:3},
      {question:'What is the main component of black holes?', options:['Dark matter','Singularity','Neutron star','White dwarf'], correct:1},
      {question:'Which law states PV=nRT?', options:['Boyle\'s Law','Charles\'s Law','Ideal Gas Law','Avogadro\'s Law'], correct:2},
      {question:'What is the Planck constant?', options:['6.626×10^-34 J·s','6.022×10^23 mol^-1','1.381×10^-23 J/K','9.109×10^-31 kg'], correct:0}
    ]
  },
  'History': {
    'Easy': [
      {question:'Who was the first President of the United States?', options:['Thomas Jefferson','George Washington','John Adams','Benjamin Franklin'], correct:1},
      {question:'In which country are the pyramids located?', options:['Greece','Egypt','Italy','Turkey'], correct:1},
      {question:'When did World War II end?', options:['1944','1945','1946','1947'], correct:1},
      {question:'Who discovered America?', options:['Christopher Columbus','Vasco da Gama','Marco Polo','Ferdinand Magellan'], correct:0},
      {question:'Which empire was ruled by Julius Caesar?', options:['Greek','Roman','Egyptian','Persian'], correct:1},
      {question:'When was the Declaration of Independence signed?', options:['1776','1789','1792','1801'], correct:0},
      {question:'Who was the first man on the moon?', options:['Buzz Aldrin','Neil Armstrong','John Glenn','Alan Shepard'], correct:1},
      {question:'Which war was fought between North and South USA?', options:['Revolutionary War','Civil War','World War I','World War II'], correct:1},
      {question:'Who wrote the Declaration of Independence?', options:['George Washington','Thomas Jefferson','Benjamin Franklin','John Adams'], correct:1},
      {question:'When did the Titanic sink?', options:['1910','1912','1914','1916'], correct:1},
      {question:'Which ancient civilization built Machu Picchu?', options:['Aztec','Maya','Inca','Olmec'], correct:2},
      {question:'Who was the first female Prime Minister of UK?', options:['Queen Elizabeth','Margaret Thatcher','Theresa May','Indira Gandhi'], correct:1},
      {question:'When did the French Revolution begin?', options:['1776','1789','1799','1812'], correct:1},
      {question:'Which pharaoh\'s tomb was discovered in 1922?', options:['Cleopatra','Ramses II','Tutankhamun','Khufu'], correct:2},
      {question:'When was the Berlin Wall built?', options:['1945','1955','1961','1975'], correct:2}
    ],
    'Medium': [
      {question:'Who wrote the Declaration of Independence?', options:['George Washington','Thomas Jefferson','Benjamin Franklin','John Adams'], correct:1},
      {question:'What year did the Titanic sink?', options:['1910','1912','1914','1916'], correct:1},
      {question:'When did World War I begin?', options:['1912','1914','1916','1918'], correct:1},
      {question:'Who was the first Roman Emperor?', options:['Julius Caesar','Augustus','Nero','Caligula'], correct:1},
      {question:'Which civilization invented writing?', options:['Egyptian','Greek','Sumerian','Chinese'], correct:2},
      {question:'When did the Renaissance begin?', options:['12th century','14th century','16th century','18th century'], correct:1},
      {question:'Who was the first female pharaoh?', options:['Nefertiti','Cleopatra','Hatshepsut','Nefertari'], correct:2},
      {question:'Which empire built the Great Wall?', options:['Mongol','Chinese','Roman','Ottoman'], correct:1},
      {question:'When was the Magna Carta signed?', options:['1066','1215','1453','1776'], correct:1},
      {question:'Who led the Protestant Reformation?', options:['John Calvin','Martin Luther','Henry VIII','John Wesley'], correct:1},
      {question:'Which war ended with Treaty of Versailles?', options:['World War I','World War II','Korean War','Vietnam War'], correct:0},
      {question:'When was the United Nations founded?', options:['1919','1945','1950','1960'], correct:1},
      {question:'Who was the first President of independent India?', options:['Jawaharlal Nehru','Rajendra Prasad','Mahatma Gandhi','Sardar Patel'], correct:1},
      {question:'Which civilization developed democracy?', options:['Roman','Greek','Egyptian','Persian'], correct:1},
      {question:'When did the Cold War end?', options:['1985','1989','1991','1995'], correct:2}
    ],
    'Hard': [
      {question:'Who was the first woman to win a Nobel Prize?', options:['Marie Curie','Rosalind Franklin','Jane Goodall','Ada Lovelace'], correct:0},
      {question:'When did the Byzantine Empire fall?', options:['476 AD','1066 AD','1204 AD','1453 AD'], correct:3},
      {question:'Who wrote "The Prince"?', options:['Machiavelli','Plato','Aristotle','Voltaire'], correct:0},
      {question:'Which treaty ended World War I?', options:['Treaty of Versailles','Treaty of Paris','Treaty of Ghent','Treaty of Tordesillas'], correct:0},
      {question:'Who was the last Tsar of Russia?', options:['Peter the Great','Nicholas II','Alexander II','Ivan the Terrible'], correct:1},
      {question:'When did the Industrial Revolution begin?', options:['16th century','17th century','18th century','19th century'], correct:2},
      {question:'Who discovered penicillin?', options:['Alexander Fleming','Louis Pasteur','Robert Koch','Joseph Lister'], correct:0},
      {question:'Which civilization built the city of Carthage?', options:['Greek','Roman','Phoenician','Egyptian'], correct:2},
      {question:'When was the Russian Revolution?', options:['1905','1917','1922','1939'], correct:1},
      {question:'Who was the first Emperor of China?', options:['Qin Shi Huang','Han Wudi','Tang Taizong','Kangxi Emperor'], correct:0},
      {question:'Which war featured the Battle of Waterloo?', options:['Seven Years War','Napoleonic Wars','Crimean War','Franco-Prussian War'], correct:1},
      {question:'When did the American Civil War end?', options:['1863','1865','1867','1870'], correct:1},
      {question:'Who was the first female Prime Minister in the world?', options:['Indira Gandhi','Margaret Thatcher','Sirimavo Bandaranaike','Golda Meir'], correct:2},
      {question:'Which empire was ruled by Suleiman the Magnificent?', options:['Mughal','Ottoman','Safavid','Byzantine'], correct:1},
      {question:'When was the European Union formed?', options:['1945','1957','1973','1993'], correct:3}
    ]
  },
  'English': {
    'Easy': [
      {question:'What is the opposite of "hot"?', options:['Warm','Cool','Cold','Freezing'], correct:2},
      {question:'Which word is a noun?', options:['run','beautiful','quickly','book'], correct:3},
      {question:'What is the plural of "child"?', options:['childs','children','childes','child'], correct:1},
      {question:'Which is a verb?', options:['happy','run','blue','quickly'], correct:1},
      {question:'What is the past tense of "go"?', options:['goed','went','gone','going'], correct:1},
      {question:'Which word is an adjective?', options:['run','beautiful','quickly','book'], correct:1},
      {question:'What is the synonym of "big"?', options:['small','large','tiny','short'], correct:1},
      {question:'Which is a proper noun?', options:['city','country','London','river'], correct:2},
      {question:'What is the plural of "mouse"?', options:['mouses','mice','mousees','meece'], correct:1},
      {question:'Which word is an adverb?', options:['happy','run','quickly','book'], correct:2},
      {question:'What is the antonym of "day"?', options:['light','sun','night','morning'], correct:2},
      {question:'Which is a conjunction?', options:['and','run','blue','quickly'], correct:0},
      {question:'What is the present tense of "ran"?', options:['run','runned','running','runs'], correct:0},
      {question:'Which word is a preposition?', options:['in','run','blue','quickly'], correct:0},
      {question:'What is the plural of "person"?', options:['persons','people','persones','peoples'], correct:1}
    ],
    'Medium': [
      {question:'Identify the verb: "She quickly ran to the store."', options:['She','quickly','ran','store'], correct:2},
      {question:'What is a synonym for "happy"?', options:['sad','joyful','angry','tired'], correct:1},
      {question:'Which sentence is correct?', options:['He don\'t like apples.','He doesn\'t like apples.','He doesn\'t likes apples.','He don\'t likes apples.'], correct:1},
      {question:'What is the comparative form of "good"?', options:['gooder','better','more good','best'], correct:1},
      {question:'Identify the metaphor: "Time is money."', options:['Simile','Metaphor','Personification','Alliteration'], correct:1},
      {question:'What is the past participle of "write"?', options:['wrote','written','writed','writing'], correct:1},
      {question:'Which is a complex sentence?', options:['I like apples.','I like apples and oranges.','Although I like apples, I prefer oranges.','Apples are tasty.'], correct:2},
      {question:'What is the antonym of "benevolent"?', options:['kind','generous','malevolent','friendly'], correct:2},
      {question:'Identify the preposition: "The book is on the table."', options:['book','is','on','table'], correct:2},
      {question:'What is the superlative form of "far"?', options:['farrer','farest','further','farthest'], correct:3},
      {question:'Which word is an interjection?', options:['Wow!','run','blue','quickly'], correct:0},
      {question:'What is the direct object in "She read the book."?', options:['She','read','the','book'], correct:3},
      {question:'Identify the adverb: "He speaks very clearly."', options:['He','speaks','very','clearly'], correct:3},
      {question:'What is the plural of "phenomenon"?', options:['phenomenons','phenomena','phenomenones','phenomenae'], correct:1},
      {question:'Which is an example of alliteration?', options:['She sells seashells.','The cat sat on the mat.','Time flies.','The wind howled.'], correct:0}
    ],
    'Hard': [
      {question:'What literary device is "the stars danced playfully"?', options:['Simile','Metaphor','Personification','Alliteration'], correct:2},
      {question:'What is the subjunctive mood?', options:['Expressing facts','Expressing wishes','Expressing commands','Expressing questions'], correct:1},
      {question:'Identify the oxymoron:', options:['Deafening silence','Running quickly','Very beautiful','Extremely large'], correct:0},
      {question:'What is a synecdoche?', options:['Part represents whole','Comparing without like/as','Giving human traits','Repeating sounds'], correct:0},
      {question:'Which is an example of iambic pentameter?', options:['Shall I compare thee to a summer\'s day?','The cat sat on the mat','Run quickly to the store','Beautiful sunset in the sky'], correct:0},
      {question:'What is the difference between "affect" and "effect"?', options:['Affect is verb, effect is noun','Affect is noun, effect is verb','Both are verbs','Both are nouns'], correct:0},
      {question:'Identify the dangling modifier:', options:['Running quickly, the finish line approached.','The runner approached the finish line quickly.','Quickly running, he approached the finish line.','He approached the finish line running quickly.'], correct:0},
      {question:'What is anaphora?', options:['Repetition at sentence start','Repetition at sentence end','Repetition of vowel sounds','Repetition of consonant sounds'], correct:0},
      {question:'Which is passive voice?', options:['The ball was thrown by the boy.','The boy threw the ball.','The boy is throwing the ball.','The boy will throw the ball.'], correct:0},
      {question:'What is zeugma?', options:['One word modifies two others','Repetition for emphasis','Contradictory terms','Exaggeration for effect'], correct:0},
      {question:'Identify the chiasmus:', options:['Ask not what your country can do for you...','The early bird catches the worm.','Time is money.','She sells seashells.'], correct:0},
      {question:'What is litotes?', options:['Understatement using negation','Overstatement for effect','Comparing two things','Giving human traits'], correct:0},
      {question:'Which is an example of metonymy?', options:['The White House announced','Time is money','She is a rose','The wind whispered'], correct:0},
      {question:'What is the difference between "who" and "whom"?', options:['Who is subject, whom is object','Who is object, whom is subject','Both are subjects','Both are objects'], correct:0},
      {question:'Identify the anticlimax:', options:['He lost his family, his home, and his favorite tie.','The hero saved the city and won the girl.','The storm raged and lightning struck.','She graduated with honors and got her dream job.'], correct:0}
    ]
  }
};

/* small helpers */
function gen_id_js() {
  return 'id_' + Math.random().toString(36).substr(2,9) + '_' + Date.now().toString(36);
}

/* Update UI functions */
function showDashboard() {
  document.getElementById('auth-section').classList.add('hidden');
  document.getElementById('dashboard-section').classList.remove('hidden');
  document.getElementById('dashboard-title').textContent = Welcome, ${currentUser.username}!;

  if (currentUser.role === 'student') {
    document.getElementById('student-dashboard').classList.remove('hidden');
    document.getElementById('educator-dashboard').classList.add('hidden');
    // show home
    document.querySelectorAll('#student-dashboard .nav-btn').forEach(b=>b.classList.remove('active'));
    document.querySelector('#student-dashboard .nav-btn[data-section="home"]').classList.add('active');
    document.querySelectorAll('#student-dashboard .dashboard-content').forEach(c=>c.classList.add('hidden'));
    document.getElementById('student-home').classList.remove('hidden');
    updateStudentStats();
    updateRecentQuizzes();
    updateQuizHistory();
  } else {
    document.getElementById('educator-dashboard').classList.remove('hidden');
    document.getElementById('student-dashboard').classList.add('hidden');
    // show analytics
    document.querySelectorAll('#educator-dashboard .nav-btn').forEach(b=>b.classList.remove('active'));
    document.querySelector('#educator-dashboard .nav-btn[data-edu="analytics"]').classList.add('active');
    document.querySelectorAll('#educator-dashboard .dashboard-content').forEach(c=>c.classList.add('hidden'));
    document.getElementById('educator-analytics').classList.remove('hidden');
    updateEducatorDashboard();
    updateEncouragementSection();
  }

  // update topic options if google synced
  updateGoogleSyncUI();
}

function updateStudentStats() {
  const userQuizzes = allQuizzes.filter(q => q.user_id === currentUser.user_id);
  const totalQuizzes = userQuizzes.length;
  const avgScore = totalQuizzes > 0 ? userQuizzes.reduce((s,q)=>s+q.score,0)/totalQuizzes : 0;
  const lastTopic = totalQuizzes > 0 ? userQuizzes[userQuizzes.length-1].topic : 'N/A';
  document.getElementById('total-quizzes').textContent = totalQuizzes;
  document.getElementById('avg-score').textContent = avgScore.toFixed(1) + '%';
  document.getElementById('last-topic').textContent = lastTopic;
}

function updateRecentQuizzes() {
  const userQuizzes = allQuizzes.filter(q => q.user_id === currentUser.user_id);
  const recent = userQuizzes.slice(-3).reverse();
  const c = document.getElementById('recent-quizzes');
  if (recent.length === 0) {
    c.innerHTML = '<div class="info-message">No quiz history yet. Take your first quiz to get started!</div>';
    return;
  }
  c.innerHTML = recent.map(q => <div class="quiz-card"><strong>${q.topic}</strong> - ${q.difficulty}<br>Score: <strong>${q.score.toFixed(1)}%</strong> | Date: ${q.quiz_date}<br>${q.feedback}</div>).join('');
}

function updateGoogleSyncUI() {
  if (googleSynced) {
    document.getElementById('google-sync-indicator').classList.remove('hidden');
    document.getElementById('synced-courses-count').textContent = ` ${syncedCourses.length} courses available`;
    const topic = document.getElementById('quiz-topic');
    topic.innerHTML = '<option value="">Choose Topic</option>';
    syncedCourses.forEach(course => {
      const opt = document.createElement('option'); opt.value = course.name; opt.textContent = course.name + ' (Google Classroom)'; topic.appendChild(opt);
    });
    ['Mathematics','Science','History','English','Physics','Biology','Chemistry','Geography','Computer Science'].forEach(t => { const o = document.createElement('option'); o.value = t; o.textContent = t; topic.appendChild(o); });
    document.getElementById('sync-disconnected').classList.add('hidden');
    document.getElementById('sync-connected').classList.remove('hidden');
    const list = document.getElementById('synced-courses-list'); list.innerHTML = syncedCourses.map(c=><div class="quiz-card"><strong>${c.name}</strong><br>Section: ${c.section}</div>).join('');
  }
}

/* Quiz flow */
document.getElementById('quiz-questions').addEventListener('input', function(){ document.getElementById('questions-count').textContent = this.value; });

document.getElementById('generate-quiz-btn').addEventListener('click', async () => {
  const topic = document.getElementById('quiz-topic').value;
  const difficulty = document.getElementById('quiz-difficulty').value;
  const numQ = parseInt(document.getElementById('quiz-questions').value || 5);
  
  if (!topic || !difficulty) { 
    showMessage('Please select topic and difficulty','error'); 
    return; 
  }
  
  showMessage('Generating quiz...','info');
  
  setTimeout(() => {
    // Get questions for the selected topic and difficulty
    const topicSet = quizTemplates[topic];
    if (!topicSet) {
      showMessage('No questions available for this topic','error');
      return;
    }
    
    const pool = topicSet[difficulty];
    if (!pool || pool.length === 0) {
      showMessage('No questions available for this difficulty level','error');
      return;
    }
    
    // Select random questions from the pool - EXACT number requested by user
    const selected = [];
    const availableQuestions = [...pool]; // Copy the array
    
    // If we don't have enough questions, use what we have
    const questionsToSelect = Math.min(numQ, availableQuestions.length);
    
    for (let i = 0; i < questionsToSelect; i++) {
      const randomIndex = Math.floor(Math.random() * availableQuestions.length);
      selected.push(availableQuestions[randomIndex]);
      availableQuestions.splice(randomIndex, 1); // Remove to avoid duplicates
    }
    
    currentQuiz = { 
      quiz_id: gen_id_js(), 
      topic, 
      difficulty, 
      questions: selected, 
      startTime: new Date().toISOString() 
    };
    quizAnswers = new Array(selected.length).fill(-1);
    document.getElementById('quiz-setup').classList.add('hidden');
    document.getElementById('quiz-interface').classList.remove('hidden');
    document.getElementById('quiz-results').classList.add('hidden');
    displayQuiz();
    
    if (selected.length < numQ) {
      showMessage(Generated ${selected.length} questions (maximum available for ${topic} ${difficulty}),'info');
    } else {
      showMessage(Quiz generated with ${selected.length} ${topic} questions,'success');
    }
  }, 600);
});

function displayQuiz() {
  document.getElementById('quiz-title').textContent = Quiz: ${currentQuiz.topic} (${currentQuiz.difficulty}) - ${currentQuiz.questions.length} Questions;
  const container = document.getElementById('quiz-questions-container');
  container.innerHTML = '';
  currentQuiz.questions.forEach((q, i) => {
    const div = document.createElement('div'); div.className = 'quiz-question';
    let html = <h4>Question ${i+1}</h4><p>${q.question}</p><div class="quiz-options">;
    q.options.forEach((opt, idx) => {
      html += <div class="quiz-option" data-q="${i}" data-opt="${idx}"><input type="radio" name="q${i}" id="q${i}_${idx}" value="${idx}"><label for="q${i}_${idx}">${opt}</label></div>;
    });
    html += </div>;
    div.innerHTML = html;
    container.appendChild(div);
  });
  // attach click handlers
  container.querySelectorAll('.quiz-option').forEach(el => {
    el.addEventListener('click', () => {
      const qi = parseInt(el.dataset.q), oi = parseInt(el.dataset.opt);
      quizAnswers[qi] = oi;
      // update radio
      const radio = el.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
      updateQuizProgress();
    });
  });
  updateQuizProgress();
}

function updateQuizProgress() {
  const answered = quizAnswers.filter(a => a !== -1).length;
  const total = currentQuiz.questions.length;
  const pct = total === 0 ? 0 : Math.round((answered / total) * 100);
  document.getElementById('quiz-progress').style.width = pct + '%';
}

document.getElementById('cancel-quiz-btn').addEventListener('click', () => {
  currentQuiz = null; quizAnswers = [];
  document.getElementById('quiz-setup').classList.remove('hidden');
  document.getElementById('quiz-interface').classList.add('hidden');
  document.getElementById('quiz-results').classList.add('hidden');
});

document.getElementById('submit-quiz-btn').addEventListener('click', async () => {
  if (quizAnswers.includes(-1)) { showMessage('Please answer all questions','error'); return; }
  let correct = 0;
  currentQuiz.questions.forEach((q,i) => { if (quizAnswers[i] === q.correct) correct++; });
  const score = (correct / currentQuiz.questions.length) * 100;
  const feedback = score >= 80 ? 'Excellent!' : score >= 60 ? 'Good job!' : 'Keep practicing!';
  const quizResult = {
    quiz_id: currentQuiz.quiz_id,
    user_id: currentUser.user_id,
    topic: currentQuiz.topic,
    difficulty: currentQuiz.difficulty,
    score: score,
    correct_answers: correct,
    total_questions: currentQuiz.questions.length,
    quiz_date: formatDate(),
    feedback
  };
  const resp = await createItem(quizResult);
  if (resp.isOk) {
    showQuizResults(score, correct, currentQuiz.questions.length, feedback);
    showMessage('Quiz submitted successfully','success');
    await fetchData();
    updateStudentStats();
    updateQuizHistory();
    updateRecentQuizzes();
  } else {
    showMessage('Failed to save quiz results','error');
  }
});

function showQuizResults(score, correct, total, feedback) {
  document.getElementById('quiz-interface').classList.add('hidden');
  document.getElementById('quiz-results').classList.remove('hidden');
  document.getElementById('final-score').textContent = score.toFixed(1) + '%';
  document.getElementById('score-feedback').textContent = feedback;
  document.getElementById('score-details').textContent = You got ${correct} out of ${total} questions correct!;
}

document.getElementById('new-quiz-btn').addEventListener('click', () => {
  currentQuiz = null; quizAnswers = [];
  document.getElementById('quiz-setup').classList.remove('hidden');
  document.getElementById('quiz-interface').classList.add('hidden');
  document.getElementById('quiz-results').classList.add('hidden');
});

/* history */
function updateQuizHistory() {
  const userQuizzes = allQuizzes.filter(q => q.user_id === currentUser.user_id);
  const container = document.getElementById('quiz-history-list');
  if (userQuizzes.length === 0) {
    container.innerHTML = '<div class="info-message">No quiz history available. Take a quiz to see your results here!</div>';
    return;
  }
  const list = userQuizzes.slice().reverse().map(q => (
<div class="quiz-card"><div style="display:flex;justify-content:space-between;"><div><strong>${q.topic}</strong> - ${q.quiz_date}</div><div style="font-weight:bold;color:${q.score>=80?'#28a745':q.score>=60?'#ffc107':'#dc3545'}">${q.score.toFixed(1)}%</div></div><div style="margin-top:8px;display:grid;grid-template-columns:repeat(3,1fr);gap:8px;"><div><strong>Score:</strong> ${q.score.toFixed(1)}%</div><div><strong>Correct:</strong> ${q.correct_answers}/${q.total_questions}</div><div><strong>Difficulty:</strong> ${q.difficulty}</div></div><div style="margin-top:8px;"><strong>Feedback:</strong> ${q.feedback}</div></div>
  )).join('');
  container.innerHTML = list;
}

/* Google sync */
document.getElementById('sync-google-btn').addEventListener('click', async () => {
  showMessage('Connecting to Google Classroom...','info');
  setTimeout(async () => {
    const res = await fetch('/api/sync_google', { method:'POST' });
    const data = await res.json();
    if (data.isOk) {
      googleSynced = true;
      syncedCourses = data.courses;
      updateGoogleSyncUI();
      showMessage('Successfully synced with Google Classroom!','success');
    } else showMessage('Google sync failed','error');
  }, 800);
});

document.getElementById('disconnect-google-btn').addEventListener('click', () => {
  googleSynced = false; syncedCourses = [];
  document.getElementById('sync-connected').classList.add('hidden');
  document.getElementById('sync-disconnected').classList.remove('hidden');
  document.getElementById('google-sync-indicator').classList.add('hidden');
  const topic = document.getElementById('quiz-topic');
  topic.innerHTML = '<option value="">Choose Topic</option><option>Mathematics</option><option>Science</option><option>History</option><option>English</option><option>Physics</option><option>Biology</option><option>Chemistry</option><option>Geography</option><option>Computer Science</option>';
  showMessage('Google Classroom disconnected','info');
});

/* Educator dashboard functions */
function updateEducatorDashboard() {
  const students = allUsers.filter(u => u.role === 'student');
  const totalStudents = students.length;
  const totalQuizzes = allQuizzes.length;
  let totalScore = 0, scoreCount = 0;
  students.forEach(s => {
    const sq = allQuizzes.filter(q => q.user_id === s.user_id);
    sq.forEach(q => { totalScore += q.score; scoreCount++; });
  });
  const classAvg = scoreCount>0 ? totalScore/scoreCount : 0;
  document.getElementById('total-students').textContent = totalStudents;
  document.getElementById('total-class-quizzes').textContent = totalQuizzes;
  document.getElementById('class-average').textContent = classAvg.toFixed(1) + '%';
  updateStudentsList();
  updateEducatorAnalytics();
}

function updateEducatorAnalytics() {
  const subjectStats = {};
  allQuizzes.forEach(q => {
    if (!subjectStats[q.topic]) subjectStats[q.topic] = { total:0, count:0 };
    subjectStats[q.topic].total += q.score; subjectStats[q.topic].count++;
  });
  const sc = document.getElementById('subject-performance');
  if (Object.keys(subjectStats).length === 0) sc.innerHTML = '<div class="info-message">No quiz data available yet.</div>';
  else sc.innerHTML = Object.entries(subjectStats).map(([s,st]) => <div style="display:flex;justify-content:space-between;padding:6px;border-bottom:1px solid #eee;"><span>${s}</span><span style="font-weight:bold;color:${(st.total/st.count)>=80?'#28a745':(st.total/st.count)>=60?'#ffc107':'#dc3545'}">${(st.total/st.count).toFixed(1)}% (${st.count} quizzes)</span></div>).join('');

  const diff = {};
  allQuizzes.forEach(q => {
    if (!diff[q.difficulty]) diff[q.difficulty] = { total:0, count:0 };
    diff[q.difficulty].total += q.score; diff[q.difficulty].count++;
  });
  const dc = document.getElementById('difficulty-analysis');
  if (Object.keys(diff).length === 0) dc.innerHTML = '<div class="info-message">No quiz data available yet.</div>';
  else dc.innerHTML = Object.entries(diff).map(([d,st]) => <div style="display:flex;justify-content:space-between;padding:6px;border-bottom:1px solid #eee;"><span>${d}</span><span style="font-weight:bold;color:${(st.total/st.count)>=80?'#28a745':(st.total/st.count)>=60?'#ffc107':'#dc3545'}">${(st.total/st.count).toFixed(1)}% (${st.count} quizzes)</span></div>).join('');
}

function updateStudentsList() {
  const students = allUsers.filter(u => u.role === 'student');
  const container = document.getElementById('students-list');
  if (students.length === 0) { container.innerHTML = '<div class="info-message">No student data available yet.</div>'; return; }
  container.innerHTML = students.map(s => {
    const sq = allQuizzes.filter(q => q.user_id === s.user_id);
    const avg = sq.length>0 ? (sq.reduce((a,b)=>a+b.score,0)/sq.length) : 0;
    const lastTopic = sq.length>0 ? sq[sq.length-1].topic : 'N/A';
    const lastDate = sq.length>0 ? sq[sq.length-1].quiz_date : 'N/A';
    const recent = sq.slice(-3).map(q => <div>• ${q.topic}: ${q.score.toFixed(1)}% (${q.quiz_date})</div>).join('');
    return <div class="quiz-card"><div style="display:flex;justify-content:space-between;"><h4>${s.username}</h4><div style="font-weight:bold;color:${avg>=80?'#28a745':avg>=60?'#ffc107':'#dc3545'}">Avg: ${avg.toFixed(1)}%</div></div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px;"><div><strong>${s.email}</strong><div>Email</div></div><div><strong>${sq.length}</strong><div>Total Quizzes</div></div><div><strong>${lastTopic}</strong><div>Last Topic</div></div><div><strong>${lastDate}</strong><div>Last Quiz</div></div></div>${sq.length>0?<div style="margin-top:8px;"><strong>Recent Performance:</strong>${recent}</div>:''}</div>;
  }).join('');
}

function updateLeaderboard() {
  const students = allUsers.filter(u => u.role === 'student');
  const studentStats = students.map(s => {
    const sq = allQuizzes.filter(q => q.user_id === s.user_id);
    const avg = sq.length>0 ? (sq.reduce((a,b)=>a+b.score,0)/sq.length) : 0;
    const subjectScores = {};
    sq.forEach(q => { if (!subjectScores[q.topic]) subjectScores[q.topic]=[]; subjectScores[q.topic].push(q.score); });
    let bestSub='N/A', bestScore=0;
    Object.entries(subjectScores).forEach(([sub,arr]) => { const avgsub = arr.reduce((a,b)=>a+b,0)/arr.length; if (avgsub>bestScore){bestScore=avgsub;bestSub=sub;} });
    return {...s, avgScore:avg, totalQuizzes: sq.length, bestSubject:bestSub, bestSubjectScore:bestScore};
  });

  const top = studentStats.filter(s=>s.totalQuizzes>0).sort((a,b)=>b.avgScore-a.avgScore).slice(0,10);
  const leaderboardContainer = document.getElementById('leaderboard-list');
  if (top.length===0) leaderboardContainer.innerHTML = '<div class="info-message">No quiz data available yet.</div>';
  else leaderboardContainer.innerHTML = top.map((s,i)=> {
    const medal = i===0?'🥇':i===1?'🥈':i===2?'🥉':(i+1)+'.';
    const color = s.avgScore>=80? '#28a745': s.avgScore>=60? '#ffc107':'#dc3545';
    return <div style="display:flex;justify-content:space-between;align-items:center;padding:8px;margin:6px 0;background:#fafafa;border-radius:8px;border-left:4px solid ${color};"><div style="display:flex;align-items:center;gap:12px;"><span style="font-weight:bold">${medal}</span><div><strong>${s.username}</strong><br><small>${s.totalQuizzes} quizzes completed</small></div></div><div style="text-align:right;"><div style="font-weight:bold;color:${color}">${s.avgScore.toFixed(1)}%</div><small>Average Score</small></div></div>;
  }).join('');

  const mostActive = [...studentStats].sort((a,b)=>b.totalQuizzes-a.totalQuizzes).slice(0,5);
  const activeContainer = document.getElementById('most-active-list');
  activeContainer.innerHTML = mostActive.length===0?'<div class="info-message">No student data available yet.</div>': mostActive.map(s=><div style="display:flex;justify-content:space-between;padding:8px;border-bottom:1px solid #eee;"><span>${s.username}</span><span style="font-weight:bold;color:#667eea">${s.totalQuizzes} quizzes</span></div>).join('');

  const subjectChampions = {};
  studentStats.forEach(s => { if (s.bestSubject!=='N/A') {
    if (!subjectChampions[s.bestSubject] || s.bestSubjectScore > subjectChampions[s.bestSubject].score) subjectChampions[s.bestSubject] = { username: s.username, score: s.bestSubjectScore };
  }});
  const championsContainer = document.getElementById('subject-champions');
  championsContainer.innerHTML = Object.keys(subjectChampions).length===0?'<div class="info-message">No subject data available yet.</div>': Object.entries(subjectChampions).map(([sub,ch])=><div style="display:flex;justify-content:space-between;padding:8px;border-bottom:1px solid #eee;"><div><strong>${sub}</strong><br><small>${ch.username}</small></div><span style="font-weight:bold;color:#28a745">${ch.score.toFixed(1)}%</span></div>).join('');
}

function updateEncouragementSection() {
  const students = allUsers.filter(u => u.role === 'student');
  const low = students.filter(s => {
    const sq = allQuizzes.filter(q => q.user_id === s.user_id);
    if (sq.length===0) return false;
    const avg = sq.reduce((a,b)=>a+b.score,0)/sq.length;
    return avg < 60;
  });
  const lowContainer = document.getElementById('low-performers-list');
  if (low.length===0) lowContainer.innerHTML = '<div class="success-message">🎉 All students are performing well! No students need encouragement at this time.</div>';
  else lowContainer.innerHTML = low.map(s => {
    const sq = allQuizzes.filter(q=>q.user_id === s.user_id);
    const avg = sq.reduce((a,b)=>a+b.score,0)/sq.length;
    return <div style="display:flex;justify-content:space-between;padding:12px;margin:8px 0;background:#fff3cd;border-radius:8px;border-left:4px solid #ffc107;"><div><strong>${s.username}</strong><br><small>${s.email} • ${sq.length} quizzes completed</small></div><div style="text-align:right;"><div style="font-weight:bold;color:#856404">${avg.toFixed(1)}%</div><small>Average Score</small></div></div>;
  }).join('');

  // update select
  const sel = document.getElementById('encourage-student'); sel.innerHTML = '<option value="">Choose a student</option>';
  students.forEach(s => { const o = document.createElement('option'); o.value = s.user_id; o.textContent = s.username + ' (' + s.email + ')'; sel.appendChild(o); });

  const history = allEncouragements.filter(enc => currentUser && enc.educator_id === currentUser.user_id).slice().sort((a,b)=> new Date(b.sent_date) - new Date(a.sent_date)).slice(0,10);
  const histContainer = document.getElementById('encouragement-history');
  histContainer.innerHTML = history.length===0?'<div class="info-message">No encouragement messages sent yet.</div>': history.map(enc => {
    const st = allUsers.find(u => u.user_id === enc.student_id);
    const name = st ? st.username : 'Unknown Student';
    return <div style="padding:12px;margin:8px 0;background:#d4edda;border-radius:8px;border-left:4px solid #28a745;"><div style="display:flex;justify-content:space-between;margin-bottom:8px;"><strong>To: ${name}</strong><small>${enc.sent_date}</small></div><div style="font-style:italic">"${enc.message}"</div></div>;
  }).join('');
}

document.getElementById('send-encouragement-btn').addEventListener('click', async () => {
  const studentId = document.getElementById('encourage-student').value;
  const message = document.getElementById('encourage-message').value.trim();
  if (!studentId) { showMessage('Please select a student','error'); return; }
  if (!message) { showMessage('Please write an encouragement message','error'); return; }
  const st = allUsers.find(u => u.user_id === studentId);
  if (!st) { showMessage('Student not found','error'); return; }
  const obj = { encouragement_id: gen_id_js(), educator_id: currentUser.user_id, student_id: studentId, message, sent_date: formatDate() };
  const resp = await createItem(obj);
  if (resp.isOk) {
    showMessage(Encouragement message sent to ${st.username}!, 'success');
    document.getElementById('encourage-message').value = "Keep up the great work! I believe in your potential. Practice makes perfect. You've got this! 🌟";
    document.getElementById('encourage-student').value = '';
    await fetchData();
    updateEncouragementSection();
  } else showMessage('Failed to send encouragement message','error');
});

/* boot */
window.addEventListener('DOMContentLoaded', async () => {
  await initializeApp();
  // ensure data loaded for UI
  await fetchData();
});
</script>
</body>
</html>
    '''
    return render_template_string(html)


if __name__ == "__main__":
    # ensure data file exists
    load_data()
    app.run(debug=True, port=5000)
