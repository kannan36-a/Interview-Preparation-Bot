import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class InterviewBot:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model = "llama-3.1-8b-instant"
        
        # Domain-specific topics based on the requirements from the images
        self.domain_topics = {
            "Software Engineer": {
                "technical": [
                    "Data Structures and Algorithms",
                    "Object-Oriented Programming",
                    "Database Design and SQL",
                    "System Design",
                    "Code Optimization",
                    "Testing and Debugging",
                    "Version Control (Git)",
                    "API Design"
                ],
                "behavioral": [
                    "Problem-solving approach",
                    "Team collaboration",
                    "Handling tight deadlines",
                    "Learning new technologies",
                    "Code review feedback"
                ]
            },
            "Product Manager": {
                "technical": [
                    "Product Strategy",
                    "Market Analysis",
                    "Feature Prioritization",
                    "User Experience Design",
                    "Data Analytics",
                    "A/B Testing",
                    "Roadmap Planning",
                    "Stakeholder Management"
                ],
                "behavioral": [
                    "Managing competing priorities",
                    "Cross-functional leadership",
                    "Customer feedback handling",
                    "Difficult decisions",
                    "Team motivation"
                ]
            },
            "Data Analyst": {
                "technical": [
                    "Statistical Analysis",
                    "Data Visualization",
                    "SQL and Database Queries",
                    "Python/R Programming",
                    "Excel and Spreadsheet Analysis",
                    "Business Intelligence Tools",
                    "Data Cleaning and Preprocessing",
                    "Hypothesis Testing"
                ],
                "behavioral": [
                    "Presenting complex data insights",
                    "Working with non-technical stakeholders",
                    "Handling data quality issues",
                    "Meeting analysis deadlines",
                    "Collaborative problem-solving"
                ]
            },
            "Frontend Developer": {
                "technical": [
                    "HTML, CSS, JavaScript",
                    "React/Vue/Angular Frameworks",
                    "Responsive Web Design",
                    "Browser Compatibility",
                    "Performance Optimization",
                    "CSS Preprocessors",
                    "Build Tools and Bundlers",
                    "State Management"
                ],
                "behavioral": [
                    "UI/UX collaboration",
                    "Cross-browser testing challenges",
                    "Design implementation feedback",
                    "Performance optimization decisions",
                    "Learning new frameworks"
                ]
            },
            "Backend Developer": {
                "technical": [
                    "Server-side Programming",
                    "Database Design and Optimization",
                    "API Development (REST/GraphQL)",
                    "Microservices Architecture",
                    "Caching Strategies",
                    "Security Implementation",
                    "Load Balancing",
                    "Message Queues"
                ],
                "behavioral": [
                    "System scalability decisions",
                    "Database optimization challenges",
                    "API design feedback",
                    "Security incident handling",
                    "Performance bottleneck resolution"
                ]
            },
            "ML Engineer": {
                "technical": [
                    "Machine Learning Algorithms",
                    "Feature Engineering",
                    "Model Evaluation Metrics",
                    "Deep Learning Frameworks",
                    "Data Preprocessing",
                    "Model Deployment and MLOps",
                    "A/B Testing for ML",
                    "Model Monitoring"
                ],
                "behavioral": [
                    "Explaining ML concepts to non-technical audiences",
                    "Handling biased datasets",
                    "Model performance issues",
                    "Interdisciplinary collaboration",
                    "Continuous learning in ML"
                ]
            },
            "System Design": {
                "technical": [
                    "Distributed Systems",
                    "Load Balancing",
                    "Database Sharding",
                    "Caching Strategies",
                    "Message Queues",
                    "Microservices vs Monolithic",
                    "Consistency Models",
                    "Fault Tolerance"
                ],
                "behavioral": [
                    "Architecture decision trade-offs",
                    "System failure incident response",
                    "Scalability planning",
                    "Cross-team technical communication",
                    "Design review feedback"
                ]
            }
        }
        
    def has_api_key(self):
        return bool(self.api_key and self.client)
    
    def setup(self, role, domain, interview_mode, difficulty):
        self.role = role
        self.domain = domain if domain != "General" else None
        self.interview_mode = interview_mode
        self.difficulty = difficulty
        self.questions_asked = []
    
    def generate_question(self, question_number):
        try:
            prompt = self._build_question_prompt(question_number)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert technical interviewer. Generate interview questions that are practical, relevant, and appropriate for the specified role and difficulty level."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            question = response.choices[0].message.content.strip()
            self.questions_asked.append(question)
            return question
            
        except Exception as e:
            print(f"Error generating question: {e}")
            return self._get_fallback_question(question_number)
    
    def evaluate_answer(self, question, answer):
        try:
            prompt = self._build_evaluation_prompt(question, answer)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert interview evaluator. Provide constructive, specific feedback with scores based on technical accuracy, communication clarity, and practical relevance."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200, # <<<< Reduced tokens for shorter feedback
                temperature=0.3
            )
            
            evaluation = response.choices[0].message.content.strip()
            return self._parse_evaluation(evaluation)
            
        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return self._fallback_evaluation(answer)

    def generate_summary(self, session_history):
        if not self.has_api_key():
            return self._generate_fallback_summary(session_history)

        try:
            prompt = self._build_summary_prompt(session_history)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert career coach and technical interviewer. Provide comprehensive, actionable feedback that helps candidates improve their interview performance."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600, # <<<< Reduced tokens for a more concise summary
                temperature=0.4
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._generate_fallback_summary(session_history)

    def _build_question_prompt(self, question_number):
        # Get relevant topics for the role/domain
        topics = self._get_relevant_topics()
        
        base_context = f"""
        Generate a {self.difficulty.lower()}-level {self.interview_mode.lower()} interview question for a {self.role} position.
        
        Question #{question_number}
        
        Relevant Topics: {', '.join(topics[:5])}   # Limit to first 5 topics
        Previous Questions: {', '.join(self.questions_asked[-2:]) if self.questions_asked else 'None'}
        """
        
        if self.interview_mode == "Technical":
            return base_context + """
            
            Requirements:
            - Focus on practical, hands-on scenarios from the role's key topics
            - Include real-world applications and problem-solving
            - Appropriate for the specified difficulty level
            - Encourage detailed explanations and examples
            - Avoid repeating similar concepts from previous questions
            - Make it specific to the role and technical domain
            
            Generate only the question:
            """
        else:  # Behavioral
            return base_context + """
            
            Requirements:
            - Use STAR method framework (Situation, Task, Action, Result)
            - Focus on professional scenarios relevant to the role and topics listed
            - Encourage specific examples with measurable outcomes
            - Appropriate for the specified experience level
            - Different from previous behavioral questions asked
            - Connect to the role's typical challenges and responsibilities
            
            Generate only the question:
            """
    
    def _build_evaluation_prompt(self, question, answer):
        return f"""
        Evaluate this {self.interview_mode.lower()} interview answer for a {self.role} position:

        QUESTION: {question}
        ANSWER: {answer}
        
        CONTEXT:
        - Role: {self.role}
        - Domain: {self.domain or 'General'}
        - Difficulty Level: {self.difficulty}
        - Interview Type: {self.interview_mode}

        EVALUATION CRITERIA (based on interview requirements):
        - Technical accuracy and depth of knowledge
        - Problem-solving approach and methodology
        - Use of appropriate examples and explanations
        - Communication clarity and structure
        - Consideration of edge cases, alternatives, or trade-offs
        - Relevance to real-world scenarios

        Provide evaluation in this exact format:
        SCORE: [number 0-100]
        FEEDBACK: [1-2 sentences of constructive feedback, including what they did well and one specific suggestion for improvement]

        Be encouraging but honest.
        """
    
    def _build_summary_prompt(self, session_history):
        if not session_history:
            return "No interview data available for summary generation."

        qa_pairs = "\\n".join([
            f"Q{i+1}: {qa['question']}\\nAnswer: {qa['answer']}\\nScore: {qa['score']}/100\\nFeedback: {qa['feedback']}\\n"
            for i, qa in enumerate(session_history)
        ])
        
        scores = [qa['score'] for qa in session_history]
        avg_score = sum(scores) / len(scores)
        
        return f"""
        Based on this {self.role} interview session, provide a brief, actionable final summary report as specified:

        INTERVIEW CONTEXT:
        - Role: {self.role}
        - Domain: {self.domain or 'General'}
        - Interview Type: {self.interview_mode}
        - Difficulty Level: {self.difficulty}
        - Questions Answered: {len(session_history)}
        - Average Score: {avg_score:.1f}/100

        INTERVIEW TRANSCRIPT:
        {qa_pairs}

        Generate a concise report following this exact format:

        ## 🎯 FINAL PERFORMANCE SUMMARY

        **Overall Rating:** [e.g., Good Candidate]

        **Final Score:** {avg_score:.0f}/100

        ## ✅ KEY STRENGTHS

        • **[Strength 1]:** [Briefly state a strength with an example]

        • **[Strength 2]:** [Briefly state a second strength]

        ## 🎯 KEY AREAS FOR IMPROVEMENT

        • **[Area 1]:** [Briefly state an area to improve]

        • **[Area 2]:** [Briefly state a second area to improve]

        ## 📚 ACTION PLAN

        • **Next Steps:** [1-2 actionable steps for improvement]
        """
    
    def _get_relevant_topics(self):
        """Get relevant topics based on role and domain"""
        role_key = self.role
        if role_key not in self.domain_topics:
            # Try to find a close match or use Software Engineer as default
            role_key = "Software Engineer"
        
        topic_type = "technical" if self.interview_mode == "Technical" else "behavioral"
        return self.domain_topics[role_key][topic_type]
    
    def _parse_evaluation(self, evaluation_text):
        """Extract score and feedback from evaluation response"""
        lines = evaluation_text.split('\n')
        score = 50  # default
        feedback = "Good effort! Continue practicing to improve your interview skills."
        
        for line in lines:
            if line.startswith('SCORE:'):
                try:
                    score_text = line.replace('SCORE:', '').strip()
                    numbers = ''.join(filter(str.isdigit, score_text))
                    if numbers:
                        score = int(numbers[:2]) if len(numbers) >= 2 else int(numbers[0]) * 10
                        score = max(0, min(100, score))
                except:
                    pass
            elif line.startswith('FEEDBACK:'):
                feedback = line.replace('FEEDBACK:', '').strip()
                if not feedback:
                    feedback = "Good effort! Continue practicing to improve your interview skills."
        
        return {'score': score, 'feedback': feedback}
    
    def _fallback_evaluation(self, answer):
        """Simple evaluation when API fails"""
        word_count = len(answer.split())
        
        if word_count < 20:
            return {
                'score': 35, 
                'feedback': "Answer is too brief. Provide more detailed explanations with specific examples and reasoning."
            }
        elif word_count < 50:
            return {
                'score': 65, 
                'feedback': "Good start! Add more depth with specific examples and explain your thought process in more detail."
            }
        elif word_count < 100:
            return {
                'score': 80, 
                'feedback': "Well-structured answer with good detail. Consider adding more specific examples or discussing trade-offs."
            }
        else:
            return {
                'score': 90, 
                'feedback': "Comprehensive and detailed response. Excellent use of examples and thorough explanations!"
            }
    
    def _generate_fallback_summary(self, session_history):
        """Generate summary when API is unavailable"""
        if not session_history:
            return "No interview data available for summary generation."
        
        scores = [qa['score'] for qa in session_history if qa['score'] > 0]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Determine rating based on average score
        if avg_score >= 85:
            rating = "Excellent Candidate"
            level = "Senior"
            readiness = "90%"
        elif avg_score >= 75:
            rating = "Strong Candidate"
            level = "Mid-Senior"
            readiness = "80%"
        elif avg_score >= 65:
            rating = "Good Candidate"
            level = "Mid"
            readiness = "70%"
        elif avg_score >= 50:
            rating = "Developing Candidate"
            level = "Entry-Mid"
            readiness = "60%"
        else:
            rating = "Needs Improvement"
            level = "Entry"
            readiness = "40%"
        
        return f"""## 🎯 FINAL PERFORMANCE SUMMARY

**Overall Rating:** {rating}

**Final Score:** {avg_score:.0f}/100

**Performance Level:** {level} level performance demonstrated

## ✅ AREAS OF STRENGTH

• **Consistent Participation:** Completed {len(session_history)} interview questions with dedication

• **Communication Skills:** Demonstrated ability to articulate responses clearly and professionally

• **{self.role} Knowledge:** Showed understanding of {self.role.lower()} concepts and practices

## 🎯 AREAS FOR IMPROVEMENT

• **Answer Depth:** {"Focus on providing more detailed explanations with specific examples" if avg_score < 70 else "Continue providing comprehensive, well-structured answers"}

• **Technical Precision:** {"Work on technical accuracy and include more specific details" if avg_score < 60 else "Maintain high technical standards while expanding on complex topics"}

• **Response Structure:** {"Use structured approaches like STAR method for behavioral questions" if self.interview_mode == "Behavioral" else "Organize technical responses with clear problem-solving steps"}

## 📚 SUGGESTED RESOURCES

• **{self.role} Fundamentals:** Study core concepts and best practices specific to your target role

• **Interview Practice:** Continue with mock interviews and domain-specific practice questions

• **Technical Communication:** Practice explaining complex concepts clearly to different audiences

---

*Keep practicing and focus on the improvement areas identified above. Your performance shows great potential for growth in the {self.role} role!*"""
    
    def _get_fallback_question(self, question_number):
        """Fallback questions when API is unavailable"""
        topics = self._get_relevant_topics()
        
        if self.interview_mode == "Technical":
            fallback_questions = [
                f"Explain your approach to {topics[0].lower()} and provide a practical example.",
                f"How would you handle a challenging scenario involving {topics[1].lower()}?",
                f"Describe the key considerations when working with {topics[2].lower()}.",
                f"What are the best practices for {topics[3].lower()} in your experience?",
                f"How would you optimize or improve {topics[4].lower()} in a real project?",
                f"Walk me through your problem-solving process for {topics[0].lower()}.",
                f"What tools and techniques do you use for {topics[1].lower()}?"
            ]
        else:
            fallback_questions = [
                f"Tell me about a time you had to deal with {topics[0].lower()}. How did you handle it?",
                f"Describe a situation where you demonstrated {topics[1].lower()}. What was the outcome?",
                f"Give me an example of how you approached {topics[2].lower()} in a previous role.",
                f"Tell me about a challenge related to {topics[3].lower()} and how you overcame it.",
                f"Describe your experience with {topics[4].lower()} and what you learned from it.",
                f"Share a time when you had to show {topics[0].lower()} under pressure.",
                f"Tell me about a project where {topics[1].lower()} was critical to success."
            ]
        
        return fallback_questions[(question_number - 1) % len(fallback_questions)]