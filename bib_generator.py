import csv
import re
import os

def main():
    df = []
    with open("data/Publications.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        df = list(reader)

    for i, ref in enumerate(df):
        # get doi reference
        ref_doi = f"doi: {ref['DOI']}"
        author_list = ref['Author']
        author_list = re.split(r";\s", author_list)
        authors = "author: "
        
        first_author_lastname = ""
        for j, names in enumerate(author_list):
            name_list = re.split(r",\s", names)
            if len(name_list) >= 2:
                first_last_name = f"{name_list[1]} {name_list[0]}"
            else:
                first_last_name = name_list[0]
            
            if j == 0:
                first_author_lastname = name_list[0]
                author_sep = ""
            else:
                author_sep = ", "
            
            authors = f"{authors}{author_sep}{first_last_name}"
        
        ref_type = f"type: {ref['Item.Type']}"
        
        if ref_type == "type: manuscript":
            ref_status = "status: Unpublished"
        else:
            ref_status = "status: Published"
        
        ref_date = f"date: {ref['Date']}"
        date_parts = ref_date.split(" ")
        if len(date_parts) > 1 and len(date_parts[1]) == 7:
            ref_date = f"{ref_date}-01"
        
        ref_title = f'title: "{ref["Title"]}"'
        
        ref_abstract = ref['Abstract.Note']
        
        # make hugo-finite theme compliant *.md files from reference
        type_value = ref_type.split(" ")[1] if len(ref_type.split(" ")) > 1 else ""
        
        if type_value == "report":
            ref_url = f"online: {ref['Url']}"
            ref_cit = f'citation: "<em>{ref["Publisher"]}</em>, No. <b>{ref["Number"]}</b>"'
            ref_hugo_md = ["---", ref_title, authors, ref_status, ref_type, ref_cit, ref_url, ref_date, "---", "\n", ref_abstract]
        elif type_value == "manuscript":
            ref_url = f"online: {ref['Url']}"
            ref_cit = f'citation: "<em>{ref["Place"]}</em>"'
            ref_hugo_md = ["---", ref_title, authors, ref_status, ref_type, ref_cit, ref_date, "---", "\n", ref_abstract]
        else:
            ref_cit = f'citation: "<em>{ref["Publication.Title"]}</em>, <b>{ref["Volume"]}</b>({ref["Issue"]}):{ref["Pages"]}"'
            ref_hugo_md = ["---", ref_title, authors, ref_status, ref_type, ref_cit, ref_doi, ref_date, "---", "\n", ref_abstract]
        
        # Process title for filename
        title_list = ref['Title'].split(" ")
        stopwords = ["in", "for", "and", "a", "an", "the", "of", "on", "this", "to", "who", "whom", "whose", "why", "how", "where", "is", "my", "from"]
        title_list = [word.lower() for word in title_list]
        title_list = [word for word in title_list if word not in stopwords]
        title_list = title_list[:3]
        title_list = [re.sub(r"[^\w]", "", word) for word in title_list]  # remove punctuation
        title_list = "-".join(title_list)
        
        # save the resulting ref_hugo_md into *.md file
        ref_name = f"{ref['Publication.Year']}-{first_author_lastname}-{title_list}".lower()
        
        ref_pdf = f"file: {ref_name}.pdf"
        
        if ref_status == "status: Unpublished":
            ref_hugo_md = ["---", ref_title, authors, ref_status, ref_type, ref_cit, ref_doi, ref_date, "---", "\n", ref_abstract]
        else:
            ref_hugo_md = ["---", ref_title, authors, ref_status, ref_type, ref_cit, ref_doi, ref_pdf, ref_date, "---", "\n", ref_abstract]
        
        filepath = f"./content/publications/{ref_name}.md"
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(ref_hugo_md))
            print(f"{i + 1} : {ref_doi} --- {ref_name}")


if __name__ == "__main__":
    main()
