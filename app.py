import streamlit as st
import json
from datetime import datetime
from bot_engine import InterviewBot
import os
from dotenv import load_dotenv

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="🤖 Interview Preparation Bot",
    page_icon="🤖",
    layout="wide"
)

# Constants based on the requirements from the images
ROLES = [
    "Software Engineer", 
    "Product Manager", 
    "Data Analyst",
    "Frontend Developer", 
    "Backend Developer", 
    "Full Stack Developer",
    "DevOps Engineer", 
    "ML Engineer", 
    "QA Engineer",
    "System Architect"
]

DOMAINS = [
    "General", 
    "Frontend", 
    "Backend", 
    "Machine Learning", 
    "System Design"
]

# Role-specific sample questions based on the requirements
ROLE_SAMPLES = {
    "Software Engineer": {
        "technical": [
            "• Explain time complexity of common algorithms",
            "• Design a scalable web application architecture", 
            "• Implement a data structure like a binary tree",
            "• Debug performance issues in production code"
        ],
        "behavioral": [
            "• Tell me about a challenging technical problem you solved",
            "• How do you handle code review feedback?",
            "• Describe a time you had to learn a new technology"
        ]
    },
    "Product Manager": {
        "technical": [
            "• How do you prioritize features on a product roadmap?",
            "• Design a feature for an existing app like Spotify or Uber",
            "• How do you measure the success of a new product launch?"
        ],
        "behavioral": [
            "• Tell me about a time you managed a difficult stakeholder",
            "• How do you handle disagreements within your team?",
            "• Describe a time you had to pivot your product strategy"
        ]
    },
    "Data Analyst": {
        "technical": [
            "• Write a SQL query to find the top 5 customers by sales",
            "• Explain the difference between correlation and causation",
            "• How would you handle missing data in a dataset?"
        ],
        "behavioral": [
            "• Tell me about a time you had to explain complex data to a non-technical audience",
            "• How do you ensure the quality of your data analysis?",
            "• Describe a project where you used data to drive a key business decision"
        ]
    },
    "Frontend Developer": {
        "technical": [
            "• Explain the JavaScript event loop",
            "• How do you optimize a website for performance?",
            "• Implement a responsive design layout using CSS Flexbox"
        ],
        "behavioral": [
            "• Tell me about a time you had to implement a design that was difficult",
            "• How do you keep up with new frameworks and libraries?",
            "• Describe a time you collaborated with a UX/UI designer"
        ]
    },
    "Backend Developer": {
        "technical": [
            "• Design a RESTful API for a blog application",
            "• Explain the concept of a microservices architecture",
            "• How do you handle database transactions and concurrency?"
        ],
        "behavioral": [
            "• Tell me about a time you had to handle a critical production issue",
            "• How do you ensure the security of a backend system?",
            "• Describe a time you had to refactor legacy code"
        ]
    },
    "ML Engineer": {
        "technical": [
            "• Explain the bias-variance trade-off",
            "• How do you deploy a machine learning model to production?",
            "• Describe the steps in a typical machine learning project pipeline"
        ],
        "behavioral": [
            "• Tell me about a time you dealt with a biased dataset",
            "• How do you handle model performance issues in production?",
            "• Describe a project where you collaborated with data scientists and engineers"
        ]
    },
    "Full Stack Developer": {
        "technical": [
            "• How do you manage state between the frontend and backend?",
            "• Explain the purpose of a CDN in a web application",
            "• Describe how to implement user authentication from end-to-end"
        ],
        "behavioral": [
            "• Tell me about a time you led a feature from start to finish",
            "• How do you stay proficient in both frontend and backend technologies?",
            "• Describe a time you had to make a trade-off between speed and quality"
        ]
    },
    "DevOps Engineer": {
        "technical": [
            "• Explain the CI/CD pipeline and its components",
            "• How would you set up monitoring for a distributed system?",
            "• Describe the benefits of using containers like Docker"
        ],
        "behavioral": [
            "• Tell me about a time you had to troubleshoot a system outage",
            "• How do you automate routine tasks in your workflow?",
            "• Describe a time you improved the reliability of a system"
        ]
    },
    "QA Engineer": {
        "technical": [
            "• What is the difference between functional and non-functional testing?",
            "• Explain the concept of test automation frameworks",
            "• How do you approach testing a new feature?"
        ],
        "behavioral": [
            "• Tell me about a time you found a critical bug in production",
            "• How do you work with developers to resolve issues?",
            "• Describe your experience with agile methodologies"
        ]
    },
    "System Architect": {
        "technical": [
            "• Design a high-level architecture for a social media platform",
            "• Explain the CAP theorem and its implications",
            "• How do you handle system scalability and performance bottlenecks?"
        ],
        "behavioral": [
            "• Tell me about a time you had to make a major architectural decision",
            "• How do you communicate complex designs to a non-technical audience?",
            "• Describe a time you successfully migrated a system"
        ]
    }
}

