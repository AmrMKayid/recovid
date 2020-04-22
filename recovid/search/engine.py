from recovid import *
from recovid.data import Paper
from recovid.process import preprocess


class SearchResults:

  def __init__(self, data: pd.DataFrame, columns=None):
    self.results = data
    if columns:
      self.results = self.results[columns]

  def __getitem__(self, item):
    return Paper(self.results.loc[item])

  def __len__(self):
    return len(self.results)

  def _repr_html_(self):
    return self.results._repr_html_()


class WordTokenIndex:

  def __init__(self,
               corpus: pd.DataFrame,
               columns: list = [
                   'title', 'abstract', 'doi', 'authors', 'journal',
                   'publish_time'
               ]):
    self.corpus = corpus
    self.columns = columns

    raw_search_str = self.corpus.abstract.fillna(
        '') + ' ' + self.corpus.title.fillna('')
    self.index = raw_search_str.apply(preprocess).to_frame()
    self.index.columns = ['terms']
    self.index.index = self.corpus.index

  def search(self, search_string: str = ''):
    search_terms = preprocess(search_string)
    result_index = self.index.terms.apply(
        lambda terms: any(i in terms for i in search_terms))
    results = self.corpus[result_index].copy().reset_index().rename(
        columns={'index': 'paper'})
    return SearchResults(results, self.columns + ['paper'])


class RankBM25Index(WordTokenIndex):

  def __init__(self,
               corpus: pd.DataFrame,
               columns: list = [
                   'title', 'abstract', 'doi', 'authors', 'journal',
                   'publish_time'
               ]):
    super().__init__(corpus, columns)
    self.bm25 = BM25Okapi(self.index.terms.tolist())

  def search(self, search_string, n=5):
    search_terms = preprocess(search_string)
    doc_scores = self.bm25.get_scores(search_terms)
    ind = np.argsort(doc_scores)[::-1][:n]
    results = self.corpus.iloc[ind][self.columns]
    results['Score'] = doc_scores[ind]
    results = results[results.Score > 0]
    return SearchResults(results.reset_index(), self.columns + ['Score'])


def search_papers(search_engine: RankBM25Index,
                  search_terms: str = 'virus',
                  results_num: int = 200,
                  display_num: int = 10):

  # gather search results by score

  output = search_engine.search(search_terms, n=results_num)
  # sort results by recency
  output = output.results.sort_values(by=['publish_time'],
                                      ascending=False).head(display_num)
  if len(output) > 0:
    display(output)

  return output
