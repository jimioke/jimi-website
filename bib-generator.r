library("rcrossref")
library("yaml")
library("anytime")
library(stringr)

# setwd("./Projects/jboke-website/")
# dois <- c("10.1103/PhysRevLett.104.070402",
#           "10.1093/jamia/ocaa033",
#           "10.1177/0361198119853553",
#           "10.1007/s11116-020-10106-y",
#           "10.1088/1748-9326/ab22c7",
#           "10.1016/j.jth.2015.08.006",
#           "10.1007/s10479-016-2358-2",
#           "10.1007/s11067-018-9387-0",
#           "10.1016/j.cor.2015.02.010"
#           )

df = read.csv("data/Publications.csv")

for(i in 1:nrow(df)) {
    ref = df[i,]
    ## get doi reference 
    ref_doi <- paste0("doi: ", ref$DOI)
    author_list <- ref$Author
    author_list <- as.list(str_split(author_list,";\\s")[[1]])
    authors <- c("author: ")
    for (j in seq(length(author_list))) {
        names <- author_list[[j]]
        name_list <- as.list(str_split(names[[1]], ",\\s")[[1]])
        first_last_name <- paste0(name_list[[2]], " ", name_list[[1]])
        if (j == 1) {
            first_author_lastname <- name_list[[1]]
            author_sep = ""
        } else {
            author_sep = ", "
        }
        authors <- paste(authors, first_last_name, sep=author_sep)
    }
    ref_status = "status: Published"
    ref_type = paste0("type: ", ref$Item.Type)
    ref_date = paste0("date: ", ref$Date)
    ref_title = paste0("title: \"", ref$Title, "\"")
    
 
    ref_abstract = ref$Abstract.Note
    ## make hugo-finite theme compliant *.md files from reference:
    if (str_split(ref_type, " ")[[1]][2] == "report") {
        ref_url <- paste0("online: ", ref$Url)
        ref_cit <- paste0("citation: \"<em>", ref$Publisher, "</em>, No. <b>", ref$Number, "</b>", "\"")
        ref_hugo_md <- c("---", ref_title, authors, ref_status, ref_type, ref_cit, ref_url, ref_date, "---", "\n", ref_abstract)
    } else {
        ref_cit = paste0("citation: \"<em>", ref$Publication.Title, "</em>, <b>", ref$Volume, "</b>(", ref$Issue, "):", ref$Pages, "\"")
        ref_hugo_md <- c("---", ref_title, authors, ref_status, ref_type, ref_cit, ref_doi, ref_date, "---", "\n", ref_abstract) 
        }

    title_list = unlist(strsplit(ref$Title, " "))
    stopwords <- c("in", "for", "and", "a", "an", "the", "of", "on", "this", "to", "who", "whom", "whose", "why", "how", "where", "is", "my", "from")
    title_list <- tolower(title_list)
    title_list <- title_list[!title_list %in% stopwords]
    title_list <- title_list[1:3]
    title_list <- gsub("[[:punct:]]", "", title_list) # remove punctuation marks
    title_list <- paste(title_list, collapse = "-")    
    
    ## save the resulting ref_hugo_md into *.md file
    
    ref_name <- tolower(paste(ref$Publication.Year,first_author_lastname,title_list,sep="-"  ))

    # if (!file.exists(paste0("./content/publications/", ref_name, ".md"))) {
    write.table(ref_hugo_md, file = paste0("./content/publications/", ref_name, ".md"),
                quote = FALSE, row.names = FALSE, col.names = FALSE)
    print(paste(i, ":",  ref_doi, "---", ref_name))
    #}
}