# Mapping between display names and internal keys
DISPLAY_TO_KEY = {
    "Software Engineer": "Software Engineer",
    "Product Manager": "Product Manager",
    "Data Analyst": "Data Analyst",
    "Frontend Developer": "Frontend Developer",
    "Backend Developer": "Backend Developer",
    "ML Engineer": "ML Engineer",
    "System Design": "System Design"
}

# UI Functions
def init_session():
    """Initialize session state variables"""
    if 'bot' not in st.session_state:
        st.session_state.bot = InterviewBot()
    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'question_count' not in st.session_state:
        st.session_state.question_count = 0
    if 'session_history' not in st.session_state:
        st.session_state.session_history = []
    if 'interview_complete' not in st.session_state:
        st.session_state.interview_complete = False
    if 'show_feedback' not in st.session_state:
        st.session_state.show_feedback = False
    if 'current_feedback' not in st.session_state:
        st.session_state.current_feedback = ""
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 5

def start_interview():
    """Setup and start the interview session"""
    st.session_state.interview_started = True
    st.session_state.interview_complete = False
    st.session_state.question_count = 0
    st.session_state.session_history = []
    st.session_state.show_feedback = False
    st.session_state.current_feedback = ""
    
    role = st.session_state.selected_role
    domain = st.session_state.selected_domain
    mode = st.session_state.selected_mode
    difficulty = st.session_state.selected_difficulty
    
    # Map display names to keys used in bot_engine.py
    mapped_role = DISPLAY_TO_KEY.get(role, "Software Engineer")
    mapped_domain = DISPLAY_TO_KEY.get(domain, "General")
    
    st.session_state.bot.setup(mapped_role, mapped_domain, mode, difficulty)
    get_next_question()

def get_next_question():
    """Generate and display the next question"""
    st.session_state.question_count += 1
    st.session_state.show_feedback = False
    st.session_state.current_feedback = ""
    st.session_state.current_question = st.session_state.bot.generate_question(st.session_state.question_count)
    st.session_state.user_answer = ""
    st.rerun()

def submit_answer():
    """Evaluate the user's answer and store it in session history"""
    if st.session_state.user_answer:
        question = st.session_state.current_question
        answer = st.session_state.user_answer
        
        evaluation = st.session_state.bot.evaluate_answer(question, answer)
        
        # Store the entire Q&A pair in history
        st.session_state.session_history.append({
            "question_number": st.session_state.question_count,
            "question": question,
            "answer": answer,
            "score": evaluation['score'],
            "feedback": evaluation['feedback'],
            "word_count": len(answer.split()),
            "timestamp": datetime.now().isoformat()
        })
        
        st.session_state.current_feedback = evaluation['feedback']
        st.session_state.show_feedback = True
        st.rerun()
    else:
        st.warning("Please provide an answer before submitting.")

def finish_interview():
    """End the interview session and generate a summary"""
    st.session_state.interview_complete = True
    st.session_state.interview_started = False
    st.session_state.show_feedback = False
    st.session_state.current_feedback = ""

