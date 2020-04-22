from recovid import *


def most_common_words_from_title(
    df: pd.DataFrame,
    column: str = "title",
    range_: int = 25,
    title: str = "Most Common Words from Title",
):

  titles = df[column].astype(str)
  words = titles.str.lower().str.split(expand=True).stack().value_counts()
  words_count = dict(Counter(words.to_dict()))
  stopwords_en = stopwords.words("english")
  popular_words = [
      word for word in sorted(words_count, key=words_count.get, reverse=True)
      if word not in stopwords_en
  ]
  plt.barh(range(range_),
           [words_count[w] for w in reversed(popular_words[:range_])])
  plt.yticks([x + 0.5 for x in range(range_)], reversed(popular_words[:range_]))
  plt.title(title)
  plt.show()


def most_common_journals(
    df: pd.DataFrame,
    column: str = "journal",
    range_: int = 25,
    title: str = "Most Common Journals in COVID-19 Dataset",
):

  journals_df = pd.DataFrame(df["journal"].value_counts())
  journals_df["journal_name"], journals_df["count"] = (
      journals_df.index,
      journals_df["journal"],
  )
  fig = px.bar(journals_df[:range_],
               x="count",
               y="journal_name",
               title=title,
               orientation="h")
  fig.show()
