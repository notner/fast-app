import asyncio
from myapp.core.repo.movie import get_movie


def test_movie(test_ctx):
    loop = asyncio.get_event_loop()
    df = loop.run_until_complete(get_movie(test_ctx, title='Avatar'))
    assert not df.empty
    assert df.to_dict('records')[0]['originalTitle'] == 'Avatar'