def display_summary():
    """Show the final interview summary report"""
    summary_report = st.session_state.bot.generate_summary(st.session_state.session_history)
    st.markdown(summary_report, unsafe_allow_html=True)
    
    # Analyze scores for performance metrics
    scores = [qa['score'] for qa in st.session_state.session_history]
    if scores:
        avg_score = sum(scores) / len(scores)
        
        excellent = sum(1 for s in scores if s >= 80)
        good = sum(1 for s in scores if 60 <= s < 80)
        fair = sum(1 for s in scores if 40 <= s < 60)
        needs_work = sum(1 for s in scores if s < 40)
        
        performance = "🟢 Excellent" if avg_score >= 70 else "🟡 Good" if avg_score >= 50 else "🔴 Practice"
        st.metric("Performance", performance)
    
    # Score chart
    st.subheader("📈 Performance Chart")
    st.line_chart(scores)
    
    # Detailed results
    st.subheader("📝 Question Review")
    for i, qa in enumerate(st.session_state.session_history, 1):
        score_color = "🟢" if qa['score'] >= 70 else "🟡" if qa['score'] >= 50 else "🔴"
        
        with st.expander(f"Q{i} {score_color} {qa['score']}/100"):
            st.write("**Question:**", qa['question'])
            st.write("**Your Answer:**", qa['answer'])
            st.write("**Feedback:**", qa['feedback'])
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 New Interview", type="primary"):
            st.session_state.interview_started = False
            st.session_state.interview_complete = False
            st.rerun()
    
    with col2:
        # Export data
        export_data = {
            'date': datetime.now().isoformat(),
            'role': st.session_state.bot.role,
            'mode': st.session_state.bot.interview_mode,
            'avg_score': avg_score,
            'questions': st.session_state.session_history
        }
        
        filename = f"interview_report_{st.session_state.bot.role.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        
        st.download_button(
            "📥 Download Report",
            data=json.dumps(export_data, indent=2),
            file_name=filename,
            mime="application/json",
            help="Download complete interview transcript and summary."
        )

# Main App Logic
init_session()

st.title("🤖 Interview Preparation Bot")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Interview Settings")
    st.session_state.selected_role = st.selectbox("Select Role", options=ROLES)
    st.session_state.selected_domain = st.selectbox("Select Domain", options=DOMAINS, index=0)
    st.session_state.selected_mode = st.radio("Interview Mode", options=["Technical", "Behavioral"], index=0)
    st.session_state.selected_difficulty = st.radio("Difficulty", options=["Easy", "Medium", "Hard"], index=1)
    
    st.session_state.total_questions = st.number_input(
        "Number of Questions",
        min_value=1,
        max_value=15,
        value=5,
        step=1
    )
    
    st.write("---")
    
    # Sample questions based on selection
    if st.session_state.selected_role in ROLE_SAMPLES:
        samples = ROLE_SAMPLES[st.session_state.selected_role].get(st.session_state.selected_mode.lower(), [])
        if samples:
            st.subheader("Sample Questions")
            for q in samples:
                st.write(q)

# Main content area
if not st.session_state.interview_started and not st.session_state.interview_complete:
    st.info("Ready to start? Configure your interview settings in the sidebar and click the button below.")
    if st.button("🚀 Start Interview", type="primary"):
        start_interview()

elif st.session_state.interview_started and not st.session_state.interview_complete:
    st.subheader(f"Question #{st.session_state.question_count} of {st.session_state.total_questions}")
    st.markdown(st.session_state.current_question)

    st.text_area("Your Answer", key="user_answer", height=200)

    col1, col2, col3 = st.columns(3) # <<<< NEW: Added a third column
    with col1:
        st.button("✅ Submit Answer", on_click=submit_answer, type="primary")
    with col2:
        if st.session_state.question_count < st.session_state.total_questions:
            st.button("➡️ Next Question", on_click=get_next_question)
        else:
            st.button("🏁 Finish Interview", on_click=finish_interview)
    with col3: # <<<< NEW: Added skip button
        st.button("⏭️ Skip", on_click=get_next_question, help="Skip this question without providing an answer.")

    if st.session_state.show_feedback and st.session_state.current_feedback:
        st.write("---")
        st.subheader("Feedback for your answer:")
        st.info(st.session_state.current_feedback)

    # Detailed results
    if st.session_state.session_history:
        st.write("---")
        st.subheader("📝 Past Question Review")
        for i, qa in enumerate(st.session_state.session_history, 1):
            score_color = "🟢" if qa['score'] >= 70 else "🟡" if qa['score'] >= 50 else "🔴"
            
            with st.expander(f"Q{i} {score_color} {qa['score']}/100"):
                st.write("**Question:**", qa['question'])
                st.write("**Your Answer:**", qa['answer'])
                st.write("**Feedback:**", qa['feedback'])

elif st.session_state.interview_complete:
    st.header("📋 Interview Summary Report")
    display_summary()