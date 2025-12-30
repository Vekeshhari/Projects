Intelligent Email Threat Analysis Framework
Behavioral and Pattern-Based Detection for Phishing and Spoofing

This project is a SOC-oriented email security system designed to detect email phishing, spoofing, and malicious links using behavioral analysis, similarity detection, and threat intelligence.  
Instead of traditional spam filtering, the framework focuses on identity deception and link-based attacks, which are the most common real-world email threats.

--------------------------------------------------

Key Capabilities

• Extracts and analyzes URLs present in email content  
• Detects mismatched links where displayed text differs from the actual destination URL  
• Identifies URL shorteners commonly abused in phishing attacks  
• Integrates VirusTotal API for real-time malicious URL intelligence  
• Detects sender spoofing using lookalike character mapping  
• Uses adaptive Levenshtein similarity analysis to identify impersonated email addresses  
• Performs behavioral profiling based on previously verified non-spoofed senders  
• Provides SOC-style logging and visualization through a GUI monitoring dashboard  

--------------------------------------------------

How the System Works

1. Emails are captured using MailHog  
2. Sender, subject, body, and timestamp are extracted  
3. All URLs inside the email body are identified and analyzed  
4. Deceptive links and URL shorteners are flagged  
5. URLs are checked against VirusTotal for threat intelligence  
6. Sender identity is verified using lookalike and similarity analysis  
7. Behavioral history is used to improve detection accuracy  
8. Results are classified and stored in MySQL  
9. Analysis is displayed in a SOC-style GUI  

--------------------------------------------------

Detection Techniques Used

Link-Based Phishing Detection  
• Regex-based URL extraction  
• HTML parsing to detect deceptive hyperlinks  
• URL shortener identification  
• VirusTotal reputation scoring  

Sender Spoofing Detection  
• Visual similarity detection using lookalike characters  
• Typo-based similarity detection using adaptive Levenshtein thresholds  
• Username-focused comparison for accuracy  

--------------------------------------------------

Technology Stack

Python  
MySQL  
MailHog  
VirusTotal API  
Tkinter  
Levenshtein Distance  
Pattern and Behavioral Analysis  

--------------------------------------------------

Project Structure

gui.py                SOC-style GUI dashboard  
mail_analyzer.py      Core phishing and spoofing detection logic  
db_handler.py         Database operations  
config.py             Configuration file  
suspicious_terms.txt  Phishing keyword list  
lookalike_map.json    Lookalike character mappings  
schema.sql            Database schema  

--------------------------------------------------

Why This Project Matters

• Goes beyond spam filtering to detect identity-based email attacks  
• Mimics how SOC teams analyze phishing and spoofing incidents  
• Focuses on real-world attack techniques used by adversaries  
• Suitable for SOC Analyst, Blue Team, and Cybersecurity roles  

--------------------------------------------------

Future Enhancements

• Domain impersonation detection  
• SPF, DKIM, and DMARC header analysis  
• Threat scoring and prioritization  
• Campaign correlation across multiple phishing emails  
• Machine learning-based classification  

--------------------------------------------------


