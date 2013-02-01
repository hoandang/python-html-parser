import urllib2
from bs4 import BeautifulSoup
import csv

def parse(url):
    page = urllib2.urlopen(url)
    html_doc = page.read()
    return BeautifulSoup(html_doc, "lxml")

print "Got faculty name"
faculty_names = []
faculty_urls  = []
faculties = parse("http://f1000.com/prime/thefaculty").find("ol", class_="faculties")
for faculty in faculties.find_all("a"):
    faculty_names.append(faculty.string)
    faculty_urls.append("http://f1000.com" + faculty["href"].strip())
    print faculty.string + ", " + "http://f1000.com" + faculty["href"].strip()


print "Got member name"
member_profiles = []
member_websites = []
for faculty_name, faculty_url in zip(faculty_names, faculty_urls):
    soup = parse(faculty_url)

    faculty_heads = soup.find_all("div", class_="facultyPhotoBlock")
    for faculty_head in faculty_heads:
        for name in faculty_head.find_all("h4"):
            link = name.find("a")
            member_profiles.append(link.string + ", " + faculty_name)
            member_websites.append(link["href"])
            print link.string + ", " + faculty_name

    sectionHeads = soup.find_all("div", class_="sectionHeads")
    for section in sectionHeads:
        for name in section.find_all("li"):
            link = name.find("a")
            member_profiles.append(link.string + ", " + faculty_name)
            member_websites.append(link["href"])
            print link.string + ", " + faculty_name

    facultyMembers = soup.find_all("div", class_="facultyMembersForInitial")
    for member in facultyMembers:
        for name in member.find_all("li"):
            link = name.find("a")
            member_profiles.append(link.string + ", " + faculty_name)
            member_websites.append(link["href"])
            print link.string + ", " + faculty_name

writer = csv.writer(open("members.csv", "wb"))
for profile, url in zip(member_profiles, member_websites):
    link = "http://f1000.com" + url.strip()
    try:
        html = parse(link)
        for website in html.find_all("div", class_="memberBiography"):
            try:
                writer.writerow([profile + ", " + website.find("a").string])
                print profile + ", " + website.find("a", class_="url").string
            except:
                writer.writerow([profile])
                print profile
    except:
        pass

print "All data was dumped to csv file !!!!"
