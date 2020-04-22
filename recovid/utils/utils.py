from recovid import *


def doi_url(id: str = ''):
  r"""Convert the doi to a url

  Returns:
      id {str} -- [doi id string]
  """
  return f'http://{id}' if id.startswith('doi.org') else f'http://doi.org/{id}'


def get_data(
    url: str = '',
    timeout: int = 10,
):
  r"""getting paper data from url

  Keyword Arguments:
      url {str} -- paper's url (default: {''})
      timeout {int} -- timeout for requests (default: {10})

  Returns:
      [str] -- [data as text]
  """
  try:
    r = requests.get(url, timeout=timeout)
    return r.text
  except ConnectionError:
    print(f'Cannot connect to {url}')
    print(f'Remember to turn Internet ON in the Kaggle notebook settings')
  except HTTPError:
    print('Got http error', r.status, r.text)
