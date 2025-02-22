from bs4 import BeautifulSoup

def get_project_titles():
    "gets all the h3 header titles projects for later use"
    with open('/Users/Damian/Desktop/Portofolio/appfile/templates/projects_page.html',encoding='utf-8') as f:
        soup = BeautifulSoup(f,'html.parser')
    return [h3.text.strip() for h3 in soup.find_all('h3')]
