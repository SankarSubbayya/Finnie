"""
Learn Page - Educational content and tutorials
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def render():
    """Render the Learn page."""
    st.title("🎓 Financial Education")
    st.caption("Learn about investing, financial concepts, and market analysis")
    
    # Learning paths
    st.subheader("🛤️ Learning Paths")
    
    # Define learning paths
    learning_paths = {
        "Beginner": {
            "description": "Start your investing journey",
            "modules": [
                "What is Investing?",
                "Types of Investments",
                "Risk vs Return",
                "Building Your First Portfolio"
            ],
            "estimated_time": "2-3 hours",
            "color": "🟢"
        },
        "Intermediate": {
            "description": "Deepen your financial knowledge",
            "modules": [
                "Portfolio Theory",
                "Technical Analysis",
                "Fundamental Analysis",
                "Risk Management"
            ],
            "estimated_time": "4-5 hours",
            "color": "🟡"
        },
        "Advanced": {
            "description": "Master advanced concepts",
            "modules": [
                "Options Trading",
                "Derivatives",
                "Quantitative Analysis",
                "Alternative Investments"
            ],
            "estimated_time": "6-8 hours",
            "color": "🔴"
        }
    }
    
    # Display learning paths
    cols = st.columns(3)
    
    for i, (path_name, path_info) in enumerate(learning_paths.items()):
        with cols[i]:
            st.markdown(f"### {path_info['color']} {path_name}")
            st.markdown(f"*{path_info['description']}*")
            st.markdown(f"**Time:** {path_info['estimated_time']}")
            
            # Show modules
            for module in path_info['modules']:
                st.markdown(f"• {module}")
            
            if st.button(f"Start {path_name} Path", key=f"start_{path_name}"):
                st.session_state.learning_progress["current_path"] = path_name
                st.success(f"Started {path_name} learning path!")
                st.rerun()
    
    # Current progress
    if st.session_state.learning_progress["current_path"]:
        st.subheader("📚 Current Learning Path")
        
        current_path = st.session_state.learning_progress["current_path"]
        st.markdown(f"**Active Path:** {current_path}")
        
        # Progress bar
        completed_modules = len(st.session_state.learning_progress["completed_modules"])
        total_modules = len(learning_paths[current_path]["modules"])
        progress = completed_modules / total_modules if total_modules > 0 else 0
        
        st.progress(progress)
        st.caption(f"Completed {completed_modules}/{total_modules} modules")
        
        # Module list with checkboxes
        st.markdown("**Modules:**")
        for i, module in enumerate(learning_paths[current_path]["modules"]):
            col1, col2 = st.columns([1, 9])
            
            with col1:
                is_completed = module in st.session_state.learning_progress["completed_modules"]
                if st.checkbox("", value=is_completed, key=f"module_{i}"):
                    if module not in st.session_state.learning_progress["completed_modules"]:
                        st.session_state.learning_progress["completed_modules"].append(module)
                        st.rerun()
                else:
                    if module in st.session_state.learning_progress["completed_modules"]:
                        st.session_state.learning_progress["completed_modules"].remove(module)
                        st.rerun()
            
            with col2:
                st.markdown(module)
    
    # Quick lessons
    st.subheader("⚡ Quick Lessons")
    
    quick_lessons = [
        {
            "title": "What is a Stock?",
            "description": "Learn the basics of stock ownership",
            "duration": "5 min",
            "difficulty": "Beginner"
        },
        {
            "title": "Understanding P/E Ratio",
            "description": "A key metric for stock valuation",
            "duration": "10 min",
            "difficulty": "Intermediate"
        },
        {
            "title": "Diversification Strategies",
            "description": "How to spread risk across investments",
            "duration": "15 min",
            "difficulty": "Intermediate"
        },
        {
            "title": "Market Volatility",
            "description": "Understanding market ups and downs",
            "duration": "8 min",
            "difficulty": "Beginner"
        }
    ]
    
    cols = st.columns(2)
    
    for i, lesson in enumerate(quick_lessons):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"**{lesson['title']}**")
                st.markdown(f"*{lesson['description']}*")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"⏱️ {lesson['duration']}")
                with col2:
                    st.caption(f"📊 {lesson['difficulty']}")
                
                if st.button(f"Start Lesson", key=f"lesson_{i}"):
                    st.info(f"Starting lesson: {lesson['title']}")
    
    # Knowledge base search
    st.subheader("🔍 Search Knowledge Base")
    
    search_query = st.text_input("Search for financial concepts, terms, or topics")
    
    if search_query:
        # Mock search results
        search_results = [
            {
                "title": f"Understanding {search_query}",
                "content": f"This article explains the concept of {search_query} in detail...",
                "relevance": 0.95,
                "source": "Financial Education Hub"
            },
            {
                "title": f"{search_query} in Portfolio Management",
                "content": f"How {search_query} applies to building and managing portfolios...",
                "relevance": 0.87,
                "source": "Investment Guide"
            },
            {
                "title": f"Common Mistakes with {search_query}",
                "content": f"Learn about common pitfalls when dealing with {search_query}...",
                "relevance": 0.82,
                "source": "Learning Center"
            }
        ]
        
        st.markdown(f"**Found {len(search_results)} results for '{search_query}'**")
        
        for result in search_results:
            with st.expander(f"{result['title']} (Relevance: {result['relevance']:.0%})"):
                st.markdown(result['content'])
                st.caption(f"Source: {result['source']}")
    
    # Notes and bookmarks
    st.subheader("📝 My Notes")
    
    # Add new note
    with st.expander("Add New Note"):
        note_title = st.text_input("Note Title")
        note_content = st.text_area("Note Content", height=100)
        
        if st.button("Save Note"):
            if note_title and note_content:
                new_note = {
                    "title": note_title,
                    "content": note_content,
                    "timestamp": datetime.now().isoformat()
                }
                st.session_state.learning_progress["notes"].append(new_note)
                st.success("Note saved!")
                st.rerun()
            else:
                st.error("Please fill in both title and content")
    
    # Display notes
    if st.session_state.learning_progress["notes"]:
        st.markdown("**Your Notes:**")
        for i, note in enumerate(st.session_state.learning_progress["notes"]):
            with st.expander(f"{note['title']} - {note['timestamp'][:10]}"):
                st.markdown(note['content'])
                if st.button(f"Delete", key=f"delete_note_{i}"):
                    st.session_state.learning_progress["notes"].pop(i)
                    st.rerun()
    else:
        st.info("No notes yet. Add your first note above!")
    
    # Quiz section
    st.subheader("🧠 Test Your Knowledge")
    
    if st.button("Take a Quiz"):
        st.session_state.quiz_active = True
        st.rerun()
    
    if st.session_state.get("quiz_active", False):
        # Mock quiz questions
        quiz_questions = [
            {
                "question": "What does P/E ratio stand for?",
                "options": ["Price/Earnings", "Profit/Equity", "Portfolio/Expense", "Performance/Evaluation"],
                "correct": 0
            },
            {
                "question": "What is diversification?",
                "options": ["Investing in one stock", "Spreading risk across investments", "Timing the market", "Following trends"],
                "correct": 1
            },
            {
                "question": "What is the primary benefit of index funds?",
                "options": ["High returns", "Low fees", "Active management", "Guaranteed profits"],
                "correct": 1
            }
        ]
        
        if "current_question" not in st.session_state:
            st.session_state.current_question = 0
            st.session_state.quiz_score = 0
        
        current_q = st.session_state.current_question
        
        if current_q < len(quiz_questions):
            question = quiz_questions[current_q]
            
            st.markdown(f"**Question {current_q + 1}:** {question['question']}")
            
            selected_option = st.radio(
                "Choose your answer:",
                question['options'],
                key=f"quiz_q_{current_q}"
            )
            
            if st.button("Submit Answer"):
                if selected_option == question['options'][question['correct']]:
                    st.success("Correct! 🎉")
                    st.session_state.quiz_score += 1
                else:
                    st.error(f"Wrong! The correct answer is: {question['options'][question['correct']]}")
                
                st.session_state.current_question += 1
                st.rerun()
        else:
            # Quiz completed
            score = st.session_state.quiz_score
            total = len(quiz_questions)
            percentage = (score / total) * 100
            
            st.markdown(f"## Quiz Complete! 🎉")
            st.markdown(f"**Score: {score}/{total} ({percentage:.0f}%)**")
            
            if percentage >= 80:
                st.success("Excellent work! You have a strong understanding of the concepts.")
            elif percentage >= 60:
                st.warning("Good job! Consider reviewing some concepts for better understanding.")
            else:
                st.info("Keep learning! The educational content will help you improve.")
            
            if st.button("Retake Quiz"):
                st.session_state.quiz_active = False
                st.session_state.current_question = 0
                st.session_state.quiz_score = 0
                st.rerun()
