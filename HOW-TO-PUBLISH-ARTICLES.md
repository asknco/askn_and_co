# How to publish an article on asknandco.com

Each article is a plain text file in `content/articles/`. A small script turns those files into web pages, adds the newest four to the homepage Journal and updates `sitemap.xml` so Google finds them.

## 1. Write the article

1. Copy `content/article-template.md` into `content/articles/`.
2. Rename it to the web address you want, using lowercase words and hyphens. The file `gst-notice-reply-drc-01.md` becomes `asknandco.com/articles/gst-notice-reply-drc-01/`.
3. Fill in the header between the `---` lines:
   - `title`: the headline. Use the words people actually type into Google.
   - `description`: one or two sentences, under 160 characters. Google shows this under the title.
   - `date`: the publishing date, as `YYYY-MM-DD`.
   - `category`: for example Income Tax, GST, Company Law, Audit or International Tax.
   - `author`: optional. Naming the partner helps Google trust the article. If you leave it out, the firm is shown as the author.
   - `updated`: optional. Add this date when you revise an older article.
   - `seo_title`: optional but recommended. A shorter title of under 60 characters for Google results, written the way people search, for example `How to Reply to a GST Show Cause Notice`. The `title` stays as the heading on the page.
4. Write the article below the header. Use `##` for headings, `-` for bullet points, `**bold**` and `[link text](/services/...)`.
5. End with a `## Frequently asked questions` section. Write each question as a `###` heading, phrased the way a client would type it into Google, with a short answer below it. The script marks these up for Google automatically.

When you link to a service page, the article automatically appears under "Related articles" on that service page.

You can open and edit `.md` files in Notepad or VS Code.

## 2. Build the pages

Run this command from the website folder:

```
py tools/build_articles.py
```

The script tells you which pages it built. If a header line is missing, it says which file and which line to fix.

To preview the result, run `py -m http.server 8123` and open http://localhost:8123/articles/ in your browser.

## 3. Publish

Commit and push the changes to GitHub, for example with GitHub Desktop. Commit the whole folder, not only the `.md` file: the new `articles/...` pages, `index.html` and `sitemap.xml` all change.

Then in Google Search Console, use **URL Inspection** on the new article's address and click **Request indexing**.

## Tips for articles that rank

- **Answer one search question per article.** "How to reply to a GST DRC-01 notice" will rank better than "GST updates".
- **Write about what clients actually ask you.** Real questions from notices and client meetings make the best topics.
- **Write at least 600 words.** Be specific: sections, deadlines, forms and worked examples.
- **Link to the matching service page.** Google sees which page to send enquiries to, and readers can contact you.
- **Publish regularly.** Two or more articles a month works better than many at once followed by none.
- **Keep articles current.** After a Budget or a change in the law, revise the article and set `updated:`.
- **Share each new article** on LinkedIn and your Google Business Profile.

## Editing or removing an article

- **To edit**, change the `.md` file, then run the script again.
- **To remove**, delete the `.md` file and run the script again. The script deletes the old page and removes it from the sitemap.

## Service pages

The eight service pages are built the same way from `tools/build_service_pages.py`. The text for each page is in that file. After changing it, run `py tools/build_service_pages.py` and then `py tools/build_articles.py` to refresh the sitemap.
