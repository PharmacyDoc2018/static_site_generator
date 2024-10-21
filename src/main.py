from textnode import *
from ssg_functions import copy_static_to_public, generate_page, generate_pages_recursive
def main():
    copy_static_to_public()
    generate_pages_recursive("content/", "template.html", "public/")
    

main()