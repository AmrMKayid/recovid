from recovid import *
from recovid.utils import doi_url, get_data


class Paper:
  r"""
  A single research paper
  """

  def __init__(
      self,
      item: pd.DataFrame,
  ):
    """[summary]

    Arguments:
        item {pd.DataFrame} -- [description]
    """
    self.paper = item.to_frame().fillna('')
    self.paper.columns = ['Value']

  def doi(self):
    """check the paper doi

    Returns:
        [type] -- [description]
    """
    return self.paper.loc['doi'].values[0]

  def html(self):
    r"""Load the paper from doi.org and display as HTML.

    Returns:
        [widget] -- return the paper as html widget
    """
    if self.doi():
      url = doi_url(self.doi())
      text = get_data(url)
      return widgets.HTML(text)

  def text(self):
    r"""
    Load the paper from doi.org and display as text.
    """
    """Load the paper from doi.org and display as text.

    Returns:
        [str] -- paper page as text
    """
    text = get_data(doi_url(self.doi()))
    return text

  def abstract(self):
    return self.paper.loc['abstract'].values[0]

  def title(self):
    return self.paper.loc['title'].values[0]

  def authors(
      self,
      split: bool = False,
  ):
    r"""
    Get a list of authors
    """
    """Get a list of authors

    Returns:
        [list] -- [list of authors]
    """
    authors = self.paper.loc['authors'].values[0]
    if not authors:
      return []
    if not split:
      return authors
    if authors.startswith('['):
      authors = authors.lstrip('[').rstrip(']')
      return [a.strip().replace("\'", "") for a in authors.split("\',")]

    return [a.strip() for a in authors.split(';')]

  def _repr_html_(self):
    return self.paper._repr_html_()


class ResearchPapers:

  def __init__(
      self,
      metadata: pd.DataFrame,
  ):
    self.metadata = metadata

  def __getitem__(
      self,
      item: int = 0,
  ):
    return Paper(self.metadata.iloc[item])

  def __len__(self):
    return len(self.metadata)

  def head(
      self,
      n: int = 3,
  ):
    return ResearchPapers(self.metadata.head(n).copy().reset_index(drop=True))

  def tail(
      self,
      n: int = 3,
  ):
    return ResearchPapers(self.metadata.tail(n).copy().reset_index(drop=True))

  def abstracts(self):
    return self.metadata.abstract.dropna()

  def titles(self):
    return self.metadata.title.dropna()

  def _repr_html_(self):
    return self.metadata._repr_html_()
