#!/usr/bin/env python3

from email.quoprimime import header_check
import os
import jinja2
import csv
import datetime
import re

def fix_latex(text):
    text = text.replace("\\&", "&")
    text = text.replace("\\_", "_")
    text = text.replace("--", "&#8211;")
    text = text.replace(r"$^\lambda$", "&lambda;")
    text = text.replace("\\'{c}", "&cacute;")    
    text = re.sub(r"\\url\{.*?\}", "", text)
    text = re.sub(r"\\footnote\{.*?\}", "", text)
    text = re.sub(r"\\ul\{(.*?)\}", r"\1", text)
    return text 

if __name__ == "__main__":
    template_loader = jinja2.FileSystemLoader("templates")
    template_environment = jinja2.Environment(loader=template_loader)
    
    events = []
    with open("./data/06-3-organization_events.txt", "r") as f:
        reader = csv.DictReader(f, delimiter=";", quotechar='"')
        for row in reader:
            if not row["endofevent"].startswith("%"):
                expires_at = datetime.datetime.strptime(row["endofevent"], '%d.%m.%y')
                row["endofevent_as_ISO_8601"] = expires_at.isoformat()
                row["role"] = fix_latex(row["role"])
                roles_without_brackets = re.sub(r"\(.*?\)", "", row["role"])
                roles = re.split(r', |\& ', roles_without_brackets)
                row["roles"] = roles
                row["event"] = fix_latex(row["event"])
                events.append(row)

    projects = []
    with open("./data/08-5-research_grants.txt", "r") as f:        
        reader = csv.DictReader(f, delimiter=";", quotechar='"')
        for row in reader:        
            if not row["grantdate"].startswith("%"):    
                expires_at = datetime.datetime.strptime(row["endofproject"], '%d.%m.%y')
                row["endofproject_as_ISO_8601"] = expires_at.isoformat()
                row["fundingbody"] = fix_latex(row["fundingbody"])
                row["fundingbody"] = re.sub(r"\(.*?\)", "", row["fundingbody"]).strip()
                if row["awardholders"].lower().__contains__(",") or row["awardholders"].lower().__contains__(" and "):
                    row["rolename"] = "Co-Investigator"
                    row["roletype"] = 2
                else:
                    row["rolename"] = "Principal investigator"
                    row["roletype"] = 1
                projects.append(row)

    with open("./data/11-2-participation_research_projects.txt", "r") as f:        
        reader = csv.DictReader(f, delimiter=";", quotechar='"')
        for row in reader:  
            if not row["startofproject"].startswith("%"):              
                expires_at = datetime.datetime.strptime(row["endofproject"], '%d.%m.%y')
                row["fundingbody"] = fix_latex(row["fundingbody"])
                row["endofproject_as_ISO_8601"] = expires_at.isoformat()
                row["rolename"] = "Researcher"
                row["roletype"] = 3
                projects.append(row)

    teaching = []
    with open("./data/05-1-teaching_experience.txt", "r") as f:        
        reader = csv.DictReader(f, delimiter=";", quotechar='"')        
        for row in reader:        
            if not row["organization"].startswith("%"):              
                row["course"] = fix_latex(row["course"])
                row["period"] = fix_latex(row["period"])
                if row["role"].lower().__contains__("l"):
                    row["islecturer"] = True
                if row["role"].lower().__contains__("ta"):
                    row["isteachingassistant"] = True
                teaching.append(row)

    projects.sort(key=lambda x: x["endofproject_as_ISO_8601"])

    publications = []
    with open("./data/09-1-publications_book_authored.txt", "r") as f:        
        reader = csv.DictReader(f, delimiter=";", quotechar='"')        
        for row in reader:          
            if not row["starred"].startswith("%"):              
                row["type"] = 1
                row["authors"] = fix_latex(row["authors"])
                row["titleofpublication"] = fix_latex(row["titleofpublication"])
                row["doiorwebaddress"] = fix_latex(row["doiorwebaddress"])
                publications.append(row)

    with open("./data/09-1-publications_book_edited.txt", "r") as f:        
        reader = csv.DictReader(f, delimiter=";", quotechar='"')        
        for row in reader:          
            if not row["starred"].startswith("%"):              
                row["type"] = 1
                row["authors"] = fix_latex(row["authors"]) + " (Editors)"
                row["titleofpublication"] = fix_latex(row["titleofpublication"])
                row["doiorwebaddress"] = fix_latex(row["doiorwebaddress"])
                publications.append(row)

    with open("./data/09-2-publications_chapter.txt", "r") as f:        
        reader = csv.DictReader(f, delimiter=";", quotechar='"')        
        for row in reader:             
            if not row["starred"].startswith("%"):
                row["type"] = 2
                row["authors"] = fix_latex(row["authors"])
                row["titleofpublication"] = fix_latex(row["titleofpublication"])
                row["doiorwebaddress"] = fix_latex(row["doiorwebaddress"])       
                row["pages"] = fix_latex(row["pages"])    
                publications.append(row)

    with open("./data/09-3-publications_conference.txt", "r") as f:        
        reader = csv.DictReader(f, delimiter=";", quotechar='"')        
        for row in reader:         
            if not row["starred"].startswith("%"):    
                row["type"] = 3
                row["authors"] = fix_latex(row["authors"])
                row["titleofpublication"] = fix_latex(row["titleofpublication"])
                row["doiorwebaddress"] = fix_latex(row["doiorwebaddress"])                           
                row["dates"] = fix_latex(row["dates"])                            
                row["acronym"] = fix_latex(row["acronym"])                
                publications.append(row)

    with open("./data/09-4-publications_journal_academic.txt", "r") as f:        
        reader = csv.DictReader(f, delimiter=";", quotechar='"')        
        for row in reader:             
            if not row["starred"].startswith("%"):
                row["type"] = 4
                row["authors"] = fix_latex(row["authors"])
                row["titleofpublication"] = fix_latex(row["titleofpublication"])
                row["titlejournal"] = fix_latex(row["titlejournal"])
                row["doiorwebaddress"] = fix_latex(row["doiorwebaddress"])                           
                row["pages"] = fix_latex(row["pages"])                            
                publications.append(row)

    with open("./data/09-5-publications_journal_professional.txt", "r") as f:        
        reader = csv.DictReader(f, delimiter=";", quotechar='"')        
        for row in reader:     
            if not row["authors"].startswith("%"):        
                row["type"] = 4
                row["authors"] = fix_latex(row["authors"])
                row["titleofpublication"] = fix_latex(row["titleofpublication"])
                row["titlejournal"] = fix_latex(row["titlejournal"])            
                row["doiorwebaddress"] = fix_latex(row["doiorwebaddress"])                           
                row["pages"] = fix_latex(row["pages"])                            
                publications.append(row)

    publications.sort(key=lambda x: x["yearofpublication"])

    template = template_environment.get_template("index.html.jinja")
    outputText = template.render(events=events, projects=projects, teaching=teaching, publications=publications)
    with open("./index.html", "w") as f:
        f.write(outputText)

    print("Done.")