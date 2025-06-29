### README: Digital Humanities Reddit Gender Studies Project

**Project Title:** A Comparative Analysis of Language Use in Gendered Political Communities on Reddit during Trump's Pre- and Post-Election 2024

**Authors:** Jasmin Schiltknecht, Luka Gfeller, Martin Fähnrich
**Date:** June 29, 2025 
**Affiliation:** University of Zurich 

**Project Description:**

This research examines the dynamics of language use of gendered political communities on Reddit and Instagram in terms of the 2024 re-election of Donald TrumpAs part of ongoing discourse, this research compares the use of gendered language before and after the 2024 election, investigating how discourses regarding gender could differ across platforms and over time This research methodology involves the use of computational linguistic methods in combination with traditional linguistic techniques The analysis begins with an investigation of keywords and collocations that examines the words that frequently occur with a range of key concepts, while also paying attention to the words that might simply appear in male-dominated communities versus female-dominated communities Second, topic modelling is used to examine the themes present or absent in the discourse in male versus female dominated communities Topic modelling allows the researcher to see dominant topics or themes over time The analysis will also include both network analysis and kernel density estimation of pathways and clusters of gendered political discourses The results of this analysis seek to provide a nuanced understanding of the ways in which gender, platform, and political context interact and shape political communication online

**Dependencies/Requirements:**

The code requires specific Python libraries to function, which can be installed via `pip3`:

* `stop-words3` 
* `textplot3` 
* `tqdm3` 
* `nltk3` 

**Data Structure (Integral to Code Design):**

A significant part of the project involves Reddit data, which is structured into JSON files for both posts and comments. The code must be designed to parse and process this specific JSON structure:

* **Data Collection Periods:** Data is divided into "Before Election" (28.05.24 - 4.11.24) and "After Election" (5.11.24 - 14.4.25) periods, each spanning 161 days 135].
* **Subreddits Analysed:** The data includes content from r/MensRights, r/Feminism, and r/lgbt.
* **JSON Structure for Comments:** Reddit comments have a detailed JSON structure including fields such as `author`, `body`, `created_utc`, `id`, `link_id` (parent post), `parent_id`, `permalink`, `score`, `subreddit`, and various flair and moderation-related fields.
* **JSON Structure for Posts:** Reddit posts also follow a comprehensive JSON structure with fields like `author`, `created_utc`, `domain`, `id`, `is_self`, `num_comments`, `permalink`, `score`, `selftext` (the main text of the post), `subreddit`, `title`, and `url`.

**Methodology:**

* **Preprocessing:** This transforms raw Reddit data into a clean, analysable text corpus. It comprises text extraction from JSON files and normalizing the text with standard text normalization techniques. This entails noise removal of links, stop words, punctuation, and formatting artifacts to ensure linguistic homogeneity.
* **Topic Modelling:** Topic modeling was conducted using K-means clustering, an unsupervised algorithm that groups similar texts based on their word usage patterns.
* **Keywords TF-IDF:** Term Frequency-Inverse Document Frequency (TF-IDF) was applied to detect key terms within the dataset. It is a statistical measure used to identify content words that are particularly prominent in a specific document relative to the entire corpus.
* **Collocations:** This procedure identifies statistically significant word collocations—common co-occurrences of two, three, or four words—which tend to reveal important multi-word expressions or phrases.
* **Kernel Density Estimation (KDE):** The python library `textplot` was used to create conceptual maps. KDE is used to model how often and where in the text a term appears.
* **Sentiment Analysis:** Sentiment analysis was performed using the pre-trained `cardiffnlp/twitter-roberta-base-sentiment` model from Cardiff NLP as part of the TweetEval benchmark, accessed via the Hugging Face transformers library.

**Results:**

Across all subreddits analyzed, `r/lgbt` exhibited the most pronounced shift in tone and discourse during the 2024 U.S. election. While negativity and uncertainty in sentiment was observed across all groups, it was especially prominent in `r/lgbt`, particularly within clusters related to introspection, identity, and attraction. TF-IDF and collocation results underscore a transition from affirmational language (e.g., “community”, “love”, “happy”) to action-oriented and politically charged terms such as “donate”, “project”, “rights”, and “country”. In contrast, `r/MensRights` exhibited slower growth, lower engagement, and less fluctuation in tone, indicating a more ideologically consistent and less reactive user base.

**Future Outlook:**

Future research could build on these findings by integrating computational analysis with qualitative approaches, such as refining sentiment models to better capture emotional nuance, particularly in politicized or identity-driven discourse, thereby enhancing interpretive precision.
