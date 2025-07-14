def analyze_resume(text):
    """
    Simulated CIQ-based resume analysis.
    Replace with real CIQ SDK usage in production.
    """
    skills = []
    suggested_roles = []

    if "Python" in text:
        skills.append("Python")
    if "Machine Learning" in text:
        skills.append("Machine Learning")
    if "Data Analysis" in text:
        skills.append("Data Analysis")
    if "SQL" in text:
        skills.append("SQL")

    if "Data" in text:
        suggested_roles.append("Data Analyst")
    if "Machine Learning" in text:
        suggested_roles.append("ML Engineer")
    if "dashboard" in text:
        suggested_roles.append("BI Developer")

    return {
        "Extracted_Skills": skills,
        "Experience_Level": "2 years" if "2 years" in text else "Fresher",
        "Suggested_Roles": suggested_roles or ["Software Developer"]
    }
